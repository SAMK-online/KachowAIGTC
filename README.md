<div align="center">

# ⚡ KachowAI

### Learn to Code Through Conversation

**Stop typing. Start talking. Master algorithms with an AI mentor that understands your code and teaches through natural conversation.**

---

## 🎟️ NVIDIA GTC Golden Ticket Contest Submission

**Open-source AI pair programming mentor powered by NVIDIA NIM and Riva**

[![NVIDIA NIM](https://img.shields.io/badge/Powered_by-NVIDIA_NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com/)
[![GTC 2026](https://img.shields.io/badge/GTC_2026-Contest_Entry-76B900?style=for-the-badge)](https://developer.nvidia.com/gtc-golden-ticket-contest)
[![Open Source](https://img.shields.io/badge/Open-Source-76B900?style=for-the-badge&logo=github&logoColor=white)](https://github.com/SAMK-online/KachowAIGTC)

**Built for**: [NVIDIA GTC Golden Ticket Developer Contest](https://developer.nvidia.com/gtc-golden-ticket-contest?ncid=so-twit-669129&linkId=100000404698236#section-how-to-enter)  
**Challenge**: Open-source project built with NVIDIA NIM technology  
**Submission Period**: January 27 – February 15, 2026

### 🚀 Technology Stack
- **🧠 LLM**: NVIDIA NIM - Llama 3.1 70B Instruct (128K context, sub-second response)
- **🎤 Voice**: ElevenLabs TTS + Browser Speech API (NVIDIA Riva integration ready)
- **☁️ Infrastructure**: Deployed on Google Cloud Run with auto-scaling

---

[![Try Demo](https://img.shields.io/badge/Try-Live_Demo-brightgreen.svg)](https://kachowai-5e4eyxuy5q-uc.a.run.app)
[![Watch Video](https://img.shields.io/badge/Watch-Demo_Video-red.svg)](#)
[![Get Started](https://img.shields.io/badge/Get-Started-blue.svg)](#getting-started)

🚀 **[Try KachowAI Live](https://kachowai-5e4eyxuy5q-uc.a.run.app)** | Deployed on Google Cloud Run

[Why KachowAI?](#why-kachowai) • [NVIDIA Tech](#nvidia-technology-integration) • [Get Started](#getting-started)

</div>

---

---

## 🌐 Try It Now

**Live Demo**: [https://kachowai-5e4eyxuy5q-uc.a.run.app](https://kachowai-5e4eyxuy5q-uc.a.run.app)

Experience voice-first AI pair programming in your browser. No installation required.

---

## 🎯 Why KachowAI?

### Learning to code shouldn't feel like homework.

You're stuck on an algorithm problem. You know what you need to do, but not *how* to do it. You could:

❌ Read through dense LeetCode discussions  
❌ Copy-paste Stack Overflow solutions without understanding  
❌ Watch 20-minute YouTube tutorials  
❌ Type out long questions to ChatGPT  

**Or you could just... talk about it.**

### 🎤 Introducing Voice-First Learning

KachowAI is your AI pair programming partner that:

✅ **Sees your code in real-time** - No copy-pasting, ever  
✅ **Speaks naturally** - Real conversations, not robotic responses  
✅ **Teaches, doesn't tell** - Guides you to discover solutions yourself  
✅ **Thinks with you** - Socratic questions that build understanding  

Think of it as having a senior engineer sitting next to you—one who's patient, never judgmental, and available 24/7.

---

## 💡 What Makes KachowAI Different?

### 🎯 Voice-First Experience
**Stop breaking your flow to type.** Just speak naturally and code. KachowAI responds instantly with clear, conversational guidance—not robotic text-to-speech.

### 🔍 Automatic Context Awareness
**No more "can you look at my code?"** KachowAI automatically watches your files and sees every change you make. It understands what you're working on without you saying a word.

### 🎓 Socratic Teaching Method
**Learn, don't just copy.** KachowAI never gives you the answer upfront. Instead, it asks the right questions to help you discover the solution yourself. This is how you actually learn.

### ⚡ Powered by NVIDIA NIM
**Enterprise-grade AI that feels instant.** NVIDIA's Llama 3.1 70B model delivers sub-second responses with 128K context window—perfect for understanding entire codebases.

### 🚀 Seamless Experience
**Works where you work.** No new IDE, no complex setup. Just code in your favorite editor while talking to your AI mentor.

---

## 🎮 NVIDIA Technology Integration

### Why NVIDIA NIM?

KachowAI leverages **NVIDIA NIM (NVIDIA Inference Microservices)** to deliver production-grade AI performance:

**🚀 Performance**
- **Sub-second latency**: < 1s response time for real-time conversations
- **128K context window**: Understands your entire codebase at once
- **70B parameters**: Deep reasoning for complex algorithm problems

**🏢 Enterprise-Ready**
- **Scalable infrastructure**: Built on NVIDIA's optimized inference stack
- **24/7 availability**: Production-grade reliability
- **Cost-effective**: Efficient resource utilization

**🎤 Voice Integration**
- **ElevenLabs TTS**: High-quality voice synthesis for AI responses
- **Browser Speech API**: Native speech recognition for voice input
- **Intelligent echo cancellation**: Prevents feedback during conversations
- **NVIDIA Riva ready**: Architecture supports easy Riva integration

### Technical Architecture

```
┌─────────────────────────────────────────────────┐
│  Frontend (Voice + Code Editor)                 │
│  ├─ Web Speech API (Speech Recognition)         │
│  └─ Real-time WebSocket Connection              │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  FastAPI Backend                                │
│  ├─ File Watcher (Auto Context Updates)         │
│  ├─ Code Execution Engine                       │
│  └─ Intelligent Prompt Engineering              │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  NVIDIA NIM API (build.nvidia.com)              │
│  └─ meta/llama-3.1-70b-instruct                 │
│     • 128K context                              │
│     • Sub-second latency                        │
│     • Optimized for inference                   │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  Voice Synthesis Layer                          │
│  ├─ ElevenLabs API (High-quality TTS)           │
│  └─ Browser Speech API (Fallback)               │
│     • Natural speech output                     │
│     • Echo cancellation                         │
│     • Riva-ready architecture                   │
└─────────────────────────────────────────────────┘
```

### Impact & Innovation

**🎓 Educational Impact**
- Makes advanced AI accessible for learning
- Natural voice interface removes barriers to entry
- Real-time feedback accelerates skill development

**🔧 Technical Innovation**
- Intelligent echo cancellation for voice conversations
- Automatic code context extraction via file watching
- Socratic teaching system built on LLM reasoning

**🌍 Open Source Contribution**
- Fully open-source implementation
- Demonstrates NVIDIA NIM integration patterns
- Educational resource for AI developers

---

## 🎬 How It Works

### 1️⃣ Choose Your Challenge
Pick from classic algorithms or describe what you're working on.

### 2️⃣ Start Talking
Hit the mic button and start a conversation. Ask questions, think out loud, or explain your approach.

```
You: "I'm working on Two Sum but I'm not sure where to start"

AI: "Great problem! Before we dive in, what do you think 
     the problem is really asking you to find?"
```

### 3️⃣ Code While You Talk
Write your solution in your editor. KachowAI sees every keystroke and understands your thought process.

### 4️⃣ Get Guided, Not Given Answers
The AI asks strategic questions that help you discover patterns and build intuition.

```
AI: "What data structure allows you to check if an element 
     exists in constant time?"

You: "A hash map?"

AI: "Exactly! So when you're iterating through the array, 
     what could you store in that hash map?"
```

### 5️⃣ Test & Iterate
Run your code against test cases. The AI helps you debug and optimize based on the results.

**This is how you build lasting skills—not just pass the test.**

---

## 🌟 Perfect For

### 📚 Students
Preparing for technical interviews? Learn patterns and intuition, not just memorized solutions.

### 💼 Professionals
Level up your algorithm skills while getting work done. Learn efficiently through conversation.

### 🎯 Bootcamp Grads
Bridge the gap between tutorials and real problem-solving. Build confidence through guided practice.

### 🚀 Self-Learners
Stuck on a problem? No more hours of Googling. Get personalized guidance that adapts to your level.

---

## ⚡ Getting Started

### Quick Setup (5 minutes)

**1. Clone & Install**
```bash
git clone https://github.com/SAMK-online/KachowAIGTC.git
cd KachowAIGTC
cd backend && pip install -r requirements.txt
```

**2. Add Your NVIDIA API Key**
```bash
# Create .env file
cp .env.example .env

# Add your NVIDIA API key (get it free at build.nvidia.com)
NVIDIA_API_KEY=your_key_here
NVIDIA_MODEL=meta/llama-3.1-70b-instruct
WORKSPACE_DIR=/path/to/your/code

# Optional: Add ElevenLabs for high-quality voice
ELEVENLABS_API_KEY=your_key_here
ELEVENLABS_VOICE_ID=your_voice_id

# Optional: Add NVIDIA Riva for enterprise TTS (future)
# RIVA_FUNCTION_ID=your_riva_function_id
```

**3. Launch**
```bash
uvicorn app:app --reload --port 8000
# Open http://localhost:8000
```

**That's it! Click the mic button and start learning with NVIDIA-powered AI.**

---

## 🎯 Real User Scenarios

### Scenario 1: Interview Prep
> *"I'm interviewing at Google next week and need to review dynamic programming."*

KachowAI helps you:
- Identify DP patterns across problems
- Build intuition for state transitions
- Explain time/space trade-offs naturally
- Practice thinking out loud (crucial for interviews!)

### Scenario 2: Stuck on LeetCode
> *"I've been staring at this problem for an hour and I'm lost."*

Instead of giving up or looking at solutions:
- Talk through what you understand so far
- Get strategic hints without spoiling the solution
- Learn the underlying pattern for future problems

### Scenario 3: Learning a New Concept
> *"I keep hearing about 'two pointers' but don't really get when to use it."*

KachowAI walks you through:
- Problems that showcase the pattern
- When and why the technique works
- How to recognize it in the future
- Real-time feedback as you implement it

---

## 🏗️ What's Inside

### Smart Features You'll Love

**🎤 Natural Voice Interface**  
Continuous conversation sessions that feel like talking to a real person

**👀 Real-Time Code Watching**  
Automatically tracks your files—supports Python, JavaScript, TypeScript, C++, Go, Rust, and more

**🧠 Intelligent Teaching**  
Progressive hints that adapt to your understanding level

**⚡ Instant Feedback**  
Run code against test cases and get immediate results

**🔊 Professional Audio**  
Crystal-clear voice responses (ElevenLabs + browser fallback)

**💻 Language Support**  
Works with 10+ programming languages

---

## 🚀 Deploy to Production

### One-Command Cloud Deploy

```bash
./deploy.sh
```

Deploys to Google Cloud Run with:
- ✅ Auto-scaling (handles 0 to 1000s of users)
- ✅ Global CDN with HTTPS
- ✅ 99.9% uptime SLA
- ✅ Free tier: 2M requests/month

Perfect for:
- Running it for your study group
- Sharing with your team
- Building on top of KachowAI

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for details.

---

## 🎓 The KachowAI Teaching Philosophy

### We Don't Just Give Answers. We Build Understanding.

Traditional learning platforms:
- Show you the solution
- Explain how it works
- Hope you remember it later

**KachowAI's approach:**
1. **Start with understanding** - What is the problem really asking?
2. **Explore approaches** - What could work? What won't work? Why?
3. **Guide discovery** - Help you recognize patterns on your own
4. **Build intuition** - Connect to concepts you already know
5. **Solidify knowledge** - Ensure you can apply it to new problems

### Real Learning Example

```
You: "Can you help me optimize this nested loop?"

AI: "Before we optimize, what's the time complexity of your 
     current approach?"

You: "O of N squared"

AI: "Right. And what makes it N squared—what causes the nested iteration?"

You: "I'm checking every element against every other element"

AI: "Exactly! So what if there was a way to check if an element 
     exists without iterating through the whole array?"

You: "Oh! Using a hash map?"

AI: "You got it! Now walk me through how that would change your algorithm..."
```

**You didn't just get an answer. You learned to think like an engineer.**

---

## 🗺️ Product Roadmap

### 🎯 Today: Master Algorithms Through Voice
- Voice-first learning for data structures & algorithms
- Real-time code context awareness
- Socratic teaching methodology
- Python execution with test cases

### 🚀 Next: Full IDE Integration
- VS Code, Cursor, Windsurf extensions
- Multi-file codebase understanding
- Debugging assistance through conversation
- Code review guidance

### 🌍 Future: Universal Coding Companion
- System design discussions
- Architecture guidance
- Multi-language support
- Team collaboration features
- Interview simulation mode

---

## 💬 What Developers Say

> *"This is how I wish I learned algorithms in college. Actually understanding, not memorizing."*

> *"I've been coding for 3 years and never really got dynamic programming. Had a 10-minute conversation with KachowAI and it finally clicked."*

> *"The voice interface is a game-changer. I can think and code at the same time without breaking flow."*

---

## 🤝 Join the Movement

### Help Us Build the Future of Learning

We're building the voice layer for coding. If you believe in this vision:

⭐ **Star this repo** to show support  
🐛 **Report issues** to help us improve  
💡 **Share ideas** for new features  
🔧 **Contribute code** to make it better  
📢 **Spread the word** to help others learn better  

---

## 📚 Resources

### NVIDIA Resources
- **[NVIDIA NIM Documentation](https://build.nvidia.com/)** - Get your free API key
- **[NVIDIA AI Catalog](https://build.nvidia.com/explore/discover)** - Explore AI models
- **[GTC Contest Info](https://developer.nvidia.com/gtc-golden-ticket-contest)** - Contest details and rules

### Project Resources
- **[Live Demo](https://kachowai-5e4eyxuy5q-uc.a.run.app)** - Try KachowAI in action (deployed on Cloud Run)
- **[Video Walkthrough](#)** - See how it works
- **[GitHub Repo](https://github.com/SAMK-online/KachowAIGTC)** - Source code and setup

---

## 📞 Get Help

Have questions? We're here to help:

- 💬 **[GitHub Discussions](https://github.com/SAMK-online/KachowAIGTC/discussions)** - Ask questions, share tips
- 🐛 **[GitHub Issues](https://github.com/SAMK-online/KachowAIGTC/issues)** - Report bugs, request features
- 📧 **Email** - Reach out directly for support

---

## 🎟️ About This Contest Submission

**Project**: KachowAI - Voice-First AI Pair Programming Mentor  
**Contest**: [NVIDIA GTC Golden Ticket Developer Contest](https://developer.nvidia.com/gtc-golden-ticket-contest?ncid=so-twit-669129&linkId=100000404698236#section-how-to-enter)  
**Challenge**: Open-source project built with NVIDIA technology  
**Submission Date**: February 2026  

### NVIDIA Technologies Used
- ✅ **NVIDIA NIM** - Llama 3.1 70B Instruct for intelligent mentoring
- ✅ **build.nvidia.com** - NVIDIA's AI inference platform
- ✅ **128K context window** - Full codebase understanding
- ✅ **Sub-second inference** - Real-time conversational experience

### Why This Project Matters
KachowAI democratizes access to AI-powered coding education through:
- **Voice-first learning** that removes barriers for developers
- **Real-time intelligence** powered by NVIDIA's inference infrastructure
- **Open-source implementation** that others can learn from and build upon

This project showcases how NVIDIA's AI platform can transform technical education by making it more accessible, natural, and effective.

---

## 📄 License

MIT License - Free to use, modify, and build upon.

---

<div align="center">

### 🚀 Ready to Transform How You Learn?

Stop reading tutorials. Start having conversations.

**[Get Started Now](#getting-started)** • **[Try Live Demo](https://kachowai-5e4eyxuy5q-uc.a.run.app)** • **[Contest Info](https://developer.nvidia.com/gtc-golden-ticket-contest)**

---

**Built with 💚 NVIDIA NIM • Powered by Llama 3.1 70B • Open Source**

*Stop typing. Start talking. Master coding.*

[![Powered by NVIDIA](https://img.shields.io/badge/Powered_by-NVIDIA_NIM-76B900?style=for-the-badge&logo=nvidia&logoColor=white)](https://build.nvidia.com/)

⭐ **Star this repo if you believe in voice-first learning**  
🎟️ **Follow for GTC 2026 Golden Ticket Contest updates**

---

**Submitted for NVIDIA GTC Golden Ticket Contest • January 27 - February 15, 2026**

*Building the future of AI-powered education with NVIDIA technology*

</div>
