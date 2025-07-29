#!/usr/bin/env python3
"""
LMU Campus LLM - Enhanced Streamlit Application
A modern, interactive platform for LMU students with AI assistance and spirit system
"""

import streamlit as st
import json
import pandas as pd
import re
import hashlib
from datetime import datetime, timedelta
import random
import time
from typing import Dict, List, Optional

# Page configuration
st.set_page_config(
    page_title="LMU Campus LLM",
    page_icon="🦁",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with modern design
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-family: 'Poppins', sans-serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #2a5298;
        margin-bottom: 1.5rem;
        border-left: 4px solid #ff6b35;
        padding-left: 1rem;
    }
    
    .card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
    }
    
    .spirit-points {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 2rem;
        font-weight: 600;
        text-align: center;
        font-size: 1.2rem;
        box-shadow: 0 4px 15px rgba(255, 107, 53, 0.3);
        margin: 1rem 0;
    }
    
    .event-card {
        background: white;
        border: 2px solid #e9ecef;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .event-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
    }
    
    .event-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.1);
        border-color: #ff6b35;
    }
    
    .prize-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 1rem;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        transition: all 0.3s ease;
    }
    
    .prize-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    .chat-message {
        padding: 1rem;
        border-radius: 1rem;
        margin: 0.5rem 0;
        max-width: 80%;
    }
    
    .user-message {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        margin-left: auto;
        border-bottom-right-radius: 0.3rem;
    }
    
    .ai-message {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        color: #2a5298;
        margin-right: auto;
        border-bottom-left-radius: 0.3rem;
        border: 1px solid #dee2e6;
    }
    
    .lmu-id-input {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border: 2px solid #dee2e6;
        border-radius: 0.5rem;
        padding: 0.75rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .lmu-id-input:focus {
        border-color: #ff6b35;
        box-shadow: 0 0 0 3px rgba(255, 107, 53, 0.1);
    }
    
    .success-message {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    .error-message {
        background: linear-gradient(135deg, #dc3545 0%, #fd7e14 100%);
        color: white;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
        font-weight: 600;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        text-align: center;
        border: 1px solid #e9ecef;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2a5298;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        border: none;
        border-radius: 0.5rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(255, 107, 53, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(255, 107, 53, 0.3);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    .leaderboard-table {
        background: white;
        border-radius: 0.5rem;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    .leaderboard-table th {
        background: linear-gradient(135deg, #2a5298 0%, #1e3c72 100%);
        color: white;
        font-weight: 600;
        padding: 1rem;
    }
    
    .leaderboard-table td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid #e9ecef;
    }
    
    .leaderboard-table tr:hover {
        background-color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

# Comprehensive LMU Knowledge Base
LMU_KNOWLEDGE_BASE = {
    "academics": {
        "colleges": [
            "Bellarmine College of Liberal Arts",
            "College of Business Administration", 
            "College of Communication and Fine Arts",
            "Frank R. Seaver College of Science and Engineering",
            "School of Education",
            "School of Film and Television",
            "Loyola Law School"
        ],
        "academic_calendar": {
            "add_drop_deadline": "First week of classes",
            "midterms": "Weeks 6-8",
            "finals": "Last week of semester",
            "graduation": "May and December"
        },
        "resources": {
            "tutoring": "Academic Resource Center in Daum Hall",
            "library": "William H. Hannon Library",
            "writing_center": "Center for Student Success",
            "advising": "Academic Advising Center"
        }
    },
    "campus_life": {
        "dining": [
            "Lair Marketplace",
            "The Lion's Den",
            "The Habit Burger Grill",
            "Starbucks",
            "Einstein Bros. Bagels"
        ],
        "housing": [
            "First Year Experience (FYE) Halls",
            "Sophomore Experience (SOE) Halls",
            "Upper Division Housing",
            "Greek Housing"
        ],
        "transportation": {
            "shuttle": "LMU Shuttle Service",
            "parking": "Student Parking Lots",
            "bike_share": "Lion Bike Share Program"
        }
    },
    "student_organizations": {
        "greek_life": [
            "Alpha Phi Omega",
            "Delta Gamma",
            "Kappa Alpha Theta",
            "Pi Beta Phi",
            "Sigma Chi",
            "Theta Xi"
        ],
        "clubs": [
            "Student Government",
            "Campus Ministry",
            "International Student Association",
            "Black Student Union",
            "Latinx Student Union",
            "Asian Pacific Student Services"
        ]
    },
    "athletics": {
        "teams": [
            "Men's Basketball",
            "Women's Basketball", 
            "Men's Soccer",
            "Women's Soccer",
            "Baseball",
            "Softball",
            "Volleyball",
            "Tennis",
            "Golf",
            "Swimming & Diving"
        ],
        "venues": {
            "basketball": "Gersten Pavilion",
            "soccer": "Sullivan Field",
            "baseball": "Page Stadium",
            "softball": "Smith Field"
        },
        "mascot": "Iggy the Lion",
        "colors": "Blue and White",
        "conference": "West Coast Conference (WCC)"
    },
    "campus_services": {
        "health": "Student Health Services",
        "counseling": "Student Psychological Services",
        "career": "Career and Professional Development",
        "financial_aid": "Financial Aid Office",
        "registrar": "Office of the Registrar",
        "it_support": "Information Technology Services"
    },
    "location": {
        "address": "1 LMU Drive, Los Angeles, CA 90045",
        "area": "Westchester neighborhood of Los Angeles",
        "nearby": [
            "Los Angeles International Airport (LAX)",
            "Playa Vista",
            "Marina del Rey",
            "Venice Beach",
            "Santa Monica"
        ]
    }
}

# Sample data with enhanced content
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
        "tailgate": "Lions Den Tailgate (4:00 PM)",
        "description": "Rivalry game against Pepperdine! Wear your blue and white!"
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
        "watch_party": "Greek Row Watch Party",
        "description": "Away game at Gonzaga - join the watch party!"
    },
    {
        "id": "fb_001",
        "sport": "⚽ Soccer", 
        "opponent": "San Diego",
        "date": "2024-03-02",
        "time": "14:00",
        "venue": "Sullivan Field",
        "type": "home",
        "spirit_points": 75,
        "tailgate": "Greek Row Tailgate (12:00 PM)",
        "description": "Home soccer match with tailgate festivities!"
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
    st.session_state.user_points = 291
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'rsvp_events' not in st.session_state:
    st.session_state.rsvp_events = []
if 'completed_challenges' not in st.session_state:
    st.session_state.completed_challenges = []
if 'lmu_id_verified' not in st.session_state:
    st.session_state.lmu_id_verified = False
if 'user_lmu_id' not in st.session_state:
    st.session_state.user_lmu_id = ""

def validate_lmu_id(lmu_id: str) -> bool:
    """Validate LMU ID format (9 digits)"""
    if not lmu_id:
        return False
    # Remove any non-digit characters (including dashes, spaces, etc.)
    clean_id = re.sub(r'\D', '', lmu_id)
    # Check if it's exactly 9 digits
    return len(clean_id) == 9 and clean_id.isdigit()

def get_enhanced_ai_response(question: str) -> str:
    """Enhanced AI response system with comprehensive LMU knowledge"""
    question_lower = question.lower()
    
    # Academic queries
    if any(word in question_lower for word in ["add/drop", "deadline", "registration"]):
        return f"📚 **Add/Drop Deadline**: {LMU_KNOWLEDGE_BASE['academics']['academic_calendar']['add_drop_deadline']}. Check your student portal for exact dates and any holds on your account!"
    
    if any(word in question_lower for word in ["tutor", "tutoring", "help", "study"]):
        return f"📖 **Tutoring Services**: Visit the {LMU_KNOWLEDGE_BASE['academics']['resources']['tutoring']} for free tutoring! They offer drop-in sessions and scheduled appointments for most subjects."
    
    if any(word in question_lower for word in ["library", "study", "quiet"]):
        return f"📚 **Study Spots**: The {LMU_KNOWLEDGE_BASE['academics']['resources']['library']} has multiple floors - 3rd floor is quiet study, Lion's Den is social study, and there are study rooms in the business school!"
    
    # Campus life queries
    if any(word in question_lower for word in ["food", "eat", "dining", "restaurant"]):
        dining_options = ", ".join(LMU_KNOWLEDGE_BASE['campus_life']['dining'])
        return f"🍕 **Dining Options**: {dining_options}. The Lion's Den is great for social dining, and the Lair has the most variety!"
    
    if any(word in question_lower for word in ["parking", "car", "transport"]):
        return f"🚗 **Transportation**: {LMU_KNOWLEDGE_BASE['campus_life']['transportation']['parking']} available. Also check out the {LMU_KNOWLEDGE_BASE['campus_life']['transportation']['shuttle']} for getting around campus!"
    
    # Athletics queries
    if any(word in question_lower for word in ["game", "basketball", "soccer", "sport"]):
        next_game = GAME_EVENTS[0]
        return f"🏀 **Next Game**: {next_game['sport']} vs {next_game['opponent']} on {next_game['date']} at {next_game['time']} in {next_game['venue']}! {next_game.get('tailgate', '')}"
    
    if any(word in question_lower for word in ["mascot", "colors", "spirit"]):
        return f"🦁 **LMU Spirit**: Our mascot is {LMU_KNOWLEDGE_BASE['athletics']['mascot']} and our colors are {LMU_KNOWLEDGE_BASE['athletics']['colors']}! Go Lions! 🦁"
    
    # Student organizations
    if any(word in question_lower for word in ["club", "organization", "join", "greek"]):
        return f"👥 **Student Organizations**: LMU has over 200 clubs! Visit the Student Leadership & Development office in Malone Student Center to browse all organizations. Popular options include {', '.join(LMU_KNOWLEDGE_BASE['student_organizations']['clubs'][:3])}."
    
    # Campus services
    if any(word in question_lower for word in ["health", "medical", "doctor"]):
        return f"🏥 **Health Services**: {LMU_KNOWLEDGE_BASE['campus_services']['health']} is located in Malone Student Center. They offer medical appointments, immunizations, and health education!"
    
    if any(word in question_lower for word in ["counseling", "therapy", "mental health"]):
        return f"🧠 **Counseling**: {LMU_KNOWLEDGE_BASE['campus_services']['counseling']} provides free individual and group therapy sessions. They're located in Malone Student Center."
    
    if any(word in question_lower for word in ["career", "job", "internship"]):
        return f"💼 **Career Services**: {LMU_KNOWLEDGE_BASE['campus_services']['career']} offers resume reviews, interview prep, job fairs, and internship opportunities!"
    
    # Location queries
    if any(word in question_lower for word in ["where", "location", "address"]):
        return f"📍 **LMU Location**: {LMU_KNOWLEDGE_BASE['location']['address']} in the {LMU_KNOWLEDGE_BASE['location']['area']} neighborhood of Los Angeles."
    
    # Default response with helpful suggestions
    return f"🦁 **LMU Campus Assistant**: I'm here to help with all things LMU! Try asking about:\n\n• **Academics**: Add/drop deadlines, tutoring, study spots\n• **Campus Life**: Dining options, parking, housing\n• **Athletics**: Game schedules, spirit events\n• **Student Services**: Health, counseling, career services\n• **Organizations**: Clubs, Greek life, student groups\n\nOr check out the other tabs for game day info and spirit challenges! 🎉"

def show_lmu_id_verification():
    """Show LMU ID verification interface"""
    st.markdown('<h2 class="sub-header">🆔 LMU Student Verification</h2>', unsafe_allow_html=True)
    
    if not st.session_state.lmu_id_verified:
        st.markdown("""
        <div class="card">
            <h3>Welcome to LMU Campus LLM!</h3>
            <p>Please enter your 9-digit LMU Student ID to access all features and earn spirit points.</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            lmu_id = st.text_input(
                "Enter your 9-digit LMU ID:",
                placeholder="123456789",
                key="lmu_id_input",
                help="Enter your 9-digit LMU Student ID number"
            )
            
            if st.button("Verify LMU ID", use_container_width=True):
                if validate_lmu_id(lmu_id):
                    st.session_state.lmu_id_verified = True
                    st.session_state.user_lmu_id = re.sub(r'\D', '', lmu_id)
                    st.success("✅ LMU ID verified successfully! Welcome to the LMU community!")
                    st.rerun()
                else:
                    st.error("❌ Please enter a valid 9-digit LMU Student ID.")
    else:
        st.markdown(f"""
        <div class="success-message">
            ✅ Verified LMU Student (ID: {st.session_state.user_lmu_id[:3]}***{st.session_state.user_lmu_id[-3:]})
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Change LMU ID", key="change_id"):
            st.session_state.lmu_id_verified = False
            st.session_state.user_lmu_id = ""
            st.rerun()

def main():
    # Header
    st.markdown('<h1 class="main-header">🦁 LMU Campus LLM</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.3rem; color: #666; margin-bottom: 2rem;">Your AI Campus Assistant & Spirit Engine</p>', unsafe_allow_html=True)
    
    # LMU ID Verification
    show_lmu_id_verification()
    
    if not st.session_state.lmu_id_verified:
        st.stop()
    
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
        st.markdown('<div class="leaderboard-table">', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
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
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{st.session_state.user_points}</div>
            <div class="metric-label">Your Points</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.rsvp_events)}</div>
            <div class="metric-label">Events RSVP'd</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(st.session_state.completed_challenges)}</div>
            <div class="metric-label">Challenges Completed</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">Top 5</div>
            <div class="metric-label">Your Rank</div>
        </div>
        """, unsafe_allow_html=True)
    
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
            <p><strong>Description:</strong> {next_event['description']}</p>
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
                <p><strong>Description:</strong> {event['description']}</p>
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
    st.markdown("""
    <div class="card">
        <h3>Ask me anything about LMU!</h3>
        <p>I can help with academics, campus life, athletics, student services, and more.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sample questions
    st.markdown("**💡 Try asking:**")
    sample_questions = [
        "When is add/drop deadline?",
        "Where can I find tutoring?",
        "What's happening on campus this weekend?",
        "How do I join a club?",
        "Where's the best place to study?",
        "What are the dining options?",
        "When's the next basketball game?",
        "How do I get parking on campus?"
    ]
    
    cols = st.columns(4)
    for i, question in enumerate(sample_questions):
        with cols[i % 4]:
            if st.button(question, key=f"sample_{i}"):
                response = get_enhanced_ai_response(question)
                st.session_state.conversation_history.append({"user": question, "ai": response})
                st.rerun()
    
    # Chat history
    if st.session_state.conversation_history:
        st.markdown("## 💬 Chat History")
        for i, message in enumerate(st.session_state.conversation_history):
            # User message
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>You:</strong> {message["user"]}
            </div>
            """, unsafe_allow_html=True)
            
            # AI message
            st.markdown(f"""
            <div class="chat-message ai-message">
                <strong>LMU Assistant:</strong> {message["ai"]}
            </div>
            """, unsafe_allow_html=True)
    
    # Manual input
    user_input = st.chat_input("Ask me anything about LMU...")
    if user_input:
        response = get_enhanced_ai_response(user_input)
        st.session_state.conversation_history.append({"user": user_input, "ai": response})
        st.rerun()

if __name__ == "__main__":
    main()