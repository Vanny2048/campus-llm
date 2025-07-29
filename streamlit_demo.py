#!/usr/bin/env python3
"""
LMU Campus LLM - Streamlit Demo
A modern, interactive demo for the LMU Campus LLM platform
"""

import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta
import random
import time

# Page configuration
st.set_page_config(
    page_title="LMU Campus LLM",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .spirit-points {
        background: linear-gradient(90deg, #ff7f0e, #ff6b6b);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 2rem;
        font-weight: bold;
        text-align: center;
    }
    .event-card {
        background: white;
        border: 1px solid #e0e0e0;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .prize-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Sample data
GAME_EVENTS = [
    {
        "id": "bb_001",
        "sport": "🏀 Basketball",
        "opponent": "Pepperdine",
        "date": "2024-02-15",
        "time": "19:00",
        "venue": "Gersten Pavilion",
        "type": "home",
        "spirit_points": 50,
        "tailgate": "Lions Den Tailgate (4:00 PM)"
    },
    {
        "id": "bb_002", 
        "sport": "🏀 Basketball",
        "opponent": "Gonzaga",
        "date": "2024-02-22",
        "time": "20:00",
        "venue": "McCarthy Athletic Center",
        "type": "away",
        "spirit_points": 30,
        "watch_party": "Greek Row Watch Party"
    },
    {
        "id": "fb_001",
        "sport": "🏈 Football", 
        "opponent": "San Diego",
        "date": "2024-03-02",
        "time": "14:00",
        "venue": "Sullivan Field",
        "type": "home",
        "spirit_points": 75,
        "tailgate": "Greek Row Tailgate (12:00 PM)"
    }
]

TAILGATES = [
    {
        "name": "Lions Den Tailgate",
        "host": "Alpha Phi Omega",
        "date": "2024-02-15",
        "time": "16:00-18:30",
        "location": "Gersten Pavilion Parking Lot",
        "theme": "Red Sea Night",
        "features": ["BBQ", "Live Music", "Face Painting", "Spirit Contests"],
        "spirit_points": 25,
        "rsvp_count": 45,
        "max_capacity": 200
    },
    {
        "name": "Greek Row Tailgate",
        "host": "Interfraternity Council",
        "date": "2024-03-02", 
        "time": "12:00-14:00",
        "location": "Greek Row",
        "theme": "Blue & White Bash",
        "features": ["Food Trucks", "DJ", "Cornhole Tournament", "Photo Booth"],
        "spirit_points": 30,
        "rsvp_count": 78,
        "max_capacity": 150
    }
]

WATCH_PARTIES = [
    {
        "name": "Greek Row Watch Party",
        "host": "Panhellenic Council",
        "date": "2024-02-22",
        "time": "19:30-22:00",
        "location": "Greek Row Common Area",
        "features": ["Big Screen", "Snacks", "Spirit Contests", "Prizes"],
        "spirit_points": 20,
        "rsvp_count": 32,
        "max_capacity": 100
    }
]

PREMIUM_PRIZES = [
    {
        "id": "prize_001",
        "name": "Day as LMU President",
        "description": "Shadow the president, attend meetings, take over LMU socials for a day",
        "points_required": 1000,
        "available": 1,
        "claimed": 0
    },
    {
        "id": "prize_002",
        "name": "Voice of the Lions",
        "description": "Co-host a game broadcast, announce starting lineups",
        "points_required": 750,
        "available": 2,
        "claimed": 0
    },
    {
        "id": "prize_003",
        "name": "Lead the Tailgate Parade",
        "description": "Designated 'Tailgate Marshal' leads pregame march with custom banner",
        "points_required": 500,
        "available": 3,
        "claimed": 0
    },
    {
        "id": "prize_004",
        "name": "Coach for a Day",
        "description": "Join team practice, be on sidelines, help plan plays",
        "points_required": 600,
        "available": 2,
        "claimed": 0
    },
    {
        "id": "prize_005",
        "name": "Jumbotron Shout-Out",
        "description": "Personalized Jumbotron message at halftime",
        "points_required": 300,
        "available": 5,
        "claimed": 0
    }
]

SPIRIT_CHALLENGES = [
    {
        "id": "challenge_001",
        "name": "Spirit Selfie",
        "description": "Post your best LMU spirit selfie at the game",
        "points": 50,
        "deadline": "2024-02-15 23:59"
    },
    {
        "id": "challenge_002",
        "name": "Chant Master",
        "description": "Record yourself leading the best LMU chant",
        "points": 75,
        "deadline": "2024-02-15 23:59"
    },
    {
        "id": "challenge_003",
        "name": "Outfit of the Game",
        "description": "Show off your most creative LMU game day fit",
        "points": 100,
        "deadline": "2024-02-15 23:59"
    }
]

# Initialize session state
if 'user_points' not in st.session_state:
    st.session_state.user_points = 250
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'rsvp_events' not in st.session_state:
    st.session_state.rsvp_events = []
if 'completed_challenges' not in st.session_state:
    st.session_state.completed_challenges = []

def main():
    # Header
    st.markdown('<h1 class="main-header">🦁 LMU Campus LLM</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your AI Campus Assistant & Spirit Engine</p>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🎯 Your Spirit Stats")
        st.markdown(f'<div class="spirit-points">{st.session_state.user_points} Spirit Points</div>', unsafe_allow_html=True)
        
        st.markdown("## 🏆 Leaderboard")
        leaderboard_data = [
            {"Rank": 1, "Name": "Sarah M.", "Points": 850, "Org": "Alpha Phi Omega"},
            {"Rank": 2, "Name": "Mike T.", "Points": 720, "Org": "Basketball Team"},
            {"Rank": 3, "Name": "Emma L.", "Points": 680, "Org": "Cheer Squad"},
            {"Rank": 4, "Name": "Alex K.", "Points": 590, "Org": "Greek Row"},
            {"Rank": 5, "Name": "You", "Points": st.session_state.user_points, "Org": "Student"}
        ]
        
        df = pd.DataFrame(leaderboard_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown("## 🎮 Quick Actions")
        if st.button("🎯 Complete Daily Challenge", use_container_width=True):
            points_gained = random.randint(10, 25)
            st.session_state.user_points += points_gained
            st.success(f"🎉 +{points_gained} points! Daily challenge completed!")
            st.rerun()
        
        if st.button("📱 Check In at Event", use_container_width=True):
            points_gained = random.randint(15, 35)
            st.session_state.user_points += points_gained
            st.success(f"🎉 +{points_gained} points! Event check-in successful!")
            st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🏠 Home", "🏀 Game Day", "🎉 Tailgates", "📺 Watch Parties", "🏆 Prizes", "💬 AI Chat"
    ])
    
    with tab1:
        show_home_dashboard()
    
    with tab2:
        show_game_day()
    
    with tab3:
        show_tailgates()
    
    with tab4:
        show_watch_parties()
    
    with tab5:
        show_prizes()
    
    with tab6:
        show_ai_chat()

def show_home_dashboard():
    st.markdown('<h2 class="sub-header">🏠 Welcome to LMU Campus LLM</h2>', unsafe_allow_html=True)
    
    # Quick stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Your Points", st.session_state.user_points)
    with col2:
        st.metric("Events RSVP'd", len(st.session_state.rsvp_events))
    with col3:
        st.metric("Challenges Completed", len(st.session_state.completed_challenges))
    with col4:
        st.metric("Rank", "Top 5")
    
    # Next big event
    st.markdown("## 🎯 Next Big Event")
    next_event = GAME_EVENTS[0]
    with st.container():
        st.markdown(f"""
        <div class="event-card">
            <h3>{next_event['sport']} vs {next_event['opponent']}</h3>
            <p><strong>Date:</strong> {next_event['date']} at {next_event['time']}</p>
            <p><strong>Venue:</strong> {next_event['venue']}</p>
            <p><strong>Spirit Points:</strong> {next_event['spirit_points']}</p>
            <p><strong>Tailgate:</strong> {next_event.get('tailgate', 'No tailgate')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Active challenges
    st.markdown("## 🎮 Active Spirit Challenges")
    for challenge in SPIRIT_CHALLENGES:
        if challenge['id'] not in st.session_state.completed_challenges:
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h4>{challenge['name']}</h4>
                    <p>{challenge['description']}</p>
                    <p><strong>Points:</strong> {challenge['points']}</p>
                    <p><strong>Deadline:</strong> {challenge['deadline']}</p>
                </div>
                """, unsafe_allow_html=True)
                if st.button(f"Complete {challenge['name']}", key=f"challenge_{challenge['id']}"):
                    st.session_state.user_points += challenge['points']
                    st.session_state.completed_challenges.append(challenge['id'])
                    st.success(f"🎉 +{challenge['points']} points! Challenge completed!")
                    st.rerun()

def show_game_day():
    st.markdown('<h2 class="sub-header">🏀 Game Day Central</h2>', unsafe_allow_html=True)
    
    for event in GAME_EVENTS:
        with st.container():
            st.markdown(f"""
            <div class="event-card">
                <h3>{event['sport']} vs {event['opponent']}</h3>
                <p><strong>Date:</strong> {event['date']} at {event['time']}</p>
                <p><strong>Venue:</strong> {event['venue']}</p>
                <p><strong>Type:</strong> {event['type'].title()} Game</p>
                <p><strong>Spirit Points:</strong> {event['spirit_points']}</p>
                {f"<p><strong>Tailgate:</strong> {event['tailgate']}</p>" if 'tailgate' in event else ""}
                {f"<p><strong>Watch Party:</strong> {event['watch_party']}</p>" if 'watch_party' in event else ""}
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"RSVP to Game", key=f"rsvp_game_{event['id']}"):
                    if event['id'] not in st.session_state.rsvp_events:
                        st.session_state.rsvp_events.append(event['id'])
                        st.session_state.user_points += 10
                        st.success("🎉 RSVP'd! +10 points")
                        st.rerun()
                    else:
                        st.info("Already RSVP'd!")
            
            with col2:
                if st.button(f"Check In at Game", key=f"checkin_game_{event['id']}"):
                    points_gained = random.randint(20, 40)
                    st.session_state.user_points += points_gained
                    st.success(f"🎉 Checked in! +{points_gained} points")
                    st.rerun()

def show_tailgates():
    st.markdown('<h2 class="sub-header">🎉 Tailgate Events</h2>', unsafe_allow_html=True)
    
    for tailgate in TAILGATES:
        with st.container():
            st.markdown(f"""
            <div class="event-card">
                <h3>{tailgate['name']}</h3>
                <p><strong>Host:</strong> {tailgate['host']}</p>
                <p><strong>Date:</strong> {tailgate['date']} at {tailgate['time']}</p>
                <p><strong>Location:</strong> {tailgate['location']}</p>
                <p><strong>Theme:</strong> {tailgate['theme']}</p>
                <p><strong>Features:</strong> {', '.join(tailgate['features'])}</p>
                <p><strong>Spirit Points:</strong> {tailgate['spirit_points']}</p>
                <p><strong>RSVP:</strong> {tailgate['rsvp_count']}/{tailgate['max_capacity']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"RSVP to {tailgate['name']}", key=f"rsvp_tailgate_{tailgate['name']}"):
                    st.session_state.user_points += 15
                    st.success("🎉 RSVP'd! +15 points")
                    st.rerun()
            
            with col2:
                if st.button(f"Check In at {tailgate['name']}", key=f"checkin_tailgate_{tailgate['name']}"):
                    points_gained = random.randint(25, 50)
                    st.session_state.user_points += points_gained
                    st.success(f"🎉 Checked in! +{points_gained} points")
                    st.rerun()

def show_watch_parties():
    st.markdown('<h2 class="sub-header">📺 Watch Parties</h2>', unsafe_allow_html=True)
    
    for party in WATCH_PARTIES:
        with st.container():
            st.markdown(f"""
            <div class="event-card">
                <h3>{party['name']}</h3>
                <p><strong>Host:</strong> {party['host']}</p>
                <p><strong>Date:</strong> {party['date']} at {party['time']}</p>
                <p><strong>Location:</strong> {party['location']}</p>
                <p><strong>Features:</strong> {', '.join(party['features'])}</p>
                <p><strong>Spirit Points:</strong> {party['spirit_points']}</p>
                <p><strong>RSVP:</strong> {party['rsvp_count']}/{party['max_capacity']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"RSVP to {party['name']}", key=f"rsvp_party_{party['name']}"):
                    st.session_state.user_points += 10
                    st.success("🎉 RSVP'd! +10 points")
                    st.rerun()
            
            with col2:
                if st.button(f"Check In at {party['name']}", key=f"checkin_party_{party['name']}"):
                    points_gained = random.randint(15, 30)
                    st.session_state.user_points += points_gained
                    st.success(f"🎉 Checked in! +{points_gained} points")
                    st.rerun()

def show_prizes():
    st.markdown('<h2 class="sub-header">🏆 Premium Prizes</h2>', unsafe_allow_html=True)
    
    for prize in PREMIUM_PRIZES:
        with st.container():
            st.markdown(f"""
            <div class="prize-card">
                <h3>{prize['name']}</h3>
                <p>{prize['description']}</p>
                <p><strong>Points Required:</strong> {prize['points_required']}</p>
                <p><strong>Available:</strong> {prize['available'] - prize['claimed']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.session_state.user_points >= prize['points_required']:
                if st.button(f"Redeem {prize['name']}", key=f"redeem_{prize['id']}"):
                    if prize['available'] > prize['claimed']:
                        st.session_state.user_points -= prize['points_required']
                        prize['claimed'] += 1
                        st.success(f"🎉 Prize redeemed! You now have {st.session_state.user_points} points left.")
                        st.rerun()
                    else:
                        st.error("Sorry, this prize is no longer available!")
            else:
                st.info(f"You need {prize['points_required'] - st.session_state.user_points} more points to redeem this prize.")

def show_ai_chat():
    st.markdown('<h2 class="sub-header">💬 AI Campus Assistant</h2>', unsafe_allow_html=True)
    
    # Chat interface
    st.markdown("Ask me anything about LMU campus life, events, or student resources!")
    
    # Sample questions
    st.markdown("**Try asking:**")
    sample_questions = [
        "When is add/drop deadline?",
        "Where can I find tutoring?",
        "What's happening on campus this weekend?",
        "How do I join a club?",
        "Where's the best place to study?"
    ]
    
    for question in sample_questions:
        if st.button(question, key=f"sample_{question}"):
            st.session_state.conversation_history.append({"user": question, "ai": get_ai_response(question)})
            st.rerun()
    
    # Chat history
    if st.session_state.conversation_history:
        st.markdown("## Chat History")
        for i, message in enumerate(st.session_state.conversation_history):
            with st.chat_message("user"):
                st.write(message["user"])
            with st.chat_message("assistant"):
                st.write(message["ai"])
    
    # Manual input
    user_input = st.chat_input("Ask me anything about LMU...")
    if user_input:
        response = get_ai_response(user_input)
        st.session_state.conversation_history.append({"user": user_input, "ai": response})
        st.rerun()

def get_ai_response(question):
    """Simple AI response system"""
    responses = {
        "add/drop": "Add/drop deadline is typically the first week of classes. Check your student portal for exact dates!",
        "tutoring": "LMU offers free tutoring at the Academic Resource Center in Daum Hall. You can also find subject-specific tutors in the library!",
        "weekend": "This weekend we have basketball vs Pepperdine on Saturday with a tailgate! Check the events tab for more details.",
        "club": "Visit the Student Leadership & Development office in Malone Student Center to browse all 200+ clubs and organizations!",
        "study": "The best study spots are the library 3rd floor (quiet), the Lion's Den (social), or the new study rooms in the business school!"
    }
    
    question_lower = question.lower()
    for key, response in responses.items():
        if key in question_lower:
            return response
    
    return "I'm here to help with LMU campus life! Try asking about events, resources, or student services. You can also check out the other tabs for game day info and spirit challenges!"

if __name__ == "__main__":
    main()