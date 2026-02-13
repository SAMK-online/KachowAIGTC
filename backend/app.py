import asyncio
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Set
from datetime import datetime

from openai import AsyncOpenAI
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, StreamingResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import subprocess
import tempfile
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Optional Riva imports (for TTS)
try:
    import riva.client
    RIVA_AVAILABLE = True
except ImportError:
    RIVA_AVAILABLE = False
    print("⚠️  nvidia-riva-client not installed. Riva TTS unavailable.")


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
# NVIDIA API (primary)
NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY")
NVIDIA_MODEL = os.getenv("NVIDIA_MODEL", "meta/llama-3.1-70b-instruct")
RIVA_FUNCTION_ID = os.getenv("RIVA_FUNCTION_ID")

# ElevenLabs (fallback TTS)
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

# Initialize NVIDIA NIM client (OpenAI-compatible)
nvidia_client = None
if NVIDIA_API_KEY:
    nvidia_client = AsyncOpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY
    )
    print(f"✅ NVIDIA NIM configured with model: {NVIDIA_MODEL}")

SYSTEM_PROMPT = """You are my Socratic DSA mentor. You ONLY ask questions - you NEVER give answers.

⛔ ABSOLUTE RULES - NEVER BREAK:
1. NEVER state the time/space complexity - ASK what they think it is
2. NEVER suggest data structures - ASK what data structure might help
3. NEVER explain the algorithm - ASK questions that lead them to discover it
4. NEVER give code unless they say "give me the solution"
5. MAXIMUM 2 sentences. ONE question only.

🎯 YOUR ONLY JOB: Ask short guiding questions.

📋 QUESTION PROGRESSION:
1. First ask about constraints and edge cases
2. Ask what approach they're considering
3. If wrong, ask "what would happen if..." to expose the flaw
4. Ask what data structure could help (don't name it!)
5. Ask about complexity only AFTER they state theirs

⚠️ WHEN THEY'RE WRONG:
- First time wrong: Ask a question that hints at the issue
- Second time wrong: Ask a more direct question
- Third time wrong: You may give a small hint (not the answer)
- ONLY give the answer if they explicitly ask

✅ GOOD (questions only):
- "What's your initial approach?"
- "What would the time complexity be with nested loops?"
- "Is there a data structure that could speed up lookups?"
- "What edge case might break this?"

❌ NEVER SAY THESE:
- "The time complexity is O of N squared" (WRONG - ask them!)
- "You could use a hash table" (WRONG - ask what structure helps!)
- "That's O of N time" (WRONG - let them figure it out!)
- "Here's how it works..." (WRONG - no explanations!)

🗣️ VOICE: Short, natural, no code formatting. Say "O of N" not "O(N)".

Remember: If you catch yourself about to STATE something, turn it into a QUESTION instead."""

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


async def synthesize_tts_riva(text: str, voice: str = "English-US.Female-1") -> bytes:
    """Synthesize speech using NVIDIA Riva TTS."""
    if not RIVA_AVAILABLE:
        raise HTTPException(status_code=400, detail="Riva TTS not available (nvidia-riva-client not installed)")

    if not NVIDIA_API_KEY or not RIVA_FUNCTION_ID:
        raise HTTPException(status_code=400, detail="Riva TTS not configured (NVIDIA_API_KEY and RIVA_FUNCTION_ID required)")

    try:
        # Create Riva auth for NVIDIA API Catalog
        metadata = [
            ("function-id", RIVA_FUNCTION_ID),
            ("authorization", f"Bearer {NVIDIA_API_KEY}")
        ]

        auth = riva.client.Auth(
            ssl_cert=None,
            use_ssl=True,
            uri="grpc.nvcf.nvidia.com:443",
            metadata_args=metadata
        )

        tts_service = riva.client.SpeechSynthesisService(auth)

        # Synthesize audio
        responses = tts_service.synthesize_online(
            text=text,
            voice_name=voice,
            language_code="en-US",
            sample_rate_hz=22050,
            encoding=riva.client.AudioEncoding.LINEAR_PCM
        )

        # Collect all audio chunks
        audio_bytes = b""
        for response in responses:
            audio_bytes += response.audio

        return audio_bytes

    except Exception as e:
        print(f"Riva TTS error: {e}")
        raise HTTPException(status_code=500, detail=f"Riva TTS failed: {str(e)}")


async def synthesize_tts_elevenlabs(text: str, voice_id: Optional[str] = None):
    """Stream audio bytes from ElevenLabs (fallback)."""
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
            "speed": 1.1,
            "style": 0.2,
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


async def synthesize_tts(text: str, voice_id: Optional[str] = None):
    """Unified TTS: Try Riva first, fallback to ElevenLabs."""
    # Try Riva first if configured
    if NVIDIA_API_KEY and RIVA_FUNCTION_ID and RIVA_AVAILABLE:
        try:
            audio_data = await synthesize_tts_riva(text, voice_id or "English-US.Female-1")
            return audio_data, "audio/wav"  # Riva returns WAV
        except Exception as e:
            print(f"⚠️  Riva TTS failed, falling back to ElevenLabs: {e}")

    # Fallback to ElevenLabs
    if ELEVENLABS_API_KEY:
        stream = await synthesize_tts_elevenlabs(text, voice_id)
        return stream, "audio/mpeg"  # ElevenLabs returns MP3

    raise HTTPException(status_code=400, detail="No TTS service configured")


async def call_llm(
    user_text: str,
    code_context: Optional[str],
    history: List[Dict[str, str]],
) -> str:
    """Call NVIDIA Nemotron via NIM API (OpenAI-compatible)."""
    if not nvidia_client:
        raise HTTPException(status_code=400, detail="NVIDIA_API_KEY is not set.")

    # Use auto-tracked context if no manual context provided
    if not code_context:
        code_context = get_current_context()

    # Build messages array for chat completion
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Add conversation history
    for item in history:
        messages.append({"role": "user", "content": item["user"]})
        messages.append({"role": "assistant", "content": item["assistant"]})

    # Add context and current message
    context_block = f"\nCode context:\n{code_context}\n" if code_context else ""
    messages.append({"role": "user", "content": f"{context_block}{user_text}"})

    # Call NVIDIA NIM
    response = await nvidia_client.chat.completions.create(
        model=NVIDIA_MODEL,
        messages=messages,
        temperature=0.5,  # Lower for more focused responses
        max_tokens=150    # Limit to encourage short responses
    )

    return response.choices[0].message.content


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
                    reply = await call_llm(user_text, code_context, history)
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
    result, media_type = await synthesize_tts(req.text, req.voice_id)

    # Riva returns bytes, ElevenLabs returns async generator
    if isinstance(result, bytes):
        return Response(content=result, media_type=media_type)
    else:
        return StreamingResponse(result, media_type=media_type)


@app.get("/health")
async def health_check():
    """Health check endpoint for Cloud Run."""
    return {
        "status": "healthy",
        "service": "KachowAI",
        "nvidia_llm_configured": bool(NVIDIA_API_KEY),
        "nvidia_model": NVIDIA_MODEL if NVIDIA_API_KEY else None,
        "riva_tts_configured": bool(NVIDIA_API_KEY and RIVA_FUNCTION_ID and RIVA_AVAILABLE),
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
