# 🦁 LMU Campus LLM - Interactive Demo

## 🚀 Quick Start

### Option 1: Simple Demo (Recommended)
```bash
# Install demo dependencies
pip install -r demo_requirements.txt

# Run the demo
python run_demo.py
```

### Option 2: Direct Streamlit
```bash
# Install streamlit
pip install streamlit pandas numpy

# Run directly
streamlit run streamlit_demo.py
```

## 🎯 What This Demo Shows

This interactive demo showcases the **LMU Campus LLM** platform with all the features you've been planning:

### 🏠 Home Dashboard
- **Spirit Points System**: Live point tracking and leaderboard
- **Quick Actions**: Daily challenges and event check-ins
- **Next Big Event**: Highlighted upcoming games and tailgates
- **Active Challenges**: Spirit selfies, chants, outfit contests

### 🏀 Game Day Central
- **Live Game Events**: Basketball, football with spirit points
- **RSVP System**: Easy event registration
- **Check-in Rewards**: Points for showing up
- **Tailgate Integration**: Pre-game festivities

### 🎉 Tailgates & Watch Parties
- **Hosted Events**: RSO-sponsored tailgates
- **Theme Nights**: Red Sea Night, Blue & White Bash
- **Features**: BBQ, live music, contests, food trucks
- **Capacity Management**: RSVP tracking

### 🏆 Premium Prizes
- **"Day as LMU President"**: Shadow the president
- **"Voice of the Lions"**: Co-host game broadcasts
- **"Lead the Tailgate Parade"**: Be the marshal
- **"Coach for a Day"**: Join team practices
- **"Jumbotron Shout-Out"**: Personal halftime message

### 💬 AI Campus Assistant
- **Smart Q&A**: Campus life questions
- **Resource Finder**: Tutoring, clubs, study spots
- **Event Updates**: What's happening this weekend
- **Interactive Chat**: Natural conversation flow

## 🎮 Demo Features

### Real-time Interaction
- ✅ Click buttons to earn points
- ✅ RSVP to events
- ✅ Complete challenges
- ✅ Redeem prizes
- ✅ Chat with AI assistant

### Visual Design
- ✅ Modern, mobile-friendly interface
- ✅ LMU branding and colors
- ✅ Responsive layout
- ✅ Professional styling

### Data Persistence
- ✅ Session state management
- ✅ Point tracking
- ✅ Event history
- ✅ Challenge completion

## 📱 How to Use the Demo

1. **Start the app**: Run `python run_demo.py`
2. **Open browser**: Go to `http://localhost:8501`
3. **Explore tabs**: Click through Home, Game Day, Tailgates, etc.
4. **Interact**: Click buttons to see points change
5. **Test features**: Try RSVPing, completing challenges, chatting

## 🎯 Perfect for:

- **RSO Presentations**: Show orgs how they can partner
- **Student Affairs Meetings**: Demonstrate engagement potential
- **LinkedIn Posts**: Share live demo link
- **Beta Testing**: Get real user feedback
- **Investor Pitches**: Professional presentation

## 🔧 Customization

### Add Your Own Events
Edit the data arrays in `streamlit_demo.py`:
- `GAME_EVENTS`: Add real LMU games
- `TAILGATES`: Add RSO tailgates
- `WATCH_PARTIES`: Add away game parties
- `PREMIUM_PRIZES`: Add your creative prizes

### Update Branding
Modify the CSS in the `<style>` section:
- Colors: Change `#1f77b4` and `#ff7f0e`
- Fonts: Update font families
- Layout: Adjust spacing and sizing

### Add Real AI
Replace the `get_ai_response()` function with:
- Your actual LLM integration
- Real campus data
- Dynamic responses

## 🚀 Deployment Options

### Local Development
```bash
python run_demo.py
```

### Streamlit Cloud (Free)
1. Push to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### Heroku/Railway
1. Add `Procfile`: `web: streamlit run streamlit_demo.py --server.port=$PORT`
2. Deploy with requirements

## 📊 Demo Metrics

Track these during demos:
- **Engagement Time**: How long people stay
- **Feature Usage**: Which tabs get most clicks
- **Feedback**: What people ask about
- **Conversion**: Who wants to partner/join

## 🎉 Next Steps After Demo

1. **Collect Feedback**: What features excite people most?
2. **Partner Outreach**: Use demo to pitch RSOs
3. **Technical Development**: Build real backend
4. **User Testing**: Get beta testers from demo users

## 🆘 Troubleshooting

### "Module not found"
```bash
pip install -r demo_requirements.txt
```

### "Port already in use"
```bash
# Kill existing process
pkill -f streamlit
# Or use different port
streamlit run streamlit_demo.py --server.port 8502
```

### "App not loading"
- Check browser console for errors
- Try refreshing the page
- Restart the streamlit server

---

**Ready to make LMU legendary?** 🦁💥

Run the demo, share it with your network, and let's build the most hype campus platform ever!