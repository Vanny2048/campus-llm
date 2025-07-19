"""
LMU Campus LLM - Main Application
The main application that integrates all components of the campus assistant
"""

import sys
import os
import logging
from typing import Dict, List, Optional
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from llm_client import OllamaClient
from rag_engine import RAGEngine
from points_system import PointsSystem

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LMUCampusAssistant:
    """Main campus assistant that integrates all components"""
    
    def __init__(self):
        """Initialize the campus assistant"""
        logger.info("Initializing LMU Campus Assistant...")
        
        # Initialize components
        self.llm_client = OllamaClient()
        self.rag_engine = RAGEngine()
        self.points_system = PointsSystem()
        
        # Test connections
        self._test_connections()
        
        logger.info("LMU Campus Assistant initialized successfully!")
    
    def _test_connections(self):
        """Test all component connections"""
        logger.info("Testing component connections...")
        
        # Test LLM connection
        llm_status = self.llm_client.test_connection()
        if llm_status["status"] == "connected":
            logger.info("✅ LLM connection successful")
        else:
            logger.warning(f"⚠️ LLM connection issue: {llm_status.get('error', 'Unknown error')}")
        
        # Test RAG engine
        if self.rag_engine.qa_pairs:
            logger.info(f"✅ RAG engine loaded {len(self.rag_engine.qa_pairs)} Q&A pairs")
        else:
            logger.warning("⚠️ RAG engine has no Q&A data")
        
        if self.rag_engine.events:
            logger.info(f"✅ RAG engine loaded {len(self.rag_engine.events)} events")
        else:
            logger.warning("⚠️ RAG engine has no events data")
        
        # Test points system
        logger.info("✅ Points system initialized")
    
    def process_query(self, query: str, student_id: str = None) -> Dict:
        """
        Process a student query and return a comprehensive response
        
        Args:
            query: Student's question
            student_id: Optional student ID for personalized responses
            
        Returns:
            Dictionary containing response and additional information
        """
        try:
            # Get relevant context from RAG engine
            context = self.rag_engine.get_context_for_query(query)
            
            # Generate LLM response
            llm_response = self.llm_client.generate_response(query, context)
            
            # Check if this is an event-related query
            relevant_events = self.rag_engine.search_events(query)
            
            # Prepare response
            response = {
                "query": query,
                "response": llm_response,
                "context_used": bool(context),
                "relevant_events": relevant_events,
                "student_id": student_id
            }
            
            # Add student-specific information if provided
            if student_id:
                student_stats = self.points_system.get_student_stats(student_id)
                if student_stats:
                    response["student_stats"] = {
                        "current_points": student_stats["current_points"],
                        "events_attended": student_stats["events_attended"],
                        "badges": student_stats["badges"]
                    }
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "query": query,
                "response": "I'm sorry, I encountered an error while processing your question. Please try again.",
                "error": str(e)
            }
    
    def register_student(self, student_id: str, name: str = None) -> Dict:
        """Register a new student in the points system"""
        return self.points_system.register_student(student_id, name)
    
    def award_event_points(self, student_id: str, event_id: str, points: int) -> bool:
        """Award points to a student for attending an event"""
        return self.points_system.award_points_for_event(student_id, event_id, points)
    
    def get_student_stats(self, student_id: str) -> Dict:
        """Get comprehensive student statistics"""
        return self.points_system.get_student_stats(student_id)
    
    def get_available_rewards(self, student_id: str = None) -> List[Dict]:
        """Get available rewards for a student"""
        return self.points_system.get_available_rewards(student_id)
    
    def claim_reward(self, student_id: str, reward_id: str) -> Dict:
        """Allow a student to claim a reward"""
        return self.points_system.claim_reward(student_id, reward_id)
    
    def get_leaderboard(self, top_n: int = 10) -> List[Dict]:
        """Get top students by points"""
        return self.points_system.get_leaderboard(top_n)
    
    def get_events_by_category(self, category: str = None) -> List[Dict]:
        """Get events filtered by category"""
        return self.rag_engine.get_events_by_category(category)
    
    def get_events_with_food(self) -> List[Dict]:
        """Get all events that offer free food"""
        return self.rag_engine.get_events_with_food()
    
    def interactive_mode(self):
        """Run the assistant in interactive mode"""
        print("🦁 Welcome to LMU Campus Assistant!")
        print("Ask me anything about LMU campus life, policies, or events!")
        print("Type 'help' for commands, 'quit' to exit")
        print("-" * 50)
        
        current_student_id = None
        
        while True:
            try:
                # Get user input
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for using LMU Campus Assistant! Go Lions! 🦁")
                    break
                
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                elif user_input.lower().startswith('register '):
                    # Register a new student
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 3:
                        student_id = parts[1]
                        name = parts[2]
                        result = self.register_student(student_id, name)
                        print(f"✅ Registered student: {result['name']}")
                        current_student_id = student_id
                    else:
                        print("❌ Usage: register <student_id> <name>")
                    continue
                
                elif user_input.lower().startswith('login '):
                    # Login as existing student
                    student_id = user_input.split(' ', 1)[1]
                    student_info = self.points_system.get_student_info(student_id)
                    if student_info:
                        current_student_id = student_id
                        print(f"✅ Logged in as: {student_info['name']}")
                        print(f"   Points: {student_info['points']}")
                        print(f"   Events attended: {len(student_info['events_attended'])}")
                    else:
                        print("❌ Student not found. Use 'register' to create a new account.")
                    continue
                
                elif user_input.lower() == 'stats':
                    # Show current student stats
                    if current_student_id:
                        stats = self.get_student_stats(current_student_id)
                        self._display_student_stats(stats)
                    else:
                        print("❌ Please login first with 'login <student_id>'")
                    continue
                
                elif user_input.lower() == 'rewards':
                    # Show available rewards
                    rewards = self.get_available_rewards(current_student_id)
                    self._display_rewards(rewards, current_student_id)
                    continue
                
                elif user_input.lower() == 'leaderboard':
                    # Show leaderboard
                    leaderboard = self.get_leaderboard()
                    self._display_leaderboard(leaderboard)
                    continue
                
                elif user_input.lower() == 'events':
                    # Show upcoming events
                    events = self.rag_engine.events
                    self._display_events(events)
                    continue
                
                elif user_input.lower() == 'food events':
                    # Show events with free food
                    food_events = self.get_events_with_food()
                    self._display_events(food_events, title="Events with Free Food 🍕")
                    continue
                
                # Process regular query
                result = self.process_query(user_input, current_student_id)
                
                # Display response
                print(f"\n🤖 LMU Assistant: {result['response']}")
                
                # Show relevant events if any
                if result.get('relevant_events'):
                    print("\n📅 Related Events:")
                    for event in result['relevant_events'][:3]:  # Show top 3
                        print(f"  • {event['title']} - {event['date']} at {event['time']}")
                        print(f"    Location: {event['location']} | Points: {event['points']}")
                        if event['free_food']:
                            print(f"    🍕 Free food included!")
                
                # Show student stats if logged in
                if current_student_id and result.get('student_stats'):
                    stats = result['student_stats']
                    print(f"\n👤 Your Stats: {stats['current_points']} points | {stats['events_attended']} events attended")
                
            except KeyboardInterrupt:
                print("\n👋 Thanks for using LMU Campus Assistant! Go Lions! 🦁")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _show_help(self):
        """Show available commands"""
        print("\n📋 Available Commands:")
        print("  register <student_id> <name>  - Register as a new student")
        print("  login <student_id>            - Login as existing student")
        print("  stats                         - Show your statistics")
        print("  rewards                       - Show available rewards")
        print("  leaderboard                   - Show top students")
        print("  events                        - Show upcoming events")
        print("  food events                   - Show events with free food")
        print("  help                          - Show this help")
        print("  quit                          - Exit the assistant")
        print("\n💡 You can also ask me any question about LMU!")
    
    def _display_student_stats(self, stats: Dict):
        """Display student statistics"""
        if not stats:
            print("❌ No student data found")
            return
        
        print(f"\n👤 Student Statistics for {stats['name']}:")
        print(f"  Current Points: {stats['current_points']}")
        print(f"  Total Points Earned: {stats['total_points_earned']}")
        print(f"  Events Attended: {stats['events_attended']}")
        print(f"  Rewards Claimed: {stats['rewards_claimed']}")
        print(f"  Badges: {', '.join(stats['badges']) if stats['badges'] else 'None'}")
        print(f"  Member since: {stats['registration_date'][:10]}")
    
    def _display_rewards(self, rewards: List[Dict], student_id: str = None):
        """Display available rewards"""
        if not rewards:
            print("❌ No rewards available")
            return
        
        print(f"\n🎁 Available Rewards:")
        for reward in rewards:
            status = ""
            if student_id:
                if reward.get('already_claimed'):
                    status = " (Claimed)"
                elif not reward.get('affordable'):
                    status = f" (Need {reward['points_required'] - reward.get('student_points', 0)} more points)"
                else:
                    status = " (Can claim!)"
            
            print(f"  • {reward['name']} - {reward['points_required']} points{status}")
            print(f"    {reward['description']}")
    
    def _display_leaderboard(self, leaderboard: List[Dict]):
        """Display leaderboard"""
        if not leaderboard:
            print("❌ No students found")
            return
        
        print(f"\n🏆 Top Students:")
        for i, student in enumerate(leaderboard, 1):
            badges_str = f" [{', '.join(student['badges'])}]" if student['badges'] else ""
            print(f"  {i}. {student['name']} - {student['points']} points{badges_str}")
    
    def _display_events(self, events: List[Dict], title: str = "Upcoming Events"):
        """Display events"""
        if not events:
            print("❌ No events found")
            return
        
        print(f"\n📅 {title}:")
        for event in events:
            food_icon = "🍕" if event['free_food'] else ""
            print(f"  • {event['title']} - {event['date']} at {event['time']}")
            print(f"    Location: {event['location']} | Points: {event['points']} {food_icon}")
            print(f"    {event['description']}")

def main():
    """Main entry point"""
    try:
        assistant = LMUCampusAssistant()
        
        # Check if running in interactive mode
        if len(sys.argv) > 1 and sys.argv[1] == '--interactive':
            assistant.interactive_mode()
        else:
            # Run a quick test
            print("🦁 LMU Campus Assistant - Quick Test")
            print("-" * 40)
            
            test_queries = [
                "What are the library hours?",
                "How do I find a math tutor?",
                "What events have free food this week?"
            ]
            
            for query in test_queries:
                print(f"\nQ: {query}")
                result = assistant.process_query(query)
                print(f"A: {result['response']}")
            
            print(f"\n✅ Test completed! Run with '--interactive' for full experience.")
            
    except Exception as e:
        logger.error(f"Failed to start assistant: {e}")
        print(f"❌ Error starting assistant: {e}")
        print("Make sure Ollama is running and the model is downloaded.")

if __name__ == "__main__":
    main()