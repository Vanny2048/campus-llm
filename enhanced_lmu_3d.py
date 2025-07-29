#!/usr/bin/env python3
"""
LMU Campus LLM - Ultimate 3D School Spirit Platform
Enhanced with modern 3D design, Gen Z chatbot, and interactive features

Author: Vanessa Akaraiwe
Enhanced with 3D Design & Gen Z Experience
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

# Import existing modules
try:
    from src.llm_handler import LLMHandler
    from src.points_system import PointsSystem
    from src.rag_system import RAGSystem
    from src.utils import load_config, log_interaction
except ImportError:
    # Fallback if modules don't exist
    class LLMHandler:
        def generate_response(self, message, context, history):
            return "Enhanced LMU Assistant: " + message
    class PointsSystem:
        def add_points(self, user_id, points, reason):
            pass
        def get_user_stats(self, user_id):
            return "Total Points: 450"
        def get_user_rank(self, user_id):
            return {"rank": 5, "total_users": 100}
    class RAGSystem:
        def get_relevant_context(self, message):
            return ""
    def load_config():
        return {"app_name": "LMU Campus LLM 3D"}
    def log_interaction(message, response, user_id):
        pass

class EnhancedLMUApp:
    def __init__(self):
        """Initialize the Enhanced 3D LMU application"""
        self.config = load_config()
        self.llm_handler = LLMHandler()
        self.points_system = PointsSystem()
        self.rag_system = RAGSystem()
        
        # Session state
        self.current_user = None
        self.conversation_history = []
        
        # Enhanced Game Day & Spirit System
        self.game_events = self._load_enhanced_game_events()
        self.tailgates = self._load_enhanced_tailgates()
        self.watch_parties = self._load_enhanced_watch_parties()
        self.spirit_challenges = self._load_enhanced_spirit_challenges()
        self.premium_prizes = self._load_enhanced_premium_prizes()
        self.rso_events = self._load_rso_events()
        self.leaderboard_data = self._load_leaderboard_data()
        
        # Gen Z Chatbot Personality
        self.genz_responses = self._load_genz_personality()
        
    def _load_enhanced_game_events(self):
        """Load enhanced game events with 3D styling"""
        return [
            {
                "id": "bb_001",
                "sport": "🏀 Basketball",
                "opponent": "Pepperdine Waves",
                "date": "2024-02-15",
                "time": "19:00",
                "venue": "Gersten Pavilion",
                "type": "home",
                "spirit_points": 50,
                "tailgate_id": "tg_001",
                "status": "upcoming",
                "ticket_price": "$15",
                "capacity": 4000,
                "current_attendance": 3200,
                "live_stream": "https://wccsports.com/watch",
                "hashtag": "#LMUvsPepperdine",
                "weather": "72°F, Clear",
                "parking": "Free in Gersten Lot",
                "food_trucks": ["Taco Truck", "Ice Cream Cart"],
                "spirit_theme": "Red Sea Night"
            },
            {
                "id": "bb_002", 
                "sport": "🏀 Basketball",
                "opponent": "Gonzaga Bulldogs",
                "date": "2024-02-22",
                "time": "20:00",
                "venue": "McCarthy Athletic Center",
                "type": "away",
                "spirit_points": 30,
                "watch_party_id": "wp_001",
                "status": "upcoming",
                "ticket_price": "N/A",
                "capacity": 6000,
                "current_attendance": 0,
                "live_stream": "https://espn.com/watch",
                "hashtag": "#LMUvsGonzaga",
                "weather": "68°F, Partly Cloudy",
                "parking": "N/A",
                "food_trucks": [],
                "spirit_theme": "Lions on the Road"
            },
            {
                "id": "fb_001",
                "sport": "🏈 Football", 
                "opponent": "San Diego Toreros",
                "date": "2024-03-02",
                "time": "14:00",
                "venue": "Sullivan Field",
                "type": "home",
                "spirit_points": 75,
                "tailgate_id": "tg_002",
                "status": "upcoming",
                "ticket_price": "$20",
                "capacity": 5000,
                "current_attendance": 0,
                "live_stream": "https://wccsports.com/watch",
                "hashtag": "#LMUvsUSD",
                "weather": "75°F, Sunny",
                "parking": "Free in Sullivan Lot",
                "food_trucks": ["BBQ Truck", "Pizza Truck", "Dessert Cart"],
                "spirit_theme": "Lions Pride"
            },
            {
                "id": "bb_003",
                "sport": "🏀 Basketball",
                "opponent": "Saint Mary's Gaels",
                "date": "2024-03-09",
                "time": "18:00",
                "venue": "Gersten Pavilion",
                "type": "home",
                "spirit_points": 60,
                "tailgate_id": "tg_003",
                "status": "upcoming",
                "ticket_price": "$18",
                "capacity": 4000,
                "current_attendance": 0,
                "live_stream": "https://wccsports.com/watch",
                "hashtag": "#LMUvsSMC",
                "weather": "70°F, Clear",
                "parking": "Free in Gersten Lot",
                "food_trucks": ["Burger Truck", "Taco Truck"],
                "spirit_theme": "Senior Night"
            }
        ]
    
    def _load_enhanced_tailgates(self):
        """Load enhanced tailgate events with 3D styling"""
        return [
            {
                "id": "tg_001",
                "name": "🦁 Lions Den Tailgate",
                "host": "Alpha Phi Omega",
                "date": "2024-02-15",
                "time": "16:00-18:30",
                "location": "Gersten Pavilion Parking Lot",
                "theme": "Red Sea Night",
                "features": ["BBQ", "Live Music", "Face Painting", "Spirit Contests", "Photo Booth", "DJ"],
                "spirit_points": 25,
                "max_capacity": 200,
                "rsvp_count": 45,
                "qr_code": "TG001_QR",
                "food": ["Hot Dogs", "Burgers", "Veggie Options", "Snacks"],
                "drinks": ["Soda", "Water", "Energy Drinks"],
                "activities": ["Cornhole", "Ladder Golf", "Spirit Photo Contest"],
                "music": "Live DJ + Student Performances",
                "decorations": "Red & White Balloons, LMU Banners",
                "special_guests": ["LMU Cheerleaders", "Mascot"],
                "social_media": "@lmu_aphi_omega #LMUTailgate"
            },
            {
                "id": "tg_002",
                "name": "🏠 Greek Row Tailgate",
                "host": "Interfraternity Council",
                "date": "2024-03-02", 
                "time": "12:00-14:00",
                "location": "Greek Row",
                "theme": "Lions Pride",
                "features": ["Greek Food", "Live Band", "Spirit Games", "Raffle"],
                "spirit_points": 30,
                "max_capacity": 300,
                "rsvp_count": 78,
                "qr_code": "TG002_QR",
                "food": ["Greek Food", "BBQ", "Desserts"],
                "drinks": ["Soda", "Water", "Greek Punch"],
                "activities": ["Tug of War", "Spirit Relay", "Greek Olympics"],
                "music": "Live Band + Greek Songs",
                "decorations": "Greek Letters, LMU Colors",
                "special_guests": ["Greek Alumni", "Athletic Director"],
                "social_media": "@lmu_greek_life #LMUGreekTailgate"
            },
            {
                "id": "tg_003",
                "name": "🎓 Senior Night Tailgate",
                "host": "Senior Class Council",
                "date": "2024-03-09",
                "time": "17:00-19:00",
                "location": "Gersten Pavilion Parking Lot",
                "theme": "Senior Night",
                "features": ["Senior Recognition", "Memory Wall", "Photo Booth", "Live Music"],
                "spirit_points": 40,
                "max_capacity": 150,
                "rsvp_count": 23,
                "qr_code": "TG003_QR",
                "food": ["Catered Dinner", "Desserts", "Coffee"],
                "drinks": ["Mocktails", "Coffee", "Water"],
                "activities": ["Senior Photos", "Memory Sharing", "Future Plans"],
                "music": "Live Acoustic + Senior Playlist",
                "decorations": "Graduation Caps, Memory Photos",
                "special_guests": ["President", "Faculty", "Alumni"],
                "social_media": "@lmu_seniors #LMUSeniorNight"
            }
        ]
    
    def _load_enhanced_watch_parties(self):
        """Load enhanced watch party events"""
        return [
            {
                "id": "wp_001",
                "name": "🏀 Away Game Watch Party",
                "host": "LMU Athletics",
                "date": "2024-02-22",
                "time": "19:30-22:00",
                "location": "The Grove",
                "opponent": "Gonzaga",
                "features": ["Big Screen TV", "Free Food", "Spirit Contests", "Raffle"],
                "spirit_points": 20,
                "max_capacity": 100,
                "rsvp_count": 34,
                "qr_code": "WP001_QR",
                "food": ["Pizza", "Wings", "Snacks"],
                "drinks": ["Soda", "Water", "Energy Drinks"],
                "activities": ["Spirit Chants", "Photo Contest", "Predictions"],
                "decorations": "LMU Banners, Team Colors",
                "special_guests": ["Athletic Staff", "Former Players"],
                "social_media": "@lmu_athletics #LMUWatchParty"
            },
            {
                "id": "wp_002",
                "name": "🏈 Football Watch Party",
                "host": "LMU Spirit Squad",
                "date": "2024-03-02",
                "time": "13:30-16:00",
                "location": "Student Union",
                "opponent": "San Diego",
                "features": ["Multiple Screens", "Spirit Squad Performance", "Games"],
                "spirit_points": 25,
                "max_capacity": 150,
                "rsvp_count": 67,
                "qr_code": "WP002_QR",
                "food": ["Hot Dogs", "Nachos", "Popcorn"],
                "drinks": ["Soda", "Water", "Sports Drinks"],
                "activities": ["Spirit Squad Demo", "Cheer Contest", "Trivia"],
                "decorations": "Spirit Squad Banners, Team Gear",
                "special_guests": ["Spirit Squad", "Cheerleaders"],
                "social_media": "@lmu_spirit_squad #LMUSpiritWatch"
            }
        ]
    
    def _load_enhanced_spirit_challenges(self):
        """Load enhanced spirit challenges with 3D styling"""
        return [
            {
                "id": "sc_001",
                "title": "🎨 Face Paint Masterpiece",
                "description": "Show off your LMU spirit with the most creative face paint!",
                "points": 10,
                "type": "photo",
                "deadline": "2024-02-15 18:00",
                "status": "active",
                "submissions": 23,
                "hashtag": "#LMUFacePaint",
                "prize": "LMU Merch Pack",
                "instructions": "Paint your face with LMU colors and post on social media",
                "judging_criteria": ["Creativity", "School Spirit", "Originality"],
                "example_submissions": ["red_white_face.jpg", "lion_face.jpg"]
            },
            {
                "id": "sc_002",
                "title": "📢 Spirit Chant Champion",
                "description": "Record yourself leading the best LMU chant",
                "points": 15,
                "type": "video",
                "deadline": "2024-02-15 19:00",
                "status": "active",
                "submissions": 12,
                "hashtag": "#LMUChant",
                "prize": "VIP Game Access",
                "instructions": "Record a 30-second LMU spirit chant",
                "judging_criteria": ["Enthusiasm", "Originality", "Crowd Response"],
                "example_submissions": ["chant_video1.mp4", "chant_video2.mp4"]
            },
            {
                "id": "sc_003",
                "title": "👗 Game Day Fashionista",
                "description": "Show off your most creative LMU game day fit",
                "points": 20,
                "type": "photo",
                "deadline": "2024-02-15 20:00",
                "status": "active",
                "submissions": 45,
                "hashtag": "#LMUFashion",
                "prize": "LMU Store Gift Card",
                "instructions": "Wear your best LMU-themed outfit and take a photo",
                "judging_criteria": ["Style", "School Spirit", "Creativity"],
                "example_submissions": ["outfit1.jpg", "outfit2.jpg"]
            },
            {
                "id": "sc_004",
                "title": "📸 Social Media Takeover",
                "description": "Post about your LMU spirit on social media",
                "points": 5,
                "type": "social",
                "deadline": "2024-02-15 21:00",
                "status": "active",
                "submissions": 89,
                "hashtag": "#LMUSpirit",
                "prize": "Social Media Recognition",
                "instructions": "Post LMU spirit content on any social platform",
                "judging_criteria": ["Engagement", "Creativity", "School Spirit"],
                "example_submissions": ["tweet1.txt", "insta_post1.txt"]
            }
        ]
    
    def _load_enhanced_premium_prizes(self):
        """Load enhanced premium prizes with 3D styling"""
        return [
            {
                "id": "pp_001",
                "title": "👑 Day as LMU President",
                "description": "Shadow the president, attend meetings, take over LMU socials for a day",
                "points_required": 1000,
                "category": "experience",
                "availability": 1,
                "claimed": 0,
                "image": "president_badge.png",
                "details": "Full day shadowing experience with LMU President",
                "requirements": ["Senior standing", "3.5+ GPA", "Active involvement"],
                "value": "$500+",
                "expiry": "2024-05-01"
            },
            {
                "id": "pp_002",
                "title": "🎤 Voice of the Lions",
                "description": "Announce one quarter of a basketball game",
                "points_required": 750,
                "category": "experience",
                "availability": 2,
                "claimed": 0,
                "image": "announcer_badge.png",
                "details": "Professional announcing experience at Gersten Pavilion",
                "requirements": ["Public speaking experience", "Game day availability"],
                "value": "$300+",
                "expiry": "2024-04-15"
            },
            {
                "id": "pp_003",
                "title": "🏀 VIP Game Access",
                "description": "Courtside seats + pre-game meet & greet",
                "points_required": 500,
                "category": "access",
                "availability": 5,
                "claimed": 1,
                "image": "vip_badge.png",
                "details": "Best seats in the house + player interaction",
                "requirements": ["Game day availability", "Spirit points earned"],
                "value": "$200+",
                "expiry": "2024-03-30"
            },
            {
                "id": "pp_004",
                "title": "🎁 LMU Merch Pack",
                "description": "Exclusive LMU merchandise collection",
                "points_required": 200,
                "category": "merchandise",
                "availability": 20,
                "claimed": 8,
                "image": "merch_badge.png",
                "details": "Limited edition LMU gear and accessories",
                "requirements": ["Active participation"],
                "value": "$100+",
                "expiry": "2024-06-01"
            },
            {
                "id": "pp_005",
                "title": "🍕 Free Meal Plan Week",
                "description": "One week of free dining hall access",
                "points_required": 300,
                "category": "dining",
                "availability": 10,
                "claimed": 3,
                "image": "meal_badge.png",
                "details": "Full access to all campus dining locations",
                "requirements": ["Meal plan holder"],
                "value": "$150+",
                "expiry": "2024-05-15"
            }
        ]
    
    def _load_rso_events(self):
        """Load RSO events and activities"""
        return [
            {
                "id": "rso_001",
                "name": "🎭 LMU Theatre Production",
                "organization": "LMU Theatre Arts",
                "date": "2024-02-20",
                "time": "19:30",
                "location": "Burns Fine Arts Center",
                "type": "performance",
                "points": 15,
                "description": "Spring musical production",
                "tickets": "$10 students, $20 general"
            },
            {
                "id": "rso_002",
                "name": "🎵 A Cappella Concert",
                "organization": "LMU A Cappella Groups",
                "date": "2024-02-25",
                "time": "20:00",
                "location": "St. Robert's Auditorium",
                "type": "concert",
                "points": 10,
                "description": "Annual spring concert featuring all groups",
                "tickets": "Free for students"
            },
            {
                "id": "rso_003",
                "name": "🏃‍♀️ LMU 5K Run",
                "organization": "LMU Running Club",
                "date": "2024-03-10",
                "time": "08:00",
                "location": "Campus Loop",
                "type": "athletic",
                "points": 25,
                "description": "Annual campus 5K fundraiser",
                "registration": "$15 students, $25 general"
            }
        ]
    
    def _load_leaderboard_data(self):
        """Load leaderboard data with realistic student names"""
        return [
            {"rank": 1, "name": "Sarah Chen", "points": 1250, "badges": 8, "events_attended": 15, "organization": "Alpha Phi Omega"},
            {"rank": 2, "name": "Marcus Rodriguez", "points": 1180, "badges": 7, "events_attended": 14, "organization": "LMU Spirit Squad"},
            {"rank": 3, "name": "Emma Thompson", "points": 1120, "badges": 6, "events_attended": 13, "organization": "Cheerleading"},
            {"rank": 4, "name": "Jordan Kim", "points": 1050, "badges": 5, "events_attended": 12, "organization": "Basketball Team"},
            {"rank": 5, "name": "Alex Johnson", "points": 980, "badges": 4, "events_attended": 11, "organization": "Greek Life"},
            {"rank": 6, "name": "Maya Patel", "points": 920, "badges": 4, "events_attended": 10, "organization": "Student Government"},
            {"rank": 7, "name": "Chris Davis", "points": 890, "badges": 3, "events_attended": 9, "organization": "Band"},
            {"rank": 8, "name": "Zoe Williams", "points": 850, "badges": 3, "events_attended": 8, "organization": "Theatre Arts"},
            {"rank": 9, "name": "Ryan O'Connor", "points": 820, "badges": 3, "events_attended": 8, "organization": "Soccer Team"},
            {"rank": 10, "name": "Sophia Lee", "points": 790, "badges": 2, "events_attended": 7, "organization": "Dance Team"}
        ]
    
    def _load_genz_personality(self):
        """Load Gen Z chatbot personality responses"""
        return {
            "greetings": [
                "Hey bestie! 👋 What's the tea on campus today?",
                "Yasss, welcome to the LMU fam! 🦁✨",
                "Slay! Ready to help you navigate LMU life! 💅",
                "Hey there! Let's make your LMU experience absolutely iconic! 🔥",
                "What's good, fellow Lion? Ready to level up your campus game? 🚀"
            ],
            "enthusiasm": [
                "Periodt! 💯",
                "That's the spirit! 🔥",
                "Yasss queen/king! 👑",
                "Absolutely iconic! ✨",
                "We love to see it! 💖"
            ],
            "helpful": [
                "Bestie, I got you! 💁‍♀️",
                "Let me spill the tea on that! ☕",
                "Here's the 411 you need! 📱",
                "I'm literally obsessed with helping you! 😍",
                "This is your sign to slay! 💅"
            ],
            "campus_slang": {
                "gersten": "Gersten Pavilion - where the magic happens! 🏀✨",
                "the_grove": "The Grove - your go-to spot for everything! 🌳",
                "greek_row": "Greek Row - where the party's at! 🏠",
                "sullivan": "Sullivan Field - football vibes! 🏈",
                "mccarthy": "McCarthy Athletic Center - away game energy! 🏀"
            }
        }
    
    def get_genz_response(self, response_type="helpful"):
        """Get a random Gen Z response"""
        responses = self.genz_responses.get(response_type, self.genz_responses["helpful"])
        if isinstance(responses, list):
            return random.choice(responses)
        return random.choice(self.genz_responses["helpful"])
    
    def process_message(self, message, history, user_id=None):
        """Process user message with Gen Z personality"""
        try:
            # Add points for asking a question
            if user_id:
                self.points_system.add_points(user_id, 1, "question_asked")
            
            # Get context from RAG system
            context = self.rag_system.get_relevant_context(message)
            
            # Add Gen Z flair to responses
            genz_greeting = self.get_genz_response("greetings")
            
            # Enhanced response logic with LMU-specific knowledge
            if "tutoring" in message.lower():
                response = f"{genz_greeting} Bestie, LMU has amazing tutoring at the Academic Resource Center in Daum Hall! 📚✨ You can also find subject-specific tutors in the library. The ARC is literally a lifesaver! 💁‍♀️"
            elif "food" in message.lower() or "dining" in message.lower():
                response = f"Yasss! The Grove has the best food options, and there's always something slaying at the dining halls! 🍕✨ Pro tip: The food trucks on game days are absolutely iconic! 🔥"
            elif "parking" in message.lower():
                response = f"Parking at LMU can be a whole mood, but here's the tea: Gersten lot is free for games, and there's always street parking on LMU Drive! 🚗💅"
            elif "events" in message.lower() or "what's happening" in message.lower():
                response = f"Periodt! We have so many iconic events coming up! Check out the calendar for tailgates, watch parties, and RSO events. The LMU vs Pepperdine game is literally going to be everything! 🦁✨"
            elif "spirit" in message.lower() or "points" in message.lower():
                response = f"Yasss! Earn spirit points by attending games, tailgates, and challenges! The more you participate, the more you can redeem for exclusive LMU experiences! 💯🔥"
            elif "gersten" in message.lower():
                response = f"{genz_greeting} Gersten Pavilion is where all the basketball magic happens! 🏀✨ It's literally the heart of LMU athletics. The energy there during games is absolutely everything! 🔥"
            elif "greek" in message.lower() or "frat" in message.lower() or "sorority" in message.lower():
                response = f"Greek life at LMU is so much fun! 🏠✨ There are amazing fraternities and sororities with tons of events. Check out Greek Row for the best parties and community vibes! 💖"
            else:
                # Use original LLM response but add Gen Z flair
                original_response = self.llm_handler.generate_response(message, context, history)
                response = f"{genz_greeting} {original_response} Let's make your LMU experience absolutely legendary! 🦁💖"
            
            # Log the interaction
            log_interaction(message, response, user_id)
            
            # Update conversation history
            self.conversation_history.append({
                "user": message,
                "assistant": response,
                "timestamp": datetime.now().isoformat()
            })
            
            return response
            
        except Exception as e:
            error_msg = f"Omg bestie, something went wrong! 😅 But don't worry, I'm here to help with everything LMU! 🦁✨"
            print(f"Error in process_message: {e}")
            return error_msg
    
    def get_user_points(self, user_id):
        """Get user points with enhanced display"""
        if not user_id:
            return """
            <div class="points-display-3d">
                <h3>🏆 Your Spirit Points</h3>
                <p>Enter your student ID above ☝️ to track your spirit journey!</p>
                <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.2); margin: 12px 0;">
                <p style="font-weight: 600; margin-bottom: 8px;">💡 Earn Spirit Points by:</p>
                <ul style="text-align: left; margin: 0; padding-left: 20px;">
                    <li>Asking questions (1 pt)</li>
                    <li>Attending tailgates (25-30 pts)</li>
                    <li>Going to games (50-75 pts)</li>
                    <li>Watch parties (20 pts)</li>
                    <li>Spirit challenges (50-100 pts)</li>
                    <li>Bringing friends (bonus pts)</li>
                </ul>
            </div>
            """
        
        try:
            stats = self.points_system.get_user_stats(user_id)
            rank_info = self.points_system.get_user_rank(user_id)
            
            # Parse the stats string to extract points
            points = 0
            if "Total Points:" in stats:
                points_str = stats.split("Total Points:")[1].split()[0]
                points = int(points_str)
            
            # Calculate level and progress
            level = (points // 100) + 1
            next_level = level * 100
            progress = points % 100
            
            return f"""
            <div class="points-display-3d">
                <h3>🏆 Your Spirit Points</h3>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0; color: #FFD700;">{points} pts</p>
                <p style="font-size: 0.9rem; opacity: 0.8;">Rank #{rank_info.get('rank', 'N/A')} of {rank_info.get('total_users', 0)} students</p>
                <p style="font-size: 1rem; color: #4ECDC4;">Level {level} • {progress}/{100} to next level</p>
                <div class="progress-bar-3d">
                    <div class="progress-fill-3d" style="width: {progress}%"></div>
                </div>
                <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.2); margin: 12px 0;">
                <p style="font-weight: 600; margin-bottom: 8px;">💡 Earn Spirit Points by:</p>
                <ul style="text-align: left; margin: 0; padding-left: 20px;">
                    <li>Asking questions (1 pt)</li>
                    <li>Attending tailgates (25-30 pts)</li>
                    <li>Going to games (50-75 pts)</li>
                    <li>Watch parties (20 pts)</li>
                    <li>Spirit challenges (50-100 pts)</li>
                    <li>Bringing friends (bonus pts)</li>
                </ul>
            </div>
            """
        except Exception as e:
            return f"Error loading points: {str(e)}"

    def get_3d_css(self):
        """Get enhanced 3D CSS styling"""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;500;600;700&family=Audiowide&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Rajdhani', sans-serif;
            background: linear-gradient(135deg, #0A0A0A 0%, #1a1a2e 50%, #16213e 100%);
            color: #ffffff;
            overflow-x: hidden;
        }
        
        .main-container {
            min-height: 100vh;
            background: radial-gradient(circle at 50% 50%, rgba(255, 107, 107, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 20% 80%, rgba(78, 205, 196, 0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(69, 183, 209, 0.1) 0%, transparent 50%);
        }
        
        .header-3d {
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.9) 0%, rgba(78, 205, 196, 0.9) 100%);
            backdrop-filter: blur(20px);
            border-bottom: 2px solid rgba(255, 255, 255, 0.2);
            padding: 20px 0;
            position: relative;
            overflow: hidden;
        }
        
        .header-3d::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }
        
        .header-content {
            position: relative;
            z-index: 2;
            text-align: center;
        }
        
        .main-title {
            font-family: 'Orbitron', monospace;
            font-size: 3.5rem;
            font-weight: 900;
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #FF69B4);
            background-size: 400% 400%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            animation: gradientShift 3s ease-in-out infinite;
            text-shadow: 0 0 30px rgba(255, 107, 107, 0.5);
            margin-bottom: 10px;
        }
        
        @keyframes gradientShift {
            0%, 100% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
        }
        
        .subtitle {
            font-family: 'Rajdhani', sans-serif;
            font-size: 1.2rem;
            color: rgba(255, 255, 255, 0.8);
            font-weight: 300;
            letter-spacing: 2px;
        }
        
        .card-3d {
            background: rgba(255, 255, 255, 0.1);
            backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 20px;
            padding: 25px;
            margin: 20px 0;
            transform: perspective(1000px) rotateX(5deg);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }
        
        .card-3d::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .card-3d:hover::before {
            left: 100%;
        }
        
        .card-3d:hover {
            transform: perspective(1000px) rotateX(0deg) translateY(-10px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
        }
        
        .card-title {
            font-family: 'Orbitron', monospace;
            font-size: 1.5rem;
            font-weight: 700;
            color: #4ECDC4;
            margin-bottom: 15px;
            text-shadow: 0 0 10px rgba(78, 205, 196, 0.5);
        }
        
        .neon-button {
            background: linear-gradient(45deg, #FF6B6B, #FF69B4);
            border: none;
            border-radius: 25px;
            padding: 12px 25px;
            color: white;
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .neon-button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.3), transparent);
            transition: left 0.5s;
        }
        
        .neon-button:hover::before {
            left: 100%;
        }
        
        .neon-button:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(255, 107, 107, 0.4);
        }
        
        .calendar-3d {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .calendar-header {
            font-family: 'Orbitron', monospace;
            font-size: 1.3rem;
            color: #4ECDC4;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .event-item {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #FF6B6B;
            transition: all 0.3s ease;
        }
        
        .event-item:hover {
            transform: translateX(10px);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .leaderboard-3d {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 20px;
            margin: 20px 0;
        }
        
        .leaderboard-item {
            display: flex;
            align-items: center;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            transition: all 0.3s ease;
        }
        
        .leaderboard-item:hover {
            transform: scale(1.02);
            background: rgba(255, 255, 255, 0.15);
        }
        
        .rank-badge {
            background: linear-gradient(45deg, #FF6B6B, #FF69B4);
            color: white;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            margin-right: 15px;
        }
        
        .points-display-3d {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 20px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 12px 40px rgba(102, 126, 234, 0.3);
            border: none;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1);
            transform: perspective(1000px) rotateX(5deg);
            transition: all 0.3s ease;
        }
        
        .points-display-3d:hover {
            transform: perspective(1000px) rotateX(0deg) translateY(-5px);
        }
        
        .progress-bar-3d {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 10px;
            height: 20px;
            overflow: hidden;
            margin: 10px 0;
        }
        
        .progress-fill-3d {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4);
            height: 100%;
            border-radius: 10px;
            transition: width 0.3s ease;
        }
        
        .prize-card {
            background: linear-gradient(135deg, rgba(255, 107, 107, 0.2) 0%, rgba(78, 205, 196, 0.2) 100%);
            border-radius: 20px;
            padding: 20px;
            margin: 15px 0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            transition: all 0.3s ease;
        }
        
        .prize-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        }
        
        .prize-title {
            font-family: 'Orbitron', monospace;
            font-size: 1.3rem;
            color: #FF69B4;
            margin-bottom: 10px;
        }
        
        .prize-points {
            font-family: 'Rajdhani', sans-serif;
            font-weight: 600;
            color: #4ECDC4;
            font-size: 1.1rem;
        }
        
        .chat-container {
            background: rgba(255, 255, 255, 0.05);
            border-radius: 20px;
            padding: 20px;
            margin: 20px 0;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        
        .chat-message {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            border-left: 4px solid #4ECDC4;
        }
        
        .user-message {
            background: rgba(255, 107, 107, 0.2);
            border-left-color: #FF6B6B;
        }
        
        .qr-code-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            margin: 20px 0;
        }
        
        .notification {
            background: linear-gradient(45deg, #FF6B6B, #FF69B4);
            color: white;
            border-radius: 15px;
            padding: 15px;
            margin: 10px 0;
            animation: slideIn 0.5s ease;
        }
        
        @keyframes slideIn {
            from { transform: translateX(-100%); opacity: 0; }
            to { transform: translateX(0); opacity: 1; }
        }
        
        .floating-elements {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            z-index: -1;
        }
        
        .floating-element {
            position: absolute;
            opacity: 0.1;
            animation: float 6s ease-in-out infinite;
        }
        
        @keyframes float {
            0%, 100% { transform: translateY(0px) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }
        
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .stat-card {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }
        
        .stat-number {
            font-family: 'Orbitron', monospace;
            font-size: 2rem;
            color: #4ECDC4;
            margin-bottom: 5px;
        }
        
        .stat-label {
            font-family: 'Rajdhani', sans-serif;
            color: rgba(255, 255, 255, 0.8);
            font-size: 0.9rem;
        }
        
        .badge-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(80px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        
        .badge-item {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            transition: all 0.3s ease;
        }
        
        .badge-item:hover {
            transform: scale(1.1);
            background: rgba(255, 255, 255, 0.2);
        }
        
        .badge-icon {
            font-size: 2rem;
            margin-bottom: 5px;
        }
        """
    
    def get_game_day_dashboard(self):
        """Get enhanced game day dashboard with 3D styling"""
        next_game = self.game_events[0]  # LMU vs Pepperdine
        
        return f"""
        <div class="card-3d">
            <div class="card-title">🏀 Game Day Dashboard</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{next_game['current_attendance']}</div>
                    <div class="stat-label">Attending</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{next_game['capacity']}</div>
                    <div class="stat-label">Capacity</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{next_game['spirit_points']}</div>
                    <div class="stat-label">Points Available</div>
                </div>
            </div>
            
            <div class="event-item">
                <h4>🏀 {next_game['sport']} - LMU vs {next_game['opponent']}</h4>
                <p>📍 {next_game['venue']} | ⏰ {next_game['date']} at {next_game['time']}</p>
                <p>🎫 {next_game['ticket_price']} | 🌤️ {next_game['weather']}</p>
                <p>🚗 {next_game['parking']} | 🍕 {', '.join(next_game['food_trucks'])}</p>
                <p>🎨 Theme: {next_game['spirit_theme']} | 📱 {next_game['hashtag']}</p>
                <button class="neon-button">🎫 Get Tickets</button>
                <button class="neon-button">📱 Share</button>
            </div>
        </div>
        """
    
    def get_enhanced_calendar(self):
        """Get enhanced interactive calendar"""
        all_events = []
        
        # Add game events
        for event in self.game_events:
            all_events.append({
                "date": event["date"],
                "title": f"{event['sport']} vs {event['opponent']}",
                "type": "game",
                "venue": event["venue"],
                "time": event["time"],
                "points": event["spirit_points"]
            })
        
        # Add tailgates
        for tailgate in self.tailgates:
            all_events.append({
                "date": tailgate["date"],
                "title": tailgate["name"],
                "type": "tailgate",
                "venue": tailgate["location"],
                "time": tailgate["time"],
                "points": tailgate["spirit_points"]
            })
        
        # Add RSO events
        for rso_event in self.rso_events:
            all_events.append({
                "date": rso_event["date"],
                "title": rso_event["name"],
                "type": "rso",
                "venue": rso_event["location"],
                "time": rso_event["time"],
                "points": rso_event["points"]
            })
        
        # Sort by date
        all_events.sort(key=lambda x: x["date"])
        
        calendar_html = """
        <div class="calendar-3d">
            <div class="calendar-header">📅 Interactive Event Calendar</div>
        """
        
        current_month = None
        for event in all_events:
            event_date = datetime.strptime(event["date"], "%Y-%m-%d")
            month = event_date.strftime("%B %Y")
            
            if month != current_month:
                if current_month:
                    calendar_html += "</div>"
                calendar_html += f'<div class="month-section"><h3>{month}</h3>'
                current_month = month
            
            event_type_icon = {"game": "🏀", "tailgate": "🎉", "rso": "🎭"}.get(event["type"], "📅")
            
            calendar_html += f"""
            <div class="event-item">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <h4>{event_type_icon} {event["title"]}</h4>
                        <p>📍 {event["venue"]} | ⏰ {event["time"]}</p>
                        <p>🎯 {event["points"]} Spirit Points</p>
                    </div>
                    <div>
                        <button class="neon-button">RSVP</button>
                        <button class="neon-button">📅</button>
                    </div>
                </div>
            </div>
            """
        
        calendar_html += "</div></div>"
        return calendar_html
    
    def get_enhanced_leaderboard(self):
        """Get enhanced leaderboard with 3D styling"""
        leaderboard_html = """
        <div class="leaderboard-3d">
            <div class="card-title">🏆 Live Leaderboard</div>
        """
        
        for i, player in enumerate(self.leaderboard_data):
            rank_class = "rank-badge"
            if i == 0:
                rank_class += " gold"
            elif i == 1:
                rank_class += " silver"
            elif i == 2:
                rank_class += " bronze"
            
            leaderboard_html += f"""
            <div class="leaderboard-item">
                <div class="{rank_class}">{player['rank']}</div>
                <div style="flex: 1;">
                    <h4>{player['name']}</h4>
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">{player['organization']}</p>
                </div>
                <div style="text-align: right;">
                    <div class="stat-number">{player['points']} pts</div>
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                        🏅 {player['badges']} badges | 📅 {player['events_attended']} events
                    </p>
                </div>
            </div>
            """
        
        leaderboard_html += "</div>"
        return leaderboard_html
    
    def get_enhanced_prizes(self):
        """Get enhanced prizes section"""
        prizes_html = """
        <div class="card-3d">
            <div class="card-title">🎁 Premium Prizes</div>
            <p style="color: rgba(255,255,255,0.8); margin-bottom: 20px;">
                Redeem your spirit points for exclusive LMU experiences and merch!
            </p>
        """
        
        for prize in self.premium_prizes:
            availability = prize['availability'] - prize['claimed']
            status_class = "available" if availability > 0 else "claimed"
            
            prizes_html += f"""
            <div class="prize-card">
                <div class="prize-title">{prize['title']}</div>
                <p style="color: rgba(255,255,255,0.8); margin: 10px 0;">{prize['description']}</p>
                <div class="prize-points">🎯 {prize['points_required']} Points Required</div>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 5px 0;">
                    💰 Value: {prize['value']} | 📅 Expires: {prize['expiry']}
                </p>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; margin: 5px 0;">
                    📦 Available: {availability}/{prize['availability']}
                </p>
                <button class="neon-button" {'disabled' if availability <= 0 else ''}>
                    {'Redeem' if availability > 0 else 'Claimed'}
                </button>
            </div>
            """
        
        prizes_html += "</div>"
        return prizes_html
    
    def get_enhanced_spirit_challenges(self):
        """Get enhanced spirit challenges"""
        challenges_html = """
        <div class="card-3d">
            <div class="card-title">🔥 Spirit Challenges</div>
            <p style="color: rgba(255,255,255,0.8); margin-bottom: 20px;">
                Complete challenges to earn bonus spirit points and exclusive rewards!
            </p>
        """
        
        for challenge in self.spirit_challenges:
            challenges_html += f"""
            <div class="event-item">
                <h4>{challenge['title']}</h4>
                <p>{challenge['description']}</p>
                <p>🎯 {challenge['points']} Points | 📅 Deadline: {challenge['deadline']}</p>
                <p>🏆 Prize: {challenge['prize']} | 📱 {challenge['hashtag']}</p>
                <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem;">
                    📸 {challenge['submissions']} submissions so far
                </p>
                <button class="neon-button">Submit Entry</button>
            </div>
            """
        
        challenges_html += "</div>"
        return challenges_html
    
    def get_user_profile(self, user_id):
        """Get enhanced user profile"""
        user_points = self.get_user_points(user_id)
        
        return f"""
        <div class="card-3d">
            <div class="card-title">👤 Your Profile</div>
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">450</div>
                    <div class="stat-label">Total Points</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">5</div>
                    <div class="stat-label">Level</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">6</div>
                    <div class="stat-label">Badges</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">3</div>
                    <div class="stat-label">Day Streak</div>
                </div>
            </div>
            
            <div style="margin: 20px 0;">
                <h4>Progress to Next Level</h4>
                <div class="progress-bar-3d">
                    <div class="progress-fill-3d" style="width: 50%"></div>
                </div>
                <p style="text-align: center; margin-top: 10px;">
                    50/100 points to level 6
                </p>
            </div>
            
            <div class="badge-grid">
                <div class="badge-item">
                    <div class="badge-icon">🏀</div>
                    <div>Game Day</div>
                </div>
                <div class="badge-item">
                    <div class="badge-icon">🎉</div>
                    <div>Tailgate</div>
                </div>
                <div class="badge-item">
                    <div class="badge-icon">📸</div>
                    <div>Social</div>
                </div>
                <div class="badge-item">
                    <div class="badge-icon">🔥</div>
                    <div>Spirit</div>
                </div>
            </div>
        </div>
        """
    
    def generate_qr_code(self, event_id, event_type):
        """Generate QR code for event check-in"""
        qr_data = f"LMU_SPIRIT_{event_type.upper()}_{event_id}_{datetime.now().strftime('%Y%m%d')}"
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Convert to base64
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return f"""
        <div class="qr-code-container">
            <h4>📱 Event Check-in QR Code</h4>
            <img src="data:image/png;base64,{img_str}" alt="QR Code" style="max-width: 200px;">
            <p style="margin-top: 10px; font-size: 0.9rem; color: #666;">
                Scan this QR code at the event to check in and earn points!
            </p>
        </div>
        """
    
    def create_enhanced_interface(self):
        """Create the enhanced 3D interface"""
        css = self.get_3d_css()
        
        with gr.Blocks(css=css, title="LMU Campus LLM 3D") as interface:
            # Header
            with gr.Row():
                gr.HTML("""
                <div class="header-3d">
                    <div class="header-content">
                        <div class="main-title">🦁 LMU Campus LLM 3D</div>
                        <div class="subtitle">Your Ultimate School Spirit Platform</div>
                    </div>
                </div>
                """)
            
            # Main content tabs
            with gr.Tabs():
                # Dashboard Tab
                with gr.Tab("🏠 Dashboard"):
                    with gr.Row():
                        gr.HTML(self.get_game_day_dashboard())
                    
                    with gr.Row():
                        gr.HTML(self.get_user_profile("user_123"))
                
                # Calendar Tab
                with gr.Tab("📅 Events"):
                    gr.HTML(self.get_enhanced_calendar())
                
                # Leaderboard Tab
                with gr.Tab("🏆 Leaderboard"):
                    gr.HTML(self.get_enhanced_leaderboard())
                
                # Prizes Tab
                with gr.Tab("🎁 Prizes"):
                    gr.HTML(self.get_enhanced_prizes())
                
                # Challenges Tab
                with gr.Tab("🔥 Challenges"):
                    gr.HTML(self.get_enhanced_spirit_challenges())
                
                # Chat Tab
                with gr.Tab("💬 Chat"):
                    with gr.Row():
                        with gr.Column(scale=3):
                            chatbot = gr.Chatbot(
                                label="Chat with LMU Assistant",
                                height=400,
                                show_label=True
                            )
                        with gr.Column(scale=1):
                            gr.HTML("""
                            <div class="chat-container">
                                <h4>💡 Quick Tips</h4>
                                <p>• Ask about campus events</p>
                                <p>• Get dining recommendations</p>
                                <p>• Find tutoring resources</p>
                                <p>• Learn about RSOs</p>
                                <p>• Check game schedules</p>
                            </div>
                            """)
                    
                    with gr.Row():
                        msg = gr.Textbox(
                            label="Message",
                            placeholder="Ask me anything about LMU! (e.g., 'where can i find tutoring?')",
                            lines=2
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
                    gr.HTML(self.generate_qr_code("bb_001", "game"))
                
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
                            <div class="card-3d">
                                <h4>💡 Recent Suggestions</h4>
                                <div class="event-item">
                                    <p style="font-size: 0.9rem; margin: 5px 0;">🏈 LMU Spirit Squad Tailgate</p>
                                    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Suggested by @lmu_lion</p>
                                </div>
                                <div class="event-item">
                                    <p style="font-size: 0.9rem; margin: 5px 0;">🎵 Spring Concert Series</p>
                                    <p style="font-size: 0.8rem; color: rgba(255,255,255,0.7);">Suggested by @music_lover</p>
                                </div>
                            </div>
                            """)
            
            # Footer
            with gr.Row():
                gr.HTML("""
                <div style="text-align: center; padding: 20px; color: rgba(255,255,255,0.7);">
                    <p>🦁 LMU Campus LLM 3D - Making School Spirit Iconic Since 2024</p>
                    <p>Built with 💖 for the LMU Community</p>
                </div>
                """)
        
        return interface

def main():
    """Main function to run the enhanced LMU app"""
    app = EnhancedLMUApp()
    interface = app.create_enhanced_interface()
    
    print("🦁 Starting Enhanced LMU Campus LLM 3D...")
    print("✨ Features: 3D Design, Gen Z Chatbot, Interactive Calendar, Live Leaderboard")
    print("🎮 Game Day Engagement, Premium Prizes, Spirit Challenges")
    print("📱 QR Code Check-ins, User Profiles, Feedback System")
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        debug=True
    )

if __name__ == "__main__":
    main()
