#!/usr/bin/env python3
"""
LMU Campus LLM - Ultimate School Spirit Platform
A student-centered AI assistant and gamified spirit engine for Loyola Marymount University

Author: Vanessa Akaraiwe
Revamped with Game Day Spirit & Creative Prizes
"""

import gradio as gr
import json
import os
import qrcode
import io
import base64
from datetime import datetime, timedelta
from src.llm_handler import LLMHandler
from src.points_system import PointsSystem
from src.rag_system import RAGSystem
from src.utils import load_config, log_interaction

class CampusLLMApp:
    def __init__(self):
        """Initialize the Campus LLM application"""
        self.config = load_config()
        self.llm_handler = LLMHandler()
        self.points_system = PointsSystem()
        self.rag_system = RAGSystem()
        
        # Session state
        self.current_user = None
        self.conversation_history = []
        
        # Game Day & Spirit System
        self.game_events = self._load_game_events()
        self.tailgates = self._load_tailgates()
        self.watch_parties = self._load_watch_parties()
        self.spirit_challenges = self._load_spirit_challenges()
        self.premium_prizes = self._load_premium_prizes()
        
    def _load_game_events(self):
        """Load upcoming game events"""
        return [
            {
                "id": "bb_001",
                "sport": "Basketball",
                "opponent": "Pepperdine",
                "date": "2024-02-15",
                "time": "19:00",
                "venue": "Gersten Pavilion",
                "type": "home",
                "spirit_points": 50,
                "tailgate_id": "tg_001",
                "status": "upcoming",
                "countdown": "3 days"
            },
            {
                "id": "bb_002", 
                "sport": "Basketball",
                "opponent": "Gonzaga",
                "date": "2024-02-22",
                "time": "20:00",
                "venue": "McCarthy Athletic Center",
                "type": "away",
                "spirit_points": 30,
                "watch_party_id": "wp_001",
                "status": "upcoming",
                "countdown": "10 days"
            },
            {
                "id": "fb_001",
                "sport": "Football", 
                "opponent": "San Diego",
                "date": "2024-03-02",
                "time": "14:00",
                "venue": "Sullivan Field",
                "type": "home",
                "spirit_points": 75,
                "tailgate_id": "tg_002",
                "status": "upcoming",
                "countdown": "18 days"
            }
        ]
    
    def _load_tailgates(self):
        """Load tailgate events"""
        return [
            {
                "id": "tg_001",
                "name": "Lions Den Tailgate",
                "host": "Alpha Phi Omega",
                "date": "2024-02-15",
                "time": "16:00-18:30",
                "location": "Gersten Pavilion Parking Lot",
                "theme": "Red Sea Night",
                "features": ["BBQ", "Live Music", "Face Painting", "Spirit Contests"],
                "spirit_points": 25,
                "max_capacity": 200,
                "rsvp_count": 45,
                "qr_code": "TG001_QR",
                "status": "active"
            },
            {
                "id": "tg_002",
                "name": "Greek Row Tailgate",
                "host": "Interfraternity Council",
                "date": "2024-03-02", 
                "time": "12:00-14:00",
                "location": "Greek Row",
                "theme": "Blue & White Bash",
                "features": ["Food Trucks", "DJ", "Cornhole Tournament", "Photo Booth"],
                "spirit_points": 30,
                "max_capacity": 300,
                "rsvp_count": 78,
                "qr_code": "TG002_QR",
                "status": "active"
            }
        ]
    
    def _load_watch_parties(self):
        """Load watch party events"""
        return [
            {
                "id": "wp_001",
                "name": "Away Game Watch Party",
                "host": "Student Government",
                "date": "2024-02-22",
                "time": "19:30-22:00",
                "location": "The Grove",
                "game": "LMU vs Gonzaga",
                "features": ["Big Screen", "Free Pizza", "Spirit Contests", "Prizes"],
                "spirit_points": 20,
                "max_capacity": 150,
                "rsvp_count": 32,
                "status": "active"
            }
        ]
    
    def _load_spirit_challenges(self):
        """Load spirit challenges"""
        return [
            {
                "id": "sc_001",
                "name": "Spirit Captain Challenge",
                "description": "Lead the crowd in LMU chants during the game",
                "points": 50,
                "deadline": "2024-02-15",
                "participants": 12,
                "status": "active"
            },
            {
                "id": "sc_002",
                "name": "Best Tailgate Outfit",
                "description": "Show off your LMU spirit with the most creative outfit",
                "points": 30,
                "deadline": "2024-02-15",
                "participants": 28,
                "status": "active"
            },
            {
                "id": "sc_003",
                "name": "Social Media Takeover",
                "description": "Create the most viral LMU game day post",
                "points": 40,
                "deadline": "2024-02-16",
                "participants": 15,
                "status": "active"
            }
        ]
    
    def _load_premium_prizes(self):
        """Load premium prizes"""
        return [
            {
                "id": "pp_001",
                "name": "Day as LMU President",
                "description": "Shadow the president for a day, attend meetings, and take over LMU socials",
                "points_required": 5000,
                "category": "experience",
                "availability": 1,
                "status": "available",
                "image": "👔"
            },
            {
                "id": "pp_002",
                "name": "Voice of the Lions",
                "description": "Co-host a game broadcast and announce starting lineups",
                "points_required": 3000,
                "category": "experience",
                "availability": 2,
                "status": "available",
                "image": "🎤"
            },
            {
                "id": "pp_003",
                "name": "Coach for a Day",
                "description": "Join team practice, be on the sidelines, and help plan plays",
                "points_required": 2500,
                "category": "experience",
                "availability": 3,
                "status": "available",
                "image": "🏀"
            },
            {
                "id": "pp_004",
                "name": "Jumbotron Shout-out",
                "description": "Get featured with a personalized message at halftime",
                "points_required": 2000,
                "category": "experience",
                "availability": 5,
                "status": "available",
                "image": "📺"
            },
            {
                "id": "pp_005",
                "name": "VIP Game Access",
                "description": "Floor seats, meet players, and exclusive game day experience",
                "points_required": 800,
                "category": "access",
                "availability": 10,
                "status": "available",
                "image": "🎫"
            },
            {
                "id": "pp_006",
                "name": "Custom Spirit Trophy",
                "description": "Traveling trophy that lives with you for a month",
                "points_required": 600,
                "category": "trophy",
                "availability": 1,
                "status": "available",
                "image": "🏆"
            }
        ]

    def process_message(self, message, history, user_id=None):
        """Process user message and return AI response"""
        try:
            # Get response from LLM
            response = self.llm_handler.get_response(message, history)
            
            # Award points for asking questions
            if user_id:
                self.points_system.award_points(user_id, 1, "question_asked")
            
            # Log interaction
            log_interaction(user_id, message, response, "chat")
            
            return response
            
        except Exception as e:
            return f"I'm having trouble processing that right now. Please try again! (Error: {str(e)})"

    def get_user_points(self, user_id):
        """Get user's current points"""
        if not user_id:
            return "Enter your Student ID to see your points!"
        
        try:
            points = self.points_system.get_points(user_id)
            return f"🦁 **{points} Spirit Points**"
        except:
            return "Enter your Student ID to see your points!"

    def get_game_day_dashboard(self):
        """Get game day dashboard HTML"""
        html = """
        <div class="game-day-dashboard">
            <div class="dashboard-header">
                <h2>🏈 Game Day Dashboard</h2>
                <p>Get ready for the most epic game day experience at LMU!</p>
            </div>
            
            <div class="upcoming-games">
                <h3>🎮 Upcoming Games</h3>
        """
        
        for game in self.game_events:
            html += f"""
                <div class="game-card">
                    <div class="game-info">
                        <div class="game-sport">{game['sport']}</div>
                        <div class="game-matchup">LMU vs {game['opponent']}</div>
                        <div class="game-details">
                            <span>📅 {game['date']} at {game['time']}</span>
                            <span>📍 {game['venue']}</span>
                            <span>🎯 {game['spirit_points']} Spirit Points</span>
                        </div>
                        <div class="game-countdown">⏰ {game['countdown']}</div>
                    </div>
                    <div class="game-actions">
                        <button class="btn-primary">RSVP</button>
                        <button class="btn-secondary">View Details</button>
                    </div>
                </div>
            """
        
        html += """
            </div>
            
            <div class="spirit-challenges">
                <h3>🔥 Spirit Challenges</h3>
        """
        
        for challenge in self.spirit_challenges:
            html += f"""
                <div class="challenge-card">
                    <div class="challenge-info">
                        <h4>{challenge['name']}</h4>
                        <p>{challenge['description']}</p>
                        <div class="challenge-meta">
                            <span>🎯 {challenge['points']} points</span>
                            <span>👥 {challenge['participants']} participants</span>
                            <span>⏰ Due: {challenge['deadline']}</span>
                        </div>
                    </div>
                    <button class="btn-challenge">Join Challenge</button>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html

    def get_tailgates_html(self):
        """Get tailgates HTML"""
        html = """
        <div class="tailgates-section">
            <div class="section-header">
                <h2>🎪 Epic Tailgates</h2>
                <p>Where the real party happens before the game!</p>
            </div>
        """
        
        for tailgate in self.tailgates:
            html += f"""
                <div class="tailgate-card">
                    <div class="tailgate-header">
                        <h3>{tailgate['name']}</h3>
                        <div class="tailgate-host">Hosted by {tailgate['host']}</div>
                    </div>
                    
                    <div class="tailgate-details">
                        <div class="tailgate-info">
                            <div>📅 {tailgate['date']} • {tailgate['time']}</div>
                            <div>📍 {tailgate['location']}</div>
                            <div>🎭 Theme: {tailgate['theme']}</div>
                            <div>🎯 {tailgate['spirit_points']} Spirit Points</div>
                        </div>
                        
                        <div class="tailgate-features">
                            <h4>🎉 What's Happening:</h4>
                            <ul>
            """
            
            for feature in tailgate['features']:
                html += f"<li>{feature}</li>"
            
            html += f"""
                            </ul>
                        </div>
                    </div>
                    
                    <div class="tailgate-stats">
                        <div class="rsvp-count">👥 {tailgate['rsvp_count']}/{tailgate['max_capacity']} RSVPs</div>
                        <div class="tailgate-actions">
                            <button class="btn-rsvp">RSVP Now</button>
                            <button class="btn-qr">Get QR Code</button>
                        </div>
                    </div>
                </div>
            """
        
        html += """
        </div>
        """
        
        return html

    def get_watch_parties_html(self):
        """Get watch parties HTML"""
        html = """
        <div class="watch-parties-section">
            <div class="section-header">
                <h2>📺 Watch Parties</h2>
                <p>Cheer on the Lions together, even when they're away!</p>
            </div>
        """
        
        for party in self.watch_parties:
            html += f"""
                <div class="watch-party-card">
                    <div class="party-header">
                        <h3>{party['name']}</h3>
                        <div class="party-host">Hosted by {party['host']}</div>
                    </div>
                    
                    <div class="party-details">
                        <div class="party-info">
                            <div>📅 {party['date']} • {party['time']}</div>
                            <div>📍 {party['location']}</div>
                            <div>🏈 {party['game']}</div>
                            <div>🎯 {party['spirit_points']} Spirit Points</div>
                        </div>
                        
                        <div class="party-features">
                            <h4>🎉 What's Included:</h4>
                            <ul>
            """
            
            for feature in party['features']:
                html += f"<li>{feature}</li>"
            
            html += f"""
                            </ul>
                        </div>
                    </div>
                    
                    <div class="party-stats">
                        <div class="rsvp-count">👥 {party['rsvp_count']}/{party['max_capacity']} RSVPs</div>
                        <div class="party-actions">
                            <button class="btn-rsvp">Join Watch Party</button>
                            <button class="btn-share">Share with Friends</button>
                        </div>
                    </div>
                </div>
            """
        
        html += """
        </div>
        """
        
        return html

    def get_premium_prizes_html(self):
        """Get premium prizes HTML"""
        html = """
        <div class="prizes-section">
            <div class="section-header">
                <h2>🏆 Legendary Prizes</h2>
                <p>Earn points and unlock once-in-a-lifetime experiences!</p>
            </div>
        """
        
        for prize in self.premium_prizes:
            html += f"""
                <div class="prize-card">
                    <div class="prize-icon">{prize['image']}</div>
                    <div class="prize-content">
                        <h3>{prize['name']}</h3>
                        <p>{prize['description']}</p>
                        <div class="prize-meta">
                            <span class="points-required">🎯 {prize['points_required']} points</span>
                            <span class="availability">📦 {prize['availability']} available</span>
                        </div>
                    </div>
                    <div class="prize-actions">
                        <button class="btn-redeem">Redeem Prize</button>
                        <button class="btn-details">Learn More</button>
                    </div>
                </div>
            """
        
        html += """
        </div>
        """
        
        return html

    def get_leaderboard_html(self):
        """Get leaderboard HTML"""
        # Mock leaderboard data
        leaders = [
            {"name": "Sarah Johnson", "points": 1250, "rank": 1, "org": "Alpha Phi Omega"},
            {"name": "Mike Chen", "points": 980, "rank": 2, "org": "Student Government"},
            {"name": "Alex Rodriguez", "points": 875, "rank": 3, "org": "Basketball Club"},
            {"name": "Jordan Smith", "points": 720, "rank": 4, "org": "Black Student Union"},
            {"name": "Taylor Wilson", "points": 650, "rank": 5, "org": "Greek Life"}
        ]
        
        html = """
        <div class="leaderboard-section">
            <div class="section-header">
                <h2>🏆 Spirit Leaderboard</h2>
                <p>Who's bringing the most energy to campus?</p>
            </div>
            
            <div class="leaderboard-list">
        """
        
        for leader in leaders:
            rank_emoji = "🥇" if leader["rank"] == 1 else "🥈" if leader["rank"] == 2 else "🥉" if leader["rank"] == 3 else f"#{leader['rank']}"
            
            html += f"""
                <div class="leaderboard-item">
                    <div class="rank">{rank_emoji}</div>
                    <div class="leader-info">
                        <div class="leader-name">{leader['name']}</div>
                        <div class="leader-org">{leader['org']}</div>
                    </div>
                    <div class="leader-points">{leader['points']} pts</div>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html

