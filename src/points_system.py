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
            "streak_bonus": 2   # Daily streak bonus
        }
        
        # Reward thresholds
        self.rewards = {
            20: "🥉 Bronze Lion Badge",
            50: "🥈 Silver Lion Badge + Free Boba",
            100: "🥇 Gold Lion Badge + LMU Merch",
            200: "👑 Legendary Lion + Priority Advising",
            500: "🌟 Campus Champion + Exclusive Events"
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
            
            # Check for milestone achievements
            self._check_milestones(user_id)
            
            logger.info(f"Added {points} points to {user_id} for {action_type}")
            return True
            
        except Exception as e:
            logger.error(f"Error adding points: {e}")
            return False

    def get_user_stats(self, user_id: str) -> str:
        """Get formatted user statistics"""
        try:
            if not validate_student_id(user_id):
                return "Invalid student ID format"
            
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
            
            # Format the stats
            stats = {
                "total_points": result[0],
                "questions_asked": result[1],
                "events_attended": result[2],
                "feedback_submitted": result[3],
                "created_at": result[4]
            }
            
            return format_points_display(stats)
            
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return f"Error loading stats: {str(e)}"

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
                                f"Milestone reached: {threshold} points - {self.rewards[threshold]}"
                            )
                            logger.info(f"User {user_id} reached milestone: {threshold} points")
            
            conn.close()
            
        except Exception as e:
            logger.error(f"Error checking milestones: {e}")

    def _get_user_level(self, points: int) -> str:
        """Get user level based on points"""
        if points >= 500:
            return "🌟 Campus Champion"
        elif points >= 200:
            return "👑 Legendary Lion"
        elif points >= 100:
            return "🥇 Gold Lion"
        elif points >= 50:
            return "🥈 Silver Lion"
        elif points >= 20:
            return "🥉 Bronze Lion"
        else:
            return "🦁 Young Lion"

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