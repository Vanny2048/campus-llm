#!/usr/bin/env python3
"""
LMU Campus LLM - Ultimate School Spirit Platform
A student-centered AI assistant and gamified spirit engine for Loyola Marymount University

Author: Vanessa Akaraiwe
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
                "tailgate_id": "tg_001"
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
                "watch_party_id": "wp_001"
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
                "tailgate_id": "tg_002"
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
                "qr_code": "TG001_QR"
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
                "qr_code": "TG002_QR"
            }
        ]
    
    def _load_watch_parties(self):
        """Load watch party events"""
        return [
            {
                "id": "wp_001",
                "name": "Away Game Watch Party",
                "host": "LMU Athletics",
                "partner": "The Lion's Den Bar",
                "date": "2024-02-22",
                "time": "19:30-22:00", 
                "location": "The Lion's Den (Off-campus)",
                "features": ["Big Screen", "Happy Hour", "Spirit Contests", "Free Appetizers"],
                "spirit_points": 20,
                "max_capacity": 100,
                "rsvp_count": 23,
                "qr_code": "WP001_QR"
            }
        ]
    
    def _load_spirit_challenges(self):
        """Load active spirit challenges"""
        return [
            {
                "id": "sc_001",
                "title": "Best Face Paint",
                "description": "Show off your LMU spirit with the most creative face paint!",
                "points": 50,
                "deadline": "2024-02-15 18:00",
                "type": "photo_submission",
                "active": True
            },
            {
                "id": "sc_002", 
                "title": "Chant Master",
                "description": "Record the most spirited group chant at the tailgate",
                "points": 75,
                "deadline": "2024-02-15 18:30",
                "type": "video_submission",
                "active": True
            },
            {
                "id": "sc_003",
                "title": "Spirit Squad",
                "description": "Bring 5+ friends to the tailgate for bonus points",
                "points": 100,
                "deadline": "2024-02-15 18:00",
                "type": "group_checkin",
                "active": True
            }
        ]
    
    def _load_premium_prizes(self):
        """Load premium experience prizes"""
        return [
            {
                "id": "pp_001",
                "title": "Day as LMU President",
                "description": "Shadow the president, attend meetings, take over LMU socials",
                "points_required": 1000,
                "available": 1,
                "claimed": 0,
                "category": "premium_experience",
                "image": "👔"
            },
            {
                "id": "pp_002",
                "title": "Voice of the Lions",
                "description": "Announce starting lineups and control music for a game",
                "points_required": 750,
                "available": 2,
                "claimed": 0,
                "category": "game_experience",
                "image": "🎤"
            },
            {
                "id": "pp_003",
                "title": "Tailgate Marshal",
                "description": "Lead the pregame parade with custom banner and cape",
                "points_required": 500,
                "available": 3,
                "claimed": 0,
                "category": "spirit_leadership",
                "image": "🎖️"
            },
            {
                "id": "pp_004",
                "title": "Coach for a Day",
                "description": "Join team practice and be on the sidelines",
                "points_required": 800,
                "available": 1,
                "claimed": 0,
                "category": "athletics_experience",
                "image": "🏀"
            },
            {
                "id": "pp_005",
                "title": "Jumbotron Shout-out",
                "description": "Personalized halftime message on the big screen",
                "points_required": 300,
                "available": 5,
                "claimed": 0,
                "category": "recognition",
                "image": "📺"
            },
            {
                "id": "pp_006",
                "title": "Spirit Trophy",
                "description": "Traveling trophy for your org/house for a month",
                "points_required": 600,
                "available": 1,
                "claimed": 0,
                "category": "prestige",
                "image": "🏆"
            }
        ]

    def process_message(self, message, history, user_id=None):
        """Process user message and return response"""
        try:
            # Add points for asking a question
            if user_id:
                self.points_system.add_points(user_id, 1, "question_asked")
            
            # Get context from RAG system
            context = self.rag_system.get_relevant_context(message)
            
            # Generate response using LLM
            response = self.llm_handler.generate_response(message, context, history)
            
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
            error_msg = f"Sorry, I encountered an error: {str(e)}"
            print(f"Error in process_message: {e}")
            return error_msg
    
    def get_user_points(self, user_id):
        """Get current points for a user"""
        if not user_id:
            return """
            <div class="points-display">
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
            
            return f"""
            <div class="points-display">
                <h3>🏆 Your Spirit Points</h3>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0; color: #FFD700;">{points} pts</p>
                <p style="font-size: 0.9rem; opacity: 0.8;">Rank #{rank_info.get('rank', 'N/A')} of {rank_info.get('total_users', 0)} students</p>
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

    def get_game_day_dashboard(self):
        """Get the main game day dashboard"""
        next_game = None
        upcoming_events = []
        
        # Find next game
        today = datetime.now().date()
        for game in self.game_events:
            game_date = datetime.strptime(game['date'], '%Y-%m-%d').date()
            if game_date >= today:
                if not next_game or game_date < datetime.strptime(next_game['date'], '%Y-%m-%d').date():
                    next_game = game
                upcoming_events.append(game)
        
        # Get related tailgates and watch parties
        related_tailgates = []
        related_watch_parties = []
        
        if next_game:
            if next_game.get('tailgate_id'):
                related_tailgates = [t for t in self.tailgates if t['id'] == next_game['tailgate_id']]
            if next_game.get('watch_party_id'):
                related_watch_parties = [w for w in self.watch_parties if w['id'] == next_game['watch_party_id']]
        
        # Countdown to next game
        countdown_html = ""
        if next_game:
            game_datetime = datetime.strptime(f"{next_game['date']} {next_game['time']}", '%Y-%m-%d %H:%M')
            now = datetime.now()
            time_diff = game_datetime - now
            
            if time_diff.total_seconds() > 0:
                days = time_diff.days
                hours = time_diff.seconds // 3600
                minutes = (time_diff.seconds % 3600) // 60
                
                countdown_html = f"""
                <div class="countdown-container">
                    <h2>🦁 Next Game: {next_game['sport']} vs {next_game['opponent']}</h2>
                    <div class="countdown-timer">
                        <div class="countdown-unit">
                            <span class="countdown-number">{days}</span>
                            <span class="countdown-label">Days</span>
                        </div>
                        <div class="countdown-unit">
                            <span class="countdown-number">{hours}</span>
                            <span class="countdown-label">Hours</span>
                        </div>
                        <div class="countdown-unit">
                            <span class="countdown-number">{minutes}</span>
                            <span class="countdown-label">Minutes</span>
                        </div>
                    </div>
                    <p class="game-details">
                        📅 {next_game['date']} at {next_game['time']}<br>
                        🏟️ {next_game['venue']}<br>
                        🏆 {next_game['spirit_points']} Spirit Points Available!
                    </p>
                </div>
                """
        
        # Active challenges
        active_challenges = [c for c in self.spirit_challenges if c['active']]
        challenges_html = ""
        if active_challenges:
            challenges_html = """
            <div class="challenges-section">
                <h3>🔥 Active Spirit Challenges</h3>
                <div class="challenges-grid">
            """
            for challenge in active_challenges:
                challenges_html += f"""
                    <div class="challenge-card">
                        <h4>{challenge['title']}</h4>
                        <p>{challenge['description']}</p>
                        <div class="challenge-meta">
                            <span class="points">🏆 {challenge['points']} pts</span>
                            <span class="deadline">⏰ {challenge['deadline']}</span>
                        </div>
                        <button class="challenge-btn">Participate</button>
                    </div>
                """
            challenges_html += "</div></div>"
        
        return f"""
        <div class="game-day-dashboard">
            {countdown_html}
            
            <div class="quick-actions">
                <h3>⚡ Quick Actions</h3>
                <div class="action-buttons">
                    <button class="action-btn primary">🎫 RSVP to Tailgate</button>
                    <button class="action-btn secondary">📱 Generate QR Code</button>
                    <button class="action-btn secondary">📸 Submit Challenge</button>
                    <button class="action-btn secondary">🏆 View Leaderboard</button>
                </div>
            </div>
            
            {challenges_html}
            
            <div class="upcoming-events">
                <h3>📅 Upcoming Spirit Events</h3>
                <div class="events-grid">
        """
        
        # Add upcoming events
        for event in upcoming_events[:3]:  # Show next 3 events
            event_html = f"""
                    <div class="event-card">
                        <div class="event-header">
                            <h4>{event['sport']} vs {event['opponent']}</h4>
                            <span class="event-type {event['type']}">{event['type'].title()}</span>
                        </div>
                        <p>📅 {event['date']} at {event['time']}</p>
                        <p>🏟️ {event['venue']}</p>
                        <p>🏆 {event['spirit_points']} pts</p>
                        <button class="event-btn">Learn More</button>
                    </div>
            """
            dashboard_html += event_html
        
        dashboard_html += """
                </div>
            </div>
        </div>
        """
        
        return dashboard_html

    def get_tailgates_html(self):
        """Get tailgates section HTML"""
        html = """
        <div class="tailgates-section">
            <h2>🎉 Official LMU Tailgates</h2>
            <p class="section-description">Join the ultimate pre-game experience! RSVP, earn points, and show your Lion pride.</p>
            
            <div class="tailgates-grid">
        """
        
        for tailgate in self.tailgates:
            # Calculate days until tailgate
            tailgate_date = datetime.strptime(tailgate['date'], '%Y-%m-%d').date()
            days_until = (tailgate_date - datetime.now().date()).days
            
            status_class = "upcoming" if days_until > 0 else "today" if days_until == 0 else "past"
            
            html += f"""
                <div class="tailgate-card {status_class}">
                    <div class="tailgate-header">
                        <h3>{tailgate['name']}</h3>
                        <span class="host-badge">Hosted by {tailgate['host']}</span>
                    </div>
                    
                    <div class="tailgate-details">
                        <p><strong>📅 Date:</strong> {tailgate['date']}</p>
                        <p><strong>⏰ Time:</strong> {tailgate['time']}</p>
                        <p><strong>📍 Location:</strong> {tailgate['location']}</p>
                        <p><strong>🎭 Theme:</strong> {tailgate['theme']}</p>
                    </div>
                    
                    <div class="tailgate-features">
                        <h4>🎪 Features:</h4>
                        <ul>
            """
            for feature in tailgate['features']:
                html += f"<li>{feature}</li>"
            
            html += f"""
                        </ul>
                    </div>
                    
                    <div class="tailgate-stats">
                        <div class="stat">
                            <span class="stat-number">🏆 {tailgate['spirit_points']}</span>
                            <span class="stat-label">Spirit Points</span>
                        </div>
                        <div class="stat">
                            <span class="stat-number">👥 {tailgate['rsvp_count']}/{tailgate['max_capacity']}</span>
                            <span class="stat-label">RSVPs</span>
                        </div>
                        <div class="stat">
                            <span class="stat-number">📅 {days_until}</span>
                            <span class="stat-label">Days Away</span>
                        </div>
                    </div>
                    
                    <div class="tailgate-actions">
                        <button class="rsvp-btn">🎫 RSVP Now</button>
                        <button class="qr-btn">📱 Get QR Code</button>
                        <button class="share-btn">📤 Share</button>
                    </div>
                </div>
            """
        
        html += """
            </div>
            
            <div class="host-info">
                <h3>🏠 Want to Host a Tailgate?</h3>
                <p>RSOs, fraternities, sororities, and student groups can apply to host official LMU tailgates!</p>
                <button class="host-btn">Apply to Host</button>
            </div>
        </div>
        """
        
        return html

    def get_watch_parties_html(self):
        """Get watch parties section HTML"""
        html = """
        <div class="watch-parties-section">
            <h2>📺 Away Game Watch Parties</h2>
            <p class="section-description">Can't make it to the away game? Join fellow Lions at these official watch parties!</p>
            
            <div class="watch-parties-grid">
        """
        
        for party in self.watch_parties:
            # Calculate days until watch party
            party_date = datetime.strptime(party['date'], '%Y-%m-%d').date()
            days_until = (party_date - datetime.now().date()).days
            
            html += f"""
                <div class="watch-party-card">
                    <div class="party-header">
                        <h3>{party['name']}</h3>
                        <span class="partner-badge">Partner: {party['partner']}</span>
                    </div>
                    
                    <div class="party-details">
                        <p><strong>📅 Date:</strong> {party['date']}</p>
                        <p><strong>⏰ Time:</strong> {party['time']}</p>
                        <p><strong>📍 Location:</strong> {party['location']}</p>
                    </div>
                    
                    <div class="party-features">
                        <h4>🎉 Features:</h4>
                        <ul>
            """
            for feature in party['features']:
                html += f"<li>{feature}</li>"
            
            html += f"""
                        </ul>
                    </div>
                    
                    <div class="party-stats">
                        <div class="stat">
                            <span class="stat-number">🏆 {party['spirit_points']}</span>
                            <span class="stat-label">Spirit Points</span>
                        </div>
                        <div class="stat">
                            <span class="stat-number">👥 {party['rsvp_count']}/{party['max_capacity']}</span>
                            <span class="stat-label">RSVPs</span>
                        </div>
                    </div>
                    
                    <div class="party-actions">
                        <button class="rsvp-btn">🎫 RSVP Now</button>
                        <button class="directions-btn">🗺️ Get Directions</button>
                        <button class="share-btn">📤 Share</button>
                    </div>
                </div>
            """
        
        html += """
            </div>
            
            <div class="partner-info">
                <h3>🤝 Partner with Us</h3>
                <p>Local businesses can host official LMU watch parties and earn exposure to our student community!</p>
                <button class="partner-btn">Become a Partner</button>
            </div>
        </div>
        """
        
        return html

    def get_premium_prizes_html(self):
        """Get premium prizes section HTML"""
        html = """
        <div class="premium-prizes-section">
            <h2>🏆 Premium Spirit Experiences</h2>
            <p class="section-description">Unlock legendary experiences that money can't buy! These exclusive rewards are earned through pure Lion spirit.</p>
            
            <div class="prizes-grid">
        """
        
        for prize in self.premium_prizes:
            availability = prize['available'] - prize['claimed']
            availability_class = "available" if availability > 0 else "claimed"
            
            html += f"""
                <div class="prize-card {availability_class}">
                    <div class="prize-icon">
                        {prize['image']}
                    </div>
                    
                    <div class="prize-content">
                        <h3>{prize['title']}</h3>
                        <p class="prize-description">{prize['description']}</p>
                        
                        <div class="prize-meta">
                            <div class="points-required">
                                <span class="points-number">🏆 {prize['points_required']}</span>
                                <span class="points-label">Spirit Points</span>
                            </div>
                            <div class="availability">
                                <span class="availability-number">{availability}</span>
                                <span class="availability-label">Available</span>
                            </div>
                        </div>
                        
                        <div class="prize-category">
                            <span class="category-badge">{prize['category'].replace('_', ' ').title()}</span>
                        </div>
                    </div>
                    
                    <div class="prize-actions">
                        <button class="redeem-btn" {'disabled' if availability <= 0 else ''}>
                            {'Redeemed' if availability <= 0 else 'Redeem Now'}
                        </button>
                        <button class="details-btn">Learn More</button>
                    </div>
                </div>
            """
        
        html += """
            </div>
            
            <div class="prize-info">
                <h3>💡 How to Earn Premium Prizes</h3>
                <div class="earning-tips">
                    <div class="tip">
                        <h4>🎯 Attend Everything</h4>
                        <p>Go to games, tailgates, and watch parties consistently</p>
                    </div>
                    <div class="tip">
                        <h4>🔥 Complete Challenges</h4>
                        <p>Participate in spirit challenges and creative contests</p>
                    </div>
                    <div class="tip">
                        <h4>👥 Bring Friends</h4>
                        <p>Earn bonus points for bringing new people to events</p>
                    </div>
                    <div class="tip">
                        <h4>📸 Share Content</h4>
                        <p>Post about your LMU spirit on social media</p>
                    </div>
                </div>
            </div>
        </div>
        """
        
        return html

    def generate_qr_code(self, event_id, event_type):
        """Generate QR code for event check-in"""
        try:
            # Create QR code data
            qr_data = f"LMU_SPIRIT_{event_type.upper()}_{event_id}_{datetime.now().strftime('%Y%m%d')}"
            
            # Generate QR code
            qr = qrcode.QRCode(version=1, box_size=10, border=5)
            qr.add_data(qr_data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_str = base64.b64encode(buffer.getvalue()).decode()
            
            return f"data:image/png;base64,{img_str}"
            
        except Exception as e:
            print(f"Error generating QR code: {e}")
            return None

    def check_in_user(self, user_id, event_id, event_type, qr_code_data):
        """Process user check-in for an event"""
        try:
            # Validate QR code
            expected_data = f"LMU_SPIRIT_{event_type.upper()}_{event_id}_{datetime.now().strftime('%Y%m%d')}"
            
            if qr_code_data != expected_data:
                return {"success": False, "message": "Invalid QR code or expired"}
            
            # Determine points based on event type
            points = 0
            if event_type == "tailgate":
                points = 25
            elif event_type == "game":
                points = 50
            elif event_type == "watch_party":
                points = 20
            elif event_type == "challenge":
                points = 50
            
            # Add points
            self.points_system.add_points(user_id, points, f"{event_type}_checkin")
            
            return {
                "success": True, 
                "message": f"Check-in successful! +{points} Spirit Points",
                "points_earned": points
            }
            
        except Exception as e:
            return {"success": False, "message": f"Check-in error: {str(e)}"}

    def submit_spirit_challenge(self, user_id, challenge_id, submission_type, submission_data):
        """Submit a spirit challenge entry"""
        try:
            # Find the challenge
            challenge = next((c for c in self.spirit_challenges if c['id'] == challenge_id), None)
            
            if not challenge or not challenge['active']:
                return {"success": False, "message": "Challenge not found or inactive"}
            
            # Validate submission type
            if submission_type != challenge['type']:
                return {"success": False, "message": "Invalid submission type for this challenge"}
            
            # Award points
            self.points_system.add_points(user_id, challenge['points'], f"challenge_{challenge_id}")
            
            return {
                "success": True,
                "message": f"Challenge submitted! +{challenge['points']} Spirit Points",
                "points_earned": challenge['points']
            }
            
        except Exception as e:
            return {"success": False, "message": f"Submission error: {str(e)}"}

    def rsvp_to_event(self, user_id, event_id, event_type):
        """RSVP to an event"""
        try:
            # Find the event
            if event_type == "tailgate":
                event = next((t for t in self.tailgates if t['id'] == event_id), None)
            elif event_type == "watch_party":
                event = next((w for w in self.watch_parties if w['id'] == event_id), None)
            else:
                return {"success": False, "message": "Invalid event type"}
            
            if not event:
                return {"success": False, "message": "Event not found"}
            
            # Check capacity
            if event['rsvp_count'] >= event['max_capacity']:
                return {"success": False, "message": "Event is at full capacity"}
            
            # Update RSVP count (in real app, this would be stored in database)
            event['rsvp_count'] += 1
            
            # Add points for RSVP
            self.points_system.add_points(user_id, 5, f"{event_type}_rsvp")
            
            return {
                "success": True,
                "message": f"RSVP successful! +5 Spirit Points",
                "event_name": event['name']
            }
            
        except Exception as e:
            return {"success": False, "message": f"RSVP error: {str(e)}"}

    def redeem_prize(self, user_id, prize_id):
        """Redeem a premium prize"""
        try:
            # Find the prize
            prize = next((p for p in self.premium_prizes if p['id'] == prize_id), None)
            
            if not prize:
                return {"success": False, "message": "Prize not found"}
            
            # Check availability
            if prize['claimed'] >= prize['available']:
                return {"success": False, "message": "Prize is no longer available"}
            
            # Get user points
            stats = self.points_system.get_user_stats(user_id)
            user_points = 0
            if "Total Points:" in stats:
                points_str = stats.split("Total Points:")[1].split()[0]
                user_points = int(points_str)
            
            # Check if user has enough points
            if user_points < prize['points_required']:
                return {"success": False, "message": f"Need {prize['points_required'] - user_points} more Spirit Points"}
            
            # Deduct points and claim prize
            self.points_system.add_points(user_id, -prize['points_required'], f"prize_redemption_{prize_id}")
            prize['claimed'] += 1
            
            return {
                "success": True,
                "message": f"Prize redeemed! You now have: {prize['title']}",
                "prize_title": prize['title']
            }
            
        except Exception as e:
            return {"success": False, "message": f"Redemption error: {str(e)}"}

def create_interface():
    """Create and configure the Gradio interface"""
    app = CampusLLMApp()
    
    # Modern CSS inspired by Claude AI and ChatGPT
    css = """
    /* Modern Chat Interface */
    .gradio-container {
        max-width: 1400px !important;
        margin: auto !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%) !important;
        min-height: 100vh !important;
        padding: 20px !important;
    }
    
    /* Header with modern gradient */
    .header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 30px 20px;
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
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
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 8px 0;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
        font-weight: 400;
    }
    
    /* Modern Points Display */
    .points-display {
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
    }
    
    .points-display::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, transparent, rgba(255,255,255,0.1), transparent);
        transform: rotate(45deg);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { transform: translateX(-100%) translateY(-100%) rotate(45deg); }
        100% { transform: translateX(100%) translateY(100%) rotate(45deg); }
    }
    
    .points-display h3 {
        margin: 0 0 12px 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    .points-display p {
        margin: 8px 0;
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Modern Chat Interface */
    .chat-container {
        background: #ffffff;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        overflow: hidden;
    }
    
    .chatbot {
        border: none !important;
        border-radius: 16px !important;
        background: #fafbfc !important;
    }
    
    .chatbot .message {
        border-radius: 12px !important;
        margin: 8px 12px !important;
        padding: 12px 16px !important;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06) !important;
    }
    
    .chatbot .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        margin-left: 20% !important;
    }
    
    .chatbot .bot-message {
        background: white !important;
        color: #2d3748 !important;
        margin-right: 20% !important;
        border: 1px solid #e2e8f0 !important;
    }
    
    /* Modern Input */
    .input-container {
        background: white;
        border-top: 1px solid #e1e5e9;
        padding: 16px;
    }
    
    .input-box {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .input-box:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    .submit-btn {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3) !important;
    }
    
    .submit-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* Modern Tabs */
    .tabs {
        background: white !important;
        border-radius: 16px !important;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08) !important;
        border: 1px solid #e1e5e9 !important;
        overflow: hidden !important;
    }
    
    .tab-nav {
        background: #f8fafc !important;
        border-bottom: 1px solid #e1e5e9 !important;
    }
    
    .tab-nav button {
        background: transparent !important;
        border: none !important;
        padding: 16px 24px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        transition: all 0.2s ease !important;
        border-radius: 0 !important;
    }
    
    .tab-nav button.selected {
        background: white !important;
        color: #667eea !important;
        border-bottom: 3px solid #667eea !important;
    }
    
    .tab-nav button:hover {
        background: #f1f5f9 !important;
        color: #475569 !important;
    }
    
    /* Modern Cards */
    .dashboard-card {
        background: rgba(255, 255, 255, 0.95);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .dashboard-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 16px 48px rgba(0,0,0,0.15);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* Modern Tables */
    .leaderboard {
        width: 100%;
        border-collapse: separate;
        border-spacing: 0;
        margin-top: 20px;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        background: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .leaderboard th {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px 16px;
        font-weight: 700;
        text-align: center;
        border: none;
        font-size: 1.1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .leaderboard td {
        padding: 16px;
        text-align: center;
        border: none;
        border-bottom: 1px solid rgba(0,0,0,0.05);
        background: white;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .leaderboard tr:nth-child(even) td {
        background: rgba(248, 250, 252, 0.8);
    }
    
    .leaderboard tr:hover td {
        background: rgba(102, 126, 234, 0.05);
        transform: scale(1.02);
    }
    
    .leaderboard tr:first-child td {
        background: linear-gradient(135deg, #ffd700, #ffed4e);
        color: #333;
        font-weight: 700;
    }
    
    .leaderboard tr:nth-child(2) td {
        background: linear-gradient(135deg, #c0c0c0, #a8a8a8);
        color: white;
        font-weight: 600;
    }
    
    .leaderboard tr:nth-child(3) td {
        background: linear-gradient(135deg, #cd7f32, #b8860b);
        color: white;
        font-weight: 600;
    }
    
    /* Modern Buttons */
    .refresh-btn {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 20px !important;
        color: white !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.3) !important;
    }
    
    .refresh-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(16, 185, 129, 0.4) !important;
    }
    
    /* Modern Form Elements */
    .feedback-form {
        background: white;
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
    }
    
    .feedback-input {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
    }
    
    .feedback-input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header h1 {
            font-size: 2rem;
        }
        
        .gradio-container {
            padding: 16px !important;
        }
        
        .dashboard-card {
            padding: 16px;
        }
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    """
    
    with gr.Blocks(css=css, title="LMU Campus LLM") as interface:
        # Modern Header
        gr.HTML("""
        <div class="header">
            <h1>🦁 LMU Campus AI</h1>
            <p>Your Gen Z friend who knows everything about The Bluff</p>
        </div>
        """)

        # ---- Global student id + points row ----
        with gr.Row():
            student_id = gr.Textbox(
                label="Student ID (Optional)",
                placeholder="Enter your ID to track points",
                type="text",
                scale=1
            )
            points_display = gr.HTML(
                value=app.get_user_points(""),
                label="Points"
            )


        with gr.Tabs():
            # -------------------- Home / Dashboard Tab --------------------
            with gr.Tab("Home/Dashboard"):
                with gr.Row():
                    with gr.Column(scale=2):
                        # Modern chat interface
                        chatbot = gr.Chatbot(
                            label="Chat with LMU Assistant",
                            height=500,
                            show_label=False,
                            elem_classes=["chatbot"],
                            type="messages"
                        )

                        with gr.Row():
                            user_input = gr.Textbox(
                                placeholder="Ask me anything about LMU! (e.g., 'where can i find tutoring?')",
                                container=False,
                                scale=4,
                                elem_classes=["input-box"]
                            )
                            submit_btn = gr.Button("Send", variant="primary", scale=1, elem_classes=["submit-btn"])

                        # Gen Z example questions
                        gr.Examples(
                            examples=[
                                "where can i find a math tutor?",
                                "what's the vibe at the rock?",
                                "events this week?",
                                "how do i add/drop a class?",
                                "where's the counseling center?",
                                "library hours?",
                                "what's the best study spot?",
                                "help me write an email to my professor"
                            ],
                            inputs=user_input,
                            label="💡 Try these questions:"
                        )

                    with gr.Column(scale=1):
                        # Modern dashboard feed
                        feed_refresh_btn = gr.Button("🔄 Refresh", variant="secondary", elem_classes=["refresh-btn"])
                        feed_display = gr.HTML(value=app.get_dynamic_feed_html())

            # -------------------- Events Tab --------------------
            with gr.Tab("Events"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h3>📅 Events & RSVP</h3>
                            <p>Find events, RSVP, and get points for attending!</p>
                        </div>
                        """)
                        
                        # Event Categories
                        with gr.Row():
                            event_categories = gr.HTML("""
                            <div class="dashboard-card">
                                <h4>🎯 Event Categories</h4>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin: 10px 0;">
                                    <button style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600;">🏈 Sports</button>
                                    <button style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600;">🎉 Social</button>
                                    <button style="background: linear-gradient(135deg, #4ecdc4, #44a08d); color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600;">📚 Academic</button>
                                    <button style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border: none; padding: 12px; border-radius: 8px; font-weight: 600;">🎨 Cultural</button>
                                </div>
                            </div>
                            """)
                        
                        # This Week's Events
                        events_btn = gr.Button("🔄 Refresh Events", variant="secondary", elem_classes=["refresh-btn"])
                        events_display = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>📅 This Week's Events</h4>
                            <div style="margin: 10px 0;">
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 15px; margin: 10px 0;">
                                    <h5>🏈 LMU vs Pepperdine Basketball</h5>
                                    <p>📍 Gersten Pavilion | ⏰ Today, 7:00 PM</p>
                                    <p>🎉 Tailgate starts at 5:00 PM</p>
                                    <button style="background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">RSVP (127 attending)</button>
                                </div>
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 15px; margin: 10px 0;">
                                    <h5>🎨 First Friday Art Walk</h5>
                                    <p>📍 The Grove | ⏰ Friday, 6:00 PM</p>
                                    <p>🎭 Student art showcase and live music</p>
                                    <button style="background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">RSVP (89 attending)</button>
                                </div>
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 15px; margin: 10px 0;">
                                    <h5>📚 Study Abroad Info Session</h5>
                                    <p>📍 University Hall | ⏰ Wednesday, 3:00 PM</p>
                                    <p>✈️ Learn about international programs</p>
                                    <button style="background: #667eea; color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">RSVP (45 attending)</button>
                                </div>
                            </div>
                        </div>
                        """)
                    
                    with gr.Column(scale=1):
                        # Quick RSVP
                        quick_rsvp = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>⚡ Quick RSVP</h4>
                            <p>Fast check-in for events you're already at!</p>
                            <div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                <h5>📱 Event Check-In</h5>
                                <p>Enter event code to check in</p>
                                <input type="text" placeholder="Enter event code" style="width: 100%; padding: 8px; border: none; border-radius: 6px; margin: 10px 0;">
                                <button style="background: white; color: #10b981; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; width: 100%;">Check In</button>
                            </div>
                        </div>
                        """)
                        
                        # Calendar Integration
                        calendar_integration = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>📅 Calendar Sync</h4>
                            <p>Automatically add events to your calendar</p>
                            <div style="background: linear-gradient(135deg, #f59e0b, #d97706); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                <h5>📱 Sync to Phone</h5>
                                <p>Get reminders and never miss an event</p>
                                <button style="background: white; color: #f59e0b; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; width: 100%;">Connect Calendar</button>
                            </div>
                        </div>
                        """)

            # -------------------- Game Day Tab --------------------
            with gr.Tab("Game Day"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h3>🏈 Game Day Hub</h3>
                            <p>Check in, earn points, and join the hype!</p>
                        </div>
                        """)
                        
                        # QR Code Check-in
                        with gr.Row():
                            qr_code_display = gr.HTML("""
                            <div class="dashboard-card">
                                <h4>📱 QR Check-In</h4>
                                <p>Scan this QR code at events to earn points!</p>
                                <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 8px; margin: 10px 0;">
                                    <div style="font-size: 48px;">📱</div>
                                    <p>QR Code Scanner</p>
                                    <p style="font-size: 0.9rem; color: #666;">Coming soon - real QR codes for events!</p>
                                </div>
                            </div>
                            """)
                        
                        # Live Challenges
                        with gr.Row():
                            challenges_display = gr.HTML("""
                            <div class="dashboard-card">
                                <h4>🔥 Live Challenges</h4>
                                <div style="margin: 10px 0;">
                                    <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                        <h5>📸 Snap Your Fit!</h5>
                                        <p>Post your game day outfit for 5 points</p>
                                        <button style="background: white; color: #ff6b6b; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">Join Challenge</button>
                                    </div>
                                    <div style="background: linear-gradient(135deg, #4ecdc4, #44a08d); color: white; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                        <h5>🎥 Chant of the Game</h5>
                                        <p>Record your best LMU chant for 10 points</p>
                                        <button style="background: white; color: #4ecdc4; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">Join Challenge</button>
                                    </div>
                                </div>
                            </div>
                            """)
                    
                    with gr.Column(scale=1):
                        # Current Tailgate
                        current_tailgate = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🎉 Current Tailgate</h4>
                            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                <h5>🏈 LMU vs Pepperdine</h5>
                                <p>📍 Gersten Pavilion</p>
                                <p>⏰ Today, 7:00 PM</p>
                                <p>👥 127 people checked in</p>
                                <button style="background: white; color: #667eea; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; margin-top: 10px;">Check In Now</button>
                            </div>
                        </div>
                        """)
                        
                        # Social Media Gallery
                        social_gallery = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>📸 Live Feed</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0;">
                                <div style="background: #f0f0f0; height: 80px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px;">📱</div>
                                <div style="background: #f0f0f0; height: 80px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px;">📱</div>
                                <div style="background: #f0f0f0; height: 80px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px;">📱</div>
                                <div style="background: #f0f0f0; height: 80px; border-radius: 8px; display: flex; align-items: center; justify-content: center; font-size: 24px;">📱</div>
                            </div>
                            <p style="text-align: center; color: #666; font-size: 0.9rem;">Live social media posts from the game!</p>
                        </div>
                        """)

            # -------------------- Leaderboard Tab --------------------
            with gr.Tab("Leaderboard"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h3>🏆 Spirit Leaderboard</h3>
                            <p>See who's bringing the most hype to The Bluff!</p>
                        </div>
                        """)
                        
                        # Leaderboard Filters
                        with gr.Row():
                            leaderboard_filters = gr.HTML("""
                            <div class="dashboard-card">
                                <h4>🎯 Leaderboard Filters</h4>
                                <div style="display: flex; gap: 10px; margin: 10px 0; flex-wrap: wrap;">
                                    <button style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">🏆 Top Overall</button>
                                    <button style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">👑 Top Ambassadors</button>
                                    <button style="background: linear-gradient(135deg, #4ecdc4, #44a08d); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">🏛️ Most Hype Org</button>
                                    <button style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">🆕 First-timers</button>
                                </div>
                            </div>
                            """)
                        
                        # Main Leaderboard
                        leaderboard_refresh_btn = gr.Button("🔄 Refresh Leaderboard", variant="secondary", elem_classes=["refresh-btn"])
                        leaderboard_display = gr.HTML(value=app.get_leaderboard_html(15))
                    
                    with gr.Column(scale=1):
                        # This Week's MVP
                        weekly_mvp = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🌟 This Week's Spirit MVP</h4>
                            <div style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #333; padding: 20px; border-radius: 12px; margin: 10px 0; text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 10px;">👑</div>
                                <h5>Sarah Johnson</h5>
                                <p>🏛️ Alpha Delta Pi</p>
                                <p>📊 245 points this week</p>
                                <p style="font-size: 0.9rem; color: #666;">Attended 8 events, hosted 2 tailgates</p>
                            </div>
                        </div>
                        """)
                        
                        # RSO of the Month
                        rso_month = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🏛️ RSO of the Month</h4>
                            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 12px; margin: 10px 0; text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 10px;">🏛️</div>
                                <h5>LMU Spirit Squad</h5>
                                <p>📊 1,247 total points</p>
                                <p style="font-size: 0.9rem; opacity: 0.8;">Hosted 15 events this month</p>
                            </div>
                        </div>
                        """)
                        
                        # Badge Showcase
                        badge_showcase = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🏅 Badge Showcase</h4>
                            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0;">
                                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center;">
                                    <div style="font-size: 24px;">🥉</div>
                                    <p style="font-size: 0.8rem; margin: 5px 0;">Bronze Lion</p>
                                </div>
                                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center;">
                                    <div style="font-size: 24px;">🥈</div>
                                    <p style="font-size: 0.8rem; margin: 5px 0;">Silver Lion</p>
                                </div>
                                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center;">
                                    <div style="font-size: 24px;">🥇</div>
                                    <p style="font-size: 0.8rem; margin: 5px 0;">Gold Lion</p>
                                </div>
                                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; text-align: center;">
                                    <div style="font-size: 24px;">👑</div>
                                    <p style="font-size: 0.8rem; margin: 5px 0;">Legendary</p>
                                </div>
                            </div>
                        </div>
                        """)

            # -------------------- Prizes Tab --------------------
            with gr.Tab("Prizes"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h3>🎁 Rewards Shop</h3>
                            <p>Redeem your points for exclusive LMU experiences and merch!</p>
                        </div>
                        """)
                        
                        # Prize Categories
                        with gr.Row():
                            prize_categories = gr.HTML("""
                            <div class="dashboard-card">
                                <h4>🎯 Prize Categories</h4>
                                <div style="display: flex; gap: 10px; margin: 10px 0; flex-wrap: wrap;">
                                    <button style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">🏆 Most Creative</button>
                                    <button style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">🔥 Limited Time</button>
                                    <button style="background: linear-gradient(135deg, #4ecdc4, #44a08d); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">💰 Best Value</button>
                                    <button style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border: none; padding: 8px 16px; border-radius: 6px; font-weight: 600;">⭐ Popular</button>
                                </div>
                            </div>
                            """)
                        
                        # Main Prizes Display
                        prizes_display = gr.HTML(value=app.get_prizes_html())
                    
                    with gr.Column(scale=1):
                        # Secret Wildcard Prize
                        wildcard_prize = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🎲 Secret Wildcard Prize</h4>
                            <div style="background: linear-gradient(135deg, #8b5cf6, #7c3aed); color: white; padding: 20px; border-radius: 12px; margin: 10px 0; text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 10px;">🎲</div>
                                <h5>Coach for a Day</h5>
                                <p>🏈 Shadow the basketball coach</p>
                                <p style="font-size: 0.9rem; opacity: 0.8;">Only 1 available!</p>
                                <button style="background: white; color: #8b5cf6; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; margin-top: 10px;">Redeem (500 pts)</button>
                            </div>
                        </div>
                        """)
                        
                        # Your Points Summary
                        points_summary = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>💰 Your Points</h4>
                            <div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 20px; border-radius: 12px; margin: 10px 0; text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 10px;">💰</div>
                                <h5>Current Balance</h5>
                                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0;">127 pts</p>
                                <p style="font-size: 0.9rem; opacity: 0.8;">Keep grinding to unlock more rewards!</p>
                            </div>
                        </div>
                        """)
                        
                        # Redeem History
                        redeem_history = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>📋 Redeem History</h4>
                            <div style="margin: 10px 0;">
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 10px; margin: 5px 0;">
                                    <p style="font-weight: 600; margin: 0;">🥤 Free Boba</p>
                                    <p style="font-size: 0.8rem; color: #666; margin: 0;">Redeemed 2 days ago</p>
                                </div>
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 10px; margin: 5px 0;">
                                    <p style="font-weight: 600; margin: 0;">🥉 Bronze Lion Badge</p>
                                    <p style="font-size: 0.8rem; color: #666; margin: 0;">Redeemed 1 week ago</p>
                                </div>
                            </div>
                        </div>
                        """)

            # -------------------- My Profile Tab --------------------
            with gr.Tab("My Profile"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h3>👤 Your Profile</h3>
                            <p>Track your progress, badges, and achievements!</p>
                        </div>
                        """)
                        
                        # Profile Stats
                        profile_points = gr.HTML(value=app.get_user_points(""))
                        refresh_profile_btn = gr.Button("🔄 Refresh Stats", elem_classes=["refresh-btn"])
                        
                        # Badges and Achievements
                        with gr.Row():
                            badges_display = gr.HTML("""
                            <div class="dashboard-card">
                                <h4>🏅 Your Badges</h4>
                                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin: 10px 0;">
                                    <div style="background: linear-gradient(135deg, #cd7f32, #b8860b); color: white; padding: 15px; border-radius: 8px; text-align: center;">
                                        <div style="font-size: 24px;">🥉</div>
                                        <p style="font-size: 0.8rem; margin: 5px 0;">Bronze Lion</p>
                                    </div>
                                    <div style="background: linear-gradient(135deg, #c0c0c0, #a8a8a8); color: white; padding: 15px; border-radius: 8px; text-align: center;">
                                        <div style="font-size: 24px;">🥈</div>
                                        <p style="font-size: 0.8rem; margin: 5px 0;">Silver Lion</p>
                                    </div>
                                    <div style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #333; padding: 15px; border-radius: 8px; text-align: center;">
                                        <div style="font-size: 24px;">🥇</div>
                                        <p style="font-size: 0.8rem; margin: 5px 0;">Gold Lion</p>
                                    </div>
                                </div>
                            </div>
                            """)
                        
                        # Event History
                        event_history = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>📅 Recent Events Attended</h4>
                            <div style="margin: 10px 0;">
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 10px; margin: 5px 0;">
                                    <p style="font-weight: 600; margin: 0;">🏈 LMU vs Pepperdine Basketball</p>
                                    <p style="font-size: 0.8rem; color: #666; margin: 0;">Yesterday • +10 points</p>
                                </div>
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 10px; margin: 5px 0;">
                                    <p style="font-weight: 600; margin: 0;">🎨 First Friday Art Walk</p>
                                    <p style="font-size: 0.8rem; color: #666; margin: 0;">Last week • +5 points</p>
                                </div>
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 10px; margin: 5px 0;">
                                    <p style="font-weight: 600; margin: 0;">📚 Study Abroad Info Session</p>
                                    <p style="font-size: 0.8rem; color: #666; margin: 0;">2 weeks ago • +5 points</p>
                                </div>
                            </div>
                        </div>
                        """)
                    
                    with gr.Column(scale=1):
                        # Social Sharing
                        social_sharing = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>📱 Share Your Achievements</h4>
                            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 12px; margin: 10px 0; text-align: center;">
                                <h5>🎉 Brag About It!</h5>
                                <p>Share your LMU spirit on social media</p>
                                <div style="display: flex; gap: 10px; margin-top: 15px; justify-content: center;">
                                    <button style="background: #1da1f2; color: white; border: none; padding: 8px 12px; border-radius: 6px; font-size: 0.8rem;">🐦 Twitter</button>
                                    <button style="background: #4267b2; color: white; border: none; padding: 8px 12px; border-radius: 6px; font-size: 0.8rem;">📘 Facebook</button>
                                    <button style="background: #e4405f; color: white; border: none; padding: 8px 12px; border-radius: 6px; font-size: 0.8rem;">📷 Instagram</button>
                                </div>
                            </div>
                        </div>
                        """)
                        
                        # Streak Counter
                        streak_counter = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🔥 Current Streak</h4>
                            <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 20px; border-radius: 12px; margin: 10px 0; text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 10px;">🔥</div>
                                <h5>7 Days</h5>
                                <p style="font-size: 0.9rem; opacity: 0.8;">Keep the streak alive!</p>
                            </div>
                        </div>
                        """)
                        
                        # Feedback Section
                        with gr.Accordion("📝 Give Feedback", open=False):
                            feedback_text = gr.Textbox(
                                label="Your feedback",
                                placeholder="How can we improve the LMU Campus AI?",
                                lines=3,
                                elem_classes=["feedback-input"]
                            )
                            rating = gr.Slider(
                                minimum=1,
                                maximum=5,
                                value=5,
                                step=1,
                                label="Rating (1-5 stars)"
                            )
                            feedback_btn = gr.Button("Submit Feedback", elem_classes=["submit-btn"])
                            feedback_status = gr.Textbox(label="Status", interactive=False)

            # -------------------- Submit Event / Host Tab --------------------
            with gr.Tab("Submit Event/Host"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h3>📝 Submit Event Proposal</h3>
                            <p>RSOs, fraternities, and sororities - let's collab on some epic events!</p>
                        </div>
                        """)
                        
                        # Event Proposal Form
                        with gr.Row():
                            host_title = gr.Textbox(
                                label="Event Title",
                                placeholder="e.g., LMU vs Pepperdine Tailgate",
                                elem_classes=["feedback-input"]
                            )
                        
                        with gr.Row():
                            host_desc = gr.Textbox(
                                label="Description",
                                placeholder="Tell us about your event idea...",
                                lines=3,
                                elem_classes=["feedback-input"]
                            )
                        
                        with gr.Row():
                            host_date = gr.Textbox(
                                label="Proposed Date & Time",
                                placeholder="e.g., Friday, March 15th at 5:00 PM",
                                elem_classes=["feedback-input"]
                            )
                        
                        with gr.Row():
                            host_location = gr.Textbox(
                                label="Location",
                                placeholder="e.g., The Grove, Gersten Pavilion",
                                elem_classes=["feedback-input"]
                            )
                        
                        with gr.Row():
                            host_org = gr.Textbox(
                                label="Your Organization",
                                placeholder="e.g., Alpha Delta Pi, LMU Spirit Squad",
                                elem_classes=["feedback-input"]
                            )
                        
                        host_submit = gr.Button("🚀 Submit Proposal", elem_classes=["submit-btn"])
                        host_status = gr.Textbox(label="Status", interactive=False)
                    
                    with gr.Column(scale=1):
                        # Quick Tips
                        quick_tips = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>💡 Pro Tips</h4>
                            <div style="margin: 10px 0;">
                                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                    <h5>🎯 What Works Best</h5>
                                    <ul style="margin: 5px 0; padding-left: 20px; font-size: 0.9rem;">
                                        <li>Game day tailgates</li>
                                        <li>Study groups & tutoring</li>
                                        <li>Cultural celebrations</li>
                                        <li>Wellness activities</li>
                                        <li>Career workshops</li>
                                    </ul>
                                </div>
                                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                    <h5>⚡ Quick Approval</h5>
                                    <ul style="margin: 5px 0; padding-left: 20px; font-size: 0.9rem;">
                                        <li>Clear event description</li>
                                        <li>Specific date & time</li>
                                        <li>On-campus location</li>
                                        <li>Open to all students</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        """)
                        
                        # Success Stories
                        success_stories = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🏆 Success Stories</h4>
                            <div style="background: linear-gradient(135deg, #10b981, #059669); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                <h5>🎉 Recent Approvals</h5>
                                <div style="margin: 10px 0;">
                                    <p style="font-size: 0.9rem; margin: 5px 0;">🏈 LMU Spirit Squad Tailgate</p>
                                    <p style="font-size: 0.8rem; opacity: 0.8;">127 attendees • Approved in 2 hours</p>
                                </div>
                                <div style="margin: 10px 0;">
                                    <p style="font-size: 0.9rem; margin: 5px 0;">📚 Alpha Delta Pi Study Group</p>
                                    <p style="font-size: 0.8rem; opacity: 0.8;">45 attendees • Approved in 1 day</p>
                                </div>
                            </div>
                        </div>
                        """)

            # -------------------- Get Involved Tab --------------------
            with gr.Tab("Get Involved"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h3>🤝 Get Involved at LMU</h3>
                            <p>Find your people, start something new, or join existing groups!</p>
                        </div>
                        """)
                        
                        # RSO Interest Form
                        with gr.Row():
                            rso_form = gr.HTML("""
                            <div class="dashboard-card">
                                <h4>🏛️ RSO Interest</h4>
                                <p>Want your organization featured? Let's collab!</p>
                                <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                    <h5>📝 Quick Interest Form</h5>
                                    <p>Tell us about your org and what you'd like to do!</p>
                                    <a href="https://forms.gle/example" target="_blank" style="background: white; color: #667eea; text-decoration: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; display: inline-block; margin-top: 10px;">Fill Out Form</a>
                                </div>
                            </div>
                            """)
                        
                        # Greek Life Interest
                        with gr.Row():
                            greek_interest = gr.HTML("""
                            <div class="dashboard-card">
                                <h4>🏛️ Greek Life</h4>
                                <p>Interested in joining a fraternity or sorority?</p>
                                <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                    <h5>🐺 Rush Information</h5>
                                    <p>Get info about rush events and Greek life at LMU</p>
                                    <a href="https://forms.gle/example" target="_blank" style="background: white; color: #ff6b6b; text-decoration: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; display: inline-block; margin-top: 10px;">Learn More</a>
                                </div>
                            </div>
                            """)
                    
                    with gr.Column(scale=1):
                        # Campus Jobs
                        campus_jobs = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>💼 Campus Jobs</h4>
                            <div style="background: linear-gradient(135deg, #4ecdc4, #44a08d); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                <h5>💰 Get That Bag</h5>
                                <p>Find on-campus employment opportunities</p>
                                <a href="https://careers.lmu.edu" target="_blank" style="background: white; color: #4ecdc4; text-decoration: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; display: inline-block; margin-top: 10px;">Browse Jobs</a>
                            </div>
                        </div>
                        """)
                        
                        # Study Abroad
                        study_abroad = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>✈️ Study Abroad</h4>
                            <div style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                <h5>🌍 Level Up Your Experience</h5>
                                <p>Explore international programs and opportunities</p>
                                <a href="https://studyabroad.lmu.edu" target="_blank" style="background: white; color: #f093fb; text-decoration: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; display: inline-block; margin-top: 10px;">Explore Programs</a>
                            </div>
                        </div>
                        """)

            # -------------------- Community Board Tab --------------------
            with gr.Tab("Community Board (Beta)"):
                with gr.Row():
                    with gr.Column(scale=2):
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h3>🤝 Community Board</h3>
                            <p>Share memes, find study buddies, and connect with fellow Lions!</p>
                        </div>
                        """)
                        
                        # Community Posts
                        community_posts = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>📱 Recent Posts</h4>
                            <div style="margin: 10px 0;">
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 15px; margin: 10px 0;">
                                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; margin-right: 10px;">SJ</div>
                                        <div>
                                            <p style="font-weight: 600; margin: 0;">Sarah Johnson</p>
                                            <p style="font-size: 0.8rem; color: #666; margin: 0;">2 hours ago</p>
                                        </div>
                                    </div>
                                    <p style="margin: 0;">Anyone want to form a study group for the math final? The struggle is real fr fr 😅</p>
                                    <div style="display: flex; gap: 10px; margin-top: 10px;">
                                        <button style="background: #667eea; color: white; border: none; padding: 5px 10px; border-radius: 4px; font-size: 0.8rem;">👍 12</button>
                                        <button style="background: #10b981; color: white; border: none; padding: 5px 10px; border-radius: 4px; font-size: 0.8rem;">💬 Reply</button>
                                    </div>
                                </div>
                                
                                <div style="border: 1px solid #e1e5e9; border-radius: 8px; padding: 15px; margin: 10px 0;">
                                    <div style="display: flex; align-items: center; margin-bottom: 10px;">
                                        <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #ff6b6b, #ee5a24); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: 600; margin-right: 10px;">MJ</div>
                                        <div>
                                            <p style="font-weight: 600; margin: 0;">Mike Johnson</p>
                                            <p style="font-size: 0.8rem; color: #666; margin: 0;">5 hours ago</p>
                                        </div>
                                    </div>
                                    <p style="margin: 0;">The Rock at sunset hits different today 🌅 #BluffLife</p>
                                    <div style="background: #f8f9fa; height: 120px; border-radius: 8px; display: flex; align-items: center; justify-content: center; margin: 10px 0; color: #666;">📸 Photo</div>
                                    <div style="display: flex; gap: 10px; margin-top: 10px;">
                                        <button style="background: #667eea; color: white; border: none; padding: 5px 10px; border-radius: 4px; font-size: 0.8rem;">👍 28</button>
                                        <button style="background: #10b981; color: white; border: none; padding: 5px 10px; border-radius: 4px; font-size: 0.8rem;">💬 Reply</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """)
                    
                    with gr.Column(scale=1):
                        # Create Post
                        create_post = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>✍️ Create Post</h4>
                            <div style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                <h5>📝 Share Something</h5>
                                <textarea placeholder="What's on your mind?" style="width: 100%; padding: 10px; border: none; border-radius: 6px; margin: 10px 0; resize: vertical; min-height: 80px;"></textarea>
                                <button style="background: white; color: #667eea; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; width: 100%;">Post</button>
                            </div>
                        </div>
                        """)
                        
                        # Watch Party Signups
                        watch_party = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>📺 Watch Party Signups</h4>
                            <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 20px; border-radius: 12px; margin: 10px 0;">
                                <h5>🏈 Away Game Watch Party</h5>
                                <p>LMU vs Gonzaga • Saturday 8PM</p>
                                <p style="font-size: 0.9rem; opacity: 0.8;">📍 The Grove • 23 people signed up</p>
                                <button style="background: white; color: #ff6b6b; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; width: 100%; margin-top: 10px;">Join Watch Party</button>
                            </div>
                        </div>
                        """)
                        
                        # Q&A Section
                        qa_section = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>❓ Quick Q&A</h4>
                            <div style="margin: 10px 0;">
                                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                    <h5>🤔 Where's the best study spot?</h5>
                                    <p style="font-size: 0.9rem; color: #666; margin: 5px 0;">Burns Backcourt fr fr, 24/7 access</p>
                                </div>
                                <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; margin: 10px 0;">
                                    <h5>🍕 Best food on campus?</h5>
                                    <p style="font-size: 0.9rem; color: #666; margin: 5px 0;">The Lair pizza be bussin sometimes</p>
                                </div>
                            </div>
                        </div>
                        """)

        # -------------------- Event handlers --------------------
        def respond(message, history, user_id):
            if not message.strip():
                return history, ""

            # Get response from the app
            response = app.process_message(message, history, user_id)

            # Update history
            history.append([message, response])
            return history, ""

        def update_points(user_id):
            return app.get_user_points(user_id)

        def update_leaderboard():
            return app.get_leaderboard_html()

        # Connect event handlers
        submit_btn.click(
            respond,
            inputs=[user_input, chatbot, student_id],
            outputs=[chatbot, user_input]
        ).then(
            update_points,
            inputs=[student_id],
            outputs=[points_display, profile_points]
        )

        user_input.submit(
            respond,
            inputs=[user_input, chatbot, student_id],
            outputs=[chatbot, user_input]
        ).then(
            update_points,
            inputs=[student_id],
            outputs=[points_display, profile_points]
        )

        events_btn.click(
            app.get_events_this_week,
            outputs=[events_display]
        )

        leaderboard_refresh_btn.click(
            update_leaderboard,
            outputs=[leaderboard_display]
        )

        feed_refresh_btn.click(
            app.get_dynamic_feed_html,
            outputs=[feed_display]
        )

        refresh_profile_btn.click(
            update_points,
            inputs=[student_id],
            outputs=[profile_points]
        )

        feedback_btn.click(
            app.submit_feedback,
            inputs=[feedback_text, rating, student_id],
            outputs=[feedback_status]
        ).then(
            update_points,
            inputs=[student_id],
            outputs=[points_display, profile_points]
        )

        student_id.change(
            update_points,
            inputs=[student_id],
            outputs=[points_display, profile_points]
        )
    
    return interface

if __name__ == "__main__":
    # Create and launch the interface
    interface = create_interface()
    
    print("🦁 Starting LMU Campus LLM...")
    print("💡 Make sure Ollama is running with: ollama serve")
    print("📚 Loading LLaMA 3.2 model...")
    
    # Launch with public sharing for testing
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True if you want a public link
        show_api=False
    )
