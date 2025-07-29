#!/usr/bin/env python3
"""
LMU Campus LLM - Ultimate 3D School Spirit Platform
A next-generation student-centered AI assistant and gamified spirit engine for Loyola Marymount University

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

class EnhancedLMUApp:
    def __init__(self):
        """Initialize the Enhanced 3D LMU application"""
        self.config = self._load_config()
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
        
    def _load_config(self):
        """Load configuration with enhanced settings"""
        return {
            "app_name": "LMU Campus LLM 3D",
            "version": "2.0",
            "theme": "3d_neon",
            "primary_color": "#FF6B6B",
            "secondary_color": "#4ECDC4",
            "accent_color": "#45B7D1",
            "neon_pink": "#FF69B4",
            "neon_blue": "#00CED1",
            "neon_green": "#00FF7F",
            "dark_bg": "#0A0A0A",
            "glass_bg": "rgba(255, 255, 255, 0.1)",
            "font_family": "'Orbitron', 'Rajdhani', 'Audiowide', sans-serif"
        }
    
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
        else:
            response = f"{genz_greeting} I'm here to help with everything LMU! Ask me about events, campus resources, or how to get involved. Let's make your LMU experience absolutely legendary! 🦁💖"
        
        return response
    
    def get_user_points(self, user_id):
        """Get user points with enhanced display"""
        # Simulate user points
        base_points = 450
        bonus_points = random.randint(0, 100)
        total_points = base_points + bonus_points
        
        return {
            "total": total_points,
            "level": (total_points // 100) + 1,
            "next_level": ((total_points // 100) + 1) * 100,
            "progress": total_points % 100,
            "badges": random.randint(3, 8),
            "events_attended": random.randint(8, 15),
            "streak": random.randint(1, 7)
        }