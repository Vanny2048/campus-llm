#!/usr/bin/env python3
"""
LMU Campus LLM - Ultimate Interactive Platform
A comprehensive Streamlit application with interactive calendar, live engagement, 
leaderboards, prize showcase, and AI assistance for Loyola Marymount University

Author: Enhanced by AI Assistant
Features: Calendar, QR Check-ins, Leaderboards, Prizes, Content Gallery, User Profiles
"""

import streamlit as st
import pandas as pd
import numpy as np
import json
import qrcode
import io
import base64
from datetime import datetime, timedelta, date
from typing import Dict, List, Optional
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import hashlib
import random
import time
import requests
from pathlib import Path

# Advanced Streamlit components
try:
    from streamlit_calendar import calendar
    CALENDAR_AVAILABLE = True
except ImportError:
    CALENDAR_AVAILABLE = False

try:
    from streamlit_option_menu import option_menu
    OPTION_MENU_AVAILABLE = True
except ImportError:
    OPTION_MENU_AVAILABLE = False
    def option_menu(*args, **kwargs):
        # Fallback implementation using selectbox
        options = kwargs.get('options', args[1] if len(args) > 1 else [])
        default_index = kwargs.get('default_index', 0)
        if options:
            selected = st.selectbox("Navigation", options, index=default_index)
            return selected
        return None

try:
    from streamlit_aggrid import AgGrid, GridOptionsBuilder
    AGGRID_AVAILABLE = True
except ImportError:
    AGGRID_AVAILABLE = False

try:
    from streamlit_lottie import st_lottie
    LOTTIE_AVAILABLE = True
except ImportError:
    LOTTIE_AVAILABLE = False

# Show warning if some packages are missing
missing_packages = []
if not CALENDAR_AVAILABLE:
    missing_packages.append("streamlit-calendar")
if not OPTION_MENU_AVAILABLE:
    missing_packages.append("streamlit-option-menu")
if not AGGRID_AVAILABLE:
    missing_packages.append("streamlit-aggrid")
if not LOTTIE_AVAILABLE:
    missing_packages.append("streamlit-lottie")

if missing_packages:
    st.warning(f"Some advanced features require additional packages. Install with: pip install {' '.join(missing_packages)}")
    st.info("The app will continue to work with basic functionality.")

