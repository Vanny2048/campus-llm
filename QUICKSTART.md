# 🚀 LMU Campus LLM - Quick Start Guide

Get your LMU Campus Assistant up and running in minutes!

## 📋 Prerequisites

- **Python 3.8+** (check with `python --version`)
- **8GB+ RAM** (for running LLaMA 3.2 3B)
- **5GB+ free disk space** (for model and dependencies)
- **Internet connection** (for downloading model and dependencies)

## ⚡ Quick Setup (5 minutes)

### 1. Clone and Setup
```bash
# Clone the repository (if you haven't already)
git clone <your-repo-url>
cd lmu-campus-llm

# Run the automated setup
python setup.py
```

### 2. Start Ollama
```bash
# Start Ollama in the background
ollama serve
```

### 3. Test the Assistant
```bash
# Run a quick test
python app.py

# Or start interactive mode
python app.py --interactive
```

### 4. Launch Web Interface (Optional)
```bash
# Start the web interface
python ui/gradio_app.py
```
Then open your browser to `http://localhost:7860`

## 🎯 What You Can Do

### Ask Questions
- "What are the library hours?"
- "How do I file an academic grievance?"
- "Where can I find a math tutor?"
- "What's the GPA requirement for study abroad?"

### Discover Events
- "What events have free food this week?"
- "Show me wellness events"
- "What's happening this weekend?"

### Earn Points
- Register with your student ID
- Attend events to earn points
- Claim rewards like free food and priority services
- Compete on the leaderboard

## 🔧 Manual Setup (if automated setup fails)

### 1. Install Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/download
```

### 2. Download LLaMA Model
```bash
ollama pull llama3.2:3b
```

### 3. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 4. Test Installation
```bash
python app.py
```

## 🐛 Troubleshooting

### Ollama Connection Issues
```bash
# Check if Ollama is running
ollama list

# Restart Ollama
ollama serve
```

### Model Download Issues
```bash
# Check available models
ollama list

# Re-download model
ollama pull llama3.2:3b
```

### Python Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Memory Issues
- Close other applications
- Try a smaller model: `ollama pull llama3.2:1b`

## 📱 Usage Examples

### Command Line Interface
```bash
# Start interactive mode
python app.py --interactive

# Register as a student
register vakaraiwe Vanessa Akaraiwe

# Ask questions
What are the library hours?
How do I find a math tutor?
What events have free food?

# Check your stats
stats

# View rewards
rewards
```

### Web Interface
1. Start: `python ui/gradio_app.py`
2. Open browser to `http://localhost:7860`
3. Register/login with your student ID
4. Ask questions and explore features

## 🎁 Features Overview

### 🤖 AI Assistant
- Answers LMU-specific questions
- Provides context-aware responses
- Suggests relevant events

### 📅 Event Discovery
- Browse upcoming events
- Filter by category (wellness, academic, social)
- Find events with free food

### 🏆 Points System
- Earn points for event attendance
- Claim rewards (free food, priority services)
- Compete on leaderboard
- Collect badges

### 📊 Student Dashboard
- Track your engagement
- View attendance history
- Monitor points and rewards

## 🔮 Next Steps

### For Students
1. Register with your student ID
2. Explore events and start earning points
3. Share feedback to improve the system

### For Developers
1. Add more Q&A data to `data/qa_pairs.json`
2. Customize rewards in the points system
3. Integrate with real LMU APIs
4. Deploy to LMU servers

### For Administrators
1. Review and approve data sources
2. Set up hosting infrastructure
3. Configure authentication
4. Monitor usage and feedback

## 📞 Support

- **Technical Issues**: Check the troubleshooting section
- **Feature Requests**: Open an issue on GitHub
- **Data Accuracy**: Contact LMU administration
- **General Questions**: Ask the assistant itself!

## 🦁 Go Lions!

Your LMU Campus Assistant is ready to help! Ask it anything about campus life, discover events, and start earning points. 

*Built with ❤️ by Vanessa Akaraiwe for LMU students*