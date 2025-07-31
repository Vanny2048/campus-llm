#!/usr/bin/env python3
"""
LMU Buddy API Server
A Flask API server for the LMU GenZ Buddy chatbot integration.
This can be connected to your fine-tuned Llama model.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Mock responses for development - replace with your actual Llama model
def get_lmu_buddy_response(question: str) -> str:
    """
    Get response from LMU Buddy. This function should be replaced with your actual Llama model.
    """
    question_lower = question.lower()
    
    # LMU-specific responses with GenZ tone
    responses = {
        "food": [
            "Omg the best food on campus is def the Lair! Their chicken tenders are *chef's kiss* 🤌 And if you're feeling fancy, try the dining hall's pasta night - it's actually fire 🔥",
            "The Lair is where it's at! Their burgers are lowkey amazing and the fries are always crispy. Pro tip: go during off-peak hours to avoid the line! 📍",
            "For real food, hit up the Lair or the dining hall. The Lair has better burgers, but the dining hall has unlimited food which is perfect for when you're broke af 💸"
        ],
        "study": [
            "Best study spots? The library is obvious but also try the 3rd floor of Malone - it's quiet af and has the best views! Plus there's coffee nearby ☕",
            "For serious studying, go to the library basement. It's like a dungeon but in a good way - super quiet and no distractions. Perfect for when you need to grind 📚",
            "The library is clutch but also check out the study rooms in Malone. They're first come first serve but worth it if you can snag one! 🎯"
        ],
        "events": [
            "Check the events page! There's always something going on - from basketball games to random club meetings. The best events are usually posted on Instagram too 📱",
            "There's literally always something happening! Basketball games are the move, and don't sleep on the random club events - they're actually fun and you get free food 🏀",
            "Events are everywhere! The app shows everything, but also follow @lmu_events on Instagram for the latest. Basketball games are a must - the energy is unmatched! 🦁"
        ],
        "parking": [
            "Parking is a nightmare ngl 😅 Try the lots near the dorms or the structure by the library. Pro tip: get here early or you'll be walking from the moon 🌙",
            "Parking is rough but the structure by the library usually has spots. Just be ready to pay like $10 for the day. Worth it to not walk a mile though! 🚗",
            "Parking is literally the worst part of LMU 😤 Try the lots near the dorms or just accept that you'll be walking. At least it's good exercise? 💪"
        ],
        "prizes": [
            "The prizes are actually insane this year! MacBooks, AirPods, even lunch with the president. Just keep checking in to events and posting on social media - it's that easy! 🏆",
            "Prizes are fire! You can win everything from tech to exclusive experiences. Just stay active on the app and you'll rack up points in no time! 💎",
            "The prize game is strong this year! From laptops to exclusive events, there's something for everyone. Just keep grinding those points! 🎁"
        ],
        "basketball": [
            "Basketball games are LITERALLY the best part of LMU! The energy is unmatched and the team is actually good this year. You have to go to at least one game! 🏀",
            "Basketball games are where it's at! The student section goes crazy and the team is actually decent this year. Plus you get points for going! 🦁",
            "Basketball games are a vibe! The student section is wild and the team is actually good. Don't miss out on the free points and the fun! 🎉"
        ],
        "classes": [
            "Classes are what you make them! Some are easy, some are hard, but most profs are actually pretty chill if you show up and do the work 📚",
            "The class difficulty really depends on your major and the professor. RateMyProfessors is your best friend for picking classes! 💡",
            "Classes can be tough but most profs are super helpful during office hours. Don't be afraid to ask for help! 🎓"
        ],
        "dorms": [
            "Dorm life is what you make it! Some dorms are nicer than others but they all have their perks. The community is what makes it fun! 🏠",
            "Dorms are a mixed bag but they're all pretty decent. The newer ones are obviously nicer but the older ones have character! Plus you're close to everything 📍",
            "Living in the dorms is actually pretty fun! You're close to classes, food, and friends. The RA's are usually cool too! 🎉"
        ]
    }
    
    # Check for keywords and return appropriate response
    for keyword, response_list in responses.items():
        if keyword in question_lower:
            return random.choice(response_list)
    
    # Default GenZ LMU Buddy response
    default_responses = [
        "That's a great question! As your LMU Buddy, I'm here to help with literally anything campus-related. What else do you want to know? 🤔",
        "Omg I love that question! LMU is the best and I know everything about it. What else are you curious about? 🦁",
        "That's such a good question! I'm your go-to for all things LMU. What else do you want to know about campus life? 💫",
        "Love that energy! I'm here to help you navigate LMU like a pro. What else are you wondering about? ✨",
        "Great question! I'm your LMU insider who knows all the tea. What else can I help you with? 🔥"
    ]
    
    return random.choice(default_responses)

@app.route('/api/genz-buddy', methods=['POST'])
def genz_buddy():
    """
    Main endpoint for LMU Buddy chat.
    Expected JSON payload: {"prompt": "user question"}
    Returns: {"answer": "buddy response", "timestamp": "iso timestamp"}
    """
    try:
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({
                "error": "Missing 'prompt' in request body",
                "answer": "Hey! I need a question to help you out! 🤔"
            }), 400
        
        question = data['prompt'].strip()
        
        if not question:
            return jsonify({
                "error": "Empty prompt",
                "answer": "What's on your mind? I'm here to help! 🦁"
            }), 400
        
        # Log the question for debugging
        logger.info(f"Received question: {question}")
        
        # Get response from LMU Buddy
        response = get_lmu_buddy_response(question)
        
        # Log the response
        logger.info(f"Generated response: {response}")
        
        return jsonify({
            "answer": response,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        })
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return jsonify({
            "error": "Internal server error",
            "answer": "Oops! I'm having some tech issues rn, but I'll be back in a sec! 🔧"
        }), 500

@app.route('/api/genz-buddy/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "LMU GenZ Buddy API",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/genz-buddy/suggestions', methods=['GET'])
def get_suggestions():
    """Get suggested questions for the chat interface"""
    suggestions = [
        "What's the best food on campus?",
        "Where should I study?",
        "What events are happening this week?",
        "How do I get more spirit points?",
        "What's the parking situation like?",
        "Tell me about basketball games!",
        "What are the best dorms?",
        "How do I join Greek life?"
    ]
    
    return jsonify({
        "suggestions": suggestions,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/', methods=['GET'])
def root():
    """Root endpoint with API information"""
    return jsonify({
        "service": "LMU GenZ Buddy API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/genz-buddy (POST)",
            "health": "/api/genz-buddy/health (GET)",
            "suggestions": "/api/genz-buddy/suggestions (GET)"
        },
        "description": "Your GenZ campus companion who knows everything about LMU!",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("🦁 Starting LMU GenZ Buddy API Server...")
    print("📡 API will be available at: http://localhost:5000")
    print("💬 Chat endpoint: POST http://localhost:5000/api/genz-buddy")
    print("🏥 Health check: GET http://localhost:5000/api/genz-buddy/health")
    print("\n" + "="*50)
    print("To integrate with your fine-tuned Llama model:")
    print("1. Replace the get_lmu_buddy_response() function")
    print("2. Add your model loading and inference code")
    print("3. Update the API endpoint to use your model")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)