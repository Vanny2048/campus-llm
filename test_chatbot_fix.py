#!/usr/bin/env python3
"""
Test script to verify chatbot functionality
"""

import sys
import os

# Add the current directory to the path so we can import from app.py
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_chatbot_functionality():
    """Test the chatbot response function"""
    try:
        # Import the function from app.py
        from app import simulate_ai_response
        
        # Test questions
        test_questions = [
            "what even is campus llm?",
            "where can i study?",
            "what's happening on campus this week?",
            "how do i join greek life?"
        ]
        
        print("🧪 Testing Chatbot Functionality")
        print("=" * 50)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n{i}. Question: {question}")
            try:
                response = simulate_ai_response(question)
                print(f"   Response: {response[:100]}...")
                print("   ✅ Success")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        print("\n" + "=" * 50)
        print("🎉 Chatbot functionality test completed!")
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("Make sure app.py is in the same directory")
    except Exception as e:
        print(f"❌ General Error: {e}")

if __name__ == "__main__":
    test_chatbot_functionality()