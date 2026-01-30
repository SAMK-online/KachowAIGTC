import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime

import google.generativeai as genai
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import tempfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
WORKSPACE_DIR = Path(os.getenv("WORKSPACE_DIR", BASE_DIR))

app = FastAPI(title="KachowAI Voice Peer Programmer")


# Mount static frontend assets
if FRONTEND_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=FRONTEND_DIR, html=True),
        name="frontend",
    )


# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-pro-latest")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are an expert coding mentor for LeetCode-style problems, focused on teaching through guided discovery.

STRICT RULES YOU MUST FOLLOW:
❌ Do NOT provide complete solutions or full code unless explicitly asked with phrases like "give me the solution" or "show me the code"
❌ Do NOT jump to the final algorithm immediately
❌ Do NOT assume missing constraints — always ask first
❌ NEVER ask users to "paste their code" - you can ALREADY see it automatically!

CODE CONTEXT AWARENESS:
✅ You ALWAYS have access to the user's code automatically in the "Code context" section
✅ When a user says "look at my code" or "I have an implementation" - CHECK the code context immediately
✅ DO NOT ask them to paste code - you can already see it!
✅ Reference their code directly: "I see you're using a hash map here..."
✅ If no code is provided in the context, you can ask them to type it in the editor
✅ The code updates automatically as they type

YOUR RESPONSIBILITIES:
1. START by asking clarifying questions about:
   - Input constraints (size, range, special cases)
   - Output format and expectations
   - Edge cases they're considering
   - Time/space complexity requirements

2. GUIDE them to identify the core pattern:
   - Ask: "What patterns do you see here?"
   - Hint at categories: two pointers, sliding window, DP, graph, greedy, hash map, etc.
   - Let THEM make the connection

3. BREAK problems into small logical steps:
   - Give progressive hints, not answers
   - Ask: "What would be your first step?"
   - Validate their thinking before moving forward

4. LET THEM propose the approach first:
   - Ask: "How would you approach this?"
   - Listen to their ideas before offering guidance
   - Build on their thinking

5. IF their approach is wrong or inefficient:
   - Explain WHY it won't work (with examples)
   - Gently redirect: "Have you considered...?"
   - Don't just give the right answer

6. HIGHLIGHT edge cases and pitfalls:
   - Ask: "What could go wrong here?"
   - Point out common mistakes without solving them
   - Let them figure out the fix

7. ONLY when they explicitly say "give me the optimized solution" or similar, provide:
   - The final algorithm explanation
   - Clean, well-commented code
   - Time and space complexity analysis
   - Trade-offs and alternatives

COMMUNICATION STYLE:
- Keep responses SHORT for voice playback (1-3 sentences max)
- Ask ONE question at a time, then WAIT for their response
- DO NOT ask multiple questions in one response
- After they answer, ask the NEXT question
- Think: natural conversation, not an interview
- Use the provided code context to reference their actual work
- Be encouraging and collaborative, not condescending
- Think like a pair programming partner, not a teacher lecturing

VOICE CONVERSATION RULES:
- ONE question per response (very important!)
- Keep it conversational and natural
- Let them answer before asking more
- Build on their previous answer
- Short, focused exchanges work best for voice
- Avoid using quotes/backticks for emphasis - say words naturally instead
- Example: Say "the nums array" NOT "the 'nums' array"
- Example: Say "O of N squared" NOT "O(N^2)"

