# 🦁 LMU Campus LLM

**A student-centered AI assistant fine-tuned on Loyola Marymount University data**

By Vanessa Akaraiwe | Computer Science x Statistics | Black Girl in Tech | Builder of Chaos + Clarity

## 🎯 Vision

Building a conversational AI tool that answers real student questions about campus life, policies, deadlines, and resources while encouraging event participation through a points system.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Ollama (for running LLaMA locally)
- Git

### Installation

1. **Install Ollama** (for local LLM):
   ```bash
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Pull LLaMA 3.2 3B model**:
   ```bash
   ollama pull llama3.2:3b
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

## 📁 Project Structure

```
lmu-campus-llm/
├── app.py                 # Main application
├── data/                  # LMU-specific data
│   ├── qa_pairs.json     # Q&A dataset
│   ├── events.json       # Campus events
│   └── policies.json     # University policies
├── src/
│   ├── llm_client.py     # Ollama integration
│   ├── rag_engine.py     # Retrieval-Augmented Generation
│   ├── points_system.py  # Engagement points tracking
│   └── event_scraper.py  # Event data collection
├── ui/
│   └── gradio_app.py     # Web interface
└── tests/                # Test files
```

## 🎯 MVP Features

- ✅ Conversational interface for LMU questions
- ✅ Context-aware answers from LMU sources
- ✅ Local deployment (no LMU infrastructure needed)
- ✅ Event recommendations with points system
- ✅ Student feedback collection

## 🔧 Technical Stack

- **Base Model**: LLaMA 3.2 3B (via Ollama)
- **Runtime**: Ollama (local deployment)
- **UI**: Gradio (web interface)
- **Data**: Custom LMU Q&A dataset
- **Points System**: Simple backend with JSON storage

## 📊 Data Sources

- Course Catalogs
- Student Handbooks  
- Academic Calendar
- ARC Tutoring Info
- Student Conduct Policies
- Orientation FAQ
- Counseling Services Info

## 🛣️ Roadmap

- 🟢 **Phase 1**: MVP (Current)
- 🟡 **Phase 2**: Expanded Pilot
- 🔵 **Phase 3**: Scalable Deployment

## 🤝 Contributing

This is a student-led project. All contributions welcome!

## 📞 Contact

Vanessa Akaraiwe
- Major: Computer Science + Statistics
- Role: Founder, LMU Campus LLM ✨