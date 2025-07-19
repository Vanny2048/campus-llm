"""
Utility functions for the LMU Campus LLM
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, Any, Optional
import sqlite3

def setup_logging():
    """Setup logging configuration"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('campus_llm.log'),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logging()

def load_config(config_path: str = "config.json") -> Dict[str, Any]:
    """Load configuration from JSON file"""
    default_config = {
        "llm": {
            "model": "llama3.2:3b",
            "temperature": 0.7,
            "max_tokens": 512,
            "timeout": 30
        },
        "rag": {
            "chunk_size": 1000,
            "chunk_overlap": 200,
            "max_results": 5,
            "similarity_threshold": 0.7
        },
        "points": {
            "question_asked": 1,
            "event_attended": 5,
            "feedback_submitted": 3,
            "referral": 5
        },
        "app": {
            "port": 7860,
            "host": "0.0.0.0",
            "debug": True
        }
    }
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
            # Merge with defaults
            for key, value in default_config.items():
                if key not in config:
                    config[key] = value
                elif isinstance(value, dict) and isinstance(config[key], dict):
                    for subkey, subvalue in value.items():
                        if subkey not in config[key]:
                            config[key][subkey] = subvalue
            return config
        except Exception as e:
            logger.warning(f"Error loading config: {e}. Using defaults.")
            return default_config
    else:
        # Create default config file
        with open(config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        logger.info(f"Created default config file: {config_path}")
        return default_config

def log_interaction(user_message: str, assistant_response: str, user_id: Optional[str] = None):
    """Log user interactions for analysis"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id,
            "user_message": user_message,
            "assistant_response": assistant_response
        }
        
        # Ensure log directory exists
        os.makedirs("data/logs", exist_ok=True)
        
        # Log to file
        log_file = f"data/logs/interactions_{datetime.now().strftime('%Y%m%d')}.json"
        
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []
        
        logs.append(log_entry)
        
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)
            
    except Exception as e:
        logger.error(f"Error logging interaction: {e}")

def init_database():
    """Initialize SQLite database for persistent storage"""
    try:
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect("data/campus_llm.db")
        cursor = conn.cursor()
        
        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                total_points INTEGER DEFAULT 0,
                questions_asked INTEGER DEFAULT 0,
                events_attended INTEGER DEFAULT 0,
                feedback_submitted INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS point_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                points INTEGER,
                action_type TEXT,
                description TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                date TEXT,
                location TEXT,
                points INTEGER DEFAULT 5,
                free_food BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS event_checkins (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                event_id INTEGER,
                checkin_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id),
                FOREIGN KEY (event_id) REFERENCES events (id)
            )
        """)
        
        conn.commit()
        conn.close()
        logger.info("Database initialized successfully")
        
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

def clean_text(text: str) -> str:
    """Clean and normalize text input"""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize
    text = " ".join(text.split())
    
    # Remove any problematic characters
    text = text.encode('utf-8', errors='ignore').decode('utf-8')
    
    return text.strip()

def format_points_display(user_stats: Dict[str, Any]) -> str:
    """Format user points for display"""
    total_points = user_stats.get('total_points', 0)
    questions = user_stats.get('questions_asked', 0)
    events = user_stats.get('events_attended', 0)
    feedback = user_stats.get('feedback_submitted', 0)
    
    # Determine user level based on points
    if total_points >= 100:
        level = "🥇 Gold Lion"
    elif total_points >= 50:
        level = "🥈 Silver Lion"
    elif total_points >= 20:
        level = "🥉 Bronze Lion"
    else:
        level = "🦁 Young Lion"
    
    return f"""
    **{level}** - {total_points} points
    
    📊 **Your Activity:**
    • Questions asked: {questions}
    • Events attended: {events}
    • Feedback given: {feedback}
    
    🎯 **Next milestone:** {get_next_milestone(total_points)} points
    """

def get_next_milestone(current_points: int) -> int:
    """Get the next point milestone for the user"""
    milestones = [20, 50, 100, 200]
    for milestone in milestones:
        if current_points < milestone:
            return milestone
    return current_points + 100  # If beyond all milestones

def validate_student_id(student_id: str) -> bool:
    """Validate student ID format (basic validation)"""
    if not student_id:
        return False
    
    # Remove spaces and convert to uppercase
    student_id = student_id.strip().upper()
    
    # Basic validation - adjust based on LMU's actual format
    if len(student_id) < 3 or len(student_id) > 15:
        return False
    
    return True

def get_database_connection():
    """Get database connection"""
    return sqlite3.connect("data/campus_llm.db")

def ensure_directories():
    """Ensure all required directories exist"""
    directories = [
        "data",
        "data/lmu_knowledge",
        "data/events",
        "data/student_feedback",
        "data/logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Initialize on import
ensure_directories()
init_database()