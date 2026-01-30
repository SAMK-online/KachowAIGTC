<div align="center">

# ⚡ KachowAI

### Learn to Code Through Conversation

**Stop typing. Start talking. Master algorithms with an AI mentor that understands your code and teaches through natural conversation.**

[![Try Demo](https://img.shields.io/badge/Try-Live_Demo-brightgreen.svg)](#getting-started)
[![Watch Video](https://img.shields.io/badge/Watch-Demo_Video-red.svg)](#)
[![Get Started](https://img.shields.io/badge/Get-Started-blue.svg)](#getting-started)

[Why KachowAI?](#why-kachowai) • [See It In Action](#how-it-works) • [Get Started](#getting-started)

</div>

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

### ⚡ Powered by Cutting-Edge AI
**Fast enough to feel real.** Gemini 2.5 Flash delivers instant responses with deep reasoning—no awkward pauses, just natural conversation flow.

### 🚀 Seamless Experience
**Works where you work.** No new IDE, no complex setup. Just code in your favorite editor while talking to your AI mentor.

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
git clone https://github.com/SAMK-online/KachowAI.git
cd KachowAI
cd backend && pip install -r requirements.txt
```

**2. Add Your API Key**
```bash
# Create .env file
cp .env.example .env

# Add your Gemini API key (get it free at ai.google.dev)
GEMINI_API_KEY=your_key_here
WORKSPACE_DIR=/path/to/your/code
```

**3. Launch**
```bash
uvicorn app:app --reload --port 8000
# Open http://localhost:8000
```

**That's it! Click the mic button and start learning.**

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

- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[Deployment Guide](DEPLOYMENT_GUIDE.md)** - Deploy to production
- **[Voice Setup](TTS_SETUP_GUIDE.md)** - Configure voice settings
- **[API Documentation](#)** - Build on top of KachowAI

---

## 📞 Get Help

Have questions? We're here to help:

- 💬 **[GitHub Discussions](https://github.com/SAMK-online/KachowAI/discussions)** - Ask questions, share tips
- 🐛 **[GitHub Issues](https://github.com/SAMK-online/KachowAI/issues)** - Report bugs, request features
- 📧 **Email** - Reach out directly for support

---

## 📄 License

MIT License - Free to use, modify, and build upon.

---

<div align="center">

### 🚀 Ready to Transform How You Learn?

Stop reading tutorials. Start having conversations.

**[Get Started Now](#getting-started)** • **[Watch Demo](#)** • **[View Docs](#)**

---

**Built with ⚡ for developers who learn by doing**

*Stop typing. Start talking. Master coding.*

⭐ Star this repo if you believe in voice-first learning

</div>
