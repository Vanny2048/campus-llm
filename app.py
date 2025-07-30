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

# Custom CSS for enhanced mobile-responsive design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Header Styles */
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: clamp(2rem, 5vw, 4rem);
        font-weight: 800;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #ff6b35 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Card Styles */
    .feature-card {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ff6b35, #f7931e, #2a5298);
    }
    
    /* Points and Badges */
    .points-display {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        font-weight: 700;
        font-size: 1.5rem;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
        margin: 1rem 0;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3); }
        to { box-shadow: 0 8px 35px rgba(255, 107, 53, 0.6); }
    }
    
    .badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.9rem;
        font-weight: 600;
        margin: 0.25rem;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    /* Event Cards */
    .event-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 5px solid #ff6b35;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .event-card:hover {
        transform: translateX(5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
    }
    
    /* Prize Cards */
    .prize-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        border: 2px solid #ff6b35;
        position: relative;
        overflow: hidden;
    }
    
    .prize-card::after {
        content: '🏆';
        position: absolute;
        top: 10px;
        right: 15px;
        font-size: 2rem;
        opacity: 0.7;
    }
    
    /* Leaderboard */
    .leaderboard-item {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    
    .leaderboard-item:hover {
        transform: scale(1.02);
    }
    
    .rank-1 { border-left: 5px solid #FFD700; }
    .rank-2 { border-left: 5px solid #C0C0C0; }
    .rank-3 { border-left: 5px solid #CD7F32; }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .feature-card {
            padding: 1rem;
            margin: 0.5rem 0;
        }
        
        .points-display {
            font-size: 1.2rem;
            padding: 1rem;
        }
    }
    
    /* Calendar Custom Styles */
    .calendar-container {
        background: white;
        border-radius: 20px;
        padding: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* QR Code Styles */
    .qr-container {
        text-align: center;
        background: white;
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    /* Progress Bar */
    .progress-container {
        background: #f0f2f6;
        border-radius: 10px;
        padding: 0.5rem;
        margin: 1rem 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #ff6b35, #f7931e);
        height: 20px;
        border-radius: 10px;
        transition: width 0.5s ease;
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
    """Simulate AI response for demo purposes"""
    responses = {
        "where": [
            "The Math Tutoring Center is in the Academic Resource Center (ARC) on the 2nd floor of Burns Rec Center! They have drop-in hours Monday-Friday 2-8pm, no appointment needed. It's literally a lifesaver during midterms ngl 📚",
            "You can find study rooms in the William H. Hannon Library - just book them online through the library website! The quiet floors are 3-6, and floor 2 has group study areas if you need to work with friends 🤓"
        ],
        "how": [
            "To register for classes, log into PROWL (student portal) during your registration time. Check your holds first though - financial or academic holds will block you from registering! Your time slot is based on credit hours completed 📝",
            "For study abroad applications, visit the LMU International Programs office in University Hall. They have info sessions every month and the application deadline is usually March 1st for fall programs ✈️"
        ],
        "what": [
            "This weekend we've got the basketball game vs Pepperdine on Friday at 7pm (Gersten Pavilion), Greek Row tailgate starting at 4pm, and the Service Learning Fair on Tuesday at Alumni Mall! All events give you spirit points 🦁",
            "GPA requirements vary by program - most need 3.0+ for study abroad, 2.5+ to stay in good standing, and 3.5+ for honors programs. Check with your advisor for specific major requirements!"
        ],
        "when": [
            "The dining halls are open: The Lair (7am-2am), The Roski (11am-8pm weekdays), and Iggy's (5pm-midnight). Lion Dollars work at all locations plus the C-Store! 🍕",
            "Finals week is May 6-10, and spring break is March 11-15. Registration for fall opens in April - dates depend on your class standing!"
        ]
    }
    
    question_lower = question.lower()
    for key in responses:
        if key in question_lower:
            return random.choice(responses[key])
    
    return "That's a great question! I'm still learning about LMU, but you can find more info on the LMU website or ask at the Student Information Desk in the Student Union. The staff there knows everything! 🦁"

# Main App Function
def main():
    # Header
    st.markdown('<h1 class="main-header">🦁 LMU Campus Spirit Hub</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666; margin-bottom: 2rem;">Your ultimate platform for campus engagement, spirit points, and Lion pride!</p>', unsafe_allow_html=True)
    
    # Load data
    events, prizes, leaderboard, badges_info = load_mock_data()
    
    # Sidebar for user authentication and navigation
    with st.sidebar:
        st.markdown("### 🔐 User Login")
        
        if st.session_state.user_id is None:
            user_input = st.text_input("Enter your Student ID or Email:", placeholder="e.g., jdoe@lion.lmu.edu")
            if st.button("🚀 Join the Spirit Squad", type="primary"):
                if user_input:
                    st.session_state.user_id = user_input
                    st.session_state.user_points = random.randint(150, 800)
                    st.session_state.user_badges = random.sample(list(badges_info.keys()), random.randint(2, 5))
                    st.success(f"Welcome to the Lion pride, {user_input.split('@')[0].title()}! 🦁")
                    st.rerun()
        else:
            st.success(f"Welcome back, {st.session_state.user_id.split('@')[0].title()}! 🦁")
            
            # User stats display
            st.markdown(f"""
            <div class="points-display">
                💰 You have {st.session_state.user_points} points to spend!
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("**Your Badges:**")
            badge_display = " ".join(st.session_state.user_badges)
            st.markdown(f'<div style="font-size: 1.5rem; text-align: center;">{badge_display}</div>', unsafe_allow_html=True)
            
            if st.button("🚪 Logout"):
                st.session_state.user_id = None
                st.session_state.user_points = 0
                st.session_state.user_badges = []
                st.rerun()
    
    # Main navigation
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "📅 Events Calendar", "🏆 Leaderboard", "🎁 Prize Shop", "📸 Content Gallery", "👤 My Profile", "🤖 AI Assistant", "💬 Feedback"],
        icons=["house", "calendar-event", "trophy", "gift", "images", "person-circle", "robot", "chat-dots"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#ff6b35", "font-size": "20px"},
            "nav-link": {"font-size": "16px", "text-align": "center", "margin": "0px", "--hover-color": "#f0f2f6"},
            "nav-link-selected": {"background-color": "#ff6b35", "color": "white"},
        }
    )
    
    # Page content based on selection
    if selected == "🏠 Home":
        show_home_page(events, leaderboard)
    elif selected == "📅 Events Calendar":
        show_calendar_page(events)
    elif selected == "🏆 Leaderboard":
        show_leaderboard_page(leaderboard, badges_info)
    elif selected == "🎁 Prize Shop":
        show_prize_shop(prizes)
    elif selected == "📸 Content Gallery":
        show_content_gallery()
    elif selected == "👤 My Profile":
        show_user_profile(events, badges_info)
    elif selected == "🤖 AI Assistant":
        show_ai_assistant()
    elif selected == "💬 Feedback":
        show_feedback_page()

def show_home_page(events, leaderboard):
    """Display the home page with quick stats and upcoming events"""
    
    # Quick stats row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #ff6b35; margin: 0;">📅</h3>
            <h4 style="margin: 0.5rem 0;">Upcoming Events</h4>
            <h2 style="color: #2a5298; margin: 0;">{}</h2>
        </div>
        """.format(len([e for e in events if datetime.strptime(e['date'], '%Y-%m-%d').date() >= date.today()])), 
        unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #ff6b35; margin: 0;">👥</h3>
            <h4 style="margin: 0.5rem 0;">Active Lions</h4>
            <h2 style="color: #2a5298; margin: 0;">847</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_rsvps = sum(event.get('rsvp_count', 0) for event in events)
        st.markdown(f"""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #ff6b35; margin: 0;">🎫</h3>
            <h4 style="margin: 0.5rem 0;">Total RSVPs</h4>
            <h2 style="color: #2a5298; margin: 0;">{total_rsvps}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #ff6b35; margin: 0;">🏆</h3>
            <h4 style="margin: 0.5rem 0;">Points Awarded</h4>
            <h2 style="color: #2a5298; margin: 0;">15.2K</h2>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Main content area
    left_col, right_col = st.columns([2, 1])
    
    with left_col:
        st.markdown("## 🔥 Trending This Week")
        
        # Featured event
        featured_event = events[0]  # Basketball game
        st.markdown(f"""
        <div class="feature-card">
            <div style="display: flex; justify-content: space-between; align-items: start;">
                <div>
                    <h3 style="color: #ff6b35; margin: 0;">{featured_event['title']}</h3>
                    <p style="color: #666; margin: 0.5rem 0;"><strong>📍 {featured_event['location']}</strong></p>
                    <p style="color: #666; margin: 0.5rem 0;">📅 {featured_event['date']} at {featured_event['time']}</p>
                    <p style="margin: 1rem 0;">{featured_event['description']}</p>
                    <div style="display: flex; gap: 1rem; align-items: center;">
                        <span class="badge">🏆 {featured_event['points']} Points</span>
                        <span class="badge">👥 {featured_event['rsvp_count']} Going</span>
                    </div>
                </div>
                <div style="font-size: 4rem;">🏀</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # RSVP and QR Code
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🎫 RSVP for Basketball Game", type="primary", use_container_width=True):
                st.success("🎉 You're registered! See you at the game!")
                st.balloons()
        
        with col_b:
            if st.button("📱 Generate Check-in QR", use_container_width=True):
                qr_buf = generate_qr_code(featured_event['id'], st.session_state.user_id)
                st.image(qr_buf, width=200, caption="Scan at the event for instant points!")
        
        # Upcoming events list
        st.markdown("### 📋 All Upcoming Events")
        
        for event in events[1:]:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d').date()
            if event_date >= date.today():
                st.markdown(f"""
                <div class="event-card">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <h4 style="margin: 0; color: #2a5298;">{event['title']}</h4>
                            <p style="margin: 0.25rem 0; color: #666;">📍 {event['location']} • 📅 {event['date']} • ⏰ {event['time']}</p>
                            <p style="margin: 0.5rem 0;">{event['description']}</p>
                        </div>
                        <div style="text-align: right;">
                            <div class="badge">🏆 {event['points']} pts</div>
                            <p style="margin: 0.25rem 0; font-size: 0.9rem;">👥 {event['rsvp_count']} going</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    with right_col:
        st.markdown("## 🏆 Top Lions This Week")
        
        # Top 5 leaderboard preview
        individual_leaders = [person for person in leaderboard if person['type'] == 'Individual'][:5]
        
        for i, person in enumerate(individual_leaders):
            rank_class = f"rank-{person['rank']}" if person['rank'] <= 3 else ""
            badge_display = " ".join(person['badges'])
            
            st.markdown(f"""
            <div class="leaderboard-item {rank_class}">
                <div style="display: flex; align-items: center; width: 100%;">
                    <div style="font-size: 1.5rem; margin-right: 1rem;">#{person['rank']}</div>
                    <div style="flex-grow: 1;">
                        <div style="font-weight: 600;">{person['name']}</div>
                        <div style="font-size: 0.9rem; color: #666;">{person['points']} points • 🔥{person['streak']} streak</div>
                        <div style="font-size: 1rem;">{badge_display}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        if st.button("🏆 View Full Leaderboard", use_container_width=True):
            st.switch_page("🏆 Leaderboard")
        
        st.markdown("---")
        
        # Quick AI Assistant
        st.markdown("## 🤖 Quick Ask")
        quick_question = st.text_input("Ask me anything about LMU!", placeholder="Where can I find a math tutor?")
        
        if quick_question:
            with st.spinner("🦁 Thinking..."):
                time.sleep(1)
                response = simulate_ai_response(quick_question)
                st.markdown(f"""
                <div class="feature-card">
                    <p style="margin: 0;"><strong>🤖 LMU AI:</strong></p>
                    <p style="margin: 0.5rem 0 0 0;">{response}</p>
                </div>
                """, unsafe_allow_html=True)

def show_calendar_page(events):
    """Display interactive calendar with events"""
    st.markdown("## 📅 Interactive Event Calendar")
    st.markdown("Click on events to see details, RSVP, and get QR codes for check-in!")
    
    # Calendar view selector
    view_option = st.selectbox("📊 Calendar View", ["Month", "Week", "List"], index=0)
    
    if view_option == "List":
        # List view of events
        st.markdown("### 📋 Event List View")
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            event_type_filter = st.selectbox("🎯 Filter by Type", ["All", "Game Day", "Tailgate", "Watch Party", "RSO Event"])
        with col2:
            date_filter = st.date_input("📅 From Date", value=date.today())
        with col3:
            points_filter = st.slider("🏆 Minimum Points", 0, 100, 0)
        
        # Apply filters
        filtered_events = events
        if event_type_filter != "All":
            filtered_events = [e for e in filtered_events if e['type'] == event_type_filter]
        
        filtered_events = [e for e in filtered_events if datetime.strptime(e['date'], '%Y-%m-%d').date() >= date_filter]
        filtered_events = [e for e in filtered_events if e['points'] >= points_filter]
        
        # Display filtered events
        for event in filtered_events:
            col_a, col_b = st.columns([3, 1])
            
            with col_a:
                st.markdown(f"""
                <div class="event-card">
                    <h4 style="margin: 0; color: #ff6b35;">{event['title']}</h4>
                    <p style="margin: 0.5rem 0; color: #666;">
                        📍 {event['location']} • 📅 {event['date']} • ⏰ {event['time']}
                    </p>
                    <p style="margin: 0.5rem 0;">{event['description']}</p>
                    <div style="display: flex; gap: 0.5rem; margin-top: 1rem;">
                        <span class="badge">🎯 {event['type']}</span>
                        <span class="badge">🏆 {event['points']} Points</span>
                        <span class="badge">👥 {event['rsvp_count']}/{event['max_capacity']}</span>
                        {f'<span class="badge">📱 QR Check-in</span>' if event.get('qr_checkin') else ''}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col_b:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button(f"🎫 RSVP", key=f"rsvp_{event['id']}", use_container_width=True):
                    st.success(f"✅ RSVP confirmed for {event['title']}!")
                    # Add to calendar functionality could be implemented here
                
                if event.get('qr_checkin') and st.button(f"📱 QR Code", key=f"qr_{event['id']}", use_container_width=True):
                    with st.expander("📱 Event Check-in QR Code"):
                        qr_buf = generate_qr_code(event['id'], st.session_state.user_id)
                        st.image(qr_buf, width=200)
                        st.markdown("**Instructions:** Show this QR code at the event entrance for instant check-in and points!")
                
                # Add to personal calendar
                if st.button(f"📆 Add to Calendar", key=f"cal_{event['id']}", use_container_width=True):
                    # Create calendar event data
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
                        label="📥 Download .ics file",
                        data=cal_data,
                        file_name=f"{event['title'].replace(' ', '_')}.ics",
                        mime="text/calendar"
                    )
    
    else:
        # Try to show calendar component if available
        try:
            calendar_events = create_calendar_events(events)
            
            st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
            
            calendar_options = {
                "editable": "true",
                "navLinks": "true",
                "selectable": "true",
            }
            
            calendar_component = calendar(
                events=calendar_events,
                options=calendar_options,
                custom_css="""
                .fc-event-past {
                    opacity: 0.6;
                }
                .fc-event {
                    font-size: 0.85em;
                    border-radius: 5px;
                }
                """
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Handle calendar interactions
            if calendar_component.get('eventClick'):
                event_clicked = calendar_component['eventClick']['event']
                st.info(f"🎯 Selected: {event_clicked['title']}")
                
        except:
            st.info("📅 Interactive calendar component not available. Showing list view instead.")
            # Fallback to a simple calendar visualization
            show_simple_calendar(events)

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
    """Display dynamic leaderboard with real-time updates"""
    st.markdown("## 🏆 Spirit Leaderboard")
    st.markdown("Live rankings updated every minute! Compete for the top spot and earn exclusive badges.")
    
    # Leaderboard type selector
    leaderboard_type = st.selectbox("🎯 View Rankings", ["Individual Students", "RSOs & Organizations", "Combined"])
    
    # Filter leaderboard based on selection
    if leaderboard_type == "Individual Students":
        filtered_leaderboard = [person for person in leaderboard if person['type'] == 'Individual']
    elif leaderboard_type == "RSOs & Organizations":
        filtered_leaderboard = [person for person in leaderboard if person['type'] == 'RSO']
    else:
        filtered_leaderboard = leaderboard
    
    # Display statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_participants = len([p for p in leaderboard if p['type'] == 'Individual'])
        st.metric("👥 Active Students", total_participants, delta=12)
    
    with col2:
        total_orgs = len([p for p in leaderboard if p['type'] == 'RSO'])
        st.metric("🏛️ Participating RSOs", total_orgs, delta=2)
    
    with col3:
        total_points = sum(person['points'] for person in leaderboard)
        st.metric("🏆 Total Points Awarded", f"{total_points:,}", delta=245)
    
    # Main leaderboard display
    st.markdown("### 🥇 Current Rankings")
    
    for i, person in enumerate(filtered_leaderboard):
        # Determine medal/rank styling
        if person['rank'] == 1:
            rank_style = "background: linear-gradient(135deg, #FFD700, #FFA500); color: #333;"
            rank_icon = "🥇"
        elif person['rank'] == 2:
            rank_style = "background: linear-gradient(135deg, #C0C0C0, #A8A8A8); color: #333;"
            rank_icon = "🥈"
        elif person['rank'] == 3:
            rank_style = "background: linear-gradient(135deg, #CD7F32, #B87333); color: white;"
            rank_icon = "🥉"
        else:
            rank_style = "background: white; border: 2px solid #e9ecef;"
            rank_icon = f"#{person['rank']}"
        
        # Badge display
        badge_display = " ".join(person['badges'])
        
        # Streak indicator
        streak_color = "#ff6b35" if person['streak'] >= 10 else "#2a5298" if person['streak'] >= 5 else "#666"
        
        st.markdown(f"""
        <div style="{rank_style} border-radius: 15px; padding: 1.5rem; margin: 1rem 0; box-shadow: 0 5px 15px rgba(0,0,0,0.1);">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div style="display: flex; align-items: center; gap: 1.5rem;">
                    <div style="font-size: 2rem; font-weight: bold;">{rank_icon}</div>
                    <div>
                        <h3 style="margin: 0; font-size: 1.3rem;">{person['name']}</h3>
                        <p style="margin: 0.25rem 0; font-size: 1rem; opacity: 0.8;">
                            🏆 {person['points']:,} points • 
                            <span style="color: {streak_color};">🔥 {person['streak']} day streak</span>
                        </p>
                        <div style="font-size: 1.2rem; margin-top: 0.5rem;">{badge_display}</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.9rem; opacity: 0.8;">
                        {person['type']}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Points progress chart
    st.markdown("### 📊 Points Progression")
    
    # Create sample data for points over time
    dates = pd.date_range(start='2024-01-01', end='2024-02-15', freq='D')
    points_data = []
    
    for person in filtered_leaderboard[:5]:  # Top 5 for chart
        person_points = []
        cumulative = 0
        for date in dates:
            daily_points = random.randint(0, 25)
            cumulative += daily_points
            person_points.append(cumulative)
        
        points_data.append({
            'Name': person['name'],
            'Dates': dates,
            'Points': person_points
        })
    
    # Create plotly chart
    fig = go.Figure()
    
    colors = ['#ff6b35', '#2a5298', '#f7931e', '#667eea', '#764ba2']
    for i, data in enumerate(points_data):
        fig.add_trace(go.Scatter(
            x=data['Dates'],
            y=data['Points'],
            mode='lines+markers',
            name=data['Name'],
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="📈 Points Progression Over Time",
        xaxis_title="Date",
        yaxis_title="Cumulative Points",
        height=400,
        hovermode='x unified',
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Badge explanation
    with st.expander("🏅 Badge Guide - What Do They Mean?"):
        cols = st.columns(3)
        badges_list = list(badges_info.items())
        
        for i, col in enumerate(cols):
            with col:
                start_idx = i * (len(badges_list) // 3)
                end_idx = (i + 1) * (len(badges_list) // 3) if i < 2 else len(badges_list)
                
                for badge, description in badges_list[start_idx:end_idx]:
                    st.markdown(f"**{badge}** {description}")

def show_prize_shop(prizes):
    """Display prize showcase with categories and detailed descriptions"""
    st.markdown("## 🎁 Prize Shop")
    st.markdown("Earn points and redeem them for exclusive LMU experiences and rewards!")
    
    # User points display
    if st.session_state.user_id:
        st.markdown(f"""
        <div class="points-display">
            💰 You have {st.session_state.user_points} points to spend!
        </div>
        """, unsafe_allow_html=True)
    
    # Prize categories
    categories = list(set(prize['category'] for prize in prizes))
    selected_category = st.selectbox("🎯 Browse by Category", ["All Categories"] + categories)
    
    # Filter prizes
    if selected_category != "All Categories":
        filtered_prizes = [p for p in prizes if p['category'] == selected_category]
    else:
        filtered_prizes = prizes
    
    # Sort options
    sort_option = st.selectbox("📊 Sort by", ["Points (Low to High)", "Points (High to Low)", "Availability", "Category"])
    
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
        
        # Prize availability styling
        if available_count == 0:
            card_style = "background: #f8f9fa; opacity: 0.6; border: 2px dashed #ccc;"
            availability_text = "🚫 Sold Out"
            button_disabled = True
        elif available_count <= 2:
            card_style = "background: linear-gradient(135deg, #fff3cd, #ffeaa7); border: 2px solid #ff6b35;"
            availability_text = f"⚡ Only {available_count} left!"
            button_disabled = False
        else:
            card_style = "background: linear-gradient(135deg, #ffecd2, #fcb69f); border: 2px solid #ff6b35;"
            availability_text = f"✅ {available_count} available"
            button_disabled = False
        
        # Disable if user can't afford
        if not can_afford and st.session_state.user_id:
            card_style += " opacity: 0.7;"
            button_disabled = True
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"""
            <div style="{card_style} border-radius: 20px; padding: 2rem; margin: 1rem 0; position: relative;">
                <div style="position: absolute; top: 15px; right: 20px; font-size: 3rem;">{prize['image']}</div>
                <h3 style="color: #2a5298; margin: 0 0 0.5rem 0;">{prize['name']}</h3>
                <p style="color: #ff6b35; font-weight: 600; margin: 0 0 1rem 0;">{prize['category']}</p>
                <p style="margin: 0 0 1rem 0; line-height: 1.5;">{prize['description']}</p>
                
                <div style="display: flex; gap: 1rem; align-items: center; margin-top: 1.5rem;">
                    <span style="background: #2a5298; color: white; padding: 0.5rem 1rem; border-radius: 25px; font-weight: 600;">
                        💰 {prize['points_required']} points
                    </span>
                    <span style="background: {'#28a745' if available_count > 2 else '#ffc107' if available_count > 0 else '#dc3545'}; 
                                 color: white; padding: 0.5rem 1rem; border-radius: 25px; font-weight: 600;">
                        {availability_text}
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<br>" * 4, unsafe_allow_html=True)
            
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
    """Display content gallery with photos, videos, and social posts"""
    st.markdown("## 📸 Content Gallery")
    st.markdown("Relive the best moments from LMU events and get hyped for what's coming next!")
    
    # Content type tabs
    content_tabs = st.tabs(["📷 Event Photos", "🎥 Video Highlights", "📱 Social Posts", "🎨 Submit Content"])
    
    with content_tabs[0]:  # Event Photos
        st.markdown("### 📷 Latest Event Photos")
        
        # Sample photo data (in real app, this would come from a database)
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
    """Display user profile with progress tracking and stats"""
    if not st.session_state.user_id:
        st.warning("🔐 Please log in to view your profile!")
        return
    
    st.markdown(f"## 👤 {st.session_state.user_id.split('@')[0].title()}'s Profile")
    
    # Profile stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #ff6b35; margin: 0;">🏆</h3>
            <h2 style="color: #2a5298; margin: 0.5rem 0;">{st.session_state.user_points}</h2>
            <p style="margin: 0;">Spirit Points</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        events_attended = len(st.session_state.attended_events)
        st.markdown(f"""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #ff6b35; margin: 0;">📅</h3>
            <h2 style="color: #2a5298; margin: 0.5rem 0;">{events_attended}</h2>
            <p style="margin: 0;">Events Attended</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #ff6b35; margin: 0;">🏅</h3>
            <h2 style="color: #2a5298; margin: 0.5rem 0;">{len(st.session_state.user_badges)}</h2>
            <p style="margin: 0;">Badges Earned</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        current_streak = random.randint(3, 15)  # Simulated
        st.markdown(f"""
        <div class="feature-card" style="text-align: center;">
            <h3 style="color: #ff6b35; margin: 0;">🔥</h3>
            <h2 style="color: #2a5298; margin: 0.5rem 0;">{current_streak}</h2>
            <p style="margin: 0;">Day Streak</p>
        </div>
        """, unsafe_allow_html=True)
    
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
    """Enhanced AI assistant with LMU-specific knowledge"""
    st.markdown("## 🤖 LMU AI Assistant")
    st.markdown("Ask me anything about LMU! I know about campus life, academics, events, and more. 🦁")
    
    # Quick suggestion buttons
    st.markdown("### 💡 Quick Questions")
    suggestion_cols = st.columns(3)
    
    suggestions = [
        "Where can I find a math tutor?",
        "What events are happening this week?",
        "How do I join Greek life?",
        "Where is the counseling center?",
        "What's the GPA requirement for study abroad?",
        "How do I get to campus by Metro?"
    ]
    
    for i, suggestion in enumerate(suggestions):
        with suggestion_cols[i % 3]:
            if st.button(f"💬 {suggestion}", key=f"suggestion_{i}"):
                st.session_state.current_question = suggestion
    
    # Chat interface
    st.markdown("### 💬 Chat with LMU AI")
    
    # Display conversation history
    if st.session_state.conversation_history:
        st.markdown("#### 📝 Recent Conversation")
        for i, exchange in enumerate(st.session_state.conversation_history[-5:]):  # Show last 5
            st.markdown(f"""
            <div class="feature-card">
                <p style="margin: 0 0 0.5rem 0;"><strong>🙋 You:</strong> {exchange['question']}</p>
                <p style="margin: 0; color: #2a5298;"><strong>🤖 LMU AI:</strong> {exchange['answer']}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Question input
    question = st.text_input(
        "Ask your question:",
        placeholder="e.g., Where can I find study rooms?",
        value=getattr(st.session_state, 'current_question', ''),
        key="ai_question_input"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        ask_button = st.button("🚀 Ask LMU AI", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear Chat", use_container_width=True)
    
    if clear_button:
        st.session_state.conversation_history = []
        st.rerun()
    
    if ask_button and question:
        with st.spinner("🤔 Thinking like a Lion..."):
            time.sleep(1.5)  # Simulate thinking time
            response = simulate_ai_response(question)
            
            # Add to conversation history
            st.session_state.conversation_history.append({
                "question": question,
                "answer": response,
                "timestamp": datetime.now().isoformat()
            })
            
            # Award points for asking questions
            if st.session_state.user_id:
                st.session_state.user_points += 1
                st.success("🏆 +1 point for asking a question!")
            
            # Display the response
            st.markdown(f"""
            <div class="feature-card" style="border-left: 5px solid #ff6b35;">
                <p style="margin: 0 0 0.5rem 0;"><strong>🙋 You:</strong> {question}</p>
                <p style="margin: 0; color: #2a5298;"><strong>🤖 LMU AI:</strong> {response}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Clear the input
            if hasattr(st.session_state, 'current_question'):
                delattr(st.session_state, 'current_question')
    
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
    st.markdown("## 💬 Feedback & Suggestions")
    st.markdown("Help us make the LMU Campus Spirit Hub even better! Your voice matters. 🦁")
    
    # Feedback type selector
    feedback_type = st.selectbox(
        "🎯 What type of feedback would you like to share?",
        ["General Feedback", "Bug Report", "Feature Request", "Event Suggestion", "Prize Idea", "Content Submission"]
    )
    
    # Feedback form based on type
    if feedback_type == "General Feedback":
        st.markdown("### 💭 General Feedback")
        rating = st.slider("⭐ Overall Rating", 1, 5, 4)
        
        st.markdown("**What's working well?**")
        positive_feedback = st.text_area("Tell us what you love...", height=100)
        
        st.markdown("**What could be improved?**")
        improvement_feedback = st.text_area("Share your improvement ideas...", height=100)
        
    elif feedback_type == "Bug Report":
        st.markdown("### 🐛 Bug Report")
        bug_severity = st.selectbox("🚨 Severity", ["Low", "Medium", "High", "Critical"])
        bug_location = st.selectbox("📍 Where did this happen?", ["Calendar", "Leaderboard", "Profile", "AI Assistant", "Prize Shop", "Other"])
        bug_description = st.text_area("🔍 Describe the bug", 
                                     placeholder="What happened? What did you expect to happen?", 
                                     height=150)
        steps_to_reproduce = st.text_area("🔄 Steps to reproduce", 
                                        placeholder="1. Go to...\n2. Click on...\n3. See error...", 
                                        height=100)
        
    elif feedback_type == "Feature Request":
        st.markdown("### ✨ Feature Request")
        feature_category = st.selectbox("📂 Category", ["UI/UX", "Events", "Social", "Gamification", "AI Assistant", "Mobile", "Other"])
        feature_title = st.text_input("💡 Feature Title", placeholder="Brief title for your idea")
        feature_description = st.text_area("📝 Feature Description", 
                                         placeholder="Describe your feature idea in detail...", 
                                         height=150)
        feature_priority = st.selectbox("🎯 Priority", ["Nice to have", "Important", "Critical"])
        
    elif feedback_type == "Event Suggestion":
        st.markdown("### 📅 Event Suggestion")
        event_name = st.text_input("🎉 Event Name", placeholder="e.g., Lions Late Night Study")
        event_type = st.selectbox("🎯 Event Type", ["Game Day", "Tailgate", "Watch Party", "RSO Event", "Social", "Academic", "Service", "Other"])
        event_description = st.text_area("📝 Event Description", height=120)
        suggested_points = st.number_input("🏆 Suggested Points Value", min_value=5, max_value=100, value=20)
        estimated_attendance = st.number_input("👥 Expected Attendance", min_value=10, max_value=1000, value=50)
        
    elif feedback_type == "Prize Idea":
        st.markdown("### 🎁 Prize Idea")
        prize_name = st.text_input("🏆 Prize Name", placeholder="e.g., Lunch with the Basketball Team")
        prize_category = st.selectbox("📂 Category", ["Ultimate Experience", "Game Day", "Academic", "Leadership", "Recognition", "Merchandise", "Other"])
        prize_description = st.text_area("📝 Prize Description", height=120)
        suggested_points_required = st.number_input("💰 Suggested Points Required", min_value=50, max_value=2000, value=300, step=50)
        prize_availability = st.number_input("📊 How many available?", min_value=1, max_value=50, value=1)
        
    else:  # Content Submission
        st.markdown("### 📸 Content Submission")
        content_type_detailed = st.selectbox("📋 Content Type", ["Photo", "Video", "Story", "Social Media Post", "Article", "Other"])
        content_title = st.text_input("📰 Content Title")
        content_description = st.text_area("📝 Content Description", height=120)
        content_event = st.selectbox("🏷️ Related Event (if any)", ["None", "Recent Basketball Game", "Latest Tailgate", "RSO Fair", "Other"])
    
    # Common fields for all feedback types
    st.markdown("---")
    st.markdown("### 👤 Contact Information (Optional)")
    
    col1, col2 = st.columns(2)
    with col1:
        contact_name = st.text_input("📛 Your Name", placeholder="How should we credit you?")
    with col2:
        contact_email = st.text_input("📧 Email", placeholder="For follow-up questions")
    
    # Anonymous option
    anonymous = st.checkbox("🕶️ Submit anonymously")
    
    # Submit button
    if st.button("🚀 Submit Feedback", type="primary", use_container_width=True):
        # Create feedback object (in real app, this would go to database)
        feedback_data = {
            "type": feedback_type,
            "timestamp": datetime.now().isoformat(),
            "anonymous": anonymous
        }
        
        if not anonymous:
            feedback_data["contact_name"] = contact_name
            feedback_data["contact_email"] = contact_email
        
        # Add type-specific data
        if feedback_type == "General Feedback":
            feedback_data.update({
                "rating": rating,
                "positive": positive_feedback,
                "improvements": improvement_feedback
            })
        elif feedback_type == "Bug Report":
            feedback_data.update({
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