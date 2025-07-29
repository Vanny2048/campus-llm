#!/usr/bin/env python3
"""
LMU Campus LLM - Spirit Interface
Enhanced interface with game day features, tailgates, watch parties, and premium prizes
"""

import gradio as gr
from app import CampusLLMApp
from datetime import datetime

def create_spirit_interface():
    """Create the enhanced spirit interface"""
    app = CampusLLMApp()
    
    # Custom CSS for spirit theme
    custom_css = """
    .spirit-theme {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .game-day-dashboard {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        backdrop-filter: blur(10px);
    }
    
    .countdown-container {
        text-align: center;
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
        border-radius: 15px;
        padding: 30px;
        margin: 20px 0;
    }
    
    .countdown-timer {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin: 20px 0;
    }
    
    .countdown-unit {
        text-align: center;
        background: rgba(255, 255, 255, 0.2);
        padding: 15px;
        border-radius: 10px;
        min-width: 80px;
    }
    
    .countdown-number {
        display: block;
        font-size: 2.5rem;
        font-weight: bold;
        color: #FFD700;
    }
    
    .countdown-label {
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .action-buttons {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin: 15px 0;
    }
    
    .action-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 12px 20px;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 0.2s;
    }
    
    .action-btn:hover {
        transform: translateY(-2px);
    }
    
    .action-btn.primary {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    }
    
    .action-btn.secondary {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
    }
    
    .challenges-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 15px;
        margin: 15px 0;
    }
    
    .challenge-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        border-left: 4px solid #FFD700;
    }
    
    .challenge-meta {
        display: flex;
        justify-content: space-between;
        margin: 15px 0;
    }
    
    .challenge-btn {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #333;
        border: none;
        padding: 10px 20px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .events-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 15px;
        margin: 15px 0;
    }
    
    .event-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .event-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .event-type {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
        color: white;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .event-type.away {
        background: linear-gradient(135deg, #ff6b6b, #ee5a24);
    }
    
    .tailgates-grid, .watch-parties-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .tailgate-card, .watch-party-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        backdrop-filter: blur(10px);
    }
    
    .tailgate-card.upcoming {
        border-left: 4px solid #4ecdc4;
    }
    
    .tailgate-card.today {
        border-left: 4px solid #FFD700;
        background: rgba(255, 215, 0, 0.1);
    }
    
    .tailgate-header, .party-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }
    
    .host-badge, .partner-badge {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .tailgate-stats, .party-stats {
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
        text-align: center;
    }
    
    .stat {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: bold;
        color: #FFD700;
    }
    
    .stat-label {
        font-size: 0.8rem;
        opacity: 0.8;
    }
    
    .tailgate-actions, .party-actions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    
    .rsvp-btn, .qr-btn, .share-btn, .directions-btn {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 10px 15px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        flex: 1;
        min-width: 100px;
    }
    
    .rsvp-btn {
        background: linear-gradient(135deg, #4ecdc4, #44a08d);
    }
    
    .prizes-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 20px;
        margin: 20px 0;
    }
    
    .prize-card {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 25px;
        display: flex;
        align-items: center;
        gap: 20px;
        backdrop-filter: blur(10px);
    }
    
    .prize-card.claimed {
        opacity: 0.6;
        background: rgba(128, 128, 128, 0.1);
    }
    
    .prize-icon {
        font-size: 3rem;
        min-width: 60px;
        text-align: center;
    }
    
    .prize-content {
        flex: 1;
    }
    
    .prize-meta {
        display: flex;
        justify-content: space-between;
        margin: 15px 0;
    }
    
    .points-number, .availability-number {
        font-size: 1.2rem;
        font-weight: bold;
        color: #FFD700;
    }
    
    .category-badge {
        background: linear-gradient(135deg, #f093fb, #f5576c);
        color: white;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 0.7rem;
        font-weight: 600;
    }
    
    .prize-actions {
        display: flex;
        flex-direction: column;
        gap: 8px;
    }
    
    .redeem-btn, .details-btn {
        background: linear-gradient(135deg, #FFD700, #FFA500);
        color: #333;
        border: none;
        padding: 8px 15px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .redeem-btn:disabled {
        background: #ccc;
        cursor: not-allowed;
    }
    
    .earning-tips {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 15px;
        margin: 20px 0;
    }
    
    .tip {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }
    
    .points-display {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }
    """
    
    with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as interface:
        gr.HTML("""
        <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #1e3c72, #2a5298); color: white;">
            <h1 style="margin: 0; font-size: 2.5rem;">🦁 LMU Campus LLM</h1>
            <p style="margin: 10px 0; font-size: 1.2rem; opacity: 0.9;">The Ultimate School Spirit Platform</p>
            <p style="margin: 5px 0; font-size: 1rem; opacity: 0.8;">Ask questions, earn points, and show your Lion pride!</p>
        </div>
        """)
        
        # User ID Input
        with gr.Row():
            user_id_input = gr.Textbox(
                label="Enter Your Student ID",
                placeholder="e.g., 12345",
                scale=2
            )
            points_display = gr.HTML(value=app.get_user_points(None), scale=1)
        
        # Main Tabs
        with gr.Tabs() as tabs:
            # -------------------- Game Day Tab --------------------
            with gr.Tab("🏈 Game Day", id=0):
                with gr.Row():
                    with gr.Column(scale=2):
                        game_day_dashboard = gr.HTML(value=app.get_game_day_dashboard())
                        
                        # Quick Actions
                        with gr.Row():
                            qr_generate_btn = gr.Button("📱 Generate QR Code", variant="secondary")
                            challenge_submit_btn = gr.Button("📸 Submit Challenge", variant="secondary")
                            check_in_btn = gr.Button("✅ Check In", variant="secondary")
                    
                    with gr.Column(scale=1):
                        # Current Spirit MVP
                        current_mvp = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🌟 Current Spirit MVP</h4>
                            <div style="background: linear-gradient(135deg, #ffd700, #ffed4e); color: #333; padding: 20px; border-radius: 12px; margin: 10px 0; text-align: center;">
                                <div style="font-size: 48px; margin-bottom: 10px;">👑</div>
                                <h5>Mike Chen</h5>
                                <p>🏛️ Sigma Chi</p>
                                <p>📊 189 points this week</p>
                                <p style="font-size: 0.9rem; color: #666;">Attended 6 events, won 2 challenges</p>
                            </div>
                        </div>
                        """)
                        
                        # Live Spirit Meter
                        spirit_meter = gr.HTML("""
                        <div class="dashboard-card">
                            <h4>🔥 Live Spirit Meter</h4>
                            <div style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; padding: 20px; border-radius: 12px; margin: 10px 0; text-align: center;">
                                <div style="font-size: 2rem; margin-bottom: 10px;">🔥🔥🔥</div>
                                <h5>HIGH SPIRIT</h5>
                                <p>847 students active today</p>
                                <p style="font-size: 0.9rem; opacity: 0.8;">+23% from yesterday</p>
                            </div>
                        </div>
                        """)
            
            # -------------------- Tailgates Tab --------------------
            with gr.Tab("🎉 Tailgates", id=1):
                tailgates_section = gr.HTML(value=app.get_tailgates_html())
                
                # RSVP and QR Code Actions
                with gr.Row():
                    tailgate_rsvp_btn = gr.Button("🎫 RSVP to Tailgate", variant="primary")
                    tailgate_qr_btn = gr.Button("📱 Get Tailgate QR", variant="secondary")
                    host_application_btn = gr.Button("🏠 Apply to Host", variant="secondary")
            
            # -------------------- Watch Parties Tab --------------------
            with gr.Tab("📺 Watch Parties", id=2):
                watch_parties_section = gr.HTML(value=app.get_watch_parties_html())
                
                # Watch Party Actions
                with gr.Row():
                    watch_party_rsvp_btn = gr.Button("🎫 RSVP to Watch Party", variant="primary")
                    directions_btn = gr.Button("🗺️ Get Directions", variant="secondary")
                    partner_btn = gr.Button("🤝 Become Partner", variant="secondary")
            
            # -------------------- Prizes Tab --------------------
            with gr.Tab("🏆 Premium Prizes", id=3):
                premium_prizes_section = gr.HTML(value=app.get_premium_prizes_html())
                
                # Prize Actions
                with gr.Row():
                    redeem_prize_btn = gr.Button("🏆 Redeem Prize", variant="primary")
                    prize_details_btn = gr.Button("ℹ️ Prize Details", variant="secondary")
                    earning_tips_btn = gr.Button("💡 Earning Tips", variant="secondary")
            
            # -------------------- Chat Tab --------------------
            with gr.Tab("💬 Ask LLM", id=4):
                with gr.Row():
                    with gr.Column(scale=3):
                        chatbot = gr.Chatbot(
                            label="LMU Campus LLM",
                            height=500,
                            show_label=True,
                            container=True,
                            bubble_full_width=False
                        )
                        
                        with gr.Row():
                            msg = gr.Textbox(
                                label="Ask me anything about LMU!",
                                placeholder="e.g., Where can I find a math tutor? What's the GPA requirement for study abroad?",
                                scale=4
                            )
                            submit_btn = gr.Button("Send", variant="primary", scale=1)
                    
                    with gr.Column(scale=1):
                        # Quick Questions
                        gr.HTML("""
                        <div class="dashboard-card">
                            <h4>💡 Quick Questions</h4>
                            <div style="display: flex; flex-direction: column; gap: 8px;">
                                <button style="background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 8px 12px; border-radius: 6px; font-size: 0.9rem; text-align: left;">Where can I find a math tutor?</button>
                                <button style="background: linear-gradient(135deg, #4ecdc4, #44a08d); color: white; border: none; padding: 8px 12px; border-radius: 6px; font-size: 0.9rem; text-align: left;">What's the GPA requirement for study abroad?</button>
                                <button style="background: linear-gradient(135deg, #ff6b6b, #ee5a24); color: white; border: none; padding: 8px 12px; border-radius: 6px; font-size: 0.9rem; text-align: left;">How do I file an academic grievance?</button>
                                <button style="background: linear-gradient(135deg, #f093fb, #f5576c); color: white; border: none; padding: 8px 12px; border-radius: 6px; font-size: 0.9rem; text-align: left;">What events have free food this week?</button>
                            </div>
                        </div>
                        """)
                        
                        # Feedback Section
                        with gr.Group():
                            gr.HTML("<h4>📝 Give Feedback</h4>")
                            feedback_text = gr.Textbox(
                                label="Your feedback",
                                placeholder="Tell us how we can improve!",
                                lines=3
                            )
                            feedback_rating = gr.Slider(
                                minimum=1,
                                maximum=5,
                                value=5,
                                step=1,
                                label="Rating",
                                show_label=True
                            )
                            feedback_btn = gr.Button("Submit Feedback", variant="secondary")
            
            # -------------------- Leaderboard Tab --------------------
            with gr.Tab("🏅 Leaderboard", id=5):
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
                        leaderboard_refresh_btn = gr.Button("🔄 Refresh Leaderboard", variant="secondary")
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
        
        # Event handlers
        def respond(message, history, user_id):
            """Handle chat responses"""
            response = app.process_message(message, history, user_id)
            return response
        
        def update_points(user_id):
            """Update points display"""
            return app.get_user_points(user_id)
        
        def update_leaderboard():
            """Update leaderboard display"""
            return app.get_leaderboard_html(15)
        
        def submit_feedback(feedback, rating, user_id):
            """Submit user feedback"""
            try:
                feedback_data = {
                    "feedback": feedback,
                    "rating": rating,
                    "user_id": user_id,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Save feedback (simplified for demo)
                print(f"Feedback submitted: {feedback_data}")
                
                # Award points for feedback
                if user_id:
                    app.points_system.add_points(user_id, 3, "feedback_submitted")
                
                return "Thank you for your feedback! You earned 3 Spirit Points! 🎉"
                
            except Exception as e:
                return f"Error submitting feedback: {str(e)}"
        
        # Connect event handlers
        submit_btn.click(
            respond,
            inputs=[msg, chatbot, user_id_input],
            outputs=[chatbot]
        )
        
        msg.submit(
            respond,
            inputs=[msg, chatbot, user_id_input],
            outputs=[chatbot]
        )
        
        user_id_input.change(
            update_points,
            inputs=[user_id_input],
            outputs=[points_display]
        )
        
        leaderboard_refresh_btn.click(
            update_leaderboard,
            outputs=[leaderboard_display]
        )
        
        feedback_btn.click(
            submit_feedback,
            inputs=[feedback_text, feedback_rating, user_id_input],
            outputs=[feedback_text]
        )
        
        # Clear feedback after submission
        feedback_btn.click(
            lambda: "",
            outputs=[feedback_text]
        )
    
    return interface

if __name__ == "__main__":
    interface = create_spirit_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )