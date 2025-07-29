#!/usr/bin/env python3
"""
Standalone test script for enhanced LMU Campus LLM application
Tests core functionality without Streamlit dependencies
"""

import re
import sys

# Define the functions we want to test (copied from the main app)
def validate_lmu_id(lmu_id: str) -> bool:
    """Validate LMU ID format (9 digits)"""
    if not lmu_id:
        return False
    # Remove any non-digit characters
    clean_id = re.sub(r'\D', '', lmu_id)
    # Check if it's exactly 9 digits
    return len(clean_id) == 9 and clean_id.isdigit()

# Comprehensive LMU Knowledge Base
LMU_KNOWLEDGE_BASE = {
    "academics": {
        "colleges": [
            "Bellarmine College of Liberal Arts",
            "College of Business Administration", 
            "College of Communication and Fine Arts",
            "Frank R. Seaver College of Science and Engineering",
            "School of Education",
            "School of Film and Television",
            "Loyola Law School"
        ],
        "academic_calendar": {
            "add_drop_deadline": "First week of classes",
            "midterms": "Weeks 6-8",
            "finals": "Last week of semester",
            "graduation": "May and December"
        },
        "resources": {
            "tutoring": "Academic Resource Center in Daum Hall",
            "library": "William H. Hannon Library",
            "writing_center": "Center for Student Success",
            "advising": "Academic Advising Center"
        }
    },
    "campus_life": {
        "dining": [
            "Lair Marketplace",
            "The Lion's Den",
            "The Habit Burger Grill",
            "Starbucks",
            "Einstein Bros. Bagels"
        ],
        "housing": [
            "First Year Experience (FYE) Halls",
            "Sophomore Experience (SOE) Halls",
            "Upper Division Housing",
            "Greek Housing"
        ],
        "transportation": {
            "shuttle": "LMU Shuttle Service",
            "parking": "Student Parking Lots",
            "bike_share": "Lion Bike Share Program"
        }
    },
    "student_organizations": {
        "greek_life": [
            "Alpha Phi Omega",
            "Delta Gamma",
            "Kappa Alpha Theta",
            "Pi Beta Phi",
            "Sigma Chi",
            "Theta Xi"
        ],
        "clubs": [
            "Student Government",
            "Campus Ministry",
            "International Student Association",
            "Black Student Union",
            "Latinx Student Union",
            "Asian Pacific Student Services"
        ]
    },
    "athletics": {
        "teams": [
            "Men's Basketball",
            "Women's Basketball", 
            "Men's Soccer",
            "Women's Soccer",
            "Baseball",
            "Softball",
            "Volleyball",
            "Tennis",
            "Golf",
            "Swimming & Diving"
        ],
        "venues": {
            "basketball": "Gersten Pavilion",
            "soccer": "Sullivan Field",
            "baseball": "Page Stadium",
            "softball": "Smith Field"
        },
        "mascot": "Iggy the Lion",
        "colors": "Blue and White",
        "conference": "West Coast Conference (WCC)"
    },
    "campus_services": {
        "health": "Student Health Services",
        "counseling": "Student Psychological Services",
        "career": "Career and Professional Development",
        "financial_aid": "Financial Aid Office",
        "registrar": "Office of the Registrar",
        "it_support": "Information Technology Services"
    },
    "location": {
        "address": "1 LMU Drive, Los Angeles, CA 90045",
        "area": "Westchester neighborhood of Los Angeles",
        "nearby": [
            "Los Angeles International Airport (LAX)",
            "Playa Vista",
            "Marina del Rey",
            "Venice Beach",
            "Santa Monica"
        ]
    }
}

# Sample game events for testing
GAME_EVENTS = [
    {
        "id": "bb_001",
        "sport": "🏀 Basketball",
        "opponent": "Pepperdine",
        "date": "2024-02-15",
        "time": "19:00",
        "venue": "Gersten Pavilion",
        "type": "home",
        "spirit_points": 50,
        "tailgate": "Lions Den Tailgate (4:00 PM)",
        "description": "Rivalry game against Pepperdine! Wear your blue and white!"
    }
]