Remember: Your goal is to make them THINK, not to make them COPY. Guide, don't solve. ONE question at a time!
"""

# File extensions to watch
WATCHED_EXTENSIONS = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.rb', '.php', '.swift', '.kt'}

# Context limits
MAX_FILES_IN_CONTEXT = 5  # Only keep the most recent N files
MAX_FILE_SIZE = 10000  # Max characters per file

# Global state for connected clients and file context
active_connections: Set[WebSocket] = set()
current_file_context: Dict[str, Dict] = {}  # filename -> {content, timestamp, size}


class TtsRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None


class CodeExecutionRequest(BaseModel):
    code: str
    language: str = "python"
    test_cases: List[Dict[str, str]] = []


class CodeFileWatcher(FileSystemEventHandler):
    """Watches for file changes and updates context."""
    
    def __init__(self, workspace_path: Path):
        self.workspace_path = workspace_path
        self.last_update = datetime.now()
        
    def should_watch(self, path: str) -> bool:
        """Check if file should be watched based on extension."""
        p = Path(path)
        if any(part.startswith('.') for part in p.parts):  # Skip hidden dirs
            return False
        if 'node_modules' in p.parts or '__pycache__' in p.parts or '.venv' in p.parts:
            return False
        return p.suffix in WATCHED_EXTENSIONS
    
    def on_modified(self, event):
        if event.is_directory or not self.should_watch(event.src_path):
            return
        
        try:
            path = Path(event.src_path)
            rel_path = path.relative_to(self.workspace_path)
            
            # Read file content
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Truncate if too large
            if len(content) > MAX_FILE_SIZE:
                content = content[:MAX_FILE_SIZE] + f"\n\n... (truncated, {len(content) - MAX_FILE_SIZE} more chars)"
            
            # Update global context with metadata
            current_file_context[str(rel_path)] = {
                'content': content,
                'timestamp': datetime.now(),
                'size': len(content)
            }
            
            # Limit number of files in context (keep most recent)
            if len(current_file_context) > MAX_FILES_IN_CONTEXT:
                oldest_file = min(current_file_context.items(), key=lambda x: x[1]['timestamp'])[0]
                del current_file_context[oldest_file]
            
            # Notify all connected clients
            loop = asyncio.get_event_loop()
            if loop.is_running():
                asyncio.ensure_future(broadcast_context_update(str(rel_path), content))
            
        except Exception as e:
            print(f"Error reading file {event.src_path}: {e}")
    
    def on_created(self, event):
        self.on_modified(event)


async def broadcast_context_update(filename: str, content: str):
    """Send context update to all connected clients."""
    message = {
        "type": "context_update",
        "filename": filename,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }
    
    disconnected = set()
    for connection in active_connections:
        try:
            await connection.send_json(message)
        except Exception:
            disconnected.add(connection)
    
    # Remove disconnected clients
    active_connections.difference_update(disconnected)


def get_current_context() -> str:
    """Get formatted context from all tracked files."""
    if not current_file_context:
        return ""
    
    # Sort by most recent first
    sorted_files = sorted(
        current_file_context.items(), 
        key=lambda x: x[1]['timestamp'], 
        reverse=True
    )
    
    context_parts = []
    for filename, metadata in sorted_files:
        context_parts.append(f"### File: {filename}\n```\n{metadata['content']}\n```")
    
    return "\n\n".join(context_parts)


async def synthesize_tts(text: str, voice_id: Optional[str] = None):
    """Stream audio bytes from ElevenLabs."""
    if not ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=400,
            detail="ELEVENLABS_API_KEY is not set.",
        )
    chosen_voice = voice_id or ELEVENLABS_VOICE_ID
    if not chosen_voice:
        raise HTTPException(
            status_code=400,
            detail="No ElevenLabs voice id provided. Set ELEVENLABS_VOICE_ID or pass voice_id.",
        )

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{chosen_voice}/stream"
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.7,
            "speed": 1.1,  # 🎯 Slightly faster (1.0 = normal, 1.1 = 10% faster)
            "style": 0.2,  # Slightly more expressive
        },
    }

    async def audio_bytes():
        async with httpx.AsyncClient(timeout=30) as client:
            async with client.stream(
                "POST",
                url,
                headers=headers,
                json=payload,
            ) as resp:
                resp.raise_for_status()
                async for chunk in resp.aiter_bytes():
                    yield chunk

    return audio_bytes()


async def call_gemini(
    user_text: str,
    code_context: Optional[str],
    history: List[Dict[str, str]],
) -> str:
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=400, detail="GEMINI_API_KEY is not set.")

    # Use auto-tracked context if no manual context provided
    if not code_context:
        code_context = get_current_context()

    # Build a simple prompt using history and context.
    history_text = "\n".join(
        [f"User: {item['user']}\nAssistant: {item['assistant']}" for item in history]
    )
    context_block = f"\nCode context:\n{code_context}\n" if code_context else ""
    prompt = (
        f"{SYSTEM_PROMPT}\n"
        f"{context_block}"
        f"{'Conversation so far:\n' + history_text + '\n' if history else ''}"
        f"Latest user message: {user_text}"
    )

    model = genai.GenerativeModel(GEMINI_MODEL)
    response = await asyncio.to_thread(model.generate_content, prompt)
    return response.text


@app.websocket("/ws")
async def chat_ws(websocket: WebSocket):
    await websocket.accept()
    active_connections.add(websocket)
    history: List[Dict[str, str]] = []

    # Send initial context
    if current_file_context:
        await websocket.send_json({
            "type": "context_sync",
            "files": list(current_file_context.keys()),
            "context": get_current_context()
        })

    try:
        while True:
            raw = await websocket.receive_text()
            try:
                message = json.loads(raw)
            except json.JSONDecodeError:
                await websocket.send_json(
                    {"type": "error", "message": "Invalid JSON payload."}
                )
                continue

            msg_type = message.get("type")
            
            if msg_type == "user_message":
                user_text = (message.get("text") or "").strip()
                code_context = message.get("code_context") or None
                if not user_text:
                    await websocket.send_json(
                        {"type": "error", "message": "Empty message."}
                    )
                    continue

                await websocket.send_json({"type": "status", "message": "thinking"})
                try:
                    reply = await call_gemini(user_text, code_context, history)
                except HTTPException as exc:
                    await websocket.send_json({"type": "error", "message": exc.detail})
                    continue
                except Exception as exc:  # pragma: no cover - defensive
                    await websocket.send_json({"type": "error", "message": str(exc)})
                    continue

                history.append({"user": user_text, "assistant": reply})
                await websocket.send_json({"type": "llm_message", "text": reply})
            
            elif msg_type == "request_context":
                # Client requesting current context
                await websocket.send_json({
                    "type": "context_sync",
                    "files": list(current_file_context.keys()),
                    "context": get_current_context()
                })
            
            else:
                await websocket.send_json(
                    {"type": "error", "message": "Unsupported message type."}
                )
                
    except WebSocketDisconnect:
        active_connections.discard(websocket)


@app.post("/tts")
async def tts_endpoint(req: TtsRequest):
    stream = await synthesize_tts(req.text, req.voice_id)
    return StreamingResponse(stream, media_type="audio/mpeg")


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {
        "status": "healthy",
        "service": "KachowAI",
        "gemini_configured": bool(GEMINI_API_KEY),
        "elevenlabs_configured": bool(ELEVENLABS_API_KEY)
    }


@app.get("/")
async def root():
    """Serve landing page."""
    landing_file = FRONTEND_DIR / "landing.html"
    if landing_file.exists():
        return FileResponse(landing_file)
    return {"message": "Landing page not found."}


@app.get("/app")
async def app_page():
    """Serve main application."""
    app_file = FRONTEND_DIR / "app-enhanced.html"
    if not app_file.exists():
        app_file = FRONTEND_DIR / "app.html"
    if app_file.exists():
        return FileResponse(app_file)
    return {"message": "App not found."}


@app.get("/legacy")
async def legacy_app():
    """Serve legacy application (old design)."""
    index_file = FRONTEND_DIR / "index.html"
    if index_file.exists():
        return FileResponse(index_file)
    return {"message": "Legacy app not found."}


@app.post("/execute")
async def execute_code(req: CodeExecutionRequest):
    """Execute Python code with test cases."""
    if req.language != "python":
        raise HTTPException(status_code=400, detail="Only Python is supported currently")
    
    try:
        # Create a temporary file with the code
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(req.code)
            temp_file = f.name
        
        results = []
        all_passed = True
        
        # Run each test case
        for i, test_case in enumerate(req.test_cases):
            try:
                # Execute the code with timeout
                process = subprocess.run(
                    ['python3', temp_file],
                    input=test_case.get('input', ''),
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                
                output = process.stdout.strip()
                expected = test_case.get('expected', '').strip()
                passed = output == expected
                
                results.append({
                    "test_num": i + 1,
                    "input": test_case.get('input', ''),
                    "expected": expected,
                    "output": output,
                    "passed": passed,
                    "error": process.stderr if process.stderr else None
                })
                
                if not passed:
                    all_passed = False
                    
            except subprocess.TimeoutExpired:
                results.append({
                    "test_num": i + 1,
                    "input": test_case.get('input', ''),
                    "expected": test_case.get('expected', ''),
                    "output": "",
                    "passed": False,
                    "error": "Timeout: Code took too long to execute"
                })
                all_passed = False
            except Exception as e:
                results.append({
                    "test_num": i + 1,
                    "input": test_case.get('input', ''),
                    "expected": test_case.get('expected', ''),
                    "output": "",
                    "passed": False,
                    "error": str(e)
                })
                all_passed = False
        
        # Clean up temp file
        import os
        try:
            os.unlink(temp_file)
        except:
            pass
        
        return {
            "success": True,
            "all_passed": all_passed,
            "results": results,
            "total_tests": len(results),
            "passed_tests": sum(1 for r in results if r["passed"])
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Execution error: {str(e)}")


# Initialize file watcher on startup
@app.on_event("startup")
async def startup_event():
    if WORKSPACE_DIR.exists():
        print(f"👀 Watching workspace: {WORKSPACE_DIR}")
        event_handler = CodeFileWatcher(WORKSPACE_DIR)
        observer = Observer()
        observer.schedule(event_handler, str(WORKSPACE_DIR), recursive=True)
        observer.start()
        
        # Store observer in app state for cleanup
        app.state.observer = observer
    else:
        print(f"⚠️  Workspace directory not found: {WORKSPACE_DIR}")


@app.on_event("shutdown")
async def shutdown_event():
    if hasattr(app.state, 'observer'):
        app.state.observer.stop()
        app.state.observer.join()
