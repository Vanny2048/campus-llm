"""
LMU Campus LLM - Points System
Manages student engagement points and rewards for event participation
"""

import json
import os
from datetime import datetime, date
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PointsSystem:
    """Manages student engagement points and rewards"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Initialize points system
        
        Args:
            data_dir: Directory to store points data
        """
        self.data_dir = data_dir
        self.students_file = os.path.join(data_dir, "students.json")
        self.events_file = os.path.join(data_dir, "events.json")
        self.rewards_file = os.path.join(data_dir, "rewards.json")
        
        # Ensure data directory exists
        os.makedirs(data_dir, exist_ok=True)
        
        # Load data
        self.students = self._load_students()
        self.events = self._load_events()
        self.rewards = self._load_rewards()
        
        # Initialize default rewards if none exist
        if not self.rewards:
            self._initialize_default_rewards()
    
    def _load_students(self) -> Dict:
        """Load student points data"""
        try:
            if os.path.exists(self.students_file):
                with open(self.students_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to load students data: {e}")
            return {}
    
    def _load_events(self) -> Dict:
        """Load events data"""
        try:
            if os.path.exists(self.events_file):
                with open(self.events_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to load events data: {e}")
            return {}
    
    def _load_rewards(self) -> List[Dict]:
        """Load rewards data"""
        try:
            if os.path.exists(self.rewards_file):
                with open(self.rewards_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Failed to load rewards data: {e}")
            return []
    
    def _save_students(self):
        """Save student points data"""
        try:
            with open(self.students_file, 'w', encoding='utf-8') as f:
                json.dump(self.students, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save students data: {e}")
    
    def _save_events(self):
        """Save events data"""
        try:
            with open(self.events_file, 'w', encoding='utf-8') as f:
                json.dump(self.events, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save events data: {e}")
    
    def _save_rewards(self):
        """Save rewards data"""
        try:
            with open(self.rewards_file, 'w', encoding='utf-8') as f:
                json.dump(self.rewards, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save rewards data: {e}")
    
    def _initialize_default_rewards(self):
        """Initialize default rewards system"""
        self.rewards = [
            {
                "id": "reward_001",
                "name": "Free Boba",
                "description": "Get a free boba drink from campus dining",
                "points_required": 100,
                "category": "food",
                "available": True
            },
            {
                "id": "reward_002",
                "name": "Priority Advising",
                "description": "Skip the line for academic advising",
                "points_required": 200,
                "category": "academic",
                "available": True
            },
            {
                "id": "reward_003",
                "name": "LMU T-Shirt",
                "description": "Get a free LMU branded t-shirt",
                "points_required": 300,
                "category": "merchandise",
                "available": True
            },
            {
                "id": "reward_004",
                "name": "Study Room Priority",
                "description": "Reserve library study rooms 24 hours in advance",
                "points_required": 150,
                "category": "academic",
                "available": True
            },
            {
                "id": "reward_005",
                "name": "Founding Lion Badge",
                "description": "Special badge for early adopters of the Campus LLM",
                "points_required": 500,
                "category": "badge",
                "available": True
            }
        ]
        self._save_rewards()
    
    def register_student(self, student_id: str, name: str = None) -> Dict:
        """
        Register a new student in the points system
        
        Args:
            student_id: Unique student identifier
            name: Student's name (optional)
            
        Returns:
            Student data
        """
        if student_id not in self.students:
            self.students[student_id] = {
                "name": name or f"Student {student_id}",
                "points": 0,
                "total_points_earned": 0,
                "events_attended": [],
                "rewards_claimed": [],
                "badges": [],
                "registration_date": datetime.now().isoformat(),
                "last_activity": datetime.now().isoformat()
            }
            self._save_students()
            logger.info(f"Registered new student: {student_id}")
        
        return self.students[student_id]
    
    def get_student_points(self, student_id: str) -> int:
        """Get current points for a student"""
        if student_id in self.students:
            return self.students[student_id]["points"]
        return 0
    
    def get_student_info(self, student_id: str) -> Optional[Dict]:
        """Get complete student information"""
        return self.students.get(student_id)
    
    def award_points_for_event(self, student_id: str, event_id: str, points: int) -> bool:
        """
        Award points to a student for attending an event
        
        Args:
            student_id: Student identifier
            event_id: Event identifier
            points: Points to award
            
        Returns:
            True if successful, False otherwise
        """
        if student_id not in self.students:
            logger.warning(f"Student {student_id} not registered")
            return False
        
        # Check if student already attended this event
        if event_id in self.students[student_id]["events_attended"]:
            logger.warning(f"Student {student_id} already attended event {event_id}")
            return False
        
        # Award points
        self.students[student_id]["points"] += points
        self.students[student_id]["total_points_earned"] += points
        self.students[student_id]["events_attended"].append(event_id)
        self.students[student_id]["last_activity"] = datetime.now().isoformat()
        
        # Update event attendance
        if event_id not in self.events:
            self.events[event_id] = {"attendees": [], "total_points_awarded": 0}
        
        self.events[event_id]["attendees"].append(student_id)
        self.events[event_id]["total_points_awarded"] += points
        
        self._save_students()
        self._save_events()
        
        logger.info(f"Awarded {points} points to student {student_id} for event {event_id}")
        return True
    
    def claim_reward(self, student_id: str, reward_id: str) -> Dict:
        """
        Allow a student to claim a reward
        
        Args:
            student_id: Student identifier
            reward_id: Reward identifier
            
        Returns:
            Result dictionary with success status and message
        """
        if student_id not in self.students:
            return {"success": False, "message": "Student not registered"}
        
        # Find the reward
        reward = None
        for r in self.rewards:
            if r["id"] == reward_id and r["available"]:
                reward = r
                break
        
        if not reward:
            return {"success": False, "message": "Reward not found or unavailable"}
        
        student = self.students[student_id]
        
        # Check if student has enough points
        if student["points"] < reward["points_required"]:
            return {
                "success": False, 
                "message": f"Not enough points. You have {student['points']}, need {reward['points_required']}"
            }
        
        # Check if student already claimed this reward
        if reward_id in student["rewards_claimed"]:
            return {"success": False, "message": "Reward already claimed"}
        
        # Claim the reward
        student["points"] -= reward["points_required"]
        student["rewards_claimed"].append(reward_id)
        student["last_activity"] = datetime.now().isoformat()
        
        # Add badge if applicable
        if reward["category"] == "badge":
            student["badges"].append(reward["name"])
        
        self._save_students()
        
        return {
            "success": True, 
            "message": f"Successfully claimed {reward['name']}!",
            "reward": reward
        }
    
    def get_available_rewards(self, student_id: str = None) -> List[Dict]:
        """
        Get list of available rewards
        
        Args:
            student_id: Optional student ID to check affordability
            
        Returns:
            List of available rewards
        """
        if not student_id:
            return [r for r in self.rewards if r["available"]]
        
        if student_id not in self.students:
            return []
        
        student_points = self.students[student_id]["points"]
        available_rewards = []
        
        for reward in self.rewards:
            if reward["available"]:
                reward_copy = reward.copy()
                reward_copy["affordable"] = student_points >= reward["points_required"]
                reward_copy["already_claimed"] = reward["id"] in self.students[student_id]["rewards_claimed"]
                available_rewards.append(reward_copy)
        
        return available_rewards
    
    def get_leaderboard(self, top_n: int = 10) -> List[Dict]:
        """
        Get top students by points
        
        Args:
            top_n: Number of top students to return
            
        Returns:
            List of top students with their points
        """
        students_list = []
        for student_id, student_data in self.students.items():
            students_list.append({
                "student_id": student_id,
                "name": student_data["name"],
                "points": student_data["points"],
                "total_points_earned": student_data["total_points_earned"],
                "events_attended": len(student_data["events_attended"]),
                "badges": student_data["badges"]
            })
        
        # Sort by points (descending)
        students_list.sort(key=lambda x: x["points"], reverse=True)
        return students_list[:top_n]
    
    def get_student_stats(self, student_id: str) -> Dict:
        """
        Get detailed statistics for a student
        
        Args:
            student_id: Student identifier
            
        Returns:
            Student statistics
        """
        if student_id not in self.students:
            return {}
        
        student = self.students[student_id]
        
        return {
            "student_id": student_id,
            "name": student["name"],
            "current_points": student["points"],
            "total_points_earned": student["total_points_earned"],
            "events_attended": len(student["events_attended"]),
            "rewards_claimed": len(student["rewards_claimed"]),
            "badges": student["badges"],
            "registration_date": student["registration_date"],
            "last_activity": student["last_activity"],
            "available_rewards": self.get_available_rewards(student_id)
        }
    
    def add_custom_reward(self, name: str, description: str, points_required: int, category: str) -> str:
        """
        Add a custom reward to the system
        
        Args:
            name: Reward name
            description: Reward description
            points_required: Points needed to claim
            category: Reward category
            
        Returns:
            Reward ID
        """
        reward_id = f"reward_{len(self.rewards) + 1:03d}"
        
        new_reward = {
            "id": reward_id,
            "name": name,
            "description": description,
            "points_required": points_required,
            "category": category,
            "available": True
        }
        
        self.rewards.append(new_reward)
        self._save_rewards()
        
        logger.info(f"Added custom reward: {name}")
        return reward_id

# Example usage
if __name__ == "__main__":
    points_system = PointsSystem()
    
    # Register a test student
    student_id = "test_student_001"
    student_data = points_system.register_student(student_id, "Test Student")
    print(f"Registered student: {student_data}")
    
    # Award points for attending an event
    success = points_system.award_points_for_event(student_id, "event_001", 50)
    print(f"Awarded points: {success}")
    
    # Check student stats
    stats = points_system.get_student_stats(student_id)
    print(f"Student stats: {stats}")
    
    # Get available rewards
    rewards = points_system.get_available_rewards(student_id)
    print(f"Available rewards: {len(rewards)}")
    
    # Get leaderboard
    leaderboard = points_system.get_leaderboard()
    print(f"Leaderboard: {leaderboard}")