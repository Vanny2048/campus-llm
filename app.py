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
            
            event_list = "🎉 **Upcoming LMU Events This Week:**\n\n"
            for event in events[:5]:  # Show top 5 events
                event_list += f"**{event.get('title', 'Unknown Event')}**\n"
                event_list += f"📅 {event.get('date', 'TBD')}\n"
                event_list += f"📍 {event.get('location', 'TBD')}\n"
                if event.get('free_food'):
                    event_list += "🍕 Free food!\n"
                event_list += f"Points: {event.get('points', 5)}\n\n"
            
            return event_list
            
        except Exception as e:
            return f"Error loading events: {str(e)}"

    # New method for leaderboard HTML
    def get_leaderboard_html(self, limit: int = 10):
        """Generate HTML representation of the leaderboard"""
        leaderboard = self.points_system.get_leaderboard(limit)
        if not leaderboard:
            return "<p>No leaderboard data available yet.</p>"

        html = """
        <div class="leaderboard-container">
            <h3>🏅 Leaderboard</h3>
            <div class="leaderboard-table">
                <div class="leaderboard-header">
                    <div class="rank-col">Rank</div>
                    <div class="user-col">User</div>
                    <div class="points-col">Points</div>
                    <div class="level-col">Level</div>
                </div>
        """
        for i, entry in enumerate(leaderboard):
            rank_class = "rank-" + str(min(i + 1, 3)) if i < 3 else ""
            html += f"""
                <div class="leaderboard-row {rank_class}">
                    <div class="rank-col">#{entry['rank']}</div>
                    <div class="user-col">{entry['user_id']}</div>
                    <div class="points-col">{entry['total_points']}</div>
                    <div class="level-col">{entry['level']}</div>
                </div>
            """
        html += "</div></div>"
        return html

    # New method: prizes catalog HTML
    def get_prizes_html(self):
        """Return HTML table of available prizes from points system"""
        prizes = self.points_system.get_reward_catalog()
        if not prizes:
            return "<p>No prizes available yet.</p>"
        html = """
        <div class="prizes-container">
            <h3>🎁 Prize Shop</h3>
            <div class="prizes-grid">
        """
        for pts, reward in sorted(prizes.items()):
            html += f"""
                <div class="prize-card">
                    <div class="prize-points">{pts} pts</div>
                    <div class="prize-name">{reward}</div>
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
        <div class="dashboard-grid">
            <div class="dashboard-card events-card">
                <h3>📅 This Week's Events</h3>
                <div class="card-content">{events_md}</div>
            </div>
            <div class="dashboard-card leaderboard-card">
                {leaderboard_html}
            </div>
        </div>
        """

