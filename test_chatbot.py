#!/usr/bin/env python3
"""
Test script for the LMU Campus LLM chatbot functionality
"""

import sys
import os

# Add the current directory to the path so we can import from app.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import simulate_ai_response

def test_chatbot():
    """Test the chatbot with various questions"""
    
    test_questions = [
        "what even is campus llm?",
        "what's happening on campus this week?",
        "what should i eat rn?",
        "how do i email my prof when i fumbled an assignment?",
        "i feel like i'm failing everything",
        "where can i study?",
        "what events are coming up?",
        "how do i join greek life?",
        "where is the library?",
        "what's the best food on campus?",
        "how do i get help with my classes?",
        "random question about nothing"
    ]
    
    print("🤖 Testing LMU Campus LLM Chatbot")
    print("=" * 50)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Question: {question}")
        try:
            response = simulate_ai_response(question)
            print(f"   Response: {response}")
            print(f"   Status: ✅ Working")
        except Exception as e:
            print(f"   Status: ❌ Error - {str(e)}")
    
    print("\n" + "=" * 50)
    print("🎉 Chatbot testing completed!")

if __name__ == "__main__":
    test_chatbot()