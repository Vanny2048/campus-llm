#!/usr/bin/env python3
"""
LMU Campus LLM - Ultimate 3D School Spirit Platform
Enhanced with modern 3D design, Gen Z chatbot, images, and interactive features

Author: Vanessa Akaraiwe
Ultimate 3D Design & Gen Z Experience
"""

import gradio as gr
import json
import os
import qrcode
import io
import base64
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import requests
from PIL import Image, ImageDraw, ImageFont
import numpy as np

class UltimateLMUApp:
    def __init__(self):
        """Initialize the Ultimate 3D LMU application"""
        self.current_user = None
        self.conversation_history = []
        
        # Image URLs for LMU content
        self.lmu_images = {
            "campus": "https://images.unsplash.com/photo-1562774053-701939374585?w=800&h=600&fit=crop",
            "gersten": "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=600&fit=crop",
            "basketball": "https://images.unsplash.com/photo-1546519638-68e109498ffc?w=800&h=600&fit=crop",
            "tailgate": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?w=800&h=600&fit=crop",
            "spirit": "https://images.unsplash.com/photo-1511886929837-354984827c0f?w=800&h=600&fit=crop",
            "campus_life": "https://images.unsplash.com/photo-1523050854058-8df90110c9e1?w=800&h=600&fit=crop",
            "library": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?w=800&h=600&fit=crop",
            "dining": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&h=600&fit=crop"
        }
        
        # Load data
        self.game_events = self._load_game_events()
        self.tailgates = self._load_tailgates()
        self.spirit_challenges = self._load_spirit_challenges()
        self.premium_prizes = self._load_premium_prizes()
        self.leaderboard_data = self._load_leaderboard_data()
        self.genz_responses = self._load_genz_personality()
        
    def _load_game_events(self):
        """Load game events with images"""
        return [
            {
                "id": "bb_001",
                "sport": "🏀 Basketball",
                "opponent": "Pepperdine Waves",
                "date": "2024-02-15",
                "time": "19:00",
                "venue": "Gersten Pavilion",
                "spirit_points": 75,
                "hashtag": "#LMUvsPepperdine",
                "image": self.lmu_images["basketball"],
                "description": "Epic rivalry game! The Bluff will be absolutely electric tonight! 🔥"
            },
            {
                "id": "bb_002", 
                "sport": "🏀 Basketball",
                "opponent": "Gonzaga Bulldogs",
                "date": "2024-02-22",
                "time": "20:00",
                "venue": "Gersten Pavilion",
                "spirit_points": 100,
                "hashtag": "#LMUvsGonzaga",
                "image": self.lmu_images["basketball"],
                "description": "The biggest game of the season! Gonzaga coming to The Bluff! 🦁"
            }
        ]
        
    def _load_tailgates(self):
        """Load tailgate events"""
        return [
            {
                "id": "tg_001",
                "name": "Alpha Delta Pi x Phi Delta Theta Tailgate",
                "date": "2024-02-15",
                "time": "17:00",
                "location": "Gersten Pavilion Parking Lot",
                "host": "Alpha Delta Pi & Phi Delta Theta",
                "image": self.lmu_images["tailgate"],
                "spirit_points": 25,
                "description": "The most iconic tailgate on The Bluff! Greek life bringing the heat! 🔥"
            },
            {
                "id": "tg_002",
                "name": "LMU Spirit Squad Mega Tailgate",
                "date": "2024-02-22", 
                "time": "18:00",
                "location": "Gersten Pavilion Parking Lot",
                "host": "LMU Spirit Squad",
                "image": self.lmu_images["spirit"],
                "spirit_points": 35,
                "description": "Spirit Squad throwing down the ultimate pre-game party! 💃"
            }
        ]
        
    def _load_spirit_challenges(self):
        """Load spirit challenges"""
        return [
            {
                "id": "sc_001",
                "title": "🔥 Best Spirit Selfie",
                "description": "Post your best LMU spirit selfie at the game",
                "points": 25,
                "hashtag": "#LMUSpiritSelfie",
                "prize": "LMU Spirit Squad T-Shirt",
                "image": self.lmu_images["spirit"],
                "status": "active"
            },
            {
                "id": "sc_002", 
                "title": "🎤 Best LMU Chant",
                "description": "Record yourself leading the best LMU chant",
                "points": 30,
                "hashtag": "#LMUChantChallenge",
                "prize": "VIP Game Access",
                "image": self.lmu_images["spirit"],
                "status": "active"
            }
        ]
        
    def _load_premium_prizes(self):
        """Load premium prizes"""
        return [
            {
                "id": "pp_001",
                "title": "👑 Day as LMU President",
                "description": "Shadow the president, attend meetings, take over LMU socials for a day",
                "points_required": 2000,
                "image": self.lmu_images["campus"],
                "category": "Ultimate Experience"
            },
            {
                "id": "pp_002",
                "title": "🎤 PA Announcer for a Game",
                "description": "Professional announcing experience at Gersten Pavilion",
                "points_required": 1500,
                "image": self.lmu_images["gersten"],
                "category": "Game Day Experience"
            }
        ]
        
    def _load_leaderboard_data(self):
        """Load leaderboard data"""
        return [
            {"rank": 1, "name": "Sarah Johnson", "points": 1450, "badges": 12, "events_attended": 18, "organization": "Alpha Delta Pi"},
            {"rank": 2, "name": "Marcus Rodriguez", "points": 1320, "badges": 10, "events_attended": 16, "organization": "LMU Spirit Squad"},
            {"rank": 3, "name": "Emily Chen", "points": 1280, "badges": 9, "events_attended": 15, "organization": "Phi Delta Theta"}
        ]
        
    def _load_genz_personality(self):
        """Load Gen Z personality responses"""
        return {
            "greetings": [
                "Hey bestie! 👋✨",
                "What's good fam! 🔥",
                "Yoooo what's the tea? ☕",
                "Hey there! Ready to slay? 💅"
            ],
            "lmu_specific": {
                "gersten": "Gersten Pavilion is where all the basketball magic happens! 🏀✨ It's literally the heart of LMU athletics. The energy there during games is absolutely everything! 🔥",
                "tutoring": "Bestie, LMU has amazing tutoring at the Academic Resource Center in Daum Hall! 📚✨ You can also find subject-specific tutors in the library. The ARC is literally a lifesaver! 💁‍♀️",
                "parking": "Parking at LMU can be a whole mood, but here's the tea: Gersten lot is free for games, and there's always street parking on LMU Drive! 🚗💅",
                "campus_life": "The Bluff life is literally unmatched! From The Rock at sunset to the vibes at The Lair, every spot has its own energy! 🌅✨",
                "spirit": "LMU spirit is on another level! The Spirit Squad, cheerleaders, and Iggy the Lion make every game day absolutely iconic! 🦁🔥"
            }
        }
        
    def get_genz_response(self, response_type="greetings"):
        """Get a Gen Z style response"""
        responses = self.genz_responses.get(response_type, [])
        if isinstance(responses, list):
            return random.choice(responses)
        return responses
        
    def process_message(self, message, history, user_id=None):
        """Process user message with Gen Z personality"""
        message_lower = message.lower()
        
        # Get Gen Z greeting
        genz_greeting = self.get_genz_response("greetings")
        
        # LMU-specific responses
        if "tutoring" in message_lower or "study" in message_lower:
            response = f"{genz_greeting} {self.genz_responses['lmu_specific']['tutoring']}"
        elif "parking" in message_lower:
            response = f"{genz_greeting} {self.genz_responses['lmu_specific']['parking']}"
        elif "gersten" in message_lower:
            response = f"{genz_greeting} {self.genz_responses['lmu_specific']['gersten']}"
        elif "campus" in message_lower or "bluff" in message_lower:
            response = f"{genz_greeting} {self.genz_responses['lmu_specific']['campus_life']}"
        elif "spirit" in message_lower or "game" in message_lower:
            response = f"{genz_greeting} {self.genz_responses['lmu_specific']['spirit']}"
        elif "food" in message_lower or "dining" in message_lower:
            response = f"{genz_greeting} The Lair food is literally bussin! 🍕✨ You've got to try the pizza and the smoothie bar. The Grove also has some fire options! 🔥"
        elif "library" in message_lower or "study" in message_lower:
            response = f"{genz_greeting} The Annex is the perfect study spot! 📚✨ Quiet vibes and great coffee. The library also has amazing resources and study rooms! 💯"
        elif "events" in message_lower or "what's happening" in message_lower:
            response = f"{genz_greeting} Check out the Events tab for all the tea on what's happening on The Bluff! 🗓️✨ From basketball games to tailgates, we've got everything! 🔥"
        else:
            # Default helpful response
            response = f"{genz_greeting} I'm your ultimate LMU bestie! Ask me about campus life, events, dining, tutoring, or anything about The Bluff! 🦁✨"
            
        return response
        
    def get_ultimate_3d_css(self):
        """Get ultimate 3D CSS styling with better fonts and effects"""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Audiowide&family=Space+Grotesk:wght@300;400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Space Grotesk', sans-serif;
            background: linear-gradient(135deg, #0A0A0A 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            overflow-x: hidden;
        }
        
        .main-container {
            min-height: 100vh;
            background: 
                radial-gradient(circle at 20% 80%, rgba(255, 107, 107, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 80% 20%, rgba(78, 205, 196, 0.15) 0%, transparent 50%),
                radial-gradient(circle at 40% 40%, rgba(69, 183, 209, 0.1) 0%, transparent 50%);
        }
        
        .header-ultimate {
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.95) 0%, rgba(78, 205, 196, 0.95) 100%);
            backdrop-filter: blur(30px);
            border-bottom: 3px solid rgba(255, 255, 255, 0.3);
            padding: 30px 0;
            position: relative;
            overflow: hidden;
        }
        
        .header-ultimate::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.4;
        }
        
        .header-content {
            position: relative;
            z-index: 2;
            text-align: center;
        }
        
        .main-title-ultimate {
            font-family: 'Orbitron', monospace;
            font-size: 4rem;
            font-weight: 900;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #FF69B4, #A8E6CF);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 4s ease-in-out infinite;
            text-shadow: 0 0 40px rgba(255, 107, 107, 0.6);
            margin-bottom: 15px;
            letter-spacing: 3px;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .subtitle-ultimate {
            font-family: 'Inter', sans-serif;
            font-size: 1.4rem;
            color: rgba(255, 255, 255, 0.9);
            font-weight: 400;
            letter-spacing: 3px;
            text-transform: uppercase;
        }
        
        .card-ultimate {
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(25px);
            border: 2px solid rgba(255, 255, 255, 0.15);
            border-radius: 25px;
            padding: 30px;
            margin: 25px 0;
            transform: perspective(1200px) rotateX(8deg);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        }
        
        .card-ultimate::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
            transition: left 0.6s;
        }
        
        .card-ultimate:hover::before {
            left: 100%;
        }
        
        .card-ultimate:hover {
            transform: perspective(1200px) rotateX(0deg) translateY(-15px);
            box-shadow: 0 25px 50px rgba(0, 0, 0, 0.4);
            border-color: rgba(255, 255, 255, 0.3);
        }
        
        .card-title-ultimate {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.8rem;
            font-weight: 700;
            color: #4ECDC4;
            margin-bottom: 20px;
            text-shadow: 0 0 15px rgba(78, 205, 196, 0.6);
            letter-spacing: 1px;
        }
        
        .neon-button-ultimate {
            background: linear-gradient(45deg, #FF6B6B, #FF69B4, #A8E6CF);
            border: none;
            border-radius: 30px;
            padding: 15px 30px;
            color: white;
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            font-size: 1.1rem;
            cursor: pointer;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 2px;
            box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
        }
        
        .neon-button-ultimate::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
            transition: left 0.6s;
        }
        
        .neon-button-ultimate:hover::before {
            left: 100%;
        }
        
        .neon-button-ultimate:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 35px rgba(255, 107, 107, 0.5);
        }
        
        .event-card-ultimate {
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(78, 205, 196, 0.1) 100%);
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .event-card-ultimate:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .event-image-ultimate {
            width: 100%;
            height: 200px;
            object-fit: cover;
            border-radius: 15px;
            margin-bottom: 15px;
            transition: transform 0.3s ease;
        }
        
        .event-image-ultimate:hover {
            transform: scale(1.05);
        }
        
        .leaderboard-ultimate {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 25px;
            padding: 25px;
            margin: 25px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .leaderboard-item-ultimate {
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            transition: all 0.3s ease;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .leaderboard-item-ultimate:hover {
            transform: scale(1.02);
            background: rgba(255, 255, 255, 0.12);
            border-color: rgba(255, 255, 255, 0.2);
        }
        
        .rank-badge-ultimate {
            background: linear-gradient(45deg, #FF6B6B, #FF69B4);
            color: white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 1.2rem;
            margin-right: 20px;
            box-shadow: 0 5px 15px rgba(255, 107, 107, 0.3);
        }
        
        .points-display-ultimate {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 25px;
            padding: 30px;
            text-align: center;
            box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.2);
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(15px);
            transform: perspective(1200px) rotateX(8deg);
            transition: all 0.4s ease;
        }
        
        .points-display-ultimate:hover {
            transform: perspective(1200px) rotateX(0deg) translateY(-8px);
        }
        
        .chat-container-ultimate {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 25px;
            padding: 25px;
            margin: 25px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .chat-message-ultimate {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            border-left: 4px solid #4ECDC4;
            transition: all 0.3s ease;
        }
        
        .user-message-ultimate {
            background: rgba(255, 107, 107, 0.15);
            border-left-color: #FF6B6B;
        }
        
        .stats-grid-ultimate {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 25px;
            margin: 25px 0;
        }
        
        .stat-card-ultimate {
            background: rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 25px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.15);
            transition: all 0.3s ease;
        }
        
        .stat-card-ultimate:hover {
            transform: translateY(-5px);
            background: rgba(255, 255, 255, 0.12);
        }
        
        .stat-number-ultimate {
            font-family: 'Orbitron', monospace;
            font-size: 2.5rem;
            color: #4ECDC4;
            margin-bottom: 10px;
            text-shadow: 0 0 15px rgba(78, 205, 196, 0.5);
        }
        
        .stat-label-ultimate {
            font-family: 'Inter', sans-serif;
            color: rgba(255, 255, 255, 0.9);
            font-size: 1rem;
            font-weight: 500;
        }
        
        .prize-card-ultimate {
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.15) 0%, rgba(78, 205, 196, 0.15) 100%);
            border-radius: 25px;
            padding: 25px;
            margin: 20px 0;
            border: 2px solid rgba(255, 255, 255, 0.2);
            transition: all 0.4s ease;
            position: relative;
            overflow: hidden;
        }
        
        .prize-card-ultimate:hover {
            transform: translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
        }
        
        .prize-title-ultimate {
            font-family: 'Space Grotesk', sans-serif;
            font-size: 1.5rem;
            color: #FF69B4;
            margin-bottom: 15px;
            font-weight: 700;
        }
        
        .prize-points-ultimate {
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: #4ECDC4;
            font-size: 1.2rem;
        }
        
        .notification-ultimate {
            background: linear-gradient(45deg, #FF6B6B, #FF69B4);
            color: white;
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            animation: slideIn 0.6s ease;
            box-shadow: 0 10px 25px rgba(255, 107, 107, 0.3);
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        """
        
    def get_game_day_dashboard_ultimate(self):
        """Get ultimate game day dashboard with images"""
        html = """
        <div class="card-ultimate">
            <div class="card-title-ultimate">🏀 Tonight's Game</div>
            <div class="event-card-ultimate">
                <img src="{}" alt="Basketball Game" class="event-image-ultimate">
                <h3 style="color: #FF6B6B; margin: 10px 0;">LMU vs Pepperdine Waves</h3>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">📍 Gersten Pavilion | ⏰ 7:00 PM</p>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">🎫 $15 | 🔥 75 Spirit Points</p>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0; font-style: italic;">Epic rivalry game! The Bluff will be absolutely electric tonight! 🔥</p>
                <button class="neon-button-ultimate" onclick="alert('RSVP Success! +75 points')">RSVP Now</button>
            </div>
        </div>
        """.format(self.lmu_images["basketball"])
        return html
        
    def get_enhanced_calendar_ultimate(self):
        """Get ultimate enhanced calendar"""
        html = """
        <div class="card-ultimate">
            <div class="card-title-ultimate">📅 Upcoming Events</div>
        """
        
        # Add game events
        for event in self.game_events:
            html += """
            <div class="event-card-ultimate">
                <img src="{}" alt="Game Event" class="event-image-ultimate">
                <h4 style="color: #4ECDC4; margin: 10px 0;">{} vs {}</h4>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">📅 {} | ⏰ {}</p>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">📍 {} | 🔥 {} Points</p>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0; font-style: italic;">{}</p>
                <button class="neon-button-ultimate" onclick="alert('Added to calendar!')">Add to Calendar</button>
            </div>
            """.format(event["image"], event["sport"], event["opponent"], event["date"], event["time"], event["venue"], event["spirit_points"], event["description"])
        
        # Add tailgates
        for tailgate in self.tailgates:
            html += """
            <div class="event-card-ultimate">
                <img src="{}" alt="Tailgate" class="event-image-ultimate">
                <h4 style="color: #FF69B4; margin: 10px 0;">{}</h4>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">📅 {} | ⏰ {}</p>
                <p style="color: rgba(255,255,255,0.8); margin: 5px 0;">📍 {} | 🔥 {} Points</p>
                <p style="color: rgba(255,255,255,0.9); margin: 10px 0; font-style: italic;">{}</p>
                <button class="neon-button-ultimate" onclick="alert('RSVP Success! +{} points')">RSVP</button>
            </div>
            """.format(tailgate["image"], tailgate["name"], tailgate["date"], tailgate["time"], tailgate["location"], tailgate["spirit_points"], tailgate["description"], tailgate["spirit_points"])
        
        html += "</div>"
        return html
        
    def get_enhanced_leaderboard_ultimate(self):
        """Get ultimate enhanced leaderboard"""
        html = """
        <div class="leaderboard-ultimate">
            <div class="card-title-ultimate">🏆 Spirit Leaderboard</div>
        """
        
        for entry in self.leaderboard_data:
            html += """
            <div class="leaderboard-item-ultimate">
                <div class="rank-badge-ultimate">{}</div>
                <div style="flex: 1;">
                    <h4 style="color: #4ECDC4; margin: 5px 0;">{}</h4>
                    <p style="color: rgba(255,255,255,0.7); margin: 2px 0; font-size: 0.9rem;">{}</p>
                </div>
                <div style="text-align: right;">
                    <div style="color: #FF6B6B; font-size: 1.2rem; font-weight: bold;">{} pts</div>
                    <div style="color: rgba(255,255,255,0.7); font-size: 0.8rem;">{} badges</div>
                </div>
            </div>
            """.format(entry["rank"], entry["name"], entry["organization"], entry["points"], entry["badges"])
        
        html += "</div>"
        return html
        
    def get_enhanced_prizes_ultimate(self):
        """Get ultimate enhanced prizes"""
        html = """
        <div class="card-ultimate">
            <div class="card-title-ultimate">🎁 Premium Prizes</div>
        """
        
        for prize in self.premium_prizes:
            html += """
            <div class="prize-card-ultimate">
                <img src="{}" alt="Prize" style="width: 100%; height: 200px; object-fit: cover; border-radius: 15px; margin-bottom: 15px;">
                <div class="prize-title-ultimate">{}</div>
                <p style="color: rgba(255,255,255,0.8); margin: 10px 0;">{}</p>
                <div class="prize-points-ultimate">🔥 {} Points Required</div>
                <button class="neon-button-ultimate" onclick="alert('Prize unlocked!')">Redeem</button>
            </div>
            """.format(prize["image"], prize["title"], prize["description"], prize["points_required"])
        
        html += "</div>"
        return html
        
    def get_enhanced_spirit_challenges_ultimate(self):
        """Get ultimate enhanced spirit challenges"""
        html = """
        <div class="card-ultimate">
            <div class="card-title-ultimate">🔥 Spirit Challenges</div>
        """
        
        for challenge in self.spirit_challenges:
            html += """
            <div class="event-card-ultimate">
                <img src="{}" alt="Challenge" class="event-image-ultimate">
                <h4 style="color: #FF69B4; margin: 10px 0;">{}</h4>
                <p style="color: rgba(255,255,255,0.8); margin: 10px 0;">{}</p>
                <p style="color: #4ECDC4; margin: 5px 0;">🔥 {} Points | 🏆 {}</p>
                <p style="color: rgba(255,255,255,0.7); margin: 5px 0;">#{}</p>
                <button class="neon-button-ultimate" onclick="alert('Challenge accepted!')">Join Challenge</button>
            </div>
            """.format(challenge["image"], challenge["title"], challenge["description"], challenge["points"], challenge["prize"], challenge["hashtag"])
        
        html += "</div>"
        return html
        
    def get_user_profile_ultimate(self, user_id):
        """Get ultimate user profile"""
        user_stats = {
            "points": 1250,
            "rank": 3,
            "total_users": 150,
            "badges": 8,
            "events_attended": 12,
            "streak": 5
        }
        
        html = """
        <div class="card-ultimate">
            <div class="card-title-ultimate">👤 Your Profile</div>
            <div class="stats-grid-ultimate">
                <div class="stat-card-ultimate">
                    <div class="stat-number-ultimate">{}</div>
                    <div class="stat-label-ultimate">Total Points</div>
                </div>
                <div class="stat-card-ultimate">
                    <div class="stat-number-ultimate">#{}</div>
                    <div class="stat-label-ultimate">Rank</div>
                </div>
                <div class="stat-card-ultimate">
                    <div class="stat-number-ultimate">{}</div>
                    <div class="stat-label-ultimate">Badges Earned</div>
                </div>
                <div class="stat-card-ultimate">
                    <div class="stat-number-ultimate">{}</div>
                    <div class="stat-label-ultimate">Events Attended</div>
                </div>
            </div>
            <div class="notification-ultimate">
                🔥 You're on a {} day streak! Keep the spirit alive!
            </div>
        </div>
        """.format(user_stats["points"], user_stats["rank"], user_stats["badges"], user_stats["events_attended"], user_stats["streak"])
        
        return html
        
    def generate_qr_code_ultimate(self, event_id, event_type):
        """Generate ultimate QR code for check-in"""
        qr_data = f"LMU_SPIRIT_{event_type.upper()}_{event_id}_{datetime.now().strftime('%Y%m%d')}"
        
        # Create QR code
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        html = """
        <div class="card-ultimate">
            <div class="card-title-ultimate">📱 Check-in QR Code</div>
            <div style="text-align: center; background: white; border-radius: 20px; padding: 30px; margin: 20px 0;">
                <img src="data:image/png;base64,{}" alt="QR Code" style="max-width: 300px;">
                <p style="color: #333; margin-top: 15px; font-weight: bold;">Scan to check in and earn points!</p>
            </div>
            <div class="notification-ultimate">
                ✅ Check-in successful! +75 points earned!
            </div>
        </div>
        """.format(img_str)
        
        return html
        
    def create_ultimate_interface(self):
        """Create the ultimate 3D interface"""
        css = self.get_ultimate_3d_css()
        
        with gr.Blocks(css=css, title="LMU Campus LLM Ultimate 3D") as interface:
            # Header
            with gr.Row():
                gr.HTML("""
                <div class="header-ultimate">
                    <div class="header-content">
                        <div class="main-title-ultimate">🦁 LMU Campus LLM Ultimate 3D</div>
                        <div class="subtitle-ultimate">Your Ultimate School Spirit Platform</div>
                    </div>
                </div>
                """)
            
            # Main content tabs
            with gr.Tabs():
                # Dashboard Tab
                with gr.Tab("🏠 Dashboard"):
                    with gr.Row():
                        gr.HTML(self.get_game_day_dashboard_ultimate())
                    
                    with gr.Row():
                        gr.HTML(self.get_user_profile_ultimate("user_123"))
                
                # Calendar Tab
                with gr.Tab("📅 Events"):
                    gr.HTML(self.get_enhanced_calendar_ultimate())
                
                # Leaderboard Tab
                with gr.Tab("🏆 Leaderboard"):
                    gr.HTML(self.get_enhanced_leaderboard_ultimate())
                
                # Prizes Tab
                with gr.Tab("🎁 Prizes"):
                    gr.HTML(self.get_enhanced_prizes_ultimate())
                
                # Challenges Tab
                with gr.Tab("🔥 Challenges"):
                    gr.HTML(self.get_enhanced_spirit_challenges_ultimate())
                
                # Chat Tab
                with gr.Tab("💬 Chat"):
                    with gr.Row():
                        with gr.Column(scale=3):
                            chatbot = gr.Chatbot(
                                label="Chat with LMU Assistant",
                                height=500,
                                show_label=True
                            )
                        with gr.Column(scale=1):
                            gr.HTML("""
                            <div class="chat-container-ultimate">
                                <h4>💡 Quick Tips</h4>
                                <p>• Ask about campus events</p>
                                <p>• Get dining recommendations</p>
                                <p>• Find tutoring resources</p>
                                <p>• Learn about RSOs</p>
                                <p>• Check game schedules</p>
                                <p>• Get parking info</p>
                            </div>
                            """)
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            label="Message",
                            placeholder="Ask me anything about LMU! (e.g., 'where can i find tutoring?')",
                            lines=3
                        )
                        send_btn = gr.Button("Send", variant="primary")
                    
                    def respond(message, history):
                        response = self.process_message(message, history)
                        history.append((message, response))
                        return "", history
                    
                    send_btn.click(respond, [msg, chatbot], [msg, chatbot])
                    msg.submit(respond, [msg, chatbot], [msg, chatbot])
                
                # QR Code Tab
                with gr.Tab("📱 Check-in"):
                    gr.HTML(self.generate_qr_code_ultimate("bb_001", "game"))
                
                # Feedback Tab
                with gr.Tab("💭 Feedback"):
                    with gr.Row():
                        with gr.Column():
                            feedback_text = gr.Textbox(
                                label="Share Your Feedback",
                                placeholder="How can we improve the LMU Campus AI?",
                                lines=4
                            )
                            feedback_btn = gr.Button("Submit Feedback", variant="primary")
                            
                            event_suggestion = gr.Textbox(
                                label="Suggest an Event",
                                placeholder="e.g., LMU vs Pepperdine Tailgate",
                                lines=2
                            )
                            location_suggestion = gr.Textbox(
                                label="Event Location",
                                placeholder="e.g., The Grove, Gersten Pavilion",
                                lines=1
                            )
                            host_suggestion = gr.Textbox(
                                label="Host Organization",
                                placeholder="e.g., Alpha Delta Pi, LMU Spirit Squad",
                                lines=1
                            )
                            suggestion_btn = gr.Button("Submit Suggestion", variant="primary")
                        
                        with gr.Column():
                            gr.HTML("""
                            <div class="card-ultimate">
                                <h4>💡 Recent Suggestions</h4>
                                <div class="event-card-ultimate">
                                    <p style="font-size: 0.9rem; margin: 5px 0;">🏈 LMU Spirit Squad Tailgate</p>
                                    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Suggested by @lmu_lion</p>
                                </div>
                                <div class="event-card-ultimate">
                                    <p style="font-size: 0.9rem; margin: 5px 0;">🎵 Spring Concert Series</p>
                                    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Suggested by @music_lover</p>
                                </div>
                            </div>
                            """)
            
            # Footer
            with gr.Row():
                gr.HTML("""
                <div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.8);">
                    <p style="font-size: 1.1rem; margin-bottom: 10px;">🦁 LMU Campus LLM Ultimate 3D - Making School Spirit Iconic Since 2024</p>
                    <p style="font-size: 0.9rem;">Built with 💖 for the LMU Community</p>
                </div>
                """)
        
        return interface

def main():
    """Main function to run the ultimate LMU app"""
    app = UltimateLMUApp()
    interface = app.create_ultimate_interface()
    
    print("🦁 Starting LMU Campus LLM Ultimate 3D...")
    print("✨ Features: Ultimate 3D Design, Gen Z Chatbot, Interactive Calendar")
    print("🎮 Live Game Day Engagement, Premium Prizes, Spirit Challenges")
    print("📱 QR Code Check-ins, User Profiles, Feedback System")
    print("🖼️ High-quality Images, Better Fonts, Responsive Design")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    )

if __name__ == "__main__":
    main()