def create_interface():
    """Create and configure the Gradio interface"""
    app = CampusLLMApp()
    
    # Modern CSS with game day spirit theme
    css = """
    /* Modern Game Day Spirit Theme */
    .gradio-container {
        max-width: 1400px !important;
        margin: auto !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%) !important;
        min-height: 100vh !important;
        padding: 20px !important;
        color: white !important;
    }
    
    /* Header with LMU spirit gradient */
    .header {
        text-align: center;
        background: linear-gradient(135deg, #d32f2f 0%, #ff6f00 50%, #ffd700 100%);
        color: white;
        padding: 40px 20px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 15px 50px rgba(211, 47, 47, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grain" width="100" height="100" patternUnits="userSpaceOnUse"><circle cx="25" cy="25" r="1" fill="white" opacity="0.1"/><circle cx="75" cy="75" r="1" fill="white" opacity="0.1"/><circle cx="50" cy="10" r="0.5" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23grain)"/></svg>');
        pointer-events: none;
    }
    
    .header h1 {
        font-size: 3rem;
        font-weight: 800;
        margin: 0 0 10px 0;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    .header p {
        font-size: 1.2rem;
        opacity: 0.95;
        margin: 0;
        font-weight: 500;
    }
    
    /* Game Day Dashboard */
    .game-day-dashboard {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .dashboard-header {
        text-align: center;
        margin-bottom: 30px;
    }
    
    .dashboard-header h2 {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 10px 0;
        background: linear-gradient(135deg, #ffd700, #ff6f00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .dashboard-header p {
        font-size: 1.1rem;
        opacity: 0.8;
    }
    
    /* Game Cards */
    .game-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.15), rgba(255, 255, 255, 0.05));
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .game-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
    }
    
    .game-info {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .game-sport {
        background: linear-gradient(135deg, #d32f2f, #ff6f00);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.9rem;
    }
    
    .game-matchup {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ffd700;
    }
    
    .game-details {
        display: flex;
        gap: 20px;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .game-countdown {
        background: linear-gradient(135deg, #ff6f00, #ffd700);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .game-actions {
        display: flex;
        gap: 15px;
    }
    
    /* Buttons */
    .btn-primary {
        background: linear-gradient(135deg, #d32f2f, #ff6f00);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px rgba(211, 47, 47, 0.4);
    }
    
    .btn-secondary {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .btn-secondary:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-2px);
    }
    
    /* Spirit Challenges */
    .spirit-challenges {
        margin-top: 40px;
    }
    
    .challenge-card {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.2), rgba(255, 111, 0, 0.1));
        border-radius: 15px;
        padding: 25px;
        margin: 20px 0;
        border: 1px solid rgba(255, 215, 0, 0.3);
        backdrop-filter: blur(10px);
    }
    
    .challenge-info h4 {
        color: #ffd700;
        font-size: 1.3rem;
        margin: 0 0 10px 0;
    }
    
    .challenge-meta {
        display: flex;
        gap: 20px;
        margin-top: 15px;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .btn-challenge {
        background: linear-gradient(135deg, #ffd700, #ff6f00);
        color: #1a1a2e;
        border: none;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: 600;
        cursor: pointer;
        margin-top: 15px;
    }
    
    /* Tailgates & Watch Parties */
    .tailgate-card, .watch-party-card {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    
    .tailgate-card:hover, .watch-party-card:hover {
        transform: translateY(-5px);
    }
    
    .tailgate-header, .party-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .tailgate-header h3, .party-header h3 {
        color: #ffd700;
        font-size: 1.5rem;
        margin: 0;
    }
    
    .tailgate-host, .party-host {
        background: rgba(255, 255, 255, 0.1);
        padding: 8px 16px;
        border-radius: 20px;
        font-size: 0.9rem;
    }
    
    .tailgate-details, .party-details {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 30px;
        margin-bottom: 25px;
    }
    
    .tailgate-features ul, .party-features ul {
        list-style: none;
        padding: 0;
    }
    
    .tailgate-features li, .party-features li {
        padding: 8px 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .tailgate-stats, .party-stats {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .rsvp-count {
        background: linear-gradient(135deg, #4caf50, #8bc34a);
        color: white;
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    .tailgate-actions, .party-actions {
        display: flex;
        gap: 15px;
    }
    
    .btn-rsvp {
        background: linear-gradient(135deg, #4caf50, #8bc34a);
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .btn-qr, .btn-share {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
    }
    
    /* Premium Prizes */
    .prize-card {
        background: linear-gradient(135deg, rgba(255, 215, 0, 0.15), rgba(255, 111, 0, 0.1));
        border-radius: 20px;
        padding: 30px;
        margin: 25px 0;
        border: 2px solid rgba(255, 215, 0, 0.3);
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        gap: 25px;
        transition: transform 0.3s ease;
    }
    
    .prize-card:hover {
        transform: translateY(-5px);
        border-color: rgba(255, 215, 0, 0.6);
    }
    
    .prize-icon {
        font-size: 3rem;
        background: linear-gradient(135deg, #ffd700, #ff6f00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        min-width: 80px;
        text-align: center;
    }
    
    .prize-content {
        flex: 1;
    }
    
    .prize-content h3 {
        color: #ffd700;
        font-size: 1.4rem;
        margin: 0 0 10px 0;
    }
    
    .prize-meta {
        display: flex;
        gap: 20px;
        margin-top: 15px;
    }
    
    .points-required {
        background: linear-gradient(135deg, #d32f2f, #ff6f00);
        color: white;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .availability {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        padding: 6px 12px;
        border-radius: 15px;
        font-size: 0.9rem;
    }
    
    .prize-actions {
        display: flex;
        flex-direction: column;
        gap: 10px;
    }
    
    .btn-redeem {
        background: linear-gradient(135deg, #ffd700, #ff6f00);
        color: #1a1a2e;
        border: none;
        padding: 12px 24px;
        border-radius: 25px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .btn-details {
        background: rgba(255, 255, 255, 0.1);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.3);
        padding: 10px 20px;
        border-radius: 20px;
        font-weight: 600;
        cursor: pointer;
    }
    
    /* Leaderboard */
    .leaderboard-item {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        border-radius: 15px;
        padding: 20px;
        margin: 15px 0;
        display: flex;
        align-items: center;
        gap: 20px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .rank {
        font-size: 1.5rem;
        font-weight: 700;
        min-width: 50px;
    }
    
    .leader-info {
        flex: 1;
    }
    
    .leader-name {
        font-size: 1.2rem;
        font-weight: 600;
        color: #ffd700;
    }
    
    .leader-org {
        font-size: 0.9rem;
        opacity: 0.7;
    }
    
    .leader-points {
        background: linear-gradient(135deg, #d32f2f, #ff6f00);
        color: white;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
    }
    
    /* Chat Interface */
    .chat-container {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 20px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }
    
    .chat-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .chat-header h3 {
        color: #ffd700;
        margin: 0;
        font-size: 1.3rem;
    }
    
    .chat-input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.3);
        border-radius: 25px;
        padding: 15px 20px;
        color: white;
        font-size: 1rem;
    }
    
    .chat-input::placeholder {
        color: rgba(255, 255, 255, 0.6);
    }
    
    /* Points Display */
    .points-display {
        background: linear-gradient(135deg, #d32f2f, #ff6f00);
        color: white;
        border-radius: 20px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(211, 47, 47, 0.3);
        border: none;
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .points-display h3 {
        margin: 0 0 15px 0;
        font-size: 1.4rem;
        font-weight: 700;
    }
    
    .points-display p {
        margin: 8px 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .gradio-container {
            padding: 10px !important;
        }
        
        .header h1 {
            font-size: 2rem;
        }
        
        .game-info, .tailgate-details, .party-details {
            flex-direction: column;
            gap: 15px;
        }
        
        .game-actions, .tailgate-actions, .party-actions {
            flex-direction: column;
        }
        
        .prize-card {
            flex-direction: column;
            text-align: center;
        }
    }
    """
    
    # Create the interface
    with gr.Blocks(css=css, title="LMU Campus LLM - Game Day Spirit", theme=gr.themes.Soft()) as interface:
        
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🦁 LMU Campus LLM</h1>
            <p>Your AI assistant for everything LMU - built by students, for students!</p>
        </div>
        """)
        
        # Main tabs
        with gr.Tabs():
            
            # -------------------- Game Day Dashboard Tab --------------------
            with gr.Tab("🏈 Game Day Dashboard"):
                gr.HTML(app.get_game_day_dashboard())
            
            # -------------------- Tailgates Tab --------------------
            with gr.Tab("🎪 Epic Tailgates"):
                gr.HTML(app.get_tailgates_html())
            
            # -------------------- Watch Parties Tab --------------------
            with gr.Tab("📺 Watch Parties"):
                gr.HTML(app.get_watch_parties_html())
            
            # -------------------- Legendary Prizes Tab --------------------
            with gr.Tab("🏆 Legendary Prizes"):
                gr.HTML(app.get_premium_prizes_html())
            
            # -------------------- Leaderboard Tab --------------------
            with gr.Tab("🏆 Spirit Leaderboard"):
                gr.HTML(app.get_leaderboard_html())
            
            # -------------------- Chat with AI Tab --------------------
            with gr.Tab("💬 Chat with AI"):
                with gr.Row():
                    with gr.Column(scale=2):
                        # Chat interface
                        with gr.Group():
                            gr.HTML("""
                            <div class="chat-header">
                                <h3>💬 Chat with LMU Assistant</h3>
                                <button style="background: none; border: none; color: white; cursor: pointer;">🗑️</button>
                            </div>
                            """)
                            
                            chatbot = gr.Chatbot(
                                label="",
                                height=400,
                                show_label=False,
                                container=True,
                                bubble_full_width=False
                            )
                            
                            with gr.Row():
                                user_input = gr.Textbox(
                                    placeholder="Ask me anything about LMU! (e.g., 'Where can I find tutoring?')",
                                    label="",
                                    show_label=False,
                                    container=False,
                                    scale=4
                                )
                                submit_btn = gr.Button("Ask", variant="primary", scale=1)
                        
                        # Example questions
                        gr.HTML("""
                        <div style="margin-top: 20px;">
                            <h4>💡 Try these example questions:</h4>
                            <div style="display: flex; flex-wrap: wrap; gap: 10px; margin-top: 10px;">
                                <button class="btn-secondary" style="font-size: 0.9rem;">Where can I find a math tutor?</button>
                                <button class="btn-secondary" style="font-size: 0.9rem;">What's the GPA requirement for study abroad?</button>
                                <button class="btn-secondary" style="font-size: 0.9rem;">What events are happening this week?</button>
                                <button class="btn-secondary" style="font-size: 0.9rem;">How do I file an academic grievance?</button>
                                <button class="btn-secondary" style="font-size: 0.9rem;">Where is the counseling center?</button>
                                <button class="btn-secondary" style="font-size: 0.9rem;">What are the library hours?</button>
                                <button class="btn-secondary" style="font-size: 0.9rem;">How do I add/drop a class?</button>
                                <button class="btn-secondary" style="font-size: 0.9rem;">Draft an email to my professor asking for help</button>
                            </div>
                        </div>
                        """)
                    
                    with gr.Column(scale=1):
                        # Student ID input
                        gr.HTML("""
                        <div style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; margin-bottom: 20px;">
                            <h4>🆔 Student ID (Optional)</h4>
                            <input type="text" placeholder="Enter your Student ID" style="width: 100%; padding: 10px; border: 1px solid rgba(255, 255, 255, 0.3); border-radius: 8px; background: rgba(255, 255, 255, 0.1); color: white;">
                        </div>
                        """)
                        
                        # Points display
                        points_display = gr.HTML("""
                        <div class="points-display">
                            <h3>🦁 Your Spirit Points</h3>
                            <p>Enter your Student ID to see your points!</p>
                        </div>
                        """)
                        
                        # Quick actions
                        gr.HTML("""
                        <div style="background: rgba(255, 255, 255, 0.1); border-radius: 15px; padding: 20px; margin-top: 20px;">
                            <h4>⚡ Quick Actions</h4>
                            <div style="display: flex; flex-direction: column; gap: 10px; margin-top: 15px;">
                                <button class="btn-primary" style="width: 100%;">Show This Week's Events</button>
                                <button class="btn-secondary" style="width: 100%;">Give Feedback</button>
                            </div>
                        </div>
                        """)
        
        # Event handlers
        def respond(message, history):
            if not message.strip():
                return history, ""
            
            response = app.process_message(message, history)
            history.append([message, response])
            return history, ""
        
        submit_btn.click(
            respond,
            inputs=[user_input, chatbot],
            outputs=[chatbot, user_input]
        )
        
        user_input.submit(
            respond,
            inputs=[user_input, chatbot],
            outputs=[chatbot, user_input]
        )
    
    return interface

if __name__ == "__main__":
    # Create and launch the interface
    interface = create_interface()
    
    print("🦁 Starting LMU Campus LLM - Game Day Spirit Edition...")
    print("💡 Make sure Ollama is running with: ollama serve")
    print("📚 Loading LLaMA 3.2 model...")
    
    # Launch with public sharing for testing
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True if you want a public link
        show_api=False
    )