"""
LMU Campus LLM - Gradio Web Interface
Provides a web-based interface for the campus assistant
"""

import sys
import os
import gradio as gr
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import LMUCampusAssistant

class GradioInterface:
    """Gradio web interface for LMU Campus Assistant"""
    
    def __init__(self):
        """Initialize the Gradio interface"""
        self.assistant = LMUCampusAssistant()
        self.current_student_id = None
        
    def process_query(self, query: str, student_id: str = "") -> str:
        """Process a query and return formatted response"""
        if not query.strip():
            return "Please enter a question!"
        
        # Update current student ID if provided
        if student_id.strip():
            self.current_student_id = student_id.strip()
        
        # Process the query
        result = self.assistant.process_query(query, self.current_student_id)
        
        # Format the response
        response = f"**🤖 LMU Assistant:** {result['response']}\n\n"
        
        # Add relevant events if any
        if result.get('relevant_events'):
            response += "**📅 Related Events:**\n"
            for event in result['relevant_events'][:3]:
                food_icon = "🍕" if event['free_food'] else ""
                response += f"• **{event['title']}** - {event['date']} at {event['time']}\n"
                response += f"  Location: {event['location']} | Points: {event['points']} {food_icon}\n"
                response += f"  {event['description']}\n\n"
        
        # Add student stats if logged in
        if self.current_student_id and result.get('student_stats'):
            stats = result['student_stats']
            response += f"**👤 Your Stats:** {stats['current_points']} points | {stats['events_attended']} events attended\n"
        
        return response
    
    def register_student(self, student_id: str, name: str) -> str:
        """Register a new student"""
        if not student_id.strip() or not name.strip():
            return "❌ Please provide both student ID and name"
        
        try:
            result = self.assistant.register_student(student_id.strip(), name.strip())
            self.current_student_id = student_id.strip()
            return f"✅ Successfully registered {result['name']}!\nCurrent points: {result['points']}"
        except Exception as e:
            return f"❌ Registration failed: {str(e)}"
    
    def login_student(self, student_id: str) -> str:
        """Login as existing student"""
        if not student_id.strip():
            return "❌ Please provide a student ID"
        
        try:
            student_info = self.assistant.points_system.get_student_info(student_id.strip())
            if student_info:
                self.current_student_id = student_id.strip()
                return f"✅ Logged in as: {student_info['name']}\nPoints: {student_info['points']}\nEvents attended: {len(student_info['events_attended'])}"
            else:
                return "❌ Student not found. Use the registration form to create a new account."
        except Exception as e:
            return f"❌ Login failed: {str(e)}"
    
    def get_student_stats(self) -> str:
        """Get current student statistics"""
        if not self.current_student_id:
            return "❌ Please login first"
        
        try:
            stats = self.assistant.get_student_stats(self.current_student_id)
            if not stats:
                return "❌ Student data not found"
            
            response = f"**👤 Student Statistics for {stats['name']}:**\n"
            response += f"• Current Points: {stats['current_points']}\n"
            response += f"• Total Points Earned: {stats['total_points_earned']}\n"
            response += f"• Events Attended: {stats['events_attended']}\n"
            response += f"• Rewards Claimed: {stats['rewards_claimed']}\n"
            response += f"• Badges: {', '.join(stats['badges']) if stats['badges'] else 'None'}\n"
            response += f"• Member since: {stats['registration_date'][:10]}"
            
            return response
        except Exception as e:
            return f"❌ Error getting stats: {str(e)}"
    
    def get_rewards(self) -> str:
        """Get available rewards"""
        try:
            rewards = self.assistant.get_available_rewards(self.current_student_id)
            if not rewards:
                return "❌ No rewards available"
            
            response = "**🎁 Available Rewards:**\n"
            for reward in rewards:
                status = ""
                if self.current_student_id:
                    if reward.get('already_claimed'):
                        status = " (Claimed)"
                    elif not reward.get('affordable'):
                        status = f" (Need {reward['points_required'] - reward.get('student_points', 0)} more points)"
                    else:
                        status = " (Can claim!)"
                
                response += f"• **{reward['name']}** - {reward['points_required']} points{status}\n"
                response += f"  {reward['description']}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting rewards: {str(e)}"
    
    def get_leaderboard(self) -> str:
        """Get leaderboard"""
        try:
            leaderboard = self.assistant.get_leaderboard()
            if not leaderboard:
                return "❌ No students found"
            
            response = "**🏆 Top Students:**\n"
            for i, student in enumerate(leaderboard, 1):
                badges_str = f" [{', '.join(student['badges'])}]" if student['badges'] else ""
                response += f"{i}. **{student['name']}** - {student['points']} points{badges_str}\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting leaderboard: {str(e)}"
    
    def get_events(self, category: str = "all") -> str:
        """Get events by category"""
        try:
            if category == "all":
                events = self.assistant.rag_engine.events
                title = "Upcoming Events"
            elif category == "food":
                events = self.assistant.get_events_with_food()
                title = "Events with Free Food 🍕"
            else:
                events = self.assistant.get_events_by_category(category)
                title = f"{category.title()} Events"
            
            if not events:
                return f"❌ No {category} events found"
            
            response = f"**📅 {title}:**\n"
            for event in events:
                food_icon = "🍕" if event['free_food'] else ""
                response += f"• **{event['title']}** - {event['date']} at {event['time']}\n"
                response += f"  Location: {event['location']} | Points: {event['points']} {food_icon}\n"
                response += f"  {event['description']}\n\n"
            
            return response
        except Exception as e:
            return f"❌ Error getting events: {str(e)}"
    
    def create_interface(self):
        """Create the Gradio interface"""
        with gr.Blocks(
            title="🦁 LMU Campus Assistant",
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="blue",
            )
        ) as interface:
            
            gr.Markdown("""
            # 🦁 LMU Campus Assistant
            
            **Your AI companion for everything LMU!** Ask questions about campus life, policies, events, and earn points for participation.
            
            ---
            """)
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Main chat interface
                    gr.Markdown("### 💬 Ask Me Anything")
                    
                    with gr.Row():
                        student_id_input = gr.Textbox(
                            label="Student ID (optional)",
                            placeholder="Enter your student ID for personalized responses",
                            scale=2
                        )
                        query_input = gr.Textbox(
                            label="Your Question",
                            placeholder="Ask about LMU policies, events, services...",
                            scale=3
                        )
                        submit_btn = gr.Button("Ask", variant="primary", scale=1)
                    
                    response_output = gr.Markdown(label="Response")
                    
                    # Quick action buttons
                    gr.Markdown("### ⚡ Quick Actions")
                    with gr.Row():
                        stats_btn = gr.Button("📊 My Stats", size="sm")
                        rewards_btn = gr.Button("🎁 Rewards", size="sm")
                        leaderboard_btn = gr.Button("🏆 Leaderboard", size="sm")
                    
                    with gr.Row():
                        events_btn = gr.Button("📅 All Events", size="sm")
                        food_events_btn = gr.Button("🍕 Food Events", size="sm")
                
                with gr.Column(scale=1):
                    # Student management
                    gr.Markdown("### 👤 Student Account")
                    
                    with gr.Accordion("Register New Student", open=False):
                        reg_student_id = gr.Textbox(label="Student ID", placeholder="e.g., vakaraiwe")
                        reg_name = gr.Textbox(label="Name", placeholder="e.g., Vanessa Akaraiwe")
                        register_btn = gr.Button("Register", variant="secondary")
                        register_output = gr.Markdown()
                    
                    with gr.Accordion("Login Existing Student", open=False):
                        login_student_id = gr.Textbox(label="Student ID", placeholder="e.g., vakaraiwe")
                        login_btn = gr.Button("Login", variant="secondary")
                        login_output = gr.Markdown()
                    
                    # Current status
                    gr.Markdown("### 📈 Current Status")
                    status_output = gr.Markdown("Not logged in")
            
            # Event handlers
            submit_btn.click(
                fn=self.process_query,
                inputs=[query_input, student_id_input],
                outputs=response_output
            )
            
            register_btn.click(
                fn=self.register_student,
                inputs=[reg_student_id, reg_name],
                outputs=register_output
            )
            
            login_btn.click(
                fn=self.login_student,
                inputs=[login_student_id],
                outputs=login_output
            )
            
            stats_btn.click(
                fn=self.get_student_stats,
                outputs=response_output
            )
            
            rewards_btn.click(
                fn=self.get_rewards,
                outputs=response_output
            )
            
            leaderboard_btn.click(
                fn=self.get_leaderboard,
                outputs=response_output
            )
            
            events_btn.click(
                fn=lambda: self.get_events("all"),
                outputs=response_output
            )
            
            food_events_btn.click(
                fn=lambda: self.get_events("food"),
                outputs=response_output
            )
            
            # Update status when student logs in
            def update_status():
                if self.current_student_id:
                    student_info = self.assistant.points_system.get_student_info(self.current_student_id)
                    if student_info:
                        return f"**Logged in as:** {student_info['name']}\n**Points:** {student_info['points']}\n**Events:** {len(student_info['events_attended'])}"
                return "Not logged in"
            
            # Update status after login/register
            login_btn.click(fn=update_status, outputs=status_output)
            register_btn.click(fn=update_status, outputs=status_output)
            
            gr.Markdown("""
            ---
            ### 🎯 How It Works
            
            1. **Ask Questions**: Get instant answers about LMU policies, services, and campus life
            2. **Discover Events**: Find upcoming events and earn points for attendance
            3. **Earn Rewards**: Use your points to claim rewards like free food, priority services, and exclusive badges
            4. **Track Progress**: Monitor your engagement and compete on the leaderboard
            
            ### 🚀 Getting Started
            
            - Register with your student ID to start earning points
            - Ask questions about anything LMU-related
            - Attend events to earn points
            - Claim rewards as you accumulate points
            
            *Built with ❤️ by Vanessa Akaraiwe for LMU students*
            """)
        
        return interface

def main():
    """Launch the Gradio interface"""
    interface = GradioInterface()
    app = interface.create_interface()
    
    print("🚀 Starting LMU Campus Assistant Web Interface...")
    print("📱 Open your browser to the URL shown below")
    print("🦁 Go Lions!")
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True to create a public link
        show_error=True
    )

if __name__ == "__main__":
    main()