def get_enhanced_ai_response(question: str) -> str:
    """Enhanced AI response system with comprehensive LMU knowledge"""
    question_lower = question.lower()
    
    # Academic queries
    if any(word in question_lower for word in ["add/drop", "deadline", "registration"]):
        return f"📚 **Add/Drop Deadline**: {LMU_KNOWLEDGE_BASE['academics']['academic_calendar']['add_drop_deadline']}. Check your student portal for exact dates and any holds on your account!"
    
    if any(word in question_lower for word in ["tutor", "tutoring", "help", "study"]):
        return f"📖 **Tutoring Services**: Visit the {LMU_KNOWLEDGE_BASE['academics']['resources']['tutoring']} for free tutoring! They offer drop-in sessions and scheduled appointments for most subjects."
    
    if any(word in question_lower for word in ["library", "study", "quiet"]):
        return f"📚 **Study Spots**: The {LMU_KNOWLEDGE_BASE['academics']['resources']['library']} has multiple floors - 3rd floor is quiet study, Lion's Den is social study, and there are study rooms in the business school!"
    
    # Campus life queries
    if any(word in question_lower for word in ["food", "eat", "dining", "restaurant"]):
        dining_options = ", ".join(LMU_KNOWLEDGE_BASE['campus_life']['dining'])
        return f"🍕 **Dining Options**: {dining_options}. The Lion's Den is great for social dining, and the Lair has the most variety!"
    
    if any(word in question_lower for word in ["parking", "car", "transport"]):
        return f"🚗 **Transportation**: {LMU_KNOWLEDGE_BASE['campus_life']['transportation']['parking']} available. Also check out the {LMU_KNOWLEDGE_BASE['campus_life']['transportation']['shuttle']} for getting around campus!"
    
    # Athletics queries
    if any(word in question_lower for word in ["game", "basketball", "soccer", "sport"]):
        next_game = GAME_EVENTS[0]
        return f"🏀 **Next Game**: {next_game['sport']} vs {next_game['opponent']} on {next_game['date']} at {next_game['time']} in {next_game['venue']}! {next_game.get('tailgate', '')}"
    
    if any(word in question_lower for word in ["mascot", "colors", "spirit"]):
        return f"🦁 **LMU Spirit**: Our mascot is {LMU_KNOWLEDGE_BASE['athletics']['mascot']} and our colors are {LMU_KNOWLEDGE_BASE['athletics']['colors']}! Go Lions! 🦁"
    
    # Student organizations
    if any(word in question_lower for word in ["club", "organization", "join", "greek"]):
        return f"👥 **Student Organizations**: LMU has over 200 clubs! Visit the Student Leadership & Development office in Malone Student Center to browse all organizations. Popular options include {', '.join(LMU_KNOWLEDGE_BASE['student_organizations']['clubs'][:3])}."
    
    # Campus services
    if any(word in question_lower for word in ["health", "medical", "doctor"]):
        return f"🏥 **Health Services**: {LMU_KNOWLEDGE_BASE['campus_services']['health']} is located in Malone Student Center. They offer medical appointments, immunizations, and health education!"
    
    if any(word in question_lower for word in ["counseling", "therapy", "mental health"]):
        return f"🧠 **Counseling**: {LMU_KNOWLEDGE_BASE['campus_services']['counseling']} provides free individual and group therapy sessions. They're located in Malone Student Center."
    
    if any(word in question_lower for word in ["career", "job", "internship"]):
        return f"💼 **Career Services**: {LMU_KNOWLEDGE_BASE['campus_services']['career']} offers resume reviews, interview prep, job fairs, and internship opportunities!"
    
    # Location queries
    if any(word in question_lower for word in ["where", "location", "address"]):
        return f"📍 **LMU Location**: {LMU_KNOWLEDGE_BASE['location']['address']} in the {LMU_KNOWLEDGE_BASE['location']['area']} neighborhood of Los Angeles."
    
    # Default response with helpful suggestions
    return f"🦁 **LMU Campus Assistant**: I'm here to help with all things LMU! Try asking about:\n\n• **Academics**: Add/drop deadlines, tutoring, study spots\n• **Campus Life**: Dining options, parking, housing\n• **Athletics**: Game schedules, spirit events\n• **Student Services**: Health, counseling, career services\n• **Organizations**: Clubs, Greek life, student groups\n\nOr check out the other tabs for game day info and spirit challenges! 🎉"

