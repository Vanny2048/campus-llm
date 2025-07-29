#!/usr/bin/env python3
"""
LMU Campus LLM - Main Application
A student-centered AI assistant for Loyola Marymount University

Author: Vanessa Akaraiwe
"""

import gradio as gr
import json
import os
from datetime import datetime
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
                <h3>🏆 Your Points</h3>
                <p>Enter your student ID above ☝️ to track points!</p>
                <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.2); margin: 12px 0;">
                <p style="font-weight: 600; margin-bottom: 8px;">💡 Earn points by:</p>
                <ul style="text-align: left; margin: 0; padding-left: 20px;">
                    <li>Asking questions (1 pt)</li>
                    <li>Attending events (5-10 pts)</li>
                    <li>Giving feedback (3 pts)</li>
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
                <h3>🏆 Your Points</h3>
                <p style="font-size: 2rem; font-weight: 700; margin: 10px 0;">{points} pts</p>
                <p style="font-size: 0.9rem; opacity: 0.8;">Rank #{rank_info.get('rank', 'N/A')} of {rank_info.get('total_users', 0)} students</p>
                <hr style="border: none; border-top: 1px solid rgba(255,255,255,0.2); margin: 12px 0;">
                <p style="font-weight: 600; margin-bottom: 8px;">💡 Earn points by:</p>
                <ul style="text-align: left; margin: 0; padding-left: 20px;">
                    <li>Asking questions (1 pt)</li>
                    <li>Attending events (5-10 pts)</li>
                    <li>Giving feedback (3 pts)</li>
                </ul>
            </div>
            """
        except Exception as e:
            return f"""
            <div class="points-display">
                <h3>🏆 Your Points</h3>
                <p>Error loading stats: {str(e)}</p>
            </div>
            """
    
    def submit_feedback(self, feedback, rating, user_id=None):
        """Submit user feedback"""
        try:
            feedback_data = {
                "feedback": feedback,
                "rating": rating,
                "user_id": user_id,
                "timestamp": datetime.now().isoformat()
            }
            
            # Save feedback
            feedback_file = "data/student_feedback/feedback.json"
            if os.path.exists(feedback_file):
                with open(feedback_file, 'r') as f:
                    all_feedback = json.load(f)
            else:
                all_feedback = []
            
            all_feedback.append(feedback_data)
            
            with open(feedback_file, 'w') as f:
                json.dump(all_feedback, f, indent=2)
            
            # Award points for feedback
            if user_id:
                self.points_system.add_points(user_id, 3, "feedback_submitted")
            
            return "Thank you for your feedback! You earned 3 points! 🎉"
            
        except Exception as e:
            return f"Error submitting feedback: {str(e)}"
    
    def get_events_this_week(self):
        """Get upcoming events for this week"""
        try:
            events_file = "data/events/current_events.json"
            if not os.path.exists(events_file):
                return "No events data available yet. Check back soon!"
            
            with open(events_file, 'r') as f:
                events = json.load(f)
            
            if not events:
                return "No events scheduled for this week."
            
            event_list = "🎉 **This Week's Vibes:**\n\n"
            for event in events[:5]:  # Show top 5 events
                event_list += f"**{event.get('title', 'Unknown Event')}**\n"
                event_list += f"📅 {event.get('date', 'TBD')}\n"
                event_list += f"📍 {event.get('location', 'TBD')}\n"
                if event.get('free_food'):
                    event_list += "🍕 Free food fr fr!\n"
                event_list += f"Points: {event.get('points', 5)}\n\n"
            
            return event_list
            
        except Exception as e:
            return f"Error loading events: {str(e)}"

    # New method for leaderboard HTML
    def get_leaderboard_html(self, limit: int = 10):
        """Generate HTML representation of the leaderboard"""
        # Add some sample data if leaderboard is empty
        self._ensure_sample_data()
        
        leaderboard = self.points_system.get_leaderboard(limit)
        if not leaderboard:
            return "<div class='dashboard-card'><p>No leaderboard data available yet.</p></div>"

        html = """
        <div class='dashboard-card'>
            <h3 style="margin: 0 0 16px 0; color: #667eea;">🏅 Spirit Leaderboard</h3>
            <table class='leaderboard'>
                <tr>
                    <th>Rank</th>
                    <th>Student</th>
                    <th>Points</th>
                    <th>Level</th>
                    <th>Activity</th>
                </tr>
        """
        for entry in leaderboard:
            rank_emoji = "🥇" if entry['rank'] == 1 else "🥈" if entry['rank'] == 2 else "🥉" if entry['rank'] == 3 else f"#{entry['rank']}"
            activity = f"Q: {entry['questions_asked']} | E: {entry['events_attended']} | F: {entry['feedback_submitted']}"
            html += f"""
            <tr>
                <td style="font-weight: bold; font-size: 1.2em;">{rank_emoji}</td>
                <td style="font-weight: 600;">{entry['user_id']}</td>
                <td style="font-weight: bold; color: #667eea;">{entry['total_points']} pts</td>
                <td><span style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 4px 8px; border-radius: 6px; font-size: 0.8em;">{entry['level']}</span></td>
                <td style="font-size: 0.9em; color: #666;">{activity}</td>
            </tr>
            """
        html += "</table></div>"
        return html

    def _ensure_sample_data(self):
        """Add sample data to the database for testing"""
        try:
            # Check if we already have data
            leaderboard = self.points_system.get_leaderboard(5)
            if len(leaderboard) > 0:
                return  # Already has data
            
            # Add sample users
            sample_users = [
                ("12345", 245, 15, 8, 3),  # Sarah Johnson
                ("67890", 189, 12, 6, 2),  # Mike Chen
                ("11111", 156, 10, 5, 1),  # Alex Rodriguez
                ("22222", 134, 8, 4, 2),   # Emma Wilson
                ("33333", 98, 6, 3, 1),    # David Kim
                ("44444", 87, 5, 2, 1),    # Lisa Park
                ("55555", 76, 4, 2, 0),    # James Brown
                ("66666", 65, 3, 1, 1),    # Maria Garcia
                ("77777", 54, 2, 1, 0),    # Tom Anderson
                ("88888", 43, 1, 1, 0),    # Rachel Green
            ]
            
            for user_id, points, questions, events, feedback in sample_users:
                # Add points for questions
                for _ in range(questions):
                    self.points_system.add_points(user_id, 1, "question_asked", "Sample question")
                
                # Add points for events
                for _ in range(events):
                    self.points_system.add_points(user_id, 5, "event_attended", "Sample event")
                
                # Add points for feedback
                for _ in range(feedback):
                    self.points_system.add_points(user_id, 3, "feedback_submitted", "Sample feedback")
                
                # Add remaining points to reach target
                current_points = questions + (events * 5) + (feedback * 3)
                if current_points < points:
                    self.points_system.add_points(user_id, points - current_points, "bonus", "Sample bonus")
            
            print("✅ Sample data added to leaderboard")
            
        except Exception as e:
            print(f"Error adding sample data: {e}")

    # New method: prizes catalog HTML
    def get_prizes_html(self):
        """Return HTML table of available prizes from points system"""
        prizes = self.points_system.get_reward_catalog()
        if not prizes:
            return "<div class='dashboard-card'><p>No prizes available yet.</p></div>"
        
        html = """
        <div class='dashboard-card'>
            <h3 style="margin: 0 0 16px 0; color: #667eea;">🎁 Available Rewards</h3>
            <div style="display: grid; gap: 16px;">
        """
        
        for pts, reward in sorted(prizes.items()):
            # Determine color based on points required
            if pts <= 50:
                color = "linear-gradient(135deg, #10b981, #059669)"  # Green
            elif pts <= 100:
                color = "linear-gradient(135deg, #f59e0b, #d97706)"  # Orange
            elif pts <= 200:
                color = "linear-gradient(135deg, #667eea, #764ba2)"  # Purple
            else:
                color = "linear-gradient(135deg, #8b5cf6, #7c3aed)"  # Violet
            
            html += f"""
            <div style="background: {color}; color: white; padding: 20px; border-radius: 12px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h4 style="margin: 0 0 8px 0;">{reward}</h4>
                    <p style="margin: 0; opacity: 0.9; font-size: 0.9rem;">Exclusive LMU experience</p>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 1.5rem; font-weight: 700;">{pts}</div>
                    <div style="font-size: 0.8rem; opacity: 0.8;">points</div>
                </div>
            </div>
            """
        
        html += "</div></div>"
        return html

    # New method: dynamic dashboard feed (events + leaderboard highlight)
    def get_dynamic_feed_html(self):
        """Combine upcoming events and leaderboard snippet for dashboard"""
        events_md = self.get_events_this_week()
        leaderboard_html = self.get_leaderboard_html(limit=3)
        return f"""
        <div style='display:flex;gap:24px;flex-wrap:wrap;'>
            <div style='flex:1;min-width:300px'>
                <div class='dashboard-card'>
                    <h3 style="margin: 0 0 16px 0; color: #667eea;">📅 This Week</h3>
                    {events_md}
                </div>
            </div>
            <div style='flex:1;min-width:300px'>
                {leaderboard_html}
            </div>
        </div>
        """

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
