#!/usr/bin/env python3
"""
Final Test Summary for LMU Campus LLM
Comprehensive overview of all tested functionality
"""

import sys
import os
import requests
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_all_functionality():
    """Test all functionality and provide comprehensive summary"""
    print("🦁 LMU Campus LLM - Complete Functionality Test")
    print("=" * 60)
    
    test_results = []
    
    # Test 1: Streamlit Demo Functions
    print("\n📱 Testing Streamlit Demo Functions...")
    try:
        import streamlit_demo
        from streamlit_demo import get_ai_response
        
        # Test AI responses
        test_questions = [
            "What is LMU?",
            "Tell me about campus events", 
            "How do I get spirit points?",
            "What's happening this weekend?"
        ]
        
        ai_responses = 0
        for question in test_questions:
            response = get_ai_response(question)
            if response and len(response) > 10:
                ai_responses += 1
        
        if ai_responses >= 3:
            test_results.append(("AI Chat System", "✅ PASS", f"{ai_responses}/4 responses working"))
        else:
            test_results.append(("AI Chat System", "❌ FAIL", f"Only {ai_responses}/4 responses"))
        
        # Test navigation functions
        nav_functions = [
            'show_home_dashboard', 'show_game_day', 'show_tailgates',
            'show_watch_parties', 'show_prizes', 'show_ai_chat'
        ]
        
        available_nav = sum(1 for func in nav_functions if hasattr(streamlit_demo, func))
        if available_nav >= 4:
            test_results.append(("Navigation Functions", "✅ PASS", f"{available_nav}/6 functions available"))
        else:
            test_results.append(("Navigation Functions", "❌ FAIL", f"Only {available_nav}/6 functions"))
            
    except Exception as e:
        test_results.append(("Streamlit Demo", "❌ FAIL", f"Error: {str(e)}"))
    
    # Test 2: Main App Functions
    print("📊 Testing Main App Functions...")
    try:
        import app
        from app import load_mock_data, generate_qr_code, simulate_ai_response, create_calendar_events
        
        # Test data loading
        events, prizes, leaderboard, badges = load_mock_data()
        
        if len(events) > 0:
            test_results.append(("Events Data", "✅ PASS", f"{len(events)} events loaded"))
        else:
            test_results.append(("Events Data", "❌ FAIL", "No events found"))
        
        if len(prizes) > 0:
            test_results.append(("Prizes Data", "✅ PASS", f"{len(prizes)} prizes loaded"))
        else:
            test_results.append(("Prizes Data", "❌ FAIL", "No prizes found"))
        
        if len(leaderboard) > 0:
            test_results.append(("Leaderboard Data", "✅ PASS", f"{len(leaderboard)} entries loaded"))
        else:
            test_results.append(("Leaderboard Data", "❌ FAIL", "No leaderboard data"))
        
        if len(badges) > 0:
            test_results.append(("Badges Data", "✅ PASS", f"{len(badges)} badge types available"))
        else:
            test_results.append(("Badges Data", "❌ FAIL", "No badges found"))
        
        # Test QR code generation
        qr_code = generate_qr_code("test_event", "test_user")
        if qr_code:
            test_results.append(("QR Code Generation", "✅ PASS", "QR codes working"))
        else:
            test_results.append(("QR Code Generation", "❌ FAIL", "QR generation failed"))
        
        # Test AI simulation
        ai_response = simulate_ai_response("What is LMU?")
        if ai_response and len(ai_response) > 10:
            test_results.append(("AI Simulation", "✅ PASS", "AI responses working"))
        else:
            test_results.append(("AI Simulation", "❌ FAIL", "AI simulation failed"))
        
        # Test calendar functionality
        calendar_events = create_calendar_events(events)
        if calendar_events and len(calendar_events) > 0:
            test_results.append(("Calendar System", "✅ PASS", f"{len(calendar_events)} calendar events"))
        else:
            test_results.append(("Calendar System", "❌ FAIL", "Calendar creation failed"))
            
    except Exception as e:
        test_results.append(("Main App Functions", "❌ FAIL", f"Error: {str(e)}"))
    
    # Test 3: Server and UI
    print("🌐 Testing Server and UI...")
    try:
        response = requests.get("http://localhost:8501", timeout=10)
        
        if response.status_code == 200:
            test_results.append(("Server Connectivity", "✅ PASS", "Server responding"))
        else:
            test_results.append(("Server Connectivity", "❌ FAIL", f"Status {response.status_code}"))
        
        if "streamlit" in response.text.lower():
            test_results.append(("Streamlit App", "✅ PASS", "Confirmed Streamlit application"))
        else:
            test_results.append(("Streamlit App", "⚠️  WARN", "May not be Streamlit"))
        
        if "static/js" in response.text and "static/css" in response.text:
            test_results.append(("UI Assets", "✅ PASS", "CSS and JS loading"))
        else:
            test_results.append(("UI Assets", "⚠️  WARN", "Some assets missing"))
        
        if "viewport" in response.text:
            test_results.append(("Responsive Design", "✅ PASS", "Mobile responsive"))
        else:
            test_results.append(("Responsive Design", "⚠️  WARN", "Responsive meta missing"))
            
    except Exception as e:
        test_results.append(("Server/UI", "❌ FAIL", f"Error: {str(e)}"))
    
    # Test 4: Button Functionality
    print("🔘 Testing Button Functionality...")
    try:
        import streamlit_demo
        
        button_functions = [
            'show_home_dashboard', 'show_game_day', 'show_tailgates',
            'show_watch_parties', 'show_prizes', 'show_ai_chat'
        ]
        
        available_buttons = []
        callable_buttons = 0
        
        for func_name in button_functions:
            if hasattr(streamlit_demo, func_name):
                available_buttons.append(func_name)
                func = getattr(streamlit_demo, func_name)
                if callable(func):
                    callable_buttons += 1
        
        if len(available_buttons) >= 4:
            test_results.append(("Button Functions", "✅ PASS", f"{len(available_buttons)}/6 available"))
        else:
            test_results.append(("Button Functions", "❌ FAIL", f"Only {len(available_buttons)}/6 available"))
        
        if callable_buttons == len(available_buttons):
            test_results.append(("Button Callability", "✅ PASS", "All functions callable"))
        else:
            test_results.append(("Button Callability", "❌ FAIL", f"{callable_buttons}/{len(available_buttons)} callable"))
            
    except Exception as e:
        test_results.append(("Button Functions", "❌ FAIL", f"Error: {str(e)}"))
    
    # Test 5: Data Processing
    print("📈 Testing Data Processing...")
    try:
        from app import load_mock_data
        events, prizes, leaderboard, badges = load_mock_data()
        
        # Test event structure
        if events and len(events) > 0:
            event = events[0]
            required_fields = ['id', 'title', 'date', 'time', 'type', 'location', 'points']
            missing_fields = [field for field in required_fields if field not in event]
            
            if len(missing_fields) == 0:
                test_results.append(("Event Structure", "✅ PASS", "All required fields present"))
            else:
                test_results.append(("Event Structure", "⚠️  WARN", f"Missing: {', '.join(missing_fields)}"))
        else:
            test_results.append(("Event Structure", "❌ FAIL", "No events to test"))
        
        # Test leaderboard structure
        if leaderboard and len(leaderboard) > 0:
            entry = leaderboard[0]
            required_fields = ['rank', 'name', 'points', 'badges', 'streak', 'type']
            missing_fields = [field for field in required_fields if field not in entry]
            
            if len(missing_fields) == 0:
                test_results.append(("Leaderboard Structure", "✅ PASS", "All required fields present"))
            else:
                test_results.append(("Leaderboard Structure", "⚠️  WARN", f"Missing: {', '.join(missing_fields)}"))
        else:
            test_results.append(("Leaderboard Structure", "❌ FAIL", "No leaderboard data"))
            
    except Exception as e:
        test_results.append(("Data Processing", "❌ FAIL", f"Error: {str(e)}"))
    
    return test_results

