#!/usr/bin/env python3
"""
LMU Campus LLM - Simple Version
A simplified version that works with minimal dependencies
"""

import sys
import os
import json
import requests
from typing import Dict, List, Optional

class SimpleLMUAssistant:
    """Simplified LMU Campus Assistant"""
    
    def __init__(self):
        """Initialize the assistant"""
        self.ollama_url = "http://localhost:11434"
        self.model = "llama3.2:3b"
        
        # Load data
        self.qa_pairs = self._load_qa_data()
        self.events = self._load_events_data()
        self.students = self._load_students_data()
        
        print("🦁 LMU Campus Assistant - Simple Version")
        print("✅ Initialized successfully!")
    
    def _load_qa_data(self) -> List[Dict]:
        """Load Q&A data"""
        try:
            with open("data/qa_pairs.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("qa_pairs", [])
        except Exception as e:
            print(f"⚠️ Warning: Could not load Q&A data: {e}")
            return []
    
    def _load_events_data(self) -> List[Dict]:
        """Load events data"""
        try:
            with open("data/events.json", "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("events", [])
        except Exception as e:
            print(f"⚠️ Warning: Could not load events data: {e}")
            return []
    
    def _load_students_data(self) -> Dict:
        """Load students data"""
        try:
            with open("data/students.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"ℹ️ No existing students data found, starting fresh")
            return {}
    
    def _save_students_data(self):
        """Save students data"""
        try:
            with open("data/students.json", "w", encoding="utf-8") as f:
                json.dump(self.students, f, indent=2)
        except Exception as e:
            print(f"⚠️ Warning: Could not save students data: {e}")
    
    def test_ollama_connection(self) -> bool:
        """Test connection to Ollama"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_available = any(model["name"] == self.model for model in models)
                if model_available:
                    print("✅ Ollama connection successful")
                    return True
                else:
                    print("❌ LLaMA 3.2 3B model not found")
                    return False
            else:
                print("❌ Ollama connection failed")
                return False
        except Exception as e:
            print(f"❌ Ollama connection error: {e}")
            return False
    
    def ask_question(self, question: str) -> str:
        """Ask a question using the LLM"""
        try:
            # First, try to find a direct answer in our Q&A data
            direct_answer = self._find_direct_answer(question)
            if direct_answer:
                return direct_answer
            
            # If no direct answer, use the LLM
            prompt = f"""You are LMU Campus Assistant, a helpful AI assistant for Loyola Marymount University students.

Student Question: {question}

Please provide a helpful response. If you don't have specific information about this topic, suggest where the student might find more information.

Response:"""
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": 300
                }
            }
            
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "I'm sorry, I couldn't generate a response at this time.")
            else:
                return "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try again later."
                
        except Exception as e:
            print(f"Error asking question: {e}")
            return "I'm sorry, something went wrong. Please try again."
    
    def _find_direct_answer(self, question: str) -> Optional[str]:
        """Find a direct answer in our Q&A data"""
        question_lower = question.lower()
        
        for qa in self.qa_pairs:
            qa_question_lower = qa["question"].lower()
            
            # Simple keyword matching
            question_words = set(question_lower.split())
            qa_words = set(qa_question_lower.split())
            
            # Check for significant word overlap
            overlap = len(question_words.intersection(qa_words))
            if overlap >= 2:  # At least 2 words match
                return qa["answer"]
        
        return None
    
    def get_events(self, category: str = None) -> List[Dict]:
        """Get events, optionally filtered by category"""
        if not category:
            return self.events
        
        return [event for event in self.events if event.get("category") == category]
    
    def get_events_with_food(self) -> List[Dict]:
        """Get events that offer free food"""
        return [event for event in self.events if event.get("free_food")]
    
    def register_student(self, student_id: str, name: str) -> Dict:
        """Register a new student"""
        if student_id in self.students:
            return {"success": False, "message": "Student already registered"}
        
        self.students[student_id] = {
            "name": name,
            "points": 0,
            "events_attended": [],
            "registration_date": "2024-10-15"  # Simplified for demo
        }
        
        self._save_students_data()
        return {"success": True, "message": f"Registered {name} successfully!"}
    
    def get_student_info(self, student_id: str) -> Optional[Dict]:
        """Get student information"""
        return self.students.get(student_id)
    
    def award_points(self, student_id: str, event_id: str, points: int) -> bool:
        """Award points to a student for attending an event"""
        if student_id not in self.students:
            return False
        
        if event_id in self.students[student_id]["events_attended"]:
            return False  # Already attended
        
        self.students[student_id]["points"] += points
        self.students[student_id]["events_attended"].append(event_id)
        self._save_students_data()
        return True
    
    def get_leaderboard(self) -> List[Dict]:
        """Get top students by points"""
        students_list = []
        for student_id, student_data in self.students.items():
            students_list.append({
                "student_id": student_id,
                "name": student_data["name"],
                "points": student_data["points"],
                "events_attended": len(student_data["events_attended"])
            })
        
        # Sort by points (descending)
        students_list.sort(key=lambda x: x["points"], reverse=True)
        return students_list[:10]  # Top 10
    
    def interactive_mode(self):
        """Run interactive mode"""
        print("\n🦁 Welcome to LMU Campus Assistant!")
        print("Ask me anything about LMU campus life, policies, or events!")
        print("Type 'help' for commands, 'quit' to exit")
        print("-" * 50)
        
        current_student_id = None
        
        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Thanks for using LMU Campus Assistant! Go Lions! 🦁")
                    break
                
                elif user_input.lower() == 'help':
                    self._show_help()
                    continue
                
                elif user_input.lower().startswith('register '):
                    parts = user_input.split(' ', 2)
                    if len(parts) >= 3:
                        student_id = parts[1]
                        name = parts[2]
                        result = self.register_student(student_id, name)
                        print(f"✅ {result['message']}")
                        current_student_id = student_id
                    else:
                        print("❌ Usage: register <student_id> <name>")
                    continue
                
                elif user_input.lower().startswith('login '):
                    student_id = user_input.split(' ', 1)[1]
                    student_info = self.get_student_info(student_id)
                    if student_info:
                        current_student_id = student_id
                        print(f"✅ Logged in as: {student_info['name']}")
                        print(f"   Points: {student_info['points']}")
                    else:
                        print("❌ Student not found. Use 'register' to create a new account.")
                    continue
                
                elif user_input.lower() == 'stats':
                    if current_student_id:
                        student_info = self.get_student_info(current_student_id)
                        if student_info:
                            print(f"\n👤 Stats for {student_info['name']}:")
                            print(f"   Points: {student_info['points']}")
                            print(f"   Events attended: {len(student_info['events_attended'])}")
                    else:
                        print("❌ Please login first with 'login <student_id>'")
                    continue
                
                elif user_input.lower() == 'events':
                    events = self.events
                    if events:
                        print("\n📅 Upcoming Events:")
                        for event in events[:5]:  # Show first 5
                            food_icon = "🍕" if event.get('free_food') else ""
                            print(f"  • {event['title']} - {event['date']} at {event['time']}")
                            print(f"    Location: {event['location']} | Points: {event['points']} {food_icon}")
                    else:
                        print("❌ No events found")
                    continue
                
                elif user_input.lower() == 'food events':
                    food_events = self.get_events_with_food()
                    if food_events:
                        print("\n🍕 Events with Free Food:")
                        for event in food_events:
                            print(f"  • {event['title']} - {event['date']} at {event['time']}")
                            print(f"    Location: {event['location']} | Points: {event['points']}")
                    else:
                        print("❌ No food events found")
                    continue
                
                elif user_input.lower() == 'leaderboard':
                    leaderboard = self.get_leaderboard()
                    if leaderboard:
                        print("\n🏆 Top Students:")
                        for i, student in enumerate(leaderboard, 1):
                            print(f"  {i}. {student['name']} - {student['points']} points")
                    else:
                        print("❌ No students found")
                    continue
                
                # Process regular query
                response = self.ask_question(user_input)
                print(f"\n🤖 LMU Assistant: {response}")
                
                # Show student stats if logged in
                if current_student_id:
                    student_info = self.get_student_info(current_student_id)
                    if student_info:
                        print(f"\n👤 Your Stats: {student_info['points']} points | {len(student_info['events_attended'])} events attended")
                
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
        print("  events                        - Show upcoming events")
        print("  food events                   - Show events with free food")
        print("  leaderboard                   - Show top students")
        print("  help                          - Show this help")
        print("  quit                          - Exit the assistant")
        print("\n💡 You can also ask me any question about LMU!")

def main():
    """Main entry point"""
    try:
        assistant = SimpleLMUAssistant()
        
        # Test Ollama connection
        if not assistant.test_ollama_connection():
            print("❌ Cannot connect to Ollama. Make sure it's running with 'ollama serve'")
            return
        
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
                response = assistant.ask_question(query)
                print(f"A: {response}")
            
            print(f"\n✅ Test completed! Run with '--interactive' for full experience.")
            
    except Exception as e:
        print(f"❌ Error starting assistant: {e}")
        print("Make sure Ollama is running and the model is downloaded.")

if __name__ == "__main__":
    main()