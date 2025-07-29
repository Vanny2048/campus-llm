"""
Points System for tracking student engagement and rewards
"""

import sqlite3
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from .utils import logger, get_database_connection, validate_student_id, format_points_display

class PointsSystem:
    def __init__(self):
        """Initialize the points system"""
        self.point_values = {
            "question_asked": 1,
            "event_attended": 5,
            "feedback_submitted": 3,
            "referral": 5,
            "daily_login": 1,
            "first_event": 10,  # Bonus for first event
            "streak_bonus": 2,   # Daily streak bonus
            "game_day_checkin": 3,  # New: Game day check-ins
            "social_media_share": 2,  # New: Sharing on social media
            "study_group_formed": 5,  # New: Forming study groups
            "campus_explorer": 2,  # New: Visiting new campus locations
            "helpful_answer": 3,  # New: Helping other students
            "event_host": 10,  # New: Hosting events
            "spirit_week_participation": 5,  # New: Spirit week activities
            "library_grind": 2,  # New: Long study sessions
            "first_friday_attendance": 3,  # New: First Friday events
            "greek_life_event": 4,  # New: Greek life participation
            "wellness_checkin": 2,  # New: Wellness activities
            "career_fair_attendance": 8,  # New: Career development
            "study_abroad_info": 3,  # New: Study abroad interest
            "volunteer_hours": 5,  # New: Community service
            "academic_achievement": 10,  # New: Academic milestones
            "campus_safety_report": 3,  # New: Safety awareness
            "dining_hall_review": 1,  # New: Dining feedback
            "transportation_tip": 1,  # New: Transportation help
            "housing_assistance": 2,  # New: Housing help
            "tech_support": 2,  # New: Tech help
            "mental_health_resource": 3,  # New: Wellness support
        }
        
        # Enhanced reward thresholds with Gen Z appeal
        self.rewards = {
            10: "🦁 Newbie Lion - Welcome to the pride!",
            25: "🥉 Bronze Lion Badge + Free Coffee at C-Store",
            50: "🥈 Silver Lion Badge + Free Boba Run",
            75: "📚 Study Buddy - Free Printing Credits",
            100: "🥇 Gold Lion Badge + LMU Merch Bundle",
            150: "🎮 Game Day VIP - Priority Basketball Tickets",
            200: "👑 Legendary Lion + Priority Advising",
            300: "🌟 Campus Champion + Exclusive Events Access",
            400: "🚀 Bluff Master + Reserved Study Spots",
            500: "💎 Diamond Lion + Meet with President",
            750: "👑 Campus Royalty + Custom Experience",
            1000: "🏆 LMU Legend + Legacy Recognition"
        }
        
        # New: Achievement badges for specific activities
        self.achievements = {
            "first_question": {"name": "🎯 First Question", "description": "Asked your first question!"},
            "study_streak": {"name": "📚 Study Streak", "description": "7 days of consistent studying"},
            "social_butterfly": {"name": "🦋 Social Butterfly", "description": "Attended 10+ events"},
            "helpful_friend": {"name": "🤝 Helpful Friend", "description": "Helped 5+ other students"},
            "campus_explorer": {"name": "🗺️ Campus Explorer", "description": "Visited all major campus locations"},
            "spirit_leader": {"name": "🔥 Spirit Leader", "description": "Perfect attendance at 5+ games"},
            "wellness_warrior": {"name": "🧘 Wellness Warrior", "description": "Completed 10 wellness activities"},
            "academic_excellence": {"name": "⭐ Academic Excellence", "description": "Maintained 3.5+ GPA for semester"},
            "community_champion": {"name": "🏆 Community Champion", "description": "50+ hours of community service"},
            "bluff_legend": {"name": "🦁 Bluff Legend", "description": "1000+ total points earned"},
            "first_friday_fanatic": {"name": "🎉 First Friday Fanatic", "description": "Attended 12+ First Fridays"},
            "greek_life_royalty": {"name": "👑 Greek Life Royalty", "description": "Active in Greek life events"},
            "career_ready": {"name": "💼 Career Ready", "description": "Attended 5+ career development events"},
            "study_abroad_enthusiast": {"name": "✈️ Study Abroad Enthusiast", "description": "Explored study abroad options"},
            "tech_savvy": {"name": "💻 Tech Savvy", "description": "Helped with 10+ tech issues"},
            "dining_critic": {"name": "🍕 Dining Critic", "description": "Reviewed all dining locations"},
            "transportation_guru": {"name": "🚌 Transportation Guru", "description": "Mastered campus transportation"},
            "housing_expert": {"name": "🏠 Housing Expert", "description": "Helped with housing questions"},
            "safety_advocate": {"name": "🛡️ Safety Advocate", "description": "Promoted campus safety"},
            "mental_health_ally": {"name": "💚 Mental Health Ally", "description": "Supported wellness initiatives"}
        }

    def add_points(self, user_id: str, points: int, action_type: str, description: str = "") -> bool:
        """Add points to a user's account"""
        try:
            if not validate_student_id(user_id):
                logger.warning(f"Invalid student ID: {user_id}")
                return False
            
            conn = get_database_connection()
            cursor = conn.cursor()
            
            # Create user if doesn't exist
            cursor.execute("""
                INSERT OR IGNORE INTO users (id, total_points, questions_asked, events_attended, feedback_submitted)
                VALUES (?, 0, 0, 0, 0)
            """, (user_id,))
            
            # Add point transaction
            cursor.execute("""
                INSERT INTO point_transactions (user_id, points, action_type, description)
                VALUES (?, ?, ?, ?)
            """, (user_id, points, action_type, description))
            
            # Update user totals
            cursor.execute("""
                UPDATE users 
                SET total_points = total_points + ?,
                    last_active = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (points, user_id))
            
            # Update specific counters
            if action_type == "question_asked":
                cursor.execute("""
                    UPDATE users SET questions_asked = questions_asked + 1 WHERE id = ?
                """, (user_id,))
            elif action_type == "event_attended":
                cursor.execute("""
                    UPDATE users SET events_attended = events_attended + 1 WHERE id = ?
                """, (user_id,))
            elif action_type == "feedback_submitted":
                cursor.execute("""
                    UPDATE users SET feedback_submitted = feedback_submitted + 1 WHERE id = ?
                """, (user_id,))
            
            conn.commit()
            conn.close()
            
            # Check for milestone achievements and badges
            self._check_milestones(user_id)
            self._check_achievements(user_id, action_type)
            
            logger.info(f"Added {points} points to {user_id} for {action_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding points: {e}")
            return False

    def get_user_stats(self, user_id: str) -> str:
        """Get formatted user statistics with Gen Z-friendly display"""
        try:
            if not validate_student_id(user_id):
                return "❌ Invalid student ID format"
            
            conn = get_database_connection()
            cursor = conn.cursor()
            
            # Get user stats
            cursor.execute("""
                SELECT total_points, questions_asked, events_attended, feedback_submitted, created_at
                FROM users WHERE id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            
            if not result:
                # Create new user
                cursor.execute("""
                    INSERT INTO users (id, total_points, questions_asked, events_attended, feedback_submitted)
                    VALUES (?, 0, 0, 0, 0)
                """, (user_id,))
                conn.commit()
                result = (0, 0, 0, 0, datetime.now().isoformat())
            
            conn.close()
            
            # Format the stats with Gen Z style
            total_points = result[0]
            questions_asked = result[1]
            events_attended = result[2]
            feedback_submitted = result[3]
            created_at = result[4]
            
            # Get user level and achievements
            level = self._get_user_level(total_points)
            achievements = self.get_user_achievements(user_id)
            
            # Build the stats display
            stats_display = f"""
            <div style="text-align: center; padding: 1rem;">
                <h3 style="margin: 0 0 1rem 0; color: #667eea; font-size: 1.5rem;">{level}</h3>
                
                <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; padding: 1.5rem; margin-bottom: 1rem;">
                    <h2 style="margin: 0; font-size: 2.5rem;">{total_points} pts</h2>
                    <p style="margin: 0.5rem 0 0 0; opacity: 0.9;">Total Points</p>
                </div>
                
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1rem;">
                    <div style="background: #f8fafc; border-radius: 10px; padding: 1rem; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">{questions_asked}</div>
                        <div style="font-size: 0.9rem; color: #64748b;">Questions</div>
                    </div>
                    <div style="background: #f8fafc; border-radius: 10px; padding: 1rem; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">{events_attended}</div>
                        <div style="font-size: 0.9rem; color: #64748b;">Events</div>
                    </div>
                    <div style="background: #f8fafc; border-radius: 10px; padding: 1rem; text-align: center;">
                        <div style="font-size: 1.5rem; font-weight: bold; color: #667eea;">{feedback_submitted}</div>
                        <div style="font-size: 0.9rem; color: #64748b;">Feedback</div>
                    </div>
                </div>
            """
            
            # Add achievements section if user has any
            if achievements:
                stats_display += """
                <div style="background: #fef3c7; border-radius: 10px; padding: 1rem; margin-bottom: 1rem;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #92400e;">🏆 Achievements</h4>
                """
                for achievement in achievements[:3]:  # Show top 3 achievements
                    stats_display += f"""
                    <div style="background: white; border-radius: 8px; padding: 0.5rem; margin-bottom: 0.5rem; font-size: 0.9rem;">
                        <strong>{achievement['name']}</strong><br>
                        <span style="color: #64748b;">{achievement['description']}</span>
                    </div>
                    """
                if len(achievements) > 3:
                    stats_display += f"<div style='text-align: center; color: #64748b; font-size: 0.9rem;'>+{len(achievements) - 3} more achievements</div>"
                stats_display += "</div>"
            
            # Add next milestone info
            next_milestone = None
            for threshold in sorted(self.rewards.keys()):
                if total_points < threshold:
                    next_milestone = threshold
                    break
            
            if next_milestone:
                points_needed = next_milestone - total_points
                stats_display += f"""
                <div style="background: #ecfdf5; border-radius: 10px; padding: 1rem; text-align: center;">
                    <h4 style="margin: 0 0 0.5rem 0; color: #065f46;">🎯 Next Milestone</h4>
                    <div style="font-size: 1.2rem; font-weight: bold; color: #059669;">{self.rewards[next_milestone]}</div>
                    <div style="color: #64748b; margin-top: 0.5rem;">Just {points_needed} more points needed!</div>
                </div>
                """
            
            stats_display += """
            <div style="margin-top: 1rem; padding: 1rem; background: #f1f5f9; border-radius: 10px;">
                <h4 style="margin: 0 0 0.5rem 0; color: #475569;">💡 How to earn points:</h4>
                <ul style="margin: 0; padding-left: 1.5rem; color: #64748b; font-size: 0.9rem;">
                    <li>Ask questions (1 pt)</li>
                    <li>Attend events (5-10 pts)</li>
                    <li>Give feedback (3 pts)</li>
                    <li>Game day check-ins (3 pts)</li>
                    <li>Form study groups (5 pts)</li>
                    <li>And much more!</li>
                </ul>
            </div>
            </div>
            """
            
            return stats_display
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return f"❌ Error loading stats: {str(e)}"

    def get_leaderboard(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get the top users leaderboard"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, total_points, questions_asked, events_attended, feedback_submitted
                FROM users 
                ORDER BY total_points DESC 
                LIMIT ?
            """, (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            leaderboard = []
            for i, result in enumerate(results):
                # Anonymize user IDs for privacy
                anonymous_id = f"Lion{i+1}"
                if len(result[0]) > 3:
                    anonymous_id = f"Lion{result[0][:2]}***"
                
                leaderboard.append({
                    "rank": i + 1,
                    "user_id": anonymous_id,
                    "total_points": result[1],
                    "questions_asked": result[2],
                    "events_attended": result[3],
                    "feedback_submitted": result[4],
                    "level": self._get_user_level(result[1])
                })
            
            return leaderboard
            
        except Exception as e:
            logger.error(f"Error getting leaderboard: {e}")
            return []

    def get_user_rank(self, user_id: str) -> Dict[str, Any]:
        """Get a user's rank and position"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            # Get user's points
            cursor.execute("SELECT total_points FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            
            if not result:
                return {"rank": "Unranked", "total_users": 0, "points": 0}
            
            user_points = result[0]
            
            # Get rank
            cursor.execute("""
                SELECT COUNT(*) + 1 as rank
                FROM users 
                WHERE total_points > ?
            """, (user_points,))
            
            rank = cursor.fetchone()[0]
            
            # Get total users
            cursor.execute("SELECT COUNT(*) FROM users")
            total_users = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "rank": rank,
                "total_users": total_users,
                "points": user_points,
                "percentile": round((total_users - rank + 1) / total_users * 100, 1)
            }
            
        except Exception as e:
            logger.error(f"Error getting user rank: {e}")
            return {"rank": "Error", "total_users": 0, "points": 0}

    def check_daily_streak(self, user_id: str) -> int:
        """Check and update user's daily streak"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            # Get last activity
            cursor.execute("""
                SELECT DATE(last_active) as last_date
                FROM users WHERE id = ?
            """, (user_id,))
            
            result = cursor.fetchone()
            if not result:
                return 0
            
            last_date = result[0]
            today = datetime.now().date()
            
            # Check if user was active today
            if str(last_date) == str(today):
                return 0  # Already counted today
            
            # Check if yesterday (streak continues)
            yesterday = today - timedelta(days=1)
            if str(last_date) == str(yesterday):
                # Award streak bonus
                self.add_points(user_id, self.point_values["streak_bonus"], "streak_bonus", "Daily streak bonus")
                return self.point_values["streak_bonus"]
            
            return 0
            
        except Exception as e:
            logger.error(f"Error checking daily streak: {e}")
            return 0

    def _check_achievements(self, user_id: str, action_type: str):
        """Check if user has earned any new achievements"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            # Get user stats for achievement checking
            cursor.execute("""
                SELECT total_points, questions_asked, events_attended, feedback_submitted
                FROM users WHERE id = ?
            """, (user_id,))
            result = cursor.fetchone()
            
            if not result:
                return
            
            total_points, questions_asked, events_attended, feedback_submitted = result
            
            # Check for specific achievements
            achievements_to_check = []
            
            # First question achievement
            if questions_asked == 1:
                achievements_to_check.append("first_question")
            
            # Social butterfly achievement
            if events_attended >= 10:
                achievements_to_check.append("social_butterfly")
            
            # Bluff legend achievement
            if total_points >= 1000:
                achievements_to_check.append("bluff_legend")
            
            # Check if achievements are new
            for achievement in achievements_to_check:
                cursor.execute("""
                    SELECT COUNT(*) FROM point_transactions 
                    WHERE user_id = ? AND action_type = 'achievement' AND description LIKE ?
                """, (user_id, f"%{achievement}%"))
                
                if cursor.fetchone()[0] == 0:
                    # Award achievement
                    achievement_info = self.achievements.get(achievement, {})
                    achievement_name = achievement_info.get("name", "Unknown Achievement")
                    achievement_desc = achievement_info.get("description", "")
                    
                    self.add_points(
                        user_id,
                        5,  # Achievement bonus points
                        "achievement",
                        f"🏆 {achievement_name}: {achievement_desc}"
                    )
                    logger.info(f"User {user_id} earned achievement: {achievement}")
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking achievements: {e}")

    def _check_milestones(self, user_id: str):
        """Check if user has reached any milestones"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT total_points FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            
            if result:
                points = result[0]
                
                # Check if just reached a milestone
                for threshold in sorted(self.rewards.keys()):
                    if points >= threshold:
                        # Check if already achieved this milestone
                        cursor.execute("""
                            SELECT COUNT(*) FROM point_transactions 
                            WHERE user_id = ? AND action_type = 'milestone' AND description LIKE ?
                        """, (user_id, f"%{threshold}%"))
                        
                        if cursor.fetchone()[0] == 0:
                            # Award milestone bonus
                            bonus_points = threshold // 10  # 10% bonus
                            self.add_points(
                                user_id, 
                                bonus_points, 
                                "milestone", 
                                f"🎉 Milestone reached: {threshold} points - {self.rewards[threshold]}"
                            )
                            logger.info(f"User {user_id} reached milestone: {threshold} points")
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking milestones: {e}")

    def _get_user_level(self, points: int) -> str:
        """Get user level based on points"""
        if points >= 1000:
            return "🏆 LMU Legend"
        elif points >= 750:
            return "👑 Campus Royalty"
        elif points >= 500:
            return "💎 Diamond Lion"
        elif points >= 300:
            return "🌟 Campus Champion"
        elif points >= 200:
            return "👑 Legendary Lion"
        elif points >= 100:
            return "🥇 Gold Lion"
        elif points >= 50:
            return "🥈 Silver Lion"
        elif points >= 25:
            return "🥉 Bronze Lion"
        elif points >= 10:
            return "🦁 Newbie Lion"
        else:
            return "🦁 Young Lion"

    def get_user_achievements(self, user_id: str) -> List[Dict[str, str]]:
        """Get user's earned achievements"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT description FROM point_transactions 
                WHERE user_id = ? AND action_type = 'achievement'
                ORDER BY created_at DESC
            """, (user_id,))
            
            achievements = []
            for row in cursor.fetchall():
                description = row[0]
                if "🏆" in description:
                    # Parse achievement from description
                    parts = description.split(": ", 1)
                    if len(parts) == 2:
                        achievements.append({
                            "name": parts[0],
                            "description": parts[1]
                        })
            
            conn.close()
            return achievements
            
        except Exception as e:
            logger.error(f"Error getting user achievements: {e}")
            return []

    def get_reward_catalog(self) -> Dict[int, str]:
        """Get the available rewards catalog"""
        return self.rewards

    def redeem_reward(self, user_id: str, reward_threshold: int) -> bool:
        """Redeem a reward (placeholder for future implementation)"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT total_points FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            
            if result and result[0] >= reward_threshold:
                # Log redemption
                cursor.execute("""
                    INSERT INTO point_transactions (user_id, points, action_type, description)
                    VALUES (?, 0, 'reward_redeemed', ?)
                """, (user_id, f"Redeemed: {self.rewards.get(reward_threshold, 'Unknown reward')}"))
                
                conn.commit()
                conn.close()
                return True
            
            conn.close()
            return False
            
        except Exception as e:
            logger.error(f"Error redeeming reward: {e}")
            return False

    def get_daily_summary(self) -> Dict[str, Any]:
        """Get daily activity summary"""
        try:
            conn = get_database_connection()
            cursor = conn.cursor()
            
            today = datetime.now().date()
            
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT user_id) as active_users,
                    SUM(CASE WHEN action_type = 'question_asked' THEN 1 ELSE 0 END) as questions,
                    SUM(CASE WHEN action_type = 'event_attended' THEN 1 ELSE 0 END) as events,
                    SUM(CASE WHEN action_type = 'feedback_submitted' THEN 1 ELSE 0 END) as feedback
                FROM point_transactions 
                WHERE DATE(timestamp) = ?
            """, (today,))
            
            result = cursor.fetchone()
            conn.close()
            
            return {
                "date": str(today),
                "active_users": result[0] or 0,
                "questions_asked": result[1] or 0,
                "events_attended": result[2] or 0,
                "feedback_submitted": result[3] or 0
            }
            
        except Exception as e:
            logger.error(f"Error getting daily summary: {e}")
            return {}

# Test function
def test_points_system():
    """Test the points system functionality"""
    points = PointsSystem()
    
    # Test adding points
    test_user = "TEST123"
    success = points.add_points(test_user, 5, "test", "Testing points system")
    print(f"Add points test: {'✅' if success else '❌'}")
    
    # Test getting stats
    stats = points.get_user_stats(test_user)
    print(f"Get stats test: {'✅' if 'points' in stats.lower() else '❌'}")
    
    # Test leaderboard
    leaderboard = points.get_leaderboard(5)
    print(f"Leaderboard test: {'✅' if isinstance(leaderboard, list) else '❌'}")
    
    print("🎯 Points system test completed!")

if __name__ == "__main__":
    test_points_system()