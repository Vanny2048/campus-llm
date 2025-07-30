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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;600&display=swap');
    
    /* Root Variables */
    :root {
        --primary-blue: #1e3c72;
        --secondary-blue: #2a5298;
        --accent-orange: #ff6b35;
        --accent-gold: #f7931e;
        --text-dark: #2d3748;
        --text-light: #718096;
        --text-white: #ffffff;
        --bg-light: #f7fafc;
        --glass-bg: rgba(255, 255, 255, 0.25);
        --glass-border: rgba(255, 255, 255, 0.18);
        --shadow-soft: 0 8px 32px rgba(31, 38, 135, 0.37);
        --shadow-hover: 0 15px 45px rgba(31, 38, 135, 0.5);
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-accent: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        --gradient-bg: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Global Styles */
    .main {
        font-family: 'Inter', sans-serif;
        background: var(--gradient-bg);
        background-attachment: fixed;
        min-height: 100vh;
        position: relative;
    }
    
    .main::before {
        content: '';
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="50" cy="50" r="0.5" fill="rgba(255,255,255,0.1)"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        opacity: 0.3;
        z-index: -1;
    }
    
    /* Glassmorphism Container */
    .glass-container {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border-radius: 24px;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-soft);
        padding: 2rem;
        margin: 1rem 0;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        color: var(--text-white);
    }
    
    .glass-container::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.8s;
    }
    
    .glass-container:hover::before {
        left: 100%;
    }
    
    .glass-container:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: var(--shadow-hover);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    /* Header Styles */
    .main-header {
        font-family: 'Poppins', sans-serif;
        font-size: clamp(3rem, 8vw, 6rem);
        font-weight: 900;
        background: linear-gradient(135deg, #ffffff 0%, #f0f8ff 50%, #ffffff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin: 2rem 0;
        text-shadow: 0 0 30px rgba(255,255,255,0.5);
        animation: headerGlow 3s ease-in-out infinite alternate;
        position: relative;
    }
    
    .main-header::after {
        content: '🦁';
        position: absolute;
        right: -80px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 4rem;
        animation: roar 2s ease-in-out infinite;
    }
    
    @keyframes headerGlow {
        0% { 
            text-shadow: 0 0 30px rgba(255,255,255,0.5);
            transform: scale(1);
        }
        100% { 
            text-shadow: 0 0 50px rgba(255,255,255,0.8), 0 0 80px rgba(255,255,255,0.3);
            transform: scale(1.05);
        }
    }
    
    @keyframes roar {
        0%, 100% { transform: translateY(-50%) scale(1); }
        50% { transform: translateY(-50%) scale(1.2) rotate(5deg); }
    }
    
    /* Chat Interface */
    .chat-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(20px);
        border-radius: 28px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        padding: 2rem;
        margin: 2rem 0;
        min-height: 500px;
        position: relative;
        overflow: hidden;
        color: var(--text-white);
    }
    
    .chat-message {
        margin: 1rem 0;
        animation: messageSlide 0.5s ease-out;
    }
    
    .user-message {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 1rem;
    }
    
    .bot-message {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 1rem;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 1.2rem 1.5rem;
        border-radius: 24px;
        font-size: 1rem;
        line-height: 1.5;
        position: relative;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        animation: bubblePop 0.3s cubic-bezier(0.68, -0.55, 0.265, 1.55);
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #ff6b35 0%, #f7931e 100%);
        color: white;
        border-bottom-right-radius: 8px;
        margin-left: auto;
    }
    
    .bot-bubble {
        background: rgba(255, 255, 255, 0.95);
        color: var(--text-dark);
        border-bottom-left-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.3);
        font-weight: 500;
    }
    
    .message-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        margin: 0 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    }
    
    .user-avatar {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    
    .bot-avatar {
        background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);
        color: #2d3748;
        animation: bounce 2s ease-in-out infinite;
    }
    
    @keyframes messageSlide {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bubblePop {
        0% {
            opacity: 0;
            transform: scale(0.3);
        }
        50% {
            transform: scale(1.05);
        }
        100% {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-6px);
        }
        60% {
            transform: translateY(-3px);
        }
    }
    
    /* Typing Indicator */
    .typing-indicator {
        display: flex;
        align-items: center;
        padding: 1rem 1.5rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 24px;
        border-bottom-left-radius: 8px;
        max-width: 80px;
        margin: 1rem 0;
        animation: messageSlide 0.3s ease-out;
    }
    
    .typing-dots {
        display: flex;
        gap: 4px;
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: var(--text-light);
        animation: typingDot 1.4s ease-in-out infinite both;
    }
    
    .typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .typing-dot:nth-child(2) { animation-delay: -0.16s; }
    .typing-dot:nth-child(3) { animation-delay: 0; }
    
    @keyframes typingDot {
        0%, 80%, 100% {
            transform: scale(0);
            opacity: 0.5;
        }
        40% {
            transform: scale(1);
            opacity: 1;
        }
    }
    
    /* Enhanced Cards */
    .feature-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        border-radius: 24px;
        padding: 2.5rem;
        margin: 1.5rem 0;
        border: 1px solid var(--glass-border);
        box-shadow: var(--shadow-soft);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
        color: var(--text-white);
    }
    
    .feature-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--gradient-accent);
        border-radius: 24px 24px 0 0;
    }
    
    .feature-card:hover {
        transform: translateY(-12px) rotateX(5deg);
        box-shadow: 0 25px 60px rgba(31, 38, 135, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.4);
    }
    
    /* Points Display */
    .points-display {
        background: var(--gradient-accent);
        color: white;
        padding: 2rem;
        border-radius: 28px;
        text-align: center;
        font-weight: 800;
        font-size: 1.8rem;
        box-shadow: 0 12px 40px rgba(255, 107, 53, 0.4);
        margin: 1.5rem 0;
        position: relative;
        overflow: hidden;
        animation: pointsGlow 2s ease-in-out infinite alternate;
    }
    
    .points-display::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: conic-gradient(from 0deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: rotate 3s linear infinite;
    }
    
    @keyframes pointsGlow {
        from { 
            box-shadow: 0 12px 40px rgba(255, 107, 53, 0.4);
            transform: scale(1);
        }
        to { 
            box-shadow: 0 20px 60px rgba(255, 107, 53, 0.7);
            transform: scale(1.05);
        }
    }
    
    @keyframes rotate {
        to { transform: rotate(360deg); }
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        background: var(--gradient-primary);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        font-size: 1rem;
        font-weight: 600;
        margin: 0.5rem;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .badge::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: left 0.6s;
    }
    
    .badge:hover {
        transform: translateY(-4px) scale(1.1);
        box-shadow: 0 12px 30px rgba(102, 126, 234, 0.6);
    }
    
    .badge:hover::before {
        left: 100%;
    }
    
    /* Input Styles */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 20px !important;
        padding: 1rem 1.5rem !important;
        font-size: 1.1rem !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(10px) !important;
        color: var(--text-dark) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: 2px solid var(--accent-orange) !important;
        box-shadow: 0 0 20px rgba(255, 107, 53, 0.3) !important;
        transform: scale(1.02) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: var(--text-light) !important;
        opacity: 0.7 !important;
    }
    
    /* Button Styles */
    .stButton > button {
        background: var(--gradient-accent) !important;
        color: white !important;
        border: none !important;
        border-radius: 20px !important;
        padding: 0.8rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1.1rem !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3) !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    .stButton > button::before {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent) !important;
        transition: left 0.6s !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-4px) scale(1.05) !important;
        box-shadow: 0 15px 40px rgba(255, 107, 53, 0.5) !important;
    }
    
    .stButton > button:hover::before {
        left: 100% !important;
    }
    
    /* Sidebar Enhancements */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(20px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.2) !important;
    }
    
    /* Leaderboard */
    .leaderboard-item {
        background: var(--glass-bg);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        display: flex;
        align-items: center;
        box-shadow: var(--shadow-soft);
        transition: all 0.3s ease;
        border: 1px solid var(--glass-border);
        position: relative;
        overflow: hidden;
        color: var(--text-white);
    }
    
    .leaderboard-item::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        transition: left 0.8s;
    }
    
    .leaderboard-item:hover {
        transform: translateX(8px) scale(1.02);
        box-shadow: var(--shadow-hover);
    }
    
    .leaderboard-item:hover::before {
        left: 100%;
    }
    
    .rank-1 { 
        border-left: 6px solid #FFD700;
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.1) 0%, var(--glass-bg) 100%);
    }
    .rank-2 { 
        border-left: 6px solid #C0C0C0;
        background: linear-gradient(135deg, rgba(192, 192, 192, 0.1) 0%, var(--glass-bg) 100%);
    }
    .rank-3 { 
        border-left: 6px solid #CD7F32;
        background: linear-gradient(135deg, rgba(205, 127, 50, 0.1) 0%, var(--glass-bg) 100%);
    }
    
    /* Mobile Responsive */
    @media (max-width: 768px) {
        .main-header {
            font-size: clamp(2rem, 8vw, 4rem);
        }
        
        .main-header::after {
            right: -40px;
            font-size: 2.5rem;
        }
        
        .glass-container,
        .feature-card {
            padding: 1.5rem;
            margin: 1rem 0;
            border-radius: 20px;
        }
        
        .points-display {
            font-size: 1.4rem;
            padding: 1.5rem;
        }
        
        .message-bubble {
            max-width: 85%;
            padding: 1rem 1.2rem;
        }
        
        .message-avatar {
            width: 40px;
            height: 40px;
            font-size: 1.2rem;
            margin: 0 8px;
        }
    }
    
    /* Suggestion Pills */
    .suggestion-pill {
        background: rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        padding: 0.8rem 1.5rem;
        margin: 0.5rem;
        color: white;
        font-weight: 500;
        transition: all 0.3s ease;
        cursor: pointer;
        display: inline-block;
    }
    
    .suggestion-pill:hover {
        background: rgba(255, 255, 255, 0.3);
        transform: translateY(-2px) scale(1.05);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gradient-accent);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #f7931e 0%, #ff6b35 100%);
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #fff;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Fix for Streamlit text elements */
    .stMarkdown, .stText, .stWrite {
        color: var(--text-white) !important;
    }
    
    /* Fix for Streamlit containers */
    .stContainer {
        color: var(--text-white) !important;
    }
    
    /* Fix for Streamlit columns */
    .stColumn {
        color: var(--text-white) !important;
    }
    
    /* Fix for Streamlit metrics */
    .stMetric {
        color: var(--text-white) !important;
    }
    
    .stMetric > div > div > div {
        color: var(--text-white) !important;
    }
    
    /* Fix for Streamlit success/error messages */
    .stSuccess, .stError, .stWarning, .stInfo {
        color: var(--text-white) !important;
        background: rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(10px) !important;
        border-radius: 15px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
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
    # Enhanced Header with glass container
    st.markdown("""
    <div class="glass-container" style="text-align: center; margin: 2rem 0;">
        <h1 class="main-header">LMU Campus Spirit Hub</h1>
        <p style="font-size: 1.3rem; color: rgba(255,255,255,0.9); margin-bottom: 1rem; font-weight: 500;">
            Your ultimate platform for campus engagement, spirit points, and Lion pride!
        </p>
        <div style="display: flex; justify-content: center; gap: 2rem; margin-top: 2rem; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.2); padding: 1rem 2rem; border-radius: 20px; backdrop-filter: blur(10px);">
                <span style="font-size: 1.1rem; font-weight: 600; color: white;">🎯 Earn Points</span>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 1rem 2rem; border-radius: 20px; backdrop-filter: blur(10px);">
                <span style="font-size: 1.1rem; font-weight: 600; color: white;">🏆 Win Prizes</span>
            </div>
            <div style="background: rgba(255,255,255,0.2); padding: 1rem 2rem; border-radius: 20px; backdrop-filter: blur(10px);">
                <span style="font-size: 1.1rem; font-weight: 600; color: white;">🤖 Get Help</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Load data
    events, prizes, leaderboard, badges_info = load_mock_data()
    
    # Sidebar for user authentication and navigation
    with st.sidebar:
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 20px; margin-bottom: 2rem; backdrop-filter: blur(10px); color: white;">
            <h3 style="color: white; margin: 0 0 1rem 0; text-align: center;">🔐 User Login</h3>
        """, unsafe_allow_html=True)
        
        if st.session_state.user_id is None:
            user_input = st.text_input("Enter your Student ID or Email:", placeholder="e.g., jdoe@lion.lmu.edu")
            if st.button("🚀 Join the Spirit Squad", type="primary", use_container_width=True):
                if user_input:
                    st.session_state.user_id = user_input
                    st.session_state.user_points = random.randint(150, 800)
                    st.session_state.user_badges = random.sample(list(badges_info.keys()), random.randint(2, 5))
                    st.success(f"Welcome to the Lion pride, {user_input.split('@')[0].title()}! 🦁")
                    st.rerun()
        else:
            st.success(f"Welcome back, {st.session_state.user_id.split('@')[0].title()}! 🦁")
            
            # Enhanced user stats display
            st.markdown(f"""
            <div class="points-display" style="margin: 1rem 0;">
                💰 {st.session_state.user_points} Spirit Points
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown('<h4 style="color: white; margin: 1.5rem 0 0.5rem 0;">Your Badges:</h4>', unsafe_allow_html=True)
            badge_display = " ".join(st.session_state.user_badges)
            st.markdown(f'<div style="font-size: 1.3rem; text-align: center; margin-bottom: 1rem;">{badge_display}</div>', unsafe_allow_html=True)
        
            # Logout button
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.user_id = None
                st.session_state.user_points = 0
                st.session_state.user_badges = []
                st.session_state.conversation_history = []
                st.success("See you later, Lion! 🦁")
                time.sleep(1)
                st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick stats in sidebar
        st.markdown("""
        <div style="background: rgba(255,255,255,0.1); padding: 1rem; border-radius: 15px; margin-top: 1rem; backdrop-filter: blur(10px); color: white;">
            <h4 style="color: white; margin: 0 0 1rem 0; text-align: center;">🎯 Quick Stats</h4>
            <div style="text-align: center; color: rgba(255,255,255,0.9);">
                <p style="margin: 0.5rem 0;">🔥 Most Active: Basketball Fans</p>
                <p style="margin: 0.5rem 0;">⭐ Top Prize: MacBook Pro</p>
                <p style="margin: 0.5rem 0;">🎉 Next Event: First Friday</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Main navigation
    st.markdown('<div class="glass-container" style="margin: 1rem 0;">', unsafe_allow_html=True)
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "📅 Events Calendar", "🏆 Leaderboard", "🎁 Prize Shop", "📸 Content Gallery", "👤 My Profile", "🤖 AI Assistant", "💬 Feedback"],
        icons=["house", "calendar-event", "trophy", "gift", "images", "person-circle", "robot", "chat-dots"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "1rem!important", "background-color": "transparent", "border-radius": "20px"},
            "icon": {"color": "#ff6b35", "font-size": "20px"},
            "nav-link": {
                "font-size": "14px", 
                "text-align": "center", 
                "margin": "0px", 
                "padding": "0.8rem 1rem",
                "border-radius": "15px",
                "background-color": "rgba(255,255,255,0.1)",
                "backdrop-filter": "blur(10px)",
                "transition": "all 0.3s ease",
                "--hover-color": "rgba(255,255,255,0.2)",
                "color": "white"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #ff6b35 0%, #f7931e 100%)", 
                "color": "white",
                "transform": "scale(1.05)",
                "box-shadow": "0 4px 15px rgba(255, 107, 53, 0.4)"
            },
        }
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
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
    
    # Enhanced Chat Interface with realistic design
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)
    st.markdown("### 💡 Quick Questions")
    st.markdown('<p style="color: rgba(255,255,255,0.8); margin-bottom: 1.5rem;">Try these popular questions or ask your own!</p>', unsafe_allow_html=True)
    
    # Suggestion pills
    suggestions = [
        "what even is campus llm?",
        "what's happening on campus this week?", 
        "what should i eat rn?",
        "how do i email my prof when i fumbled an assignment?",
        "i feel like i'm failing everything",
        "where can i study?",
        "what events are coming up?",
        "how do i join greek life?"
    ]
    
    # Display suggestions as pills
    cols = st.columns(4)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 4]:
            if st.button(suggestion, key=f"pill_{i}", help="Click to ask this question"):
                st.session_state.current_question = suggestion
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Main chat container
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Initialize typing state
    if 'show_typing' not in st.session_state:
        st.session_state.show_typing = False
    
    # Display conversation history with realistic chat bubbles
    if st.session_state.conversation_history:
        st.markdown('<div style="max-height: 400px; overflow-y: auto; padding: 1rem 0; margin-bottom: 2rem;">', unsafe_allow_html=True)
        
        for exchange in st.session_state.conversation_history[-10:]:  # Show last 10 messages
            # User message
            st.markdown(f"""
            <div class="user-message chat-message">
                <div class="message-bubble user-bubble">
                    {exchange['question']}
                </div>
                <div class="message-avatar user-avatar">
                    You
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Bot message
            st.markdown(f"""
            <div class="bot-message chat-message">
                <div class="message-avatar bot-avatar">
                    🤖
                </div>
                <div class="message-bubble bot-bubble">
                    {exchange['answer']}
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Welcome message when no conversation
        st.markdown("""
        <div class="bot-message chat-message" style="margin-bottom: 2rem;">
            <div class="message-avatar bot-avatar">
                🤖
            </div>
            <div class="message-bubble bot-bubble">
                hey! i'm your campus ai assistant. basically that friend who's been at lmu forever and knows all the tea. ask me anything about campus life, events, food, studying, or just how to survive the bluff! 
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Show typing indicator when bot is "thinking"
    if st.session_state.show_typing:
        st.markdown("""
        <div class="bot-message chat-message">
            <div class="message-avatar bot-avatar">
                🤖
            </div>
            <div class="typing-indicator">
                <div class="typing-dots">
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                    <div class="typing-dot"></div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Input section
    st.markdown('<div class="glass-container" style="margin-top: 1rem;">', unsafe_allow_html=True)
    
    # Question input with enhanced styling
    question = st.text_input(
        "",
        placeholder="type your question here... (e.g., where's the best place to cry on campus?)",
        value=getattr(st.session_state, 'current_question', ''),
        key="ai_question_input",
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        ask_button = st.button("💬 Send", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ Clear", use_container_width=True)
    with col3:
        random_button = st.button("🎲 Random", use_container_width=True, help="Ask a random question")
    
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
            # Show typing indicator
            st.session_state.show_typing = True
            st.rerun()
            
            # Simulate realistic response time
            time.sleep(random.uniform(1.5, 3.0))
            
            # Generate response
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
            
            # Hide typing indicator and clear input
            st.session_state.show_typing = False
            if hasattr(st.session_state, 'current_question'):
                delattr(st.session_state, 'current_question')
            
            st.rerun()
            
        except Exception as e:
            st.error(f"Oops! Something went wrong: {str(e)}")
            st.session_state.show_typing = False
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