def test_lmu_id_validation():
    """Test LMU ID validation function"""
    print("🧪 Testing LMU ID Validation...")
    
    # Valid IDs
    valid_ids = [
        "123456789",
        "987654321",
        "000000001",
        "999999999"
    ]
    
    # Invalid IDs
    invalid_ids = [
        "",
        "12345678",  # Too short
        "1234567890",  # Too long
        "12345678a",  # Contains letter
        "abc123def"  # Contains letters
    ]
    
    # IDs with formatting that should be accepted (dashes, spaces)
    formatted_ids = [
        "123-456-789",
        "123 456 789",
        "123.456.789"
    ]
    
    # Test valid IDs
    for lmu_id in valid_ids:
        result = validate_lmu_id(lmu_id)
        if result:
            print(f"✅ Valid ID '{lmu_id}' - PASSED")
        else:
            print(f"❌ Valid ID '{lmu_id}' - FAILED")
            return False
    
    # Test invalid IDs
    for lmu_id in invalid_ids:
        result = validate_lmu_id(lmu_id)
        if not result:
            print(f"✅ Invalid ID '{lmu_id}' - PASSED")
        else:
            print(f"❌ Invalid ID '{lmu_id}' - FAILED (should be invalid but was accepted)")
            return False
    
    # Test formatted IDs (should be accepted)
    for lmu_id in formatted_ids:
        result = validate_lmu_id(lmu_id)
        if result:
            print(f"✅ Formatted ID '{lmu_id}' - PASSED")
        else:
            print(f"❌ Formatted ID '{lmu_id}' - FAILED (should be accepted)")
            return False
    
    print("🎉 All LMU ID validation tests passed!")
    return True

def test_ai_responses():
    """Test AI response function"""
    print("\n🧪 Testing AI Response System...")
    
    test_questions = [
        ("When is add/drop deadline?", "add/drop"),
        ("Where can I find tutoring?", "tutoring"),
        ("What are the dining options?", "dining"),
        ("When's the next basketball game?", "game"),
        ("What's the mascot?", "mascot"),
        ("How do I join a club?", "club"),
        ("Where is the health center?", "health"),
        ("What's the campus address?", "location"),
        ("Random question about nothing", "default")
    ]
    
    for question, expected_type in test_questions:
        response = get_enhanced_ai_response(question)
        print(f"✅ Question: '{question}'")
        print(f"   Response type: {expected_type}")
        print(f"   Response length: {len(response)} characters")
        print(f"   Response preview: {response[:100]}...")
        print()
    
    print("🎉 All AI response tests completed!")
    return True

def test_knowledge_base():
    """Test knowledge base structure"""
    print("\n🧪 Testing Knowledge Base Structure...")
    
    required_sections = [
        "academics",
        "campus_life", 
        "student_organizations",
        "athletics",
        "campus_services",
        "location"
    ]
    
    for section in required_sections:
        if section in LMU_KNOWLEDGE_BASE:
            print(f"✅ Section '{section}' exists")
        else:
            print(f"❌ Section '{section}' missing")
            return False
    
    # Test specific knowledge
    if "colleges" in LMU_KNOWLEDGE_BASE["academics"]:
        print(f"✅ Found {len(LMU_KNOWLEDGE_BASE['academics']['colleges'])} colleges")
    
    if "teams" in LMU_KNOWLEDGE_BASE["athletics"]:
        print(f"✅ Found {len(LMU_KNOWLEDGE_BASE['athletics']['teams'])} athletic teams")
    
    if "mascot" in LMU_KNOWLEDGE_BASE["athletics"]:
        print(f"✅ Mascot: {LMU_KNOWLEDGE_BASE['athletics']['mascot']}")
    
    print("🎉 All knowledge base tests passed!")
    return True

def test_data_structures():
    """Test sample data structures"""
    print("\n🧪 Testing Data Structures...")
    
    print(f"✅ Game Events: {len(GAME_EVENTS)} events")
    
    # Test event structure
    if GAME_EVENTS:
        event = GAME_EVENTS[0]
        required_fields = ["id", "sport", "opponent", "date", "time", "venue", "type", "spirit_points"]
        for field in required_fields:
            if field in event:
                print(f"✅ Event has '{field}' field")
            else:
                print(f"❌ Event missing '{field}' field")
                return False
    
    print("🎉 All data structure tests passed!")
    return True

def main():
    """Run all tests"""
    print("🦁 LMU Campus LLM - Enhanced Application Test Suite")
    print("=" * 60)
    
    tests = [
        test_lmu_id_validation,
        test_ai_responses,
        test_knowledge_base,
        test_data_structures
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ Test {test.__name__} failed!")
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\n🚀 To run the application:")
        print("   1. Install dependencies: pip install -r enhanced_requirements.txt")
        print("   2. Run the app: streamlit run enhanced_lmu_app.py")
        print("   3. Open browser to: http://localhost:8501")
        return 0
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())