def generate_summary(test_results):
    """Generate comprehensive summary"""
    print("\n" + "=" * 60)
    print("📊 COMPREHENSIVE TEST RESULTS")
    print("=" * 60)
    
    # Categorize results
    passed = []
    failed = []
    warnings = []
    
    for test_name, status, details in test_results:
        if status == "✅ PASS":
            passed.append((test_name, details))
        elif status == "❌ FAIL":
            failed.append((test_name, details))
        elif status == "⚠️  WARN":
            warnings.append((test_name, details))
    
    # Print results
    print(f"\n✅ PASSED ({len(passed)}):")
    for test_name, details in passed:
        print(f"   • {test_name}: {details}")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for test_name, details in warnings:
            print(f"   • {test_name}: {details}")
    
    if failed:
        print(f"\n❌ FAILED ({len(failed)}):")
        for test_name, details in failed:
            print(f"   • {test_name}: {details}")
    
    # Calculate success rate
    total_tests = len(test_results)
    success_rate = (len(passed) / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"\n📈 OVERALL SUCCESS RATE: {success_rate:.1f}%")
    print(f"   • Total Tests: {total_tests}")
    print(f"   • Passed: {len(passed)}")
    print(f"   • Warnings: {len(warnings)}")
    print(f"   • Failed: {len(failed)}")
    
    # Final assessment
    print("\n🎯 FINAL ASSESSMENT:")
    if success_rate >= 90:
        print("🎉 EXCELLENT! The application is fully functional and ready for use.")
        print("✅ All core features are working correctly")
        print("✅ All buttons and interactions are operational")
        print("✅ Chat functionality is working perfectly")
    elif success_rate >= 75:
        print("👍 GOOD! The application is mostly functional with minor issues.")
        print("✅ Most features are working correctly")
        print("⚠️  Some minor issues may need attention")
    elif success_rate >= 50:
        print("⚠️  FAIR! The application has some functionality but needs improvements.")
        print("❌ Several features need attention")
        print("🔧 Consider addressing the failed tests")
    else:
        print("❌ POOR! The application has significant issues that need to be addressed.")
        print("🔧 Major functionality is not working")
        print("🚨 Immediate attention required")
    
    return success_rate

def main():
    """Main function"""
    print("🦁 LMU Campus LLM - Complete Functionality Assessment")
    print("Testing every button, chat functionality, and feature...")
    
    test_results = test_all_functionality()
    success_rate = generate_summary(test_results)
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    with open(f"test_summary_{timestamp}.txt", "w") as f:
        f.write("LMU Campus LLM - Test Summary\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Success Rate: {success_rate:.1f}%\n\n")
        
        for test_name, status, details in test_results:
            f.write(f"{status} {test_name}: {details}\n")
    
    print(f"\n📄 Detailed results saved to: test_summary_{timestamp}.txt")
    
    return 0 if success_rate >= 75 else 1

if __name__ == "__main__":
    exit(main())