# 🦁 LMU Campus LLM - MVP

A student-centered AI assistant fine-tuned on Loyola Marymount University data to give real-time answers to common LMU questions and boost campus engagement.

## 🧠 The Vision

Think ChatGPT... but for everything LMU. This Campus LLM provides:
- **Real-time answers** to LMU-specific questions
- **Event discovery** and engagement tracking
- **Points system** to reward campus participation
- **FERPA-safe** data usage (public sources only)

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- 8GB+ RAM (for local LLM)
- Ollama (for running LLaMA locally)

### Installation

1. **Clone and setup**:
```bash
git clone <your-repo-url>
cd campus-llm
pip install -r requirements.txt
```

2. **Install Ollama** (if not already installed):
```bash
# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve &

# Download LLaMA 3.2 3B model
ollama pull llama3.2:3b
```

3. **Initialize the knowledge base**:
```bash
python scripts/setup_knowledge_base.py
```

4. **Launch the interface**:
```bash
python app.py
```

## 📁 Project Structure

```
campus-llm/
├── app.py                 # Main Gradio interface
├── src/
│   ├── llm_handler.py     # LLM interaction logic
│   ├── rag_system.py      # Retrieval-Augmented Generation
│   ├── data_collector.py  # LMU data scraping/processing
│   ├── points_system.py   # Engagement tracking
│   └── utils.py           # Helper functions
├── data/
│   ├── lmu_knowledge/     # LMU-specific Q&A pairs
│   ├── events/           # Event data and tracking
│   └── student_feedback/ # Feedback collection
├── scripts/
│   ├── setup_knowledge_base.py
│   └── update_events.py
└── tests/
    └── test_basic_functionality.py
```

## 🔧 Features

### ✅ MVP Features
- [x] Conversational interface with Gradio
- [x] Local LLM with LLaMA 3.2 3B
- [x] RAG system for LMU-specific context
- [x] Event discovery and recommendations
- [x] Basic points tracking system
- [x] Student feedback collection

### 🔜 Coming Soon
- [ ] QR code check-in system
- [ ] Advanced event recommendations
- [ ] Integration with LMU calendars
- [ ] Mobile-responsive interface

## 🎯 Sample Use Cases

- "Where can I find a math tutor?"
- "What's the GPA requirement for study abroad?"
- "What events are happening this week with free food?"
- "How do I file an academic grievance?"
- "Draft an email to my professor asking for help"

## 🏆 Points & Engagement System

Students earn points by:
- Asking questions (1 point)
- Attending events (5-10 points)
- Providing feedback (3 points)
- Referring friends (5 points)

Rewards include:
- Free boba/food
- LMU merch
- Priority advising
- Exclusive events

## 📊 Data Sources

- LMU Course Catalogs
- Student Handbooks
- Academic Calendar
- ARC Tutoring Info
- Student Conduct Policies
- Orientation FAQ
- Counseling Services Info

*Note: Only publicly available data is used to ensure FERPA compliance*

## 🤝 Contributing

This is a student-led project! To contribute:
1. Fork the repository
2. Create a feature branch
3. Test your changes
4. Submit a pull request

## 📬 Contact

**Vanessa Akaraiwe**
- Major: Computer Science + Statistics
- Role: Founder, LMU Campus LLM
- Email: [your-email]
- LinkedIn: [your-linkedin]

## 📄 License

MIT License - see LICENSE file for details

---

*Built by students, for students. Let's bring LMU back to life! 🦁*