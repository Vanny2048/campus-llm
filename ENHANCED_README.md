# 🦁 LMU Campus LLM - Enhanced Streamlit Application

A modern, interactive platform for Loyola Marymount University students featuring AI assistance, spirit system, and comprehensive campus information.

## ✨ Features

### 🆔 LMU Student Verification
- **9-digit LMU ID validation** - Students must enter their valid LMU Student ID to access the platform
- **Secure verification** - ID format validation with masked display for privacy
- **Session management** - Verified status persists throughout the session

### 🎨 Modern Design
- **Beautiful UI/UX** - Modern gradient designs with hover effects and animations
- **Custom fonts** - Inter and Poppins fonts for professional appearance
- **Responsive layout** - Optimized for different screen sizes
- **Color scheme** - LMU blue and white theme with orange accents

### 💬 Enhanced AI Chatbot
- **Comprehensive knowledge base** - Deep LMU information including:
  - Academic resources and deadlines
  - Campus life and dining options
  - Athletics and spirit information
  - Student services and organizations
  - Location and transportation details
- **Smart responses** - Context-aware answers to student queries
- **Sample questions** - Quick access to common inquiries
- **Chat history** - Persistent conversation tracking

### 🏆 Spirit Points System
- **Gamified experience** - Earn points through various activities
- **Leaderboard** - Compete with other students
- **Quick actions** - Daily challenges and event check-ins
- **Premium prizes** - Redeem points for exclusive experiences

### 📅 Event Management
- **Game Day Central** - Basketball, soccer, and other sports events
- **Tailgate Events** - Pre-game festivities with RSVP functionality
- **Watch Parties** - Away game viewing events
- **Spirit Challenges** - Interactive challenges for points

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone or download the application files**
   ```bash
   # If you have the files locally
   cd /path/to/lmu-campus-llm
   ```

2. **Install dependencies**
   ```bash
   pip install -r enhanced_requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run enhanced_lmu_app.py
   ```

4. **Access the application**
   - Open your browser and go to `http://localhost:8501`
   - Enter your 9-digit LMU Student ID to get started

## 📋 LMU Knowledge Base

The application includes comprehensive information about:

### 🎓 Academics
- **Colleges & Schools**: All 7 LMU colleges and schools
- **Academic Calendar**: Add/drop deadlines, exam periods, graduation dates
- **Resources**: Tutoring centers, library, writing center, academic advising

### 🏠 Campus Life
- **Dining Options**: Lair Marketplace, Lion's Den, Starbucks, and more
- **Housing**: FYE, SOE, upper division, and Greek housing
- **Transportation**: Shuttle service, parking, bike share program

### 🏃 Athletics
- **Teams**: Basketball, soccer, baseball, softball, volleyball, tennis, golf, swimming
- **Venues**: Gersten Pavilion, Sullivan Field, Page Stadium, Smith Field
- **Spirit**: Mascot (Iggy the Lion), colors (Blue & White), WCC conference

### 👥 Student Organizations
- **Greek Life**: Alpha Phi Omega, Delta Gamma, Kappa Alpha Theta, and more
- **Clubs**: Student Government, Campus Ministry, cultural organizations

### 🏥 Campus Services
- **Health Services**: Student Health Services, counseling, psychological services
- **Career Development**: Resume reviews, interview prep, job fairs
- **Support**: Financial aid, registrar, IT services

## 🎮 How to Use

### 1. **Student Verification**
   - Enter your 9-digit LMU Student ID
   - Click "Verify LMU ID" to access all features
   - Your ID is securely validated and masked for privacy

### 2. **Explore Features**
   - **Home**: Dashboard with stats and upcoming events
   - **Game Day**: Sports events with RSVP and check-in
   - **Tailgates**: Pre-game events and festivities
   - **Watch Parties**: Away game viewing events
   - **Prizes**: Redeem spirit points for exclusive experiences
   - **AI Chat**: Ask questions about LMU campus life

### 3. **Earn Spirit Points**
   - Complete daily challenges (+10-25 points)
   - Check in at events (+15-50 points)
   - RSVP to games and tailgates (+10-15 points)
   - Complete spirit challenges (+50-100 points)

### 4. **Chat with AI Assistant**
   - Ask about academics, campus life, athletics
   - Get information about student services
   - Learn about events and organizations
   - Use sample questions for quick access

## 🛠️ Technical Details

### Architecture
- **Frontend**: Streamlit with custom CSS
- **Backend**: Python with session state management
- **Data**: In-memory data structures (can be extended to database)
- **Styling**: Custom CSS with Google Fonts integration

### Key Components
- **LMU ID Validation**: Regex-based validation for 9-digit format
- **Enhanced AI Responses**: Pattern matching with comprehensive knowledge base
- **Session Management**: Streamlit session state for user data persistence
- **Responsive Design**: CSS Grid and Flexbox for layout

### Customization
The application is highly customizable:
- **Colors**: Modify CSS variables for different themes
- **Content**: Update knowledge base and event data
- **Features**: Add new tabs and functionality
- **Styling**: Customize fonts, layouts, and animations

## 🔧 Development

### File Structure
```
enhanced_lmu_app.py          # Main application file
enhanced_requirements.txt     # Python dependencies
ENHANCED_README.md           # This documentation
```

### Adding New Features
1. **New Knowledge Base Entries**: Add to `LMU_KNOWLEDGE_BASE` dictionary
2. **New Events**: Add to `GAME_EVENTS`, `TAILGATES`, or `WATCH_PARTIES` lists
3. **New Challenges**: Add to `SPIRIT_CHALLENGES` list
4. **New Prizes**: Add to `PREMIUM_PRIZES` list

### Extending AI Responses
Modify the `get_enhanced_ai_response()` function to add new response patterns:
```python
def get_enhanced_ai_response(question: str) -> str:
    question_lower = question.lower()
    
    # Add new patterns here
    if "your_keyword" in question_lower:
        return "Your custom response"
    
    # Default response
    return "Default response"
```

## 🎯 Future Enhancements

### Potential Additions
- **Database Integration**: SQLite or PostgreSQL for persistent data
- **User Authentication**: Secure login system
- **Real-time Updates**: WebSocket integration for live data
- **Mobile App**: React Native or Flutter mobile application
- **QR Code Integration**: Event check-ins via QR codes
- **Push Notifications**: Event reminders and updates
- **Social Features**: Student profiles and social networking
- **Analytics Dashboard**: Usage statistics and insights

### Advanced AI Features
- **Natural Language Processing**: More sophisticated query understanding
- **Machine Learning**: Personalized recommendations
- **Voice Integration**: Voice-to-text and text-to-speech
- **Multi-language Support**: International student support

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**
3. **Make your changes**
4. **Test thoroughly**
5. **Submit a pull request**

## 📞 Support

For questions or issues:
- Check the AI Chat feature in the application
- Review the knowledge base for common questions
- Contact the development team

## 📄 License

This project is developed for Loyola Marymount University students and staff.

---

**🦁 Go Lions! 🦁**

*Built with ❤️ for the LMU community*