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
        <h3>🏅 Leaderboard</h3>
        <table class='leaderboard'>
            <tr>
                <th>Rank</th>
                <th>User</th>
                <th>Points</th>
                <th>Level</th>
            </tr>
        """
        for entry in leaderboard:
            html += f"<tr><td>{entry['rank']}</td><td>{entry['user_id']}</td><td>{entry['total_points']}</td><td>{entry['level']}</td></tr>"
        html += "</table>"
        return html

def create_interface():
    """Create and configure the Gradio interface"""
    app = CampusLLMApp()
    
    # Custom CSS for LMU branding
    css = """
    .gradio-container {
        max-width: 1200px !important;
        margin: auto !important;
    }
    .header {
        text-align: center;
        background: linear-gradient(90deg, #8B0000, #FFD700);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .points-display {
        background: #f0f8ff;
        border: 2px solid #8B0000;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    }
    .leaderboard {
        width: 100%;
        border-collapse: collapse;
        margin-top: 10px;
    }
    .leaderboard th, .leaderboard td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: center;
    }
    .leaderboard th {
        background: #8B0000;
        color: white;
    }
    .leaderboard tr:nth-child(even) {
        background: #f9f9f9;
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
                        # Student ID input
                        student_id = gr.Textbox(
                            label="Student ID (Optional)",
                            placeholder="Enter your ID to track points",
                            type="text"
                        )

                        # Points display
                        points_display = gr.HTML(
                            value="""
                            <div class="points-display">
                                <h3>🏆 Your Points</h3>
                                <p>Enter your student ID to track points!</p>
                                <hr>
                                <p><b>Earn points by:</b></p>
                                <ul style="text-align: left;">
                                    <li>Asking questions (1 pt)</li>
                                    <li>Attending events (5-10 pts)</li>
                                    <li>Giving feedback (3 pts)</li>
                                </ul>
                            </div>
                            """,
                            label="Points Status"
                        )

                        # Feedback section
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

            # -------------------- Events Tab --------------------
            with gr.Tab("Events"):
                events_btn = gr.Button("🎉 Show This Week's Events", variant="secondary")
                events_display = gr.Markdown(label="Upcoming Events")

            # -------------------- Game Day Tab --------------------
            with gr.Tab("Game Day"):
                game_day_placeholder = gr.HTML("""
                <h3>🏈 Game Day features coming soon!</h3>
                <p>Stay tuned for real-time check-ins, live challenges, and more.</p>
                """)

            # -------------------- Leaderboard Tab --------------------
            with gr.Tab("Leaderboard"):
                leaderboard_refresh_btn = gr.Button("🔄 Refresh Leaderboard")
                leaderboard_display = gr.HTML(value=app.get_leaderboard_html())

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
            outputs=[points_display]
        )

        user_input.submit(
            respond,
            inputs=[user_input, chatbot, student_id],
            outputs=[chatbot, user_input]
        ).then(
            update_points,
            inputs=[student_id],
            outputs=[points_display]
        )

        events_btn.click(
            app.get_events_this_week,
            outputs=[events_display]
        )

        leaderboard_refresh_btn.click(
            update_leaderboard,
            outputs=[leaderboard_display]
        )

        feedback_btn.click(
            app.submit_feedback,
            inputs=[feedback_text, rating, student_id],
            outputs=[feedback_status]
        ).then(
            update_points,
            inputs=[student_id],
            outputs=[points_display]
        )

        student_id.change(
            update_points,
            inputs=[student_id],
            outputs=[points_display]
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
