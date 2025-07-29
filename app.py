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
            return "Please enter your student ID to track points!"
        return self.points_system.get_user_stats(user_id)
    
    def submit_feedback(self, feedback, rating, user_id=None):
        """Submit user feedback"""
        try:
            if not feedback or not feedback.strip():
                return "Please write some feedback before submitting! 📝"
                
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
                return "bet! thanks for the feedback - you earned 3 spirit points! 🎉✨"
            else:
                return "thanks for the feedback! (add your student ID to earn 3 points next time) 💫"
            
        except Exception as e:
            return f"oops, something went wrong submitting your feedback: {str(e)} 😅"
    
    def get_events_this_week(self):
        """Get upcoming events for this week"""
        try:
            events_file = "data/events/current_events.json"
            if not os.path.exists(events_file):
                return "no events data loaded yet, but check back soon! first fridays are coming up and they always slap 🎉"
            
            with open(events_file, 'r') as f:
                events = json.load(f)
            
            if not events:
                return "no events scheduled this week, but that's lowkey a good time to catch up on studying! 📚"
            
            event_list = "**what's happening on the bluff this week:**\n\n"
            for event in events[:5]:  # Show top 5 events
                event_list += f"**{event.get('title', 'mystery event lol')}**\n"
                event_list += f"📅 {event.get('date', 'date TBD')}\n"
                event_list += f"📍 {event.get('location', 'location TBD')}\n"
                if event.get('free_food'):
                    event_list += "🍕 free food!! (this one's gonna be packed)\n"
                event_list += f"⚡ earn {event.get('points', 5)} spirit points\n\n"
            
            event_list += "*psst... attend events to climb the leaderboard! 👑*"
            return event_list
            
        except Exception as e:
            return f"couldn't load events rn: {str(e)} 😅"

    # New method for leaderboard HTML
    def get_leaderboard_html(self, limit: int = 10):
        """Generate HTML representation of the leaderboard"""
        leaderboard = self.points_system.get_leaderboard(limit)
        if not leaderboard:
            return """
            <div class="dashboard-card animated">
                <h3>🏅 Spirit Leaderboard</h3>
                <p style="text-align: center; color: #718096; margin: 20px 0;">
                    No rankings yet - be the first to earn points! 🚀
                </p>
            </div>
            """

        html = """
        <div class="dashboard-card animated">
            <h3>🏅 Spirit Leaderboard</h3>
            <p style="color: #4a5568; margin-bottom: 15px;">Top Lions on campus - where do you rank? 👑</p>
            <table class='leaderboard'>
                <thead>
                    <tr>
                        <th>🏆 Rank</th>
                        <th>🦁 Lion</th>
                        <th>⚡ Points</th>
                        <th>🎯 Level</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        for entry in leaderboard:
            rank_emoji = "👑" if entry['rank'] == 1 else "🥈" if entry['rank'] == 2 else "🥉" if entry['rank'] == 3 else f"{entry['rank']}"
            html += f"""
                <tr class="leaderboard-row">
                    <td style="font-weight: 600;">{rank_emoji}</td>
                    <td style="font-weight: 500;">{entry['user_id']}</td>
                    <td style="font-weight: 600; color: #8B0000;">{entry['total_points']}</td>
                    <td>{entry['level']}</td>
                </tr>
            """
        
        html += """
                </tbody>
            </table>
            <p style="text-align: center; margin-top: 15px; color: #718096; font-size: 0.9rem;">
                💡 Ask questions, attend events, and give feedback to climb the rankings!
            </p>
        </div>
        """
        return html

    # New method: prizes catalog HTML
    def get_prizes_html(self):
        """Return HTML table of available prizes from points system"""
        prizes = self.points_system.get_reward_catalog()
        if not prizes:
            return """
            <div class="dashboard-card animated">
                <h3>🎁 Spirit Shop</h3>
                <p style="text-align: center; color: #718096; margin: 20px 0;">
                    Prize catalog coming soon! Keep earning points! 💎
                </p>
            </div>
            """
        
        html = """
        <div class="dashboard-card animated">
            <h3>🎁 Spirit Shop</h3>
            <p style="color: #4a5568; margin-bottom: 20px;">Redeem your points for amazing rewards! ✨</p>
            <div style="display: grid; gap: 15px;">
        """
        
        for pts, reward in sorted(prizes.items()):
            html += f"""
                <div style="background: linear-gradient(45deg, #f7fafc, #edf2f7); border-radius: 12px; padding: 15px; border: 1px solid #e2e8f0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="font-weight: 600; color: #2d3748;">{reward}</span>
                        </div>
                        <div style="background: linear-gradient(45deg, #8B0000, #a61b1b); color: white; padding: 6px 12px; border-radius: 20px; font-weight: 600; font-size: 0.9rem;">
                            {pts} pts
                        </div>
                    </div>
                </div>
            """
        
        html += """
            </div>
            <p style="text-align: center; margin-top: 20px; color: #718096; font-size: 0.9rem;">
                🔥 More exclusive prizes coming soon - stay tuned!
            </p>
        </div>
        """
        return html

    # New method: dynamic dashboard feed (events + leaderboard highlight)
    def get_dynamic_feed_html(self):
        """Combine upcoming events and leaderboard snippet for dashboard"""
        events_md = self.get_events_this_week()
        leaderboard_html = self.get_leaderboard_html(limit=3)
        
        return f"""
        <div class="feed-container">
            <div class="dashboard-card animated">
                <h3>📅 This Week on the Bluff</h3>
                <div style="color: #4a5568; line-height: 1.6;">
                    {events_md if events_md else "<p style='text-align: center; color: #718096;'>No events this week - check back soon! 🎉</p>"}
                </div>
            </div>
            <div>
                {leaderboard_html}
            </div>
        </div>
        """

def create_interface():
    """Create and configure the Gradio interface"""
    app = CampusLLMApp()
    
    # Custom CSS for modern, sleek design inspired by Claude AI/ChatGPT
    css = """
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    .gradio-container {
        max-width: 1400px !important;
        margin: auto !important;
        padding: 20px !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        min-height: 100vh;
    }
    
    /* Header styling */
    .header {
        text-align: center;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        color: #2d3748;
        padding: 30px;
        border-radius: 20px;
        margin-bottom: 30px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #8B0000, #FFD700);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    
    .header p {
        font-size: 1.1rem;
        color: #4a5568;
        font-weight: 400;
    }
    
    /* Main container styling */
    .main-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Chat interface styling */
    .chatbot {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }
    
    /* Input styling */
    .input-row {
        background: #f8fafc;
        border-radius: 12px;
        padding: 8px;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .input-row:focus-within {
        border-color: #8B0000;
        box-shadow: 0 0 0 3px rgba(139, 0, 0, 0.1);
    }
    
    /* Button styling */
    .primary-btn {
        background: linear-gradient(45deg, #8B0000, #a61b1b);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(139, 0, 0, 0.2);
    }
    
    .primary-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(139, 0, 0, 0.3);
    }
    
    .secondary-btn {
        background: rgba(255, 255, 255, 0.9);
        color: #4a5568;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .secondary-btn:hover {
        background: #f7fafc;
        border-color: #cbd5e0;
        transform: translateY(-1px);
    }
    
    /* Points display */
    .points-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
        border: none;
    }
    
    .points-display h3 {
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 10px;
    }
    
    .points-display ul {
        text-align: left;
        padding-left: 20px;
    }
    
    /* Tab styling */
    .tab-nav button {
        background: rgba(255, 255, 255, 0.8);
        border: 2px solid #e2e8f0;
        border-radius: 12px 12px 0 0;
        color: #4a5568;
        font-weight: 500;
        padding: 12px 20px;
        margin-right: 4px;
        transition: all 0.3s ease;
    }
    
    .tab-nav button.selected {
        background: linear-gradient(45deg, #8B0000, #a61b1b);
        color: white;
        border-color: #8B0000;
    }
    
    /* Leaderboard styling */
    .leaderboard {
        width: 100%;
        border-collapse: collapse;
        margin-top: 15px;
        background: white;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }
    
    .leaderboard th {
        background: linear-gradient(45deg, #8B0000, #a61b1b);
        color: white;
        padding: 15px 12px;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.9rem;
        letter-spacing: 0.5px;
    }
    
    .leaderboard td {
        padding: 12px;
        border-bottom: 1px solid #f1f5f9;
        text-align: center;
        font-weight: 500;
    }
    
    .leaderboard tr:hover {
        background: #f8fafc;
        transition: all 0.2s ease;
    }
    
    .leaderboard tr:nth-child(even) {
        background: #fafbfc;
    }
    
    /* Dashboard cards */
    .dashboard-card {
        background: white;
        border-radius: 16px;
        padding: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .dashboard-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.1);
    }
    
    .dashboard-card h3 {
        color: #2d3748;
        font-weight: 600;
        font-size: 1.2rem;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* Feed layout */
    .feed-container {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 25px;
        margin-top: 20px;
    }
    
    @media (max-width: 768px) {
        .feed-container {
            grid-template-columns: 1fr;
        }
    }
    
    /* Examples styling */
    .examples-container {
        background: #f8fafc;
        border-radius: 12px;
        padding: 20px;
        margin-top: 20px;
    }
    
    .examples-container .example {
        background: white;
        border-radius: 8px;
        padding: 10px 15px;
        margin: 5px 0;
        border: 1px solid #e2e8f0;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .examples-container .example:hover {
        background: #f1f5f9;
        border-color: #cbd5e0;
        transform: translateX(4px);
    }
    
    /* Accordion styling */
    .accordion {
        background: white;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
        margin: 10px 0;
    }
    
    .accordion summary {
        background: #f8fafc;
        padding: 15px 20px;
        font-weight: 600;
        color: #2d3748;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .accordion summary:hover {
        background: #f1f5f9;
    }
    
    .accordion[open] summary {
        background: linear-gradient(45deg, #8B0000, #a61b1b);
        color: white;
    }
    
    /* Animations */
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animated {
        animation: slideIn 0.5s ease-out;
    }
    
    /* Status messages */
    .status-success {
        background: linear-gradient(45deg, #48bb78, #38a169);
        color: white;
        padding: 15px;
        border-radius: 12px;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(72, 187, 120, 0.3);
    }
    
    .status-error {
        background: linear-gradient(45deg, #f56565, #e53e3e);
        color: white;
        padding: 15px;
        border-radius: 12px;
        font-weight: 500;
        box-shadow: 0 4px 15px rgba(245, 101, 101, 0.3);
    }
    
    /* Responsive design */
    @media (max-width: 1024px) {
        .gradio-container {
            padding: 15px !important;
        }
        
        .header h1 {
            font-size: 2rem;
        }
        
        .main-container {
            padding: 20px;
        }
    }
    
    @media (max-width: 768px) {
        .header {
            padding: 20px;
        }
        
        .header h1 {
            font-size: 1.8rem;
        }
        
        .main-container {
            padding: 15px;
        }
        
        .points-display {
            padding: 15px;
        }
    }
    """
    
    with gr.Blocks(css=css, title="LMU Campus LLM") as interface:
        # Header
        gr.HTML("""
        <div class="header animated">
            <h1>🦁 LMU Campus AI</h1>
            <p>your lowkey helpful friend on the bluff - ask me anything about LMU life! no cap 💯</p>
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
                value="""
                <div class='points-display'>
                    <h3>🏆 Your Points</h3>
                    <p>Enter your student ID to track points!</p>
                </div>
                """,
                label="Points"
            )


        with gr.Tabs():
            # -------------------- Home / Dashboard Tab --------------------
            with gr.Tab("Home/Dashboard"):
                with gr.Row():
                    with gr.Column(scale=2):
                        # Main chat interface
                        chatbot = gr.Chatbot(
                            label="Chat with LMU Assistant",
                            height=400,
                            show_label=True
                        )

                        with gr.Row():
                            user_input = gr.Textbox(
                                placeholder="ask me anything about LMU! (like 'where's the best study spot?' or 'how do i add/drop classes?')",
                                container=False,
                                scale=4,
                                elem_classes=["input-row"]
                            )
                            submit_btn = gr.Button("Ask 🚀", variant="primary", scale=1, elem_classes=["primary-btn"])

                        # Example questions
                        gr.Examples(
                            examples=[
                                "where's the best study spot that actually has good wifi?",
                                "what's the tea on study abroad requirements?", 
                                "what events are happening this week on the bluff?",
                                "how do i file an academic grievance? (asking for a friend)",
                                "where's the counseling center? lowkey need it",
                                "what are doheny's hours during finals week?",
                                "how do i add/drop classes without my advisor judging me?",
                                "draft an email to my prof asking for an extension",
                                "where can i get free food on campus rn?",
                                "what's the vibe with first fridays?",
                                "best coffee spots near campus?",
                                "how do i get lion dollars on my card?"
                            ],
                            inputs=user_input,
                            label="try these questions (or ask literally anything about LMU):"
                        )

                    with gr.Column(scale=1):
                        # Dashboard feed
                        feed_refresh_btn = gr.Button("🔄 refresh feed", variant="secondary", elem_classes=["secondary-btn"])
                        feed_display = gr.HTML(value=app.get_dynamic_feed_html())

            # -------------------- Events Tab --------------------
            with gr.Tab("Events"):
                events_btn = gr.Button("🎉 what's happening this week?", variant="secondary", elem_classes=["secondary-btn"])
                events_display = gr.Markdown(label="Upcoming Events")

            # -------------------- Game Day Tab --------------------
            with gr.Tab("Game Day"):
                game_day_placeholder = gr.HTML("""
                <div class="dashboard-card animated">
                    <h3>🏈 game day features coming soon!</h3>
                    <p style="color: #4a5568;">stay tuned for real-time check-ins, live challenges, and more lions spirit! 🦁</p>
                </div>
                """)

            # -------------------- Leaderboard Tab --------------------
            with gr.Tab("Leaderboard"):
                leaderboard_refresh_btn = gr.Button("🔄 refresh rankings", elem_classes=["secondary-btn"])
                leaderboard_display = gr.HTML(value=app.get_leaderboard_html())

            # -------------------- Prizes Tab --------------------
            with gr.Tab("Prizes"):
                prizes_display = gr.HTML(value=app.get_prizes_html())

            # -------------------- My Profile Tab --------------------
            with gr.Tab("My Profile"):
                gr.Markdown("## your stats & feedback")
                profile_points = gr.HTML(value="""<div class='dashboard-card animated'>enter your ID above ☝️ and ask a question to see your spirit points!</div>""")

                def sync_profile(user_id):
                    return app.get_user_points(user_id)
                # Button to refresh profile stats
                refresh_profile_btn = gr.Button("🔄 refresh my stats", elem_classes=["secondary-btn"])

                with gr.Accordion("📝 drop some feedback", open=False):
                    feedback_text = gr.Textbox(
                        label="your thoughts",
                        placeholder="how can we make this even better? spill the tea ☕",
                        lines=3
                    )
                    rating = gr.Slider(
                        minimum=1,
                        maximum=5,
                        value=5,
                        step=1,
                        label="rating (1-5 stars)"
                    )
                    feedback_btn = gr.Button("submit feedback ✨", elem_classes=["primary-btn"])
                    feedback_status = gr.Textbox(label="Status", interactive=False)

            # -------------------- Submit Event / Host Tab --------------------
            with gr.Tab("Submit Event/Host"):
                gr.Markdown("### propose a collab event 📝")
                host_title = gr.Textbox(label="event title", placeholder="what's the vibe?")
                host_desc = gr.Textbox(label="description", lines=3, placeholder="tell us more about this event!")
                host_date = gr.Textbox(label="date & time", placeholder="when's it happening?")
                host_submit = gr.Button("submit proposal (coming soon) 🚀", elem_classes=["primary-btn"])
                host_status = gr.Textbox(label="status", interactive=False)

            # -------------------- Community Board Tab --------------------
            with gr.Tab("Community Board (Beta)"):
                gr.HTML("""
                <div class="dashboard-card animated">
                    <h3>🤝 community wall coming soon!</h3>
                    <p style="color: #4a5568;">share memes, watch-party signups, and more campus vibes! 📱</p>
                    <p style="color: #718096; font-size: 0.9rem; margin-top: 15px;">
                        this is gonna be the spot for student-to-student connections ✨
                    </p>
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
            if user_id:
                stats = app.get_user_points(user_id)
                return f"""
                <div class="points-display animated">
                    <h3>🏆 Your Spirit Points</h3>
                    <div style="font-size: 1.1rem; margin: 10px 0;">{stats}</div>
                    <hr style="border: 1px solid rgba(255,255,255,0.3); margin: 15px 0;">
                    <p><b>Earn more points by:</b></p>
                    <ul style="text-align: left; color: rgba(255,255,255,0.9);">
                        <li>💬 Asking questions (1 pt each)</li>
                        <li>🎉 Attending events (5-10 pts)</li>
                        <li>📝 Giving feedback (3 pts)</li>
                        <li>🔥 Daily streak bonus (2 pts)</li>
                    </ul>
                </div>
                """
            return """
                <div class="points-display animated">
                    <h3>🏆 Spirit Points</h3>
                    <p style="margin: 15px 0;">Enter your student ID above to start tracking points! 📊</p>
                    <p style="font-size: 0.9rem; opacity: 0.8;">Join the campus leaderboard and earn rewards! 🎁</p>
                </div>
                """

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