def create_interface():
    """Create and configure the Gradio interface"""
    app = CampusLLMApp()
    
    # Modern CSS for sleek design like Claude AI/ChatGPT
    css = """
    /* Modern Reset and Base Styles */
    * {
        box-sizing: border-box;
    }
    
    .gradio-container {
        max-width: 1400px !important;
        margin: auto !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    /* Header Styles */
    .header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(45deg, #fff, #f0f0f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        opacity: 0.9;
    }
    
    /* Points Display */
    .points-display {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .points-display h3 {
        margin: 0 0 1rem 0;
        font-size: 1.3rem;
    }
    
    /* Chat Interface */
    .chat-container {
        background: white;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        overflow: hidden;
    }
    
    .chatbot {
        border: none !important;
        border-radius: 20px !important;
        background: #f8fafc !important;
    }
    
    /* Input Styling */
    .input-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .textbox {
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .textbox:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Button Styling */
    .btn-primary {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    .btn-primary:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    .btn-secondary {
        background: #f1f5f9 !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        color: #475569 !important;
        transition: all 0.3s ease !important;
    }
    
    .btn-secondary:hover {
        background: #e2e8f0 !important;
        transform: translateY(-1px) !important;
    }
    
    /* Tab Styling */
    .tabs {
        background: white !important;
        border-radius: 20px !important;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1) !important;
        overflow: hidden !important;
    }
    
    .tab-nav {
        background: #f8fafc !important;
        border-bottom: 1px solid #e2e8f0 !important;
    }
    
    .tab-nav button {
        background: transparent !important;
        border: none !important;
        padding: 1rem 1.5rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        transition: all 0.3s ease !important;
        border-radius: 0 !important;
    }
    
    .tab-nav button.selected {
        background: white !important;
        color: #667eea !important;
        border-bottom: 3px solid #667eea !important;
    }
    
    /* Dashboard Grid */
    .dashboard-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1.5rem;
        margin-top: 1rem;
    }
    
    .dashboard-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
    }
    
    .dashboard-card h3 {
        margin: 0 0 1rem 0;
        color: #1e293b;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    /* Leaderboard Styling */
    .leaderboard-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
    }
    
    .leaderboard-table {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .leaderboard-header {
        display: grid;
        grid-template-columns: 80px 1fr 100px 80px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        font-weight: 600;
    }
    
    .leaderboard-row {
        display: grid;
        grid-template-columns: 80px 1fr 100px 80px;
        padding: 1rem;
        border-bottom: 1px solid #e2e8f0;
        transition: background 0.3s ease;
    }
    
    .leaderboard-row:hover {
        background: #f8fafc;
    }
    
    .leaderboard-row.rank-1 {
        background: linear-gradient(135deg, #ffd700 0%, #ffed4e 100%);
        color: #1e293b;
        font-weight: 600;
    }
    
    .leaderboard-row.rank-2 {
        background: linear-gradient(135deg, #c0c0c0 0%, #e5e5e5 100%);
        color: #1e293b;
        font-weight: 600;
    }
    
    .leaderboard-row.rank-3 {
        background: linear-gradient(135deg, #cd7f32 0%, #daa520 100%);
        color: white;
        font-weight: 600;
    }
    
    /* Prizes Grid */
    .prizes-container {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
    }
    
    .prizes-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .prize-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        border: 2px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .prize-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        border-color: #667eea;
    }
    
    .prize-points {
        font-size: 1.5rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .prize-name {
        color: #475569;
        font-weight: 500;
    }
    
    /* Examples Styling */
    .examples {
        background: #f8fafc;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    .examples button {
        background: white !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 0.5rem 1rem !important;
        margin: 0.25rem !important;
        font-size: 0.9rem !important;
        transition: all 0.3s ease !important;
    }
    
    .examples button:hover {
        background: #667eea !important;
        color: white !important;
        border-color: #667eea !important;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .dashboard-grid {
            grid-template-columns: 1fr;
        }
        
        .leaderboard-header,
        .leaderboard-row {
            grid-template-columns: 60px 1fr 80px 60px;
            font-size: 0.9rem;
        }
        
        .prizes-grid {
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        }
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .dashboard-card,
    .leaderboard-container,
    .prizes-container {
        animation: fadeIn 0.5s ease-out;
    }
    """
    
    with gr.Blocks(css=css, title="LMU Campus LLM") as interface:
        # Header
        gr.HTML("""
        <div class="header">
            <h1>🦁 LMU Campus LLM</h1>
            <p>Your AI assistant for everything LMU - built by students, for students!</p>
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
                            height=500,
                            show_label=True
                        )

                        with gr.Row():
                            user_input = gr.Textbox(
                                placeholder="Ask me anything about LMU! (e.g., 'Where can I find tutoring?')",
                                container=False,
                                scale=4
                            )
                            submit_btn = gr.Button("Ask", variant="primary", scale=1)

                        # Example questions
                        gr.Examples(
                            examples=[
                                "Where can I find a math tutor?",
                                "What's the GPA requirement for study abroad?",
                                "What events are happening this week?",
                                "How do I file an academic grievance?",
                                "Where is the counseling center?",
                                "What are the library hours?",
                                "How do I add/drop a class?",
                                "Draft an email to my professor asking for help"
                            ],
                            inputs=user_input,
                            label="Try these example questions:"
                        )

                    with gr.Column(scale=1):
                        # Dashboard feed
                        feed_refresh_btn = gr.Button("🔄 Refresh Feed", variant="secondary")
                        feed_display = gr.HTML(value=app.get_dynamic_feed_html())

            # -------------------- Events Tab --------------------
            with gr.Tab("Events"):
                events_btn = gr.Button("🎉 Show This Week's Events", variant="secondary")
                events_display = gr.Markdown(label="Upcoming Events")

            # -------------------- Game Day Tab --------------------
            with gr.Tab("Game Day"):
                game_day_placeholder = gr.HTML("""
                <div class="dashboard-card">
                    <h3>🏈 Game Day features coming soon!</h3>
                    <p>Stay tuned for real-time check-ins, live challenges, and more.</p>
                </div>
                """)

            # -------------------- Leaderboard Tab --------------------
            with gr.Tab("Leaderboard"):
                leaderboard_refresh_btn = gr.Button("🔄 Refresh Leaderboard")
                leaderboard_display = gr.HTML(value=app.get_leaderboard_html())

            # -------------------- Prizes Tab --------------------
            with gr.Tab("Prizes"):
                prizes_display = gr.HTML(value=app.get_prizes_html())

            # -------------------- My Profile Tab --------------------
            with gr.Tab("My Profile"):
                gr.Markdown("## Your Stats & Feedback")
                profile_points = gr.HTML(value="""<div class='points-display'>Enter your ID above ☝️ and ask a question to see points.</div>""")

                def sync_profile(user_id):
                    return app.get_user_points(user_id)
                # Button to refresh profile stats
                refresh_profile_btn = gr.Button("🔄 Refresh My Stats")

                with gr.Accordion("📝 Give Feedback", open=False):
                    feedback_text = gr.Textbox(
                        label="Your feedback",
                        placeholder="How can we improve the LMU Campus LLM?",
                        lines=3
                    )
                    rating = gr.Slider(
                        minimum=1,
                        maximum=5,
                        value=5,
                        step=1,
                        label="Rating (1-5 stars)"
                    )
                    feedback_btn = gr.Button("Submit Feedback")
                    feedback_status = gr.Textbox(label="Status", interactive=False)

            # -------------------- Submit Event / Host Tab --------------------
            with gr.Tab("Submit Event/Host"):
                gr.Markdown("### Propose a Collab Event 📝")
                host_title = gr.Textbox(label="Event Title")
                host_desc = gr.Textbox(label="Description", lines=3)
                host_date = gr.Textbox(label="Date & Time")
                host_submit = gr.Button("Submit Proposal (Coming Soon)")
                host_status = gr.Textbox(label="Status", interactive=False)

            # -------------------- Community Board Tab --------------------
            with gr.Tab("Community Board (Beta)"):
                gr.HTML("""
                <div class="dashboard-card">
                    <h3>🤝 Community wall coming soon!</h3>
                    <p>Share memes, watch-party signups, and more.</p>
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
                <div class="points-display">
                    <h3>🏆 Your Points</h3>
                    <p>{stats}</p>
                    <hr>
                    <p><b>Earn points by:</b></p>
                    <ul style="text-align: left;">
                        <li>Asking questions (1 pt)</li>
                        <li>Attending events (5-10 pts)</li>
                        <li>Giving feedback (3 pts)</li>
                    </ul>
                </div>
                """
            return points_display.value

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
