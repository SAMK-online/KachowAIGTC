<div align="center">

# ⚡ KachowAI

### The Voice Layer for Peer Programming

**Master data structures & algorithms through natural conversation with an AI mentor that sees your code in real-time.**

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-61dafb.svg)](https://reactjs.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Demo Video](#) • [Launch App](#getting-started) • [Documentation](#features)

</div>

---

## 🎯 What is KachowAI?

KachowAI is a **voice-first AI peer programming companion** that transforms how developers learn data structures and algorithms. Instead of typing questions and copy-pasting code, you have natural conversations with an AI mentor that automatically sees your code changes in real-time.

Think of it as having an expert pair programmer sitting next to you—one that guides you with Socratic questions, never just hands you answers, and speaks naturally through voice.

### ✨ The Vision

> **Voice should be the primary interface between humans and AI-powered coding tools.**

While AI assistants have revolutionized coding, they still require typing—breaking flow and slowing thinking. We're building the voice layer for peer programming.

**Today:** Proving the model works for DSA learning with voice-driven Socratic teaching.  
**Tomorrow:** Full IDE integration (Cursor, Windsurf) with access to entire codebases for voice-powered pair programming.

---

## 🚀 Key Features

### 🎤 Voice-First Interface
- **Continuous voice sessions** with instant responses
- **Natural conversation flow** - talk, think out loud, learn
- **ElevenLabs TTS** with browser fallback for professional quality
- **Smart text sanitization** - no robotic "back quote" interruptions

### 🔍 Real-Time Context Awareness
- **Automatic file watching** across your workspace
- **Tracks 5 most recent files** with instant updates
- **WebSocket-powered** synchronization (0ms latency)
- **Supports 10+ languages** - Python, JS, TypeScript, C++, Go, Rust, and more

### 🎓 Socratic Teaching Methodology
- **Guided discovery** instead of direct answers
- **Progressive hints** that build understanding
- **One question at a time** for natural learning
- **Context-aware guidance** based on your actual code

### ⚡ Powered by Latest AI
- **Gemini 2.5 Flash** - Google's latest model with 1M+ token context
- **Ultra-fast responses** for real-time conversations
- **Advanced reasoning** for complex algorithm discussions
- **Knowledge cutoff: January 2025**

### 💻 Integrated Code Execution
- **Run Python code** against test cases in real-time
- **Instant feedback** with pass/fail results
- **Multiple test cases** with detailed error messages
- **Safe sandboxed execution**

### 🎯 Smart Features
- **Natural speech synthesis** - converts O(N^2) to "O of N squared"
- **Comfortable 1.15x speed** - fast but clear
- **Auto-greeting** - AI introduces itself when you start
- **Persistent history** - remembers your conversation

---

## 🏗️ Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Google Gemini 2.5 Flash** - Latest LLM via Vertex AI
- **ElevenLabs API** - Premium text-to-speech
- **Watchdog** - File system monitoring
- **WebSockets** - Real-time bidirectional communication

### Frontend
- **React 18** - Modern UI framework (CDN-based)
- **Web Speech API** - Browser speech recognition
- **WebSocket Client** - Real-time updates
- **Glassmorphism UI** - Modern dark design

### Infrastructure
- **Python 3.9+** - Core runtime
- **Uvicorn** - ASGI server
- **httpx** - Async HTTP client

---

## 🎬 Quick Start

### Prerequisites
```bash
# Python 3.9 or higher
python --version

# pip package manager
pip --version
```

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/kachowai.git
cd kachowai
```

2. **Set up backend**
```bash
cd backend
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
# Create .env file
cp .env.example .env

# Edit .env with your API keys
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash-preview-09-2025
ELEVENLABS_API_KEY=your_elevenlabs_key_here  # Optional
ELEVENLABS_VOICE_ID=your_voice_id_here        # Optional
WORKSPACE_DIR=/path/to/your/workspace
```

4. **Launch the application**
```bash
# Start the server
uvicorn app:app --reload --port 8000

# Open your browser
open http://localhost:8000
```

### Getting API Keys

**Google Gemini API:**
1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create an API key
3. Add to `.env` as `GEMINI_API_KEY`

**ElevenLabs (Optional):**
1. Visit [ElevenLabs](https://elevenlabs.io)
2. Sign up for free account
3. Get API key from Profile → API Keys
4. Choose a voice ID from [Voice Library](https://elevenlabs.io/voice-library)
5. Add to `.env`

*Note: ElevenLabs is optional. The app works with browser TTS by default.*

---

## ☁️ Cloud Deployment

### Deploy to Google Cloud Run (Production)

**One-command deployment:**
```bash
./deploy.sh
```

Or follow the detailed guide in **[CLOUD_RUN_QUICKSTART.md](CLOUD_RUN_QUICKSTART.md)**

**Benefits:**
- ✅ Fully managed infrastructure
- ✅ Auto-scaling (0 to N instances)
- ✅ Global CDN with HTTPS
- ✅ Pay only for what you use
- ✅ 2M requests/month FREE

**Quick Manual Deploy:**
```bash
# Install gcloud CLI and login
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Build and deploy
docker build -t gcr.io/YOUR_PROJECT_ID/kachowai:latest .
gcloud auth configure-docker
docker push gcr.io/YOUR_PROJECT_ID/kachowai:latest

gcloud run deploy kachowai \
  --image gcr.io/YOUR_PROJECT_ID/kachowai:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --set-env-vars "GEMINI_API_KEY=YOUR_KEY,GEMINI_MODEL=gemini-2.5-flash-preview-09-2025"
```

See **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** for advanced configuration, custom domains, and CI/CD setup.

---

## 📖 How to Use

### 1. Start a Voice Session

Click **"🎤 Start Voice Session"** and wait for the AI greeting:

```
AI: "Hi! I'm Kachow, your AI pair programming mentor. 
     How can I help you today?"
```

### 2. Select a Problem

Choose from the problem list (e.g., "Two Sum") or describe your own challenge.

### 3. Start Coding

Type your solution in the code editor. The AI automatically sees your code in real-time.

### 4. Have a Conversation

Talk naturally with the AI:

```
You: "I'm working on Two Sum. Can you help me think through this?"

AI: "Great! What do you think the problem is asking you to find?"

You: "Two numbers that add up to a target"

AI: "Exactly! What approach would you try first?"

You: "Maybe a nested loop?"

AI: "That works! What's the time complexity of that?"

You: "O of N squared"

AI: "Right! Can we do better than that?"
```

### 5. Run Tests

Click **"▶ Run Tests"** to execute your code against test cases and see results.

### 6. Iterate

Keep refining based on AI feedback until you've mastered the problem!

---

## 🏛️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │  Problems    │  │  Code Editor │  │     Chat     │ │
│  │    List      │  │   (Monaco)   │  │  (Voice/Text)│ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   WebSocket Layer                       │
│  • Real-time bidirectional communication               │
│  • Context updates • Voice recognition • TTS           │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐ │
│  │ File Watcher │  │ Gemini 2.5   │  │ Code Runner  │ │
│  │  (Watchdog)  │  │    Flash     │  │  (Python)    │ │
│  └──────────────┘  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │  ElevenLabs  │  │   Context    │                   │
│  │     TTS      │  │  Management  │                   │
│  └──────────────┘  └──────────────┘                   │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  External Services                      │
│  • Google Vertex AI (Gemini)                           │
│  • ElevenLabs API (TTS)                                │
│  • File System (Workspace)                             │
└─────────────────────────────────────────────────────────┘
```

### Key Components

**File Watcher:**
- Monitors workspace for code changes
- Filters by extension (.py, .js, .ts, etc.)
- Broadcasts updates via WebSocket
- Maintains context of 5 most recent files

**AI Mentor (Gemini 2.5 Flash):**
- Processes user questions with full code context
- Implements Socratic teaching methodology
- One question at a time for natural flow
- Maintains conversation history

**Code Execution Engine:**
- Runs Python code in sandboxed environment
- Executes against provided test cases
- Returns pass/fail results with error messages
- Timeout protection (5 seconds per test)

**Voice Interface:**
- Browser Speech Recognition for input
- ElevenLabs + Browser TTS for output
- Text sanitization for natural speech
- Smart speed control (1.15x)

---

## 🎓 Educational Philosophy

### Socratic Teaching Approach

KachowAI follows strict Socratic principles:

❌ **NEVER:**
- Provide complete solutions upfront
- Jump to final algorithms immediately
- Give answers without making you think

✅ **ALWAYS:**
- Ask clarifying questions about constraints
- Help identify patterns (two pointers, hash maps, DP, etc.)
- Give progressive hints that build understanding
- Let you propose approaches first
- Explain WHY approaches work or don't work
- Only provide full solutions when explicitly requested

### Example Interaction

```
User: "Help me with Two Sum"

AI: "Great choice! What data structure allows you to check 
     if an element exists in O of 1 time?"

User: "A hash map"

AI: "Perfect! When you iterate over the nums array, 
     what would you store in the hash map?"

User: "The number and its index"

AI: "Exactly! Now, how would you use that to find 
     the complement?"
```

---

## 🗺️ Roadmap

### ✅ Phase 1: Core Features (Completed)
- [x] Voice-first interface with continuous sessions
- [x] Real-time code context awareness
- [x] Socratic teaching methodology
- [x] Python code execution with test cases
- [x] Natural speech synthesis
- [x] Gemini 2.5 Flash integration
- [x] File watching system
- [x] WebSocket real-time updates

### 🚧 Phase 2: Enhanced Learning (In Progress)
- [ ] More LeetCode problems (currently 8)
- [ ] Difficulty progression system
- [ ] Hint levels (gentle → direct)
- [ ] Progress tracking
- [ ] Problem recommendations
- [ ] Visual algorithm visualization

### 🔮 Phase 3: IDE Integration (Future)
- [ ] VS Code extension
- [ ] Cursor IDE integration
- [ ] Windsurf integration
- [ ] Full codebase access
- [ ] Multi-file refactoring guidance
- [ ] Debugging assistance
- [ ] Code review mode

### 🌟 Phase 4: Platform Evolution (Vision)
- [ ] Support for all programming languages
- [ ] System design discussions
- [ ] Architecture guidance
- [ ] Team collaboration features
- [ ] Interview preparation mode
- [ ] Custom problem sets

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Areas for Contribution

1. **More Problems** - Add LeetCode problems with test cases
2. **Language Support** - Add more programming languages
3. **UI Improvements** - Enhance the interface
4. **Documentation** - Improve guides and examples
5. **Bug Fixes** - Report and fix issues
6. **Feature Requests** - Suggest new capabilities

### Development Setup

```bash
# Fork the repository
# Clone your fork
git clone https://github.com/yourusername/kachowai.git

# Create a feature branch
git checkout -b feature/amazing-feature

# Make your changes
# Test thoroughly

# Commit with descriptive messages
git commit -m "Add amazing feature"

# Push to your fork
git push origin feature/amazing-feature

# Open a Pull Request
```

### Code Style

- **Python:** Follow PEP 8
- **JavaScript:** Use ES6+ features
- **Comments:** Clear and concise
- **Tests:** Include test cases for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

### Powered By

- **Google Gemini 2.5 Flash** - Latest AI model with exceptional reasoning
- **ElevenLabs** - Professional text-to-speech API
- **FastAPI** - Modern Python web framework
- **React** - UI library for building interfaces

### Inspiration

Built with inspiration from the future of voice-first development tools. Special thanks to the AI coding assistant community for pushing the boundaries of what's possible.

---

## 📞 Contact & Support

- **GitHub Issues:** [Report a bug or request a feature](https://github.com/yourusername/kachowai/issues)
- **Discussions:** [Join the conversation](https://github.com/yourusername/kachowai/discussions)
- **Email:** your.email@example.com

---

<div align="center">

### 🚀 Ready to Transform Your Learning?

**[Launch KachowAI](http://localhost:8000)** • **[View Demo](#)** • **[Read Docs](#)**

---

**Built with ⚡ by developers, for developers**

⭐ **Star this repo** if you find it helpful!

</div>
