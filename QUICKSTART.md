# 🚀 LMU Campus LLM - Quick Start Guide

Get your LMU Campus AI Assistant running in minutes!

## 🎯 One-Command Setup

For the fastest setup, run our automated installer:

```bash
python start_campus_llm.py
```

This script will:
- ✅ Check your Python version
- ✅ Install Python dependencies
- ✅ Install and configure Ollama
- ✅ Download the LLaMA 3.2 model
- ✅ Set up the knowledge base
- ✅ Run tests
- ✅ Launch the application

## 📋 Manual Setup (if needed)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Ollama

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**macOS/Windows:**
- Visit [ollama.ai](https://ollama.ai)
- Download the installer for your system
- Run the installer

### 3. Start Ollama & Download Model

```bash
# Start Ollama service
ollama serve &

# Download LLaMA 3.2 model (this may take a while)
ollama pull llama3.2:3b
```

### 4. Initialize Knowledge Base

```bash
python scripts/setup_knowledge_base.py
```

### 5. Launch the Application

```bash
python app.py
```

## 🌐 Using the Application

1. **Open your browser** to `http://localhost:7860`
2. **Enter your student ID** (optional) to track points
3. **Ask questions** about LMU!

### Example Questions to Try:
- "Where can I find a math tutor?"
- "What's the GPA requirement for study abroad?"
- "What events are happening this week?"
- "How do I file an academic grievance?"
- "Where is the counseling center?"

## 🏆 Points & Engagement System

Earn points by:
- **Asking questions**: 1 point
- **Attending events**: 5-10 points
- **Giving feedback**: 3 points

### Point Levels:
- 🦁 **Young Lion**: 0-19 points
- 🥉 **Bronze Lion**: 20-49 points
- 🥈 **Silver Lion**: 50-99 points
- 🥇 **Gold Lion**: 100-199 points
- 👑 **Legendary Lion**: 200+ points

## 🎉 Managing Events

### View Current Events
```bash
python scripts/update_events.py --list
```

### Add New Event
```bash
python scripts/update_events.py --add
```

### Generate Sample Events
```bash
python scripts/update_events.py --sample
```

## 🔧 Troubleshooting

### "Ollama not found" Error
```bash
# Check if Ollama is installed
ollama --version

# If not, install it:
curl -fsSL https://ollama.ai/install.sh | sh
```

### "Model not available" Error
```bash
# Download the model
ollama pull llama3.2:3b

# Check available models
ollama list
```

### "Service not running" Error
```bash
# Start Ollama service
ollama serve

# Check if it's running (in another terminal)
curl http://localhost:11434/api/tags
```

### Python Dependencies Issues
```bash
# Create virtual environment (recommended)
python -m venv campus_llm_env
source campus_llm_env/bin/activate  # Linux/macOS
# campus_llm_env\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## 🧪 Testing

### Quick Test
```bash
python tests/test_basic_functionality.py --quick
```

### Full Test Suite
```bash
python tests/test_basic_functionality.py --full
```

## 📁 Project Structure

```
campus-llm/
├── app.py                 # Main Gradio application
├── start_campus_llm.py    # One-command setup
├── requirements.txt       # Python dependencies
├── src/                   # Core modules
│   ├── llm_handler.py     # LLM interface
│   ├── rag_system.py      # Knowledge retrieval
│   ├── points_system.py   # Engagement tracking
│   └── data_collector.py  # Data gathering
├── data/                  # Knowledge and user data
├── scripts/               # Utility scripts
└── tests/                 # Test files
```

## 💡 Tips for Success

1. **Start with sample data**: Use `--sample` flag to populate events
2. **Customize knowledge**: Add your own LMU information to `data/lmu_knowledge/`
3. **Monitor usage**: Check `data/logs/` for user interactions
4. **Engage students**: Promote the points system and rewards
5. **Keep events updated**: Regular updates keep students engaged

## 🤝 Getting Help

### Common Issues:
- **Slow responses**: Normal for first run (model loading)
- **Memory usage**: LLaMA 3.2 3B needs ~4GB RAM
- **Port conflicts**: Change port in `config.json` if 7860 is busy

### Support Resources:
- Check the logs in `campus_llm.log`
- Review the test results
- Verify your Python version (3.8+ required)

## 🎓 Next Steps

1. **Deploy to cloud**: Consider AWS, GCP, or Azure for broader access
2. **Integrate with LMU systems**: Connect to PROWL, LionsConnect
3. **Add more data sources**: Scrape additional LMU websites
4. **Implement QR codes**: For event check-ins
5. **Build mobile app**: React Native or Flutter frontend

---

**Built with ❤️ by Vanessa Akaraiwe for the LMU community**

🦁 *Let's bring LMU back to life!* 🦁