# Page configuration
st.set_page_config(
    page_title="LMU Campus Spirit Hub",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for minimal black design
st.markdown("""
<style>
    /* Minimal black design - remove all decorative elements */
    .main {
        background: #000000 !important;
        color: #ffffff !important;
    }
    
    .stApp {
        background: #000000 !important;
    }
    
    .main .block-container {
        background: #000000 !important;
    }
    
    /* Make all text white */
    * {
        color: #ffffff !important;
    }
    
    /* Make inputs and buttons visible */
    .stTextInput > div > div > input {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stButton > button {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stSelectbox > div > div > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stCheckbox > div > div > div {
        background: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 3px !important;
    }
    
    .stRadio > div > div > div > div {
        background: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 50% !important;
    }
    
    .stTextArea > div > div > textarea {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stNumberInput > div > div > input {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stDateInput > div > div > input {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stTimeInput > div > div > input {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stFileUploader > div > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stSlider > div > div > div > div {
        background: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stProgress > div > div > div > div {
        background: #ffffff !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stMetric > div > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stAlert > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stSuccess > div, .stError > div, .stWarning > div, .stInfo > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stDataFrame > div > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .streamlit-expanderHeader {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    .stTabs > div > div > div > div > div {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
        border-radius: 5px !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #000000 !important;
        border-right: 1px solid #ffffff !important;
    }
    
    /* Remove all decorative elements */
    .glass-container, .feature-card, .points-display, .badge, .leaderboard-item, .chat-container, .message-bubble, .typing-indicator {
        background: transparent !important;
        backdrop-filter: none !important;
        border: none !important;
        box-shadow: none !important;
        animation: none !important;
    }
    
    /* Remove all gradients and animations */
    * {
        background-image: none !important;
        animation: none !important;
        transition: none !important;
    }
    
    /* Make links visible */
    a {
        color: #ffffff !important;
        text-decoration: underline !important;
    }
    
    /* Ensure all form elements are functional */
    button, input, select, textarea {
        background: #ffffff !important;
        color: #000000 !important;
        border: 1px solid #ffffff !important;
    }
    
    /* Override any remaining styling */
    .stMarkdown, .stText, .stWrite, .stContainer, .stColumn {
        color: #ffffff !important;
        background: transparent !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'user_points' not in st.session_state:
    st.session_state.user_points = 0
if 'user_badges' not in st.session_state:
    st.session_state.user_badges = []
if 'attended_events' not in st.session_state:
    st.session_state.attended_events = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'show_rsvp_modal' not in st.session_state:
    st.session_state.show_rsvp_modal = False
if 'selected_event' not in st.session_state:
    st.session_state.selected_event = None
if 'show_checkin_modal' not in st.session_state:
    st.session_state.show_checkin_modal = False

# Load mock data and configurations
@st.cache_data
def load_mock_data():
    """Load mock data for events, prizes, leaderboard, etc."""
    
    events = [
        {
            "id": "game_001",
            "title": "Lions vs Pepperdine Basketball",
            "date": "2024-02-15",
            "time": "19:00",
            "type": "Game Day",
            "location": "Gersten Pavilion",
            "points": 75,
            "description": "Red Sea Night! Wear red and white to support the Lions!",
            "rsvp_count": 324,
            "max_capacity": 4000,
            "qr_checkin": True
        },
        {
            "id": "tailgate_001",
            "title": "Greek Row Tailgate",
            "date": "2024-02-15",
            "time": "16:00",
            "type": "Tailgate",
            "location": "Greek Row",
            "points": 25,
            "description": "BBQ, music, and spirit competitions before the big game!",
            "rsvp_count": 89,
            "max_capacity": 200,
            "qr_checkin": True
        },
        {
            "id": "watch_001",
            "title": "Lions Den Watch Party",
            "date": "2024-02-22",
            "time": "20:00",
            "type": "Watch Party",
            "location": "Student Union",
            "points": 20,
            "description": "Watch the away game together with snacks and prizes!",
            "rsvp_count": 56,
            "max_capacity": 150,
            "qr_checkin": False
        },
        {
            "id": "rso_001",
            "title": "Service Learning Fair",
            "date": "2024-02-20",
            "time": "12:00",
            "type": "RSO Event",
            "location": "Alumni Mall",
            "points": 15,
            "description": "Discover volunteer opportunities and service organizations",
            "rsvp_count": 112,
            "max_capacity": 300,
            "qr_checkin": False
        }
    ]
    
    prizes = [
        {
            "id": "prize_001",
            "name": "Day as LMU President",
            "description": "Shadow President Snyder, attend meetings, take over LMU socials for a day",
            "points_required": 1000,
            "category": "Ultimate Experience",
            "available": 1,
            "claimed": 0,
            "image": "🏛️"
        },
        {
            "id": "prize_002",
            "name": "Voice of the Lions",
            "description": "Co-host a game broadcast, announce starting lineups on ESPN+",
            "points_required": 750,
            "category": "Media Experience",
            "available": 2,
            "claimed": 0,
            "image": "🎙️"
        },
        {
            "id": "prize_003",
            "name": "VIP Game Day Experience",
            "description": "Courtside seats, halftime meet & greet with players, exclusive merchandise",
            "points_required": 500,
            "category": "Game Day",
            "available": 5,
            "claimed": 1,
            "image": "🏀"
        },
        {
            "id": "prize_004",
            "name": "Tailgate Marshal",
            "description": "Lead the pregame parade with custom banner, megaphone, and spirit squad",
            "points_required": 300,
            "category": "Leadership",
            "available": 3,
            "claimed": 0,
            "image": "📯"
        },
        {
            "id": "prize_005",
            "name": "Jumbotron Feature",
            "description": "Personalized Jumbotron message during halftime + photo package",
            "points_required": 200,
            "category": "Recognition",
            "available": 10,
            "claimed": 3,
            "image": "📺"
        }
    ]
    
    leaderboard = [
        {"rank": 1, "name": "Alex Chen", "points": 1250, "badges": ["🏆", "🔥", "⭐"], "streak": 12, "type": "Individual"},
        {"rank": 2, "name": "Jordan Smith", "points": 1180, "badges": ["🥈", "🎯", "⚡"], "streak": 8, "type": "Individual"},
        {"rank": 3, "name": "Taylor Johnson", "points": 1050, "badges": ["🥉", "💪", "🎪"], "streak": 15, "type": "Individual"},
        {"rank": 4, "name": "Riley Martinez", "points": 980, "badges": ["🌟", "🎨"], "streak": 6, "type": "Individual"},
        {"rank": 5, "name": "Casey Wilson", "points": 875, "badges": ["🎵", "🏃"], "streak": 4, "type": "Individual"},
        {"rank": 1, "name": "Alpha Phi Omega", "points": 3450, "badges": ["👑", "🏛️", "🤝"], "streak": 20, "type": "RSO"},
        {"rank": 2, "name": "Delta Sigma Pi", "points": 2890, "badges": ["🥈", "💼", "📈"], "streak": 14, "type": "RSO"},
        {"rank": 3, "name": "Kappa Alpha Theta", "points": 2650, "badges": ["🥉", "💝", "🌸"], "streak": 11, "type": "RSO"}
    ]
    
    badges_info = {
        "🏆": "Champion - Top 3 in leaderboard",
        "🔥": "Streak Master - 10+ event streak",
        "⭐": "Rising Star - 5+ events this month",
        "🎯": "Event Specialist - Attended all types",
        "⚡": "Quick Check-in - Fastest QR scans",
        "💪": "Spirit Champion - Max spirit participation",
        "🎪": "Social Butterfly - Most RSVP'd events",
        "🌟": "Newcomer Star - Outstanding new member",
        "🎨": "Creative Contributor - Best photo submissions",
        "🎵": "Chant Champion - Best spirit chants",
        "🏃": "Marathon Attendee - 20+ events",
        "👑": "RSO Legend - Highest group points",
        "🏛️": "Community Leader - Service champion",
        "🤝": "Team Player - Best collaboration",
        "💼": "Professional Spirit - Business events",
        "📈": "Growth Leader - Biggest improvement",
        "💝": "Service Heart - Most volunteer hours",
        "🌸": "Spirit Squad - Best team spirit"
    }
    
    return events, prizes, leaderboard, badges_info

def generate_qr_code(event_id: str, user_id: str = None):
    """Generate QR code for event check-in"""
    check_in_data = {
        "event_id": event_id,
        "user_id": user_id or "guest",
        "timestamp": datetime.now().isoformat(),
        "type": "checkin"
    }
    
    qr_data = json.dumps(check_in_data)
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    
    return buf

def create_calendar_events(events):
    """Convert events to calendar format"""
    calendar_events = []
    for event in events:
        calendar_events.append({
            "title": event["title"],
            "start": f"{event['date']}T{event['time']}",
            "backgroundColor": {
                "Game Day": "#ff6b35",
                "Tailgate": "#2a5298", 
                "Watch Party": "#f7931e",
                "RSO Event": "#667eea"
            }.get(event["type"], "#cccccc"),
            "borderColor": {
                "Game Day": "#ff6b35",
                "Tailgate": "#2a5298",
                "Watch Party": "#f7931e", 
                "RSO Event": "#667eea"
            }.get(event["type"], "#cccccc"),
            "extendedProps": {
                "id": event["id"],
                "type": event["type"],
                "location": event["location"],
                "points": event["points"],
                "description": event["description"]
            }
        })
    return calendar_events

def simulate_ai_response(question: str) -> str:
    """Authentic Gen Z LMU student chatbot responses"""
    question_lower = question.lower()
    
    # Specific sample responses from user's examples
    if "campus llm" in question_lower or "what even is" in question_lower:
        return "it's like if chatgpt went to lmu, joined like 3 clubs, and started giving fire recs. i'm here to make campus less confusing and more fun. u feel me?"
    
    if "happening" in question_lower and ("week" in question_lower or "campus" in question_lower):
        return "hold up… *checks imaginary calendar* okay so:\n– thurs: free tacos at first gen lounge\n– fri: tailgate before the game (show up, get clout)\n– sat: vibes-only open mic at founders, bring ur feelings\ni gotchu."
    
    if "eat" in question_lower and ("what" in question_lower or "should" in question_lower):
        return "u hungry-hungry or just bored?\n– real hunger = hit up iggy's, get that grilled chicken bowl no cap\n– broke & bored = snag snacks from the C-store & manifest a meal\n– tryna flirt = get lunch at la monica & hope a cutie sits nearby 💅"
    
    if "email" in question_lower and ("prof" in question_lower or "assignment" in question_lower):
        return "say less.\n\n```\nhi [prof name],\ni hope you're doing well. i wanted to be transparent—i missed the deadline for [assignment] due to [life being lifey / mental health / rough week]. is there any way i could still submit or make it up?\ni totally understand if not. thank you for your time.\nbest,\n[you]\n```"
    
    if "failing" in question_lower or ("feel like" in question_lower and "everything" in question_lower):
        return "same sometimes. but you're not. fr, breathe. talk to your advisors, email your profs, maybe cry a little, then bounce back. you're still in the game."
    
    # Location-based responses
    if any(word in question_lower for word in ["where", "find", "location"]):
        location_responses = [
            "the rock is literally the main character of campus - best vibes for studying outside when it's not too hot",
            "burns backcourt is where you go to actually get work done. that grind hits different on the 2nd floor ngl",
            "the lair has fire food but it gets chaotic during lunch rush. pro tip: go at like 2pm for no lines",
            "hannon library quiet floors (3-6) are sacred spaces. don't be that person talking on floor 4 💀",
            "founders is cute for coffee dates or crying over your midterm grade. both valid tbh",
            "the grove is where everyone hangs but good luck finding a seat during peak hours"
        ]
        return random.choice(location_responses)
    
    # Academic help
    if any(word in question_lower for word in ["study", "help", "tutor", "academic"]):
        academic_responses = [
            "arc tutoring on burns 2nd floor is clutch for math/science. just walk in, no appointment needed fr",
            "writing center saves lives during essay szn. book online but they fill up fast so don't sleep on it",
            "office hours are literally free tutoring but half y'all don't go... that's on you bestie",
            "study groups hit different when you find the right people. try making friends in class first",
            "prowl has all your academic info but the interface is giving 2015... we make it work tho"
        ]
        return random.choice(academic_responses)
    
    # Events and activities
    if any(word in question_lower for word in ["event", "activity", "fun", "party", "social"]):
        event_responses = [
            "first fridays are mandatory for the vibes. good music, free food, and everyone shows up",
            "basketball games at gersten are unmatched energy. even if you don't watch sports, the atmosphere is chef's kiss",
            "greek life is big here but not like overwhelming. join if you want, don't if you don't. both are valid",
            "involvement fair is chaos but in a good way. so many clubs to join and free merch everywhere",
            "spring concert lineup usually slaps. last year was fire and this year better not disappoint"
        ]
        return random.choice(event_responses)
    
    # Food and dining
    if any(word in question_lower for word in ["food", "eat", "hungry", "dining", "meal"]):
        food_responses = [
            "iggy's grilled chicken bowl is the move when you want something healthy-ish and filling",
            "la monica lowkey has the best coffee on campus but don't tell everyone i said that",
            "c-store runs at 2am hit different. overpriced but convenient when you're cramming",
            "the lair pizza is mid but sometimes mid is exactly what you need at 1pm on a tuesday",
            "roski dining gets busy but their stir fry station goes hard when you're tired of everything else"
        ]
        return random.choice(food_responses)
    
    # How-to questions
    if any(word in question_lower for word in ["how", "register", "apply", "sign up"]):
        how_responses = [
            "prowl is your best friend and worst enemy. everything you need is there but finding it is the real challenge",
            "email your advisor before doing anything major. they've seen it all and can save you from mistakes",
            "check the academic calendar religiously. deadlines sneak up on you faster than you think",
            "most applications are online but some offices still do paper because we're apparently stuck in 2010",
            "when in doubt, ask someone who's been here longer. upperclassmen usually know the shortcuts"
        ]
        return random.choice(how_responses)
    
    # Stress and mental health
    if any(word in question_lower for word in ["stress", "anxiety", "overwhelmed", "help", "counseling"]):
        wellness_responses = [
            "cps (counseling services) is free and actually helpful. they get it fr and won't judge you",
            "everyone's stressed here but we all pretend we're fine. it's giving toxic productivity culture",
            "take breaks bestie. burnout is real and the grind ain't worth your mental health",
            "talk to someone - friends, family, counselors, whoever. keeping it all inside hits different (in a bad way)",
            "campus wellness events are lowkey helpful. free therapy dogs during finals week? yes please"
        ]
        return random.choice(wellness_responses)
    
    # Transportation and logistics  
    if any(word in question_lower for word in ["metro", "parking", "transport", "bus", "car"]):
        transport_responses = [
            "metro expo line goes straight to santa monica but it takes forever. bring headphones and patience",
            "parking permits are expensive but street parking around campus is a nightmare during the day",
            "campus shuttle is free but runs on its own timeline. don't rely on it if you're already late",
            "uber/lyft surge pricing near campus is criminal but sometimes you gotta do what you gotta do",
            "walking to westwood is doable but it's uphill both ways somehow??? make it make sense"
        ]
        return random.choice(transport_responses)
    
    # Greek life
    if any(word in question_lower for word in ["greek", "sorority", "fraternity", "rush"]):
        greek_responses = [
            "rush is a whole experience. if you're thinking about it, just try it out - worst case you meet people",
            "greek life here isn't like the movies but it's still a big part of social life for some people",
            "philanthropy events are actually fun and you don't have to be greek to participate",
            "mixer season gets chaotic but the vibes are usually good if you're into that scene",
            "don't let anyone pressure you either way. do what feels right for you and your wallet"
        ]
        return random.choice(greek_responses)
    
    # Default responses with personality
    default_responses = [
        "that's a vibe question but i don't have the tea on that one. try asking someone in student services maybe?",
        "ngl i'm still learning about that. check the lmu website or slide into someone's dms who might know",
        "hmm idk about that specific thing but the people at the info desk in the student union usually have answers",
        "that's outside my expertise bestie. maybe try google or ask on the lmu reddit? those people know everything",
        "lowkey don't know that one off the top of my head. prowl might have info or ask around campus",
        "not sure about that one chief. you could probably find someone who knows tho - lmu students are helpful like that"
    ]
    
    return random.choice(default_responses)

# Main App Function
def main():
    # Simple header
    st.title("LMU Campus Spirit Hub")
    st.write("Your platform for campus engagement, spirit points, and Lion pride!")
    
    # Load data
    events, prizes, leaderboard, badges_info = load_mock_data()
    
    # Sidebar for user authentication and navigation
    with st.sidebar:
        st.header("User Login")
        
        if st.session_state.user_id is None:
            user_input = st.text_input("Enter your Student ID or Email:", placeholder="e.g., jdoe@lion.lmu.edu")
            if st.button("Join the Spirit Squad", type="primary", use_container_width=True):
                if user_input:
                    st.session_state.user_id = user_input
                    st.session_state.user_points = random.randint(150, 800)
                    st.session_state.user_badges = random.sample(list(badges_info.keys()), random.randint(2, 5))
                    st.success(f"Welcome, {user_input.split('@')[0].title()}!")
                    st.rerun()
        else:
            st.success(f"Welcome back, {st.session_state.user_id.split('@')[0].title()}!")
            st.write(f"Points: {st.session_state.user_points}")
            st.write(f"Badges: {', '.join(st.session_state.user_badges)}")
            
            # Logout button
            if st.button("Logout", use_container_width=True):
                st.session_state.user_id = None
                st.session_state.user_points = 0
                st.session_state.user_badges = []
                st.session_state.conversation_history = []
                st.success("See you later!")
                time.sleep(1)
                st.rerun()
        
        # Quick stats
        st.header("Quick Stats")
        st.write("Most Active: Basketball Fans")
        st.write("Top Prize: MacBook Pro")
        st.write("Next Event: First Friday")
    
    # Simple navigation
    selected = option_menu(
        menu_title=None,
        options=["Home", "Events Calendar", "Leaderboard", "Prize Shop", "Content Gallery", "My Profile", "AI Assistant", "Feedback"],
        icons=["house", "calendar-event", "trophy", "gift", "images", "person-circle", "robot", "chat-dots"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal"
    )
    
    # Page content based on selection
    if selected == "Home":
        show_home_page(events, leaderboard)
    elif selected == "Events Calendar":
        show_calendar_page(events)
    elif selected == "Leaderboard":
        show_leaderboard_page(leaderboard, badges_info)
    elif selected == "Prize Shop":
        show_prize_shop(prizes)
    elif selected == "Content Gallery":
        show_content_gallery()
    elif selected == "My Profile":
        show_user_profile(events, badges_info)
    elif selected == "AI Assistant":
        show_ai_assistant()
    elif selected == "Feedback":
        show_feedback_page()

def show_rsvp_modal(event):
    """Display RSVP confirmation modal"""
    st.markdown("""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(5px);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            position: relative;
        ">
            <div style="
                width: 100%;
                height: 150px;
                background: var(--lmu-crimson);
                border-radius: 15px;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4rem;
            ">🏀</div>
            
            <h2 style="color: var(--lmu-crimson); font-size: 24px; text-align: center; margin-bottom: 1rem;">
                {event['title']}
            </h2>
            
            <p style="color: #666; font-size: 16px; text-align: center; margin-bottom: 0.5rem;">
                📅 {event['date']} at {event['time']}
            </p>
            <p style="color: #666; font-size: 16px; text-align: center; margin-bottom: 1.5rem;">
                📍 {event['location']}
            </p>
            
            <div style="
                background: var(--lmu-gold);
                color: var(--lmu-crimson-dark);
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 1.5rem;
            ">
                🏆 Earn {event['points']} Spirit Points for attending!
            </div>
            
            <p style="color: #333; font-size: 18px; text-align: center; margin-bottom: 2rem; font-weight: bold;">
                Are you sure you want to RSVP?
            </p>
            
            <div style="display: flex; gap: 1rem;">
                <button style="
                    flex: 1;
                    background: var(--lmu-gold);
                    color: var(--lmu-crimson-dark);
                    border: none;
                    padding: 1rem;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                " onclick="window.parent.postMessage({type: 'rsvp_confirm'}, '*')">
                    Yes, RSVP Me!
                </button>
                <button style="
                    flex: 1;
                    background: transparent;
                    color: var(--lmu-crimson);
                    border: 2px solid var(--lmu-crimson);
                    padding: 1rem;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                " onclick="window.parent.postMessage({type: 'rsvp_cancel'}, '*')">
                    Cancel
                </button>
            </div>
        </div>
    </div>
    """.format(event=event), unsafe_allow_html=True)

def show_checkin_modal(event):
    """Display check-in confirmation modal with live spirit meter"""
    st.markdown("""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: linear-gradient(135deg, rgba(139, 0, 0, 0.9) 0%, rgba(165, 42, 42, 0.9) 100%);
        backdrop-filter: blur(10px);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            position: relative;
            text-align: center;
        ">
            <div style="
                width: 80px;
                height: 80px;
                background: #4CAF50;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 3rem;
                margin: 0 auto 1.5rem;
                animation: checkmarkPulse 1s ease-in-out;
            ">✅</div>
            
            <h2 style="color: var(--lmu-crimson); font-size: 36px; margin-bottom: 1rem; font-weight: bold;">
                You're Checked In!
            </h2>
            
            <div style="
                background: var(--lmu-gold);
                color: var(--lmu-crimson-dark);
                padding: 1rem;
                border-radius: 10px;
                font-weight: bold;
                font-size: 20px;
                margin-bottom: 2rem;
                animation: confetti 0.5s ease-out;
            ">
                +350 Spirit Points awarded 🎉
            </div>
            
            <h3 style="color: #333; font-size: 18px; margin-bottom: 1rem; font-weight: bold;">
                Current Spirit Meter:
            </h3>
            
            <div style="
                width: 100%;
                height: 30px;
                background: #f0f0f0;
                border-radius: 15px;
                overflow: hidden;
                margin-bottom: 2rem;
                position: relative;
            ">
                <div style="
                    width: 75%;
                    height: 100%;
                    background: var(--lmu-gold);
                    border-radius: 15px;
                    animation: fillBar 2s ease-out;
                "></div>
                <div style="
                    position: absolute;
                    top: 50%;
                    left: 75%;
                    transform: translateY(-50%);
                    color: var(--lmu-crimson-dark);
                    font-weight: bold;
                    font-size: 14px;
                ">75% Loudest</div>
            </div>
            
            <div style="display: flex; flex-direction: column; gap: 1rem;">
                <button style="
                    background: var(--lmu-gold);
                    color: var(--lmu-crimson-dark);
                    border: none;
                    padding: 1rem;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                " onclick="window.parent.postMessage({type: 'upload_selfie'}, '*')">
                    📸 Upload Your Game-Day Selfie
                </button>
                
                <button style="
                    background: transparent;
                    color: var(--lmu-crimson);
                    border: 2px solid var(--lmu-crimson);
                    padding: 1rem;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                " onclick="window.parent.postMessage({type: 'share_social'}, '*')">
                    📤 Share to Social
                </button>
                
                <button style="
                    background: transparent;
                    color: #666;
                    border: none;
                    padding: 0.5rem;
                    font-style: italic;
                    font-size: 14px;
                    cursor: pointer;
                    text-decoration: underline;
                " onclick="window.parent.postMessage({type: 'back_to_game'}, '*')">
                    ← Back to Game Day Zone
                </button>
            </div>
        </div>
    </div>
    
    <style>
    @keyframes checkmarkPulse {
        0% { transform: scale(0); }
        50% { transform: scale(1.2); }
        100% { transform: scale(1); }
    }
    
    @keyframes confetti {
        0% { transform: scale(0) rotate(0deg); }
        50% { transform: scale(1.2) rotate(180deg); }
        100% { transform: scale(1) rotate(360deg); }
    }
    
    @keyframes fillBar {
        0% { width: 0%; }
        100% { width: 75%; }
    }
    </style>
    """, unsafe_allow_html=True)
    """Display RSVP confirmation modal"""
    st.markdown("""
    <div style="
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(5px);
        z-index: 1000;
        display: flex;
        align-items: center;
        justify-content: center;
    ">
        <div style="
            background: white;
            border-radius: 20px;
            padding: 2rem;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            position: relative;
        ">
            <div style="
                width: 100%;
                height: 150px;
                background: var(--lmu-crimson);
                border-radius: 15px;
                margin-bottom: 1.5rem;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 4rem;
            ">🏀</div>
            
            <h2 style="color: var(--lmu-crimson); font-size: 24px; text-align: center; margin-bottom: 1rem;">
                {event['title']}
            </h2>
            
            <p style="color: #666; font-size: 16px; text-align: center; margin-bottom: 0.5rem;">
                📅 {event['date']} at {event['time']}
            </p>
            <p style="color: #666; font-size: 16px; text-align: center; margin-bottom: 1.5rem;">
                📍 {event['location']}
            </p>
            
            <div style="
                background: var(--lmu-gold);
                color: var(--lmu-crimson-dark);
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 1.5rem;
            ">
                🏆 Earn {event['points']} Spirit Points for attending!
            </div>
            
            <p style="color: #333; font-size: 18px; text-align: center; margin-bottom: 2rem; font-weight: bold;">
                Are you sure you want to RSVP?
            </p>
            
            <div style="display: flex; gap: 1rem;">
                <button style="
                    flex: 1;
                    background: var(--lmu-gold);
                    color: var(--lmu-crimson-dark);
                    border: none;
                    padding: 1rem;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                " onclick="window.parent.postMessage({type: 'rsvp_confirm'}, '*')">
                    Yes, RSVP Me!
                </button>
                <button style="
                    flex: 1;
                    background: transparent;
                    color: var(--lmu-crimson);
                    border: 2px solid var(--lmu-crimson);
                    padding: 1rem;
                    border-radius: 10px;
                    font-weight: bold;
                    font-size: 16px;
                    cursor: pointer;
                " onclick="window.parent.postMessage({type: 'rsvp_cancel'}, '*')">
                    Cancel
                </button>
            </div>
        </div>
    </div>
    """.format(event=event), unsafe_allow_html=True)

def show_home_page(events, leaderboard):
    """Display the home page"""
    
    # Get user's first name for greeting
    user_name = "User" if st.session_state.user_id is None else st.session_state.user_id.split('@')[0].title()
    
    # Greeting Section
    st.header(f"Hi, {user_name}!")
    
    # Featured Event
    featured_event = events[0]  # Basketball game
    st.subheader("Featured Event")
    st.write(f"**{featured_event['title']}**")
    st.write(f"Date: {featured_event['date']} at {featured_event['time']}")
    st.write(f"Location: {featured_event['location']}")
    
    if st.button("RSVP + Add to Calendar"):
        st.success("RSVP successful!")
    
    # Leaderboard preview
    st.subheader("Top Leaders")
    individual_leaders = [person for person in leaderboard if person['type'] == 'Individual'][:5]
    for person in individual_leaders:
        st.write(f"{person['rank']}. {person['name']} - {person['points']} points")
    
    # Spirit Challenge
    st.subheader("Spirit Challenge")
    st.write("Post a game-day selfie for 200 points!")
    if st.button("Upload Now"):
        st.success("Upload successful!")
    
    # Quick stats
    st.subheader("Quick Stats")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Upcoming Events", len([e for e in events if datetime.strptime(e['date'], '%Y-%m-%d').date() >= date.today()]))
    
    with col2:
        st.metric("Active Users", 847)
    
    with col3:
        total_rsvps = sum(event.get('rsvp_count', 0) for event in events)
        st.metric("Total RSVPs", total_rsvps)
    
    with col4:
        st.metric("Points Awarded", "15.2K")
    if st.session_state.show_rsvp_modal and st.session_state.selected_event:
        show_rsvp_modal(st.session_state.selected_event)
    
    # Check if RSVP button was clicked (using JavaScript message)
    st.markdown("""
    <script>
    window.addEventListener('message', function(event) {
        if (event.data.type === 'rsvp_click') {
            // This will be handled by Streamlit's rerun mechanism
            window.location.reload();
        }
    });
    </script>
    """, unsafe_allow_html=True)

def show_calendar_page(events):
    """Display interactive calendar with events"""
    st.header("Event Calendar")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        event_type_filter = st.selectbox("Filter by Type", ["All", "Game Day", "Tailgate", "Watch Party", "RSO Event"])
    with col2:
        date_filter = st.date_input("From Date", value=date.today())
    
    # Apply filters
    filtered_events = events
    if event_type_filter != "All":
        filtered_events = [e for e in filtered_events if e['type'] == event_type_filter]
    
    filtered_events = [e for e in filtered_events if datetime.strptime(e['date'], '%Y-%m-%d').date() >= date_filter]
    
    # Display filtered events
    for event in filtered_events:
        st.subheader(event['title'])
        st.write(f"Location: {event['location']}")
        st.write(f"Date: {event['date']} at {event['time']}")
        st.write(f"Type: {event['type']} • Points: {event['points']}")
        st.write(f"Description: {event['description']}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"RSVP", key=f"rsvp_{event['id']}"):
                st.success(f"RSVP confirmed for {event['title']}!")
        with col2:
            if event.get('qr_checkin') and st.button(f"Check-In", key=f"checkin_{event['id']}"):
                st.session_state.show_checkin_modal = True
                st.session_state.selected_event = event
                st.rerun()
        with col3:
            if st.button(f"Add to Calendar", key=f"cal_{event['id']}"):
                cal_data = f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//LMU Campus Spirit Hub//EN
BEGIN:VEVENT
UID:{event['id']}@lmu.edu
DTSTAMP:{datetime.now().strftime('%Y%m%dT%H%M%SZ')}
DTSTART:{event['date'].replace('-', '')}{event['time'].replace(':', '')}00
SUMMARY:{event['title']}
DESCRIPTION:{event['description']}
LOCATION:{event['location']}
END:VEVENT
END:VCALENDAR"""
                
                st.download_button(
                    label="Download .ics file",
                    data=cal_data,
                    file_name=f"{event['title'].replace(' ', '_')}.ics",
                    mime="text/calendar"
                )
        st.divider()
    
    # Check-in Modal
    if st.session_state.show_checkin_modal and st.session_state.selected_event:
        show_checkin_modal(st.session_state.selected_event)

def show_simple_calendar(events):
    """Fallback simple calendar display"""
    import calendar as cal
    
    today = datetime.now()
    
    # Create a simple monthly view
    st.markdown(f"### 📅 {today.strftime('%B %Y')}")
    
    # Group events by date
    events_by_date = {}
    for event in events:
        event_date = event['date']
        if event_date not in events_by_date:
            events_by_date[event_date] = []
        events_by_date[event_date].append(event)
    
    # Show calendar grid (simplified)
    cal_html = f"<div style='display: grid; grid-template-columns: repeat(7, 1fr); gap: 1px; background: #ddd; margin: 1rem 0;'>"
    
    # Days of week header
    for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
        cal_html += f"<div style='background: #ff6b35; color: white; padding: 0.5rem; text-align: center; font-weight: bold;'>{day}</div>"
    
    # Calendar days
    month_cal = cal.monthcalendar(today.year, today.month)
    for week in month_cal:
        for day in week:
            if day == 0:
                cal_html += "<div style='background: #f8f9fa; padding: 0.5rem;'></div>"
            else:
                day_str = f"{today.year}-{today.month:02d}-{day:02d}"
                has_events = day_str in events_by_date
                bg_color = "#ffe6e6" if has_events else "white"
                cal_html += f"<div style='background: {bg_color}; padding: 0.5rem; text-align: center; min-height: 60px;'>"
                cal_html += f"<div style='font-weight: bold;'>{day}</div>"
                if has_events:
                    cal_html += f"<div style='font-size: 0.7rem; color: #ff6b35;'>📅 {len(events_by_date[day_str])} events</div>"
                cal_html += "</div>"
    
    cal_html += "</div>"
    st.markdown(cal_html, unsafe_allow_html=True)

def show_leaderboard_page(leaderboard, badges_info):
    """Display leaderboard"""
    st.header("Leaderboard")
    
    # Leaderboard tabs
    tab1, tab2, tab3 = st.tabs(["Individuals", "Organizations", "Dorms"])
    
    with tab1:
        show_individual_leaderboard(leaderboard, badges_info)
    
    with tab2:
        show_org_leaderboard(leaderboard, badges_info)
    
    with tab3:
        show_dorm_leaderboard(leaderboard, badges_info)

def show_individual_leaderboard(leaderboard, badges_info):
    """Display individual student leaderboard"""
    # Filter dropdown
    time_filter = st.selectbox("Time Period", ["Weekly", "Monthly", "All-Time"], index=0)
    
    # Get individual leaders
    individual_leaders = [person for person in leaderboard if person['type'] == 'Individual']
    
    # Display rankings
    for person in individual_leaders:
        st.write(f"{person['rank']}. {person['name']} - {person['points']} points ({person['streak']} day streak)")
        st.write(f"Badges: {', '.join(person['badges'])}")
        st.divider()

def show_org_leaderboard(leaderboard, badges_info):
    """Display organization leaderboard"""
    # Get RSO leaders
    rso_leaders = [person for person in leaderboard if person['type'] == 'RSO']
    
    if not rso_leaders:
        st.info("No organization data available yet.")
        return
    
    for person in rso_leaders:
        st.write(f"{person['rank']}. {person['name']} - {person['points']} points ({person['streak']} day streak)")
        st.write(f"Badges: {', '.join(person['badges'])}")
        st.divider()

def show_dorm_leaderboard(leaderboard, badges_info):
    """Display dorm leaderboard"""
    st.info("Dorm leaderboard coming soon!")
    st.write("Compete with your dorm mates for the most spirited residence hall!")
    st.write("Launching Spring 2024")

def show_prize_shop(prizes):
    """Display prize shop"""
    st.header("Prize Shop")
    st.write("Earn points and redeem them for exclusive LMU experiences and rewards!")
    
    # User points display
    if st.session_state.user_id:
        st.write(f"You have {st.session_state.user_points} points to spend!")
    
    # Prize categories
    categories = list(set(prize['category'] for prize in prizes))
    selected_category = st.selectbox("Browse by Category", ["All Categories"] + categories)
    
    # Filter prizes
    if selected_category != "All Categories":
        filtered_prizes = [p for p in prizes if p['category'] == selected_category]
    else:
        filtered_prizes = prizes
    
    # Sort options
    sort_option = st.selectbox("Sort by", ["Points (Low to High)", "Points (High to Low)", "Availability", "Category"])
    
    if sort_option == "Points (Low to High)":
        filtered_prizes = sorted(filtered_prizes, key=lambda x: x['points_required'])
    elif sort_option == "Points (High to Low)":
        filtered_prizes = sorted(filtered_prizes, key=lambda x: x['points_required'], reverse=True)
    elif sort_option == "Availability":
        filtered_prizes = sorted(filtered_prizes, key=lambda x: x['available'] - x['claimed'], reverse=True)
    elif sort_option == "Category":
        filtered_prizes = sorted(filtered_prizes, key=lambda x: x['category'])
    
    # Display prizes
    for prize in filtered_prizes:
        available_count = prize['available'] - prize['claimed']
        can_afford = st.session_state.user_points >= prize['points_required'] if st.session_state.user_id else False
        
        st.subheader(prize['name'])
        st.write(f"Category: {prize['category']}")
        st.write(f"Description: {prize['description']}")
        st.write(f"Points Required: {prize['points_required']}")
        st.write(f"Available: {available_count}")
        
        if st.button(f"Redeem {prize['points_required']} points", key=f"redeem_{prize['id']}", disabled=not can_afford or available_count == 0):
            st.success(f"Successfully redeemed {prize['name']}!")
        st.divider()
            
            if not st.session_state.user_id:
                st.info("Login to redeem prizes!")
            elif button_disabled:
                if available_count == 0:
                    st.error("Sold Out")
                else:
                    points_needed = prize['points_required'] - st.session_state.user_points
                    st.warning(f"Need {points_needed} more points")
            else:
                if st.button(f"🎁 Redeem Now", key=f"redeem_{prize['id']}", type="primary", use_container_width=True):
                    # Redeem prize
                    st.session_state.user_points -= prize['points_required']
                    prize['claimed'] += 1  # This would be saved to database in real app
                    
                    st.success(f"🎉 Congratulations! You've redeemed '{prize['name']}'!")
                    st.balloons()
                    
                    # Show redemption details
                    st.info(f"📧 Check your LMU email for redemption instructions. Prize ID: {prize['id']}")
                    
                    time.sleep(2)
                    st.rerun()
    
    # Prize request section
    st.markdown("---")
    st.markdown("### 💡 Suggest a New Prize")
    
    with st.expander("🗣️ Have an idea for a new prize?"):
        new_prize_name = st.text_input("Prize Name", placeholder="e.g., Lunch with President Snyder")
        new_prize_description = st.text_area("Prize Description", placeholder="Describe what makes this prize special...")
        suggested_points = st.number_input("Suggested Points Required", min_value=50, max_value=2000, value=300, step=50)
        
        if st.button("💌 Submit Suggestion", type="primary"):
            # In a real app, this would save to database
            st.success("🙌 Thank you for your suggestion! Our team will review it and consider adding it to the prize shop.")

def show_content_gallery():
    """Display content gallery"""
    st.header("Content Gallery")
    st.write("Relive the best moments from LMU events!")
    
    # Content type tabs
    content_tabs = st.tabs(["Event Photos", "Video Highlights", "Social Posts", "Submit Content"])
    
    with content_tabs[0]:  # Event Photos
        st.subheader("Latest Event Photos")
        
        # Sample photo data
        photo_albums = [
            {
                "title": "Basketball vs Pepperdine - Red Sea Night",
                "date": "2024-02-10",
                "photos": 45,
                "highlights": ["packed stadium", "amazing atmosphere", "overtime win"]
            },
            {
                "title": "Greek Row Tailgate Extravaganza", 
                "date": "2024-02-08",
                "photos": 32,
                "highlights": ["BBQ feast", "spirit competitions", "group photos"]
            },
            {
                "title": "Service Learning Fair",
                "date": "2024-02-05", 
                "photos": 28,
                "highlights": ["community involvement", "RSO booths", "networking"]
            }
        ]
        
        for album in photo_albums:
            st.markdown(f"""
            <div class="feature-card">
                <div style="display: flex; justify-content: space-between; align-items: start;">
                    <div style="flex-grow: 1;">
                        <h4 style="color: #ff6b35; margin: 0;">{album['title']}</h4>
                        <p style="color: #666; margin: 0.5rem 0;">📅 {album['date']} • 📸 {album['photos']} photos</p>
                        <div style="margin: 1rem 0;">
                            {' '.join([f'<span class="badge">{highlight}</span>' for highlight in album['highlights']])}
                        </div>
                    </div>
                    <div style="font-size: 3rem;">📸</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Simulate photo thumbnails
            cols = st.columns(4)
            for i, col in enumerate(cols):
                with col:
                    # Create placeholder image
                    placeholder_img = Image.new('RGB', (200, 150), color=(random.randint(100, 255), random.randint(100, 255), random.randint(100, 255)))
                    st.image(placeholder_img, caption=f"Photo {i+1}", use_column_width=True)
    
    with content_tabs[1]:  # Video Highlights
        st.markdown("### 🎥 Video Highlights")
        
        video_content = [
            {
                "title": "Game Winning Shot - Lions vs Pepperdine",
                "duration": "0:45",
                "views": "1.2K",
                "description": "The crowd went wild! Amazing buzzer beater by #23 Johnson!"
            },
            {
                "title": "Best Tailgate Moments Compilation",
                "duration": "2:30", 
                "views": "856",
                "description": "All the fun from our epic pre-game celebration"
            },
            {
                "title": "Student Interviews: Why LMU Spirit Matters",
                "duration": "3:15",
                "views": "643",
                "description": "Students share what Lion pride means to them"
            }
        ]
        
        for video in video_content:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                # Video thumbnail placeholder
                thumbnail = Image.new('RGB', (300, 200), color=(30, 60, 114))
                st.image(thumbnail, caption=f"▶️ {video['duration']}")
            
            with col2:
                st.markdown(f"""
                <div style="padding: 1rem;">
                    <h4 style="color: #2a5298; margin: 0 0 0.5rem 0;">{video['title']}</h4>
                    <p style="color: #666; margin: 0 0 1rem 0;">👀 {video['views']} views • ⏱️ {video['duration']}</p>
                    <p style="margin: 0;">{video['description']}</p>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown("---")
    
    with content_tabs[2]:  # Social Posts
        st.markdown("### 📱 Social Media Highlights")
        
        social_posts = [
            {
                "platform": "Instagram",
                "username": "@lmu_campus_spirit",
                "content": "Red Sea Night was UNREAL! 🔴⚪ The energy in Gersten was off the charts! Who else was there? #LionUp #RedSeaNight",
                "likes": 245,
                "comments": 32,
                "timestamp": "2 hours ago"
            },
            {
                "platform": "TikTok", 
                "username": "@lmu_lions",
                "content": "POV: You're at the best tailgate on campus 🔥 Greek Row knows how to party! #LMU #Tailgate #CollegeLife",
                "likes": 892,
                "comments": 67,
                "timestamp": "1 day ago"
            },
            {
                "platform": "Twitter/X",
                "username": "@LMU_Spirit",
                "content": "Shoutout to everyone who came to the Service Learning Fair! 🙌 Our community impact is incredible. Next up: Basketball game Friday! 🏀",
                "likes": 156,
                "comments": 18,
                "timestamp": "3 days ago"
            }
        ]
        
        for post in social_posts:
            platform_color = {"Instagram": "#E4405F", "TikTok": "#000000", "Twitter/X": "#1DA1F2"}[post['platform']]
            platform_icon = {"Instagram": "📷", "TikTok": "🎵", "Twitter/X": "🐦"}[post['platform']]
            
            st.markdown(f"""
            <div class="feature-card" style="border-left: 5px solid {platform_color};">
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <span style="font-size: 1.5rem; margin-right: 0.5rem;">{platform_icon}</span>
                    <strong style="color: {platform_color};">{post['platform']}</strong>
                    <span style="margin-left: 0.5rem; color: #666;">@{post['username'].replace('@', '')}</span>
                    <span style="margin-left: auto; color: #999; font-size: 0.9rem;">{post['timestamp']}</span>
                </div>
                <p style="margin: 1rem 0; line-height: 1.5;">{post['content']}</p>
                <div style="display: flex; gap: 2rem; color: #666; font-size: 0.9rem;">
                    <span>❤️ {post['likes']} likes</span>
                    <span>💬 {post['comments']} comments</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with content_tabs[3]:  # Submit Content
        st.markdown("### 🎨 Submit Your Content")
        st.markdown("Share your LMU moments and help build our community gallery!")
        
        content_type = st.selectbox("📋 Content Type", ["Photo", "Video", "Social Media Post", "Story/Caption"])
        
        if content_type == "Photo":
            uploaded_file = st.file_uploader("📸 Upload Photo", type=['png', 'jpg', 'jpeg'])
            photo_caption = st.text_area("Photo Caption", placeholder="Tell us about this moment...")
            event_tag = st.selectbox("🏷️ Tag Event (if applicable)", ["None", "Basketball Game", "Tailgate", "Watch Party", "RSO Event", "Other"])
            
        elif content_type == "Video":
            st.info("📹 For video submissions, please share your content via email to spirit@lmu.edu or tag us on social media!")
            video_description = st.text_area("Video Description", placeholder="Describe your video content...")
            
        elif content_type == "Social Media Post":
            platform = st.selectbox("📱 Platform", ["Instagram", "TikTok", "Twitter/X", "Facebook"])
            post_link = st.text_input("🔗 Post Link", placeholder="Paste the link to your post...")
            
        else:  # Story/Caption
            story_content = st.text_area("📝 Your LMU Story", placeholder="Share your experience, memorable moment, or why you love LMU...", height=150)
        
        # Submission form
        submitter_name = st.text_input("Your Name", placeholder="How should we credit you?")
        submitter_email = st.text_input("Email (optional)", placeholder="For follow-up questions")
        
        if st.button("🚀 Submit Content", type="primary"):
            st.success("🎉 Thank you for your submission! Our team will review it and potentially feature it in our gallery.")
            st.balloons()

def show_user_profile(events, badges_info):
    """Display user profile"""
    if not st.session_state.user_id:
        st.warning("Please log in to view your profile!")
        return
    
    st.header(f"{st.session_state.user_id.split('@')[0].title()}'s Profile")
    
    # Profile stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Spirit Points", st.session_state.user_points)
    
    with col2:
        events_attended = len(st.session_state.attended_events)
        st.metric("Events Attended", events_attended)
    
    with col3:
        st.metric("Badges Earned", len(st.session_state.user_badges))
    
    with col4:
        current_streak = random.randint(3, 15)  # Simulated
        st.metric("Day Streak", current_streak)
    
    # Main profile content
    tab1, tab2, tab3, tab4 = st.tabs(["🏆 Achievements", "📊 Progress", "📅 Event History", "⚙️ Settings"])
    
    with tab1:  # Achievements
        st.markdown("### 🏅 Your Badges")
        
        if st.session_state.user_badges:
            # Display badges in a grid
            cols = st.columns(4)
            for i, badge in enumerate(st.session_state.user_badges):
                with cols[i % 4]:
                    description = badges_info.get(badge, "Special achievement")
                    st.markdown(f"""
                    <div class="feature-card" style="text-align: center; padding: 1rem;">
                        <div style="font-size: 3rem; margin-bottom: 0.5rem;">{badge}</div>
                        <p style="margin: 0; font-size: 0.9rem;">{description}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("🎯 Attend events and participate to earn your first badges!")
        
        # Next badges to earn
        st.markdown("### 🎯 Next Achievements")
        available_badges = [badge for badge in badges_info.keys() if badge not in st.session_state.user_badges]
        
        for i in range(min(3, len(available_badges))):
            badge = available_badges[i]
            st.markdown(f"""
            <div class="feature-card" style="opacity: 0.7; border: 2px dashed #ccc;">
                <div style="display: flex; align-items: center; gap: 1rem;">
                    <div style="font-size: 2rem;">{badge}</div>
                    <div>
                        <p style="margin: 0; font-weight: 600;">Coming Soon</p>
                        <p style="margin: 0; font-size: 0.9rem; color: #666;">{badges_info[badge]}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with tab2:  # Progress
        st.markdown("### 📊 Your Progress")
        
        # Level system
        levels = [
            {"name": "Young Lion", "min_points": 0, "max_points": 199, "icon": "🦁"},
            {"name": "Bronze Lion", "min_points": 200, "max_points": 499, "icon": "🥉"},
            {"name": "Silver Lion", "min_points": 500, "max_points": 999, "icon": "🥈"},
            {"name": "Gold Lion", "min_points": 1000, "max_points": 1999, "icon": "🥇"},
            {"name": "Legendary Lion", "min_points": 2000, "max_points": float('inf'), "icon": "👑"}
        ]
        
        current_level = None
        next_level = None
        
        for i, level in enumerate(levels):
            if level["min_points"] <= st.session_state.user_points <= level["max_points"]:
                current_level = level
                if i < len(levels) - 1:
                    next_level = levels[i + 1]
                break
        
        if current_level:
            if next_level:
                progress_percentage = ((st.session_state.user_points - current_level["min_points"]) / 
                                     (next_level["min_points"] - current_level["min_points"])) * 100
                points_needed = next_level["min_points"] - st.session_state.user_points
            else:
                progress_percentage = 100
                points_needed = 0
            
            st.markdown(f"""
            <div class="feature-card">
                <h3 style="color: #ff6b35; margin: 0 0 1rem 0;">Current Level: {current_level['icon']} {current_level['name']}</h3>
                <div class="progress-container">
                    <div class="progress-bar" style="width: {progress_percentage}%;"></div>
                </div>
                <p style="margin: 1rem 0 0 0; text-align: center;">
                    {f"{points_needed} points to {next_level['icon']} {next_level['name']}" if next_level else "Max level achieved! 🎉"}
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Points breakdown chart
        st.markdown("### 📈 Points Sources")
        
        # Simulate points breakdown
        points_sources = {
            "Game Attendance": random.randint(200, 400),
            "Tailgate Participation": random.randint(100, 200),
            "RSO Events": random.randint(50, 150),
            "Social Challenges": random.randint(30, 100),
            "QR Check-ins": random.randint(40, 120),
            "Other": random.randint(20, 80)
        }
        
        fig = px.pie(
            values=list(points_sources.values()),
            names=list(points_sources.keys()),
            title="Where Your Points Come From",
            color_discrete_sequence=['#ff6b35', '#2a5298', '#f7931e', '#667eea', '#764ba2', '#ffecd2']
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:  # Event History
        st.markdown("### 📅 Your Event History")
        
        # Simulate event history
        sample_history = [
            {"event": "Lions vs Pepperdine Basketball", "date": "2024-02-10", "points": 75, "type": "Game Day"},
            {"event": "Greek Row Tailgate", "date": "2024-02-08", "points": 25, "type": "Tailgate"},
            {"event": "Service Learning Fair", "date": "2024-02-05", "points": 15, "type": "RSO Event"},
            {"event": "Lions Den Watch Party", "date": "2024-01-28", "points": 20, "type": "Watch Party"},
        ]
        
        for event in sample_history:
            st.markdown(f"""
            <div class="event-card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4 style="margin: 0; color: #2a5298;">{event['event']}</h4>
                        <p style="margin: 0.25rem 0; color: #666;">📅 {event['date']} • 🎯 {event['type']}</p>
                    </div>
                    <div class="badge">🏆 +{event['points']} pts</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if len(sample_history) == 0:
            st.info("🎯 No events attended yet. Check out the calendar to find upcoming events!")
    
    with tab4:  # Settings
        st.markdown("### ⚙️ Profile Settings")
        
        # Notification preferences
        st.markdown("#### 📢 Notification Preferences")
        notify_events = st.checkbox("📅 Notify me about new events", value=True)
        notify_prizes = st.checkbox("🎁 Notify me about new prizes", value=True)
        notify_leaderboard = st.checkbox("🏆 Notify me about leaderboard changes", value=False)
        
        # Privacy settings
        st.markdown("#### 🔒 Privacy Settings")
        public_profile = st.checkbox("👥 Make my profile visible to other students", value=True)
        show_real_name = st.checkbox("📛 Display my real name on leaderboard", value=False)
        
        # Data export
        st.markdown("#### 📊 Data Management")
        if st.button("📥 Download My Data"):
            # Create sample data export
            user_data = {
                "user_id": st.session_state.user_id,
                "points": st.session_state.user_points,
                "badges": st.session_state.user_badges,
                "events_attended": sample_history,
                "export_date": datetime.now().isoformat()
            }
            
            st.download_button(
                label="💾 Download JSON",
                data=json.dumps(user_data, indent=2),
                file_name=f"lmu_spirit_data_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        
        if st.button("🗑️ Delete My Account", type="secondary"):
            st.warning("⚠️ This action cannot be undone. All your points, badges, and history will be lost.")
            if st.button("❌ Confirm Delete", type="secondary"):
                # In real app, this would delete from database
                st.session_state.user_id = None
                st.session_state.user_points = 0
                st.session_state.user_badges = []
                st.session_state.attended_events = []
                st.success("Account deleted successfully.")
                st.rerun()

def show_ai_assistant():
    """AI assistant"""
    st.header("LMU AI Assistant")
    st.write("Ask me anything about LMU! I know about campus life, academics, events, and more.")
    
    # Quick questions
    st.subheader("Quick Questions")
    suggestions = [
        "What's happening on campus this week?",
        "Where can I study?",
        "What events are coming up?",
        "How do I join Greek life?"
    ]
    
    for suggestion in suggestions:
        if st.button(suggestion, key=f"pill_{suggestion}"):
            st.session_state.current_question = suggestion
            st.rerun()
    
    # Display conversation history
    if st.session_state.conversation_history:
        st.subheader("Recent Conversation")
        for exchange in st.session_state.conversation_history[-5:]:  # Show last 5 messages
            st.write(f"**You:** {exchange['question']}")
            st.write(f"**Assistant:** {exchange['answer']}")
            st.divider()
    else:
        st.write("Hey! I'm your campus AI assistant. Ask me anything about campus life, events, food, studying, or just how to survive the bluff!")
    
    # Input section
    st.markdown('<div class="glass-container" style="margin-top: 1rem;">', unsafe_allow_html=True)
    
    # Use form for better input handling
    with st.form(key="chat_form", clear_on_submit=True):
        question = st.text_input(
            "",
            placeholder="type your question here... (e.g., where's the best place to cry on campus?)",
            key="ai_question_input",
            label_visibility="collapsed"
        )
        
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            ask_button = st.form_submit_button("💬 Send", type="primary", use_container_width=True)
        with col2:
            clear_button = st.form_submit_button("🗑️ Clear", use_container_width=True)
        with col3:
            random_button = st.form_submit_button("🎲 Random", use_container_width=True, help="Ask a random question")
    
    # Handle random question
    if random_button:
        st.session_state.current_question = random.choice(suggestions)
        st.rerun()
    
    # Handle clear chat
    if clear_button:
        st.session_state.conversation_history = []
        st.session_state.show_typing = False
        if hasattr(st.session_state, 'current_question'):
            delattr(st.session_state, 'current_question')
        st.success("Chat cleared! Ready for a fresh convo 🌟")
        st.rerun()
    
    # Handle sending message
    if ask_button and question:
        try:
            # Generate response immediately
            response = simulate_ai_response(question)
            
            # Add to conversation history
            st.session_state.conversation_history.append({
                "question": question,
                "answer": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Award points for asking questions
            if st.session_state.user_id:
                points_earned = random.randint(1, 3)
                st.session_state.user_points += points_earned
                st.success(f"🏆 +{points_earned} points for staying engaged!")
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")
            st.rerun()
    
    # Debug info (remove this in production)
    with st.expander("🔧 Debug Info"):
        st.write("Question:", question)
        st.write("Ask button clicked:", ask_button)
        st.write("Conversation history length:", len(st.session_state.conversation_history))
        st.write("Session state keys:", list(st.session_state.keys()))
        
        # Test button
        if st.button("🧪 Test Chatbot"):
            test_response = simulate_ai_response("Hello, this is a test!")
            st.session_state.conversation_history.append({
                "question": "Hello, this is a test!",
                "answer": test_response,
                "timestamp": datetime.now().isoformat()
            })
            st.success("Test message added!")
            st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # AI Features showcase
    st.markdown("---")
    st.markdown("### 🧠 What I Can Help With")
    
    feature_cols = st.columns(2)
    
    with feature_cols[0]:
        st.markdown("""
        **📚 Academic Support:**
        - Finding tutoring and study resources
        - Registration and class information
        - GPA requirements and policies
        - Study abroad programs
        - Academic deadlines and schedules
        
        **🏛️ Campus Life:**
        - Campus building locations
        - Dining hall hours and options
        - Transportation and parking
        - Campus events and activities
        - Student organizations and clubs
        """)
    
    with feature_cols[1]:
        st.markdown("""
        **🎯 Student Services:**
        - Health and counseling services
        - Career center resources
        - Financial aid information
        - Technology support
        - Library services and hours
        
        **🦁 LMU Spirit:**
        - Sports schedules and tickets
        - Spirit events and traditions
        - Greek life information
        - School pride and culture
        - Alumni connections
        """)
    
    # Knowledge base stats
    st.markdown("### 📊 My Knowledge Base")
    
    stats_cols = st.columns(4)
    with stats_cols[0]:
        st.metric("📄 Documents", "2,847", delta="23")
    with stats_cols[1]:
        st.metric("❓ Q&As", "1,256", delta="15")
    with stats_cols[2]:
        st.metric("🏢 Campus Locations", "450+", delta="5")
    with stats_cols[3]:
        st.metric("📅 Events Tracked", "95", delta="8")

def show_feedback_page():
    """Display feedback and suggestion module"""
    st.header("Feedback & Suggestions")
    st.write("Help us make the LMU Campus Spirit Hub even better!")
    
    # Feedback type selector
    feedback_type = st.selectbox(
        "What type of feedback would you like to share?",
        ["General Feedback", "Bug Report", "Feature Request", "Event Suggestion", "Prize Idea"]
    )
    
    # Simple feedback form
    if feedback_type == "General Feedback":
        rating = st.slider("Overall Rating", 1, 5, 4)
        positive_feedback = st.text_area("What's working well?", height=100)
        improvement_feedback = st.text_area("What could be improved?", height=100)
        
    elif feedback_type == "Bug Report":
        bug_severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        bug_location = st.selectbox("Where did this happen?", ["Calendar", "Leaderboard", "Profile", "AI Assistant", "Prize Shop", "Other"])
        bug_description = st.text_area("Describe the bug", height=150)
        
    elif feedback_type == "Feature Request":
        feature_title = st.text_input("Feature Title")
        feature_description = st.text_area("Feature Description", height=150)
        
    elif feedback_type == "Event Suggestion":
        event_name = st.text_input("Event Name")
        event_description = st.text_area("Event Description", height=120)
        
    elif feedback_type == "Prize Idea":
        prize_name = st.text_input("Prize Name")
        prize_description = st.text_area("Prize Description", height=120)
    
    # Contact information
    st.subheader("Contact Information (Optional)")
    contact_name = st.text_input("Your Name")
    contact_email = st.text_input("Email")
    anonymous = st.checkbox("Submit anonymously")
    
    # Submit button
    if st.button("Submit Feedback", type="primary"):
        st.success("Thank you for your feedback!")
                "severity": bug_severity,
                "location": bug_location,
                "description": bug_description,
                "steps": steps_to_reproduce
            })
        # ... and so on for other types
        
        st.success("🎉 Thank you for your feedback! We really appreciate your input.")
        st.balloons()
        
        # Award points for feedback
        if st.session_state.user_id:
            st.session_state.user_points += 3
            st.success("🏆 +3 points for providing feedback!")
        
        # Show confirmation message based on type
        if feedback_type == "Bug Report":
            st.info("🔧 Our tech team will investigate this issue. If you provided contact info, we'll update you on the fix!")
        elif feedback_type == "Feature Request":
            st.info("💡 Our product team will review your suggestion for future updates!")
        elif feedback_type == "Event Suggestion":
            st.info("📅 Our events team will consider your suggestion for upcoming programming!")
        elif feedback_type == "Prize Idea":
            st.info("🎁 Our rewards team will evaluate your prize idea for the next prize refresh!")
    
    # Recent feedback summary
    st.markdown("---")
    st.markdown("### 📊 Community Feedback Summary")
    
    # Mock recent feedback stats
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💌 Total Feedback", "347", delta="23 this week")
    with col2:
        st.metric("⭐ Average Rating", "4.2", delta="0.3")
    with col3:
        st.metric("🔧 Bugs Fixed", "28", delta="5 this week")
    with col4:
        st.metric("✨ Features Added", "12", delta="2 this month")
    
    # Recent improvements based on feedback
    st.markdown("### 🎯 Recent Improvements")
    
    improvements = [
        {"date": "2024-02-10", "improvement": "Added QR code check-in for events", "source": "Feature Request"},
        {"date": "2024-02-08", "improvement": "Improved mobile responsiveness", "source": "Bug Report"},
        {"date": "2024-02-05", "improvement": "Added badge explanations", "source": "General Feedback"},
        {"date": "2024-02-01", "improvement": "New prize: VIP Game Day Experience", "source": "Prize Idea"}
    ]
    
    for improvement in improvements:
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0; color: #2a5298;">✅ {improvement['improvement']}</h4>
                    <p style="margin: 0.25rem 0; color: #666;">📅 {improvement['date']}</p>
                </div>
                <span class="badge">💡 {improvement['source']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()