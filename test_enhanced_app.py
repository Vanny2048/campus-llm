#!/usr/bin/env python3
"""
Test script for Enhanced LMU Campus LLM 3D
Tests all major functionality without breaking existing code
"""

import sys
import traceback

def test_enhanced_app():
    """Test the enhanced LMU app functionality"""
    print("🧪 Testing Enhanced LMU Campus LLM 3D...")
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from enhanced_lmu_3d import EnhancedLMUApp
        print("✅ Imports successful")
        
        # Test app initialization
        print("🚀 Testing app initialization...")
        app = EnhancedLMUApp()
        print("✅ App initialized successfully")
        
        # Test data loading
        print("📊 Testing data loading...")
        assert len(app.game_events) > 0, "Game events not loaded"
        assert len(app.tailgates) > 0, "Tailgates not loaded"
        assert len(app.spirit_challenges) > 0, "Spirit challenges not loaded"
        assert len(app.premium_prizes) > 0, "Premium prizes not loaded"
        assert len(app.leaderboard_data) > 0, "Leaderboard data not loaded"
        print("✅ All data loaded successfully")
        
        # Test Gen Z personality
        print("💬 Testing Gen Z personality...")
        response = app.process_message("Hello", [])
        # Check for any Gen Z elements (emojis, slang, enthusiasm)
        genz_indicators = ["👋", "✨", "🔥", "💅", "bestie", "yasss", "slay", "periodt", "literally", "obsessed"]
        has_genz = any(indicator in response.lower() for indicator in genz_indicators)
        assert has_genz, f"Gen Z personality not working. Response: {response}"
        print("✅ Gen Z personality working")
        
        # Test specific responses
        print("🎯 Testing specific responses...")
        tutoring_response = app.process_message("Where can I find tutoring?", [])
        assert "academic resource center" in tutoring_response.lower() or "arc" in tutoring_response.lower() or "tutoring" in tutoring_response.lower(), "Tutoring response not working"
        print("✅ Specific responses working")
        
        # Test user points
        print("🏆 Testing user points...")
        points_html = app.get_user_points("test_user")
        assert "Spirit Points" in points_html, "User points not working"
        print("✅ User points working")
        
        # Test dashboard
        print("📊 Testing dashboard...")
        dashboard_html = app.get_game_day_dashboard()
        assert "Game Day Dashboard" in dashboard_html, "Dashboard not working"
        print("✅ Dashboard working")
        
        # Test calendar
        print("📅 Testing calendar...")
        calendar_html = app.get_enhanced_calendar()
        assert "Interactive Event Calendar" in calendar_html, "Calendar not working"
        print("✅ Calendar working")
        
        # Test leaderboard
        print("🏆 Testing leaderboard...")
        leaderboard_html = app.get_enhanced_leaderboard()
        assert "Live Leaderboard" in leaderboard_html, "Leaderboard not working"
        print("✅ Leaderboard working")
        
        # Test prizes
        print("🎁 Testing prizes...")
        prizes_html = app.get_enhanced_prizes()
        assert "Premium Prizes" in prizes_html, "Prizes not working"
        print("✅ Prizes working")
        
        # Test challenges
        print("🔥 Testing challenges...")
        challenges_html = app.get_enhanced_spirit_challenges()
        assert "Spirit Challenges" in challenges_html, "Challenges not working"
        print("✅ Challenges working")
        
        # Test QR code generation
        print("📱 Testing QR code generation...")
        qr_html = app.generate_qr_code("test_event", "game")
        assert "QR Code" in qr_html, "QR code generation not working"
        print("✅ QR code generation working")
        
        # Test CSS generation
        print("🎨 Testing CSS generation...")
        css = app.get_3d_css()
        assert "Orbitron" in css and "Rajdhani" in css, "CSS generation not working"
        print("✅ CSS generation working")
        
        print("\n🎉 All tests passed! Enhanced LMU Campus LLM 3D is working perfectly!")
        print("\n✨ Features tested:")
        print("   • 3D Design & Styling")
        print("   • Gen Z Chatbot Personality")
        print("   • Interactive Calendar")
        print("   • Live Leaderboard")
        print("   • Premium Prizes")
        print("   • Spirit Challenges")
        print("   • QR Code Generation")
        print("   • User Points System")
        print("   • Dashboard & Profile")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        print(f"🔍 Error details: {traceback.format_exc()}")
        return False

def test_existing_app():
    """Test that the original app still works"""
    print("\n🔍 Testing existing app compatibility...")
    
    try:
        # Test original app imports
        from app import CampusLLMApp
        print("✅ Original app imports successful")
        
        # Test original app initialization
        app = CampusLLMApp()
        print("✅ Original app initialized successfully")
        
        # Test original app functionality
        response = app.process_message("Hello", [])
        assert len(response) > 0, "Original app response not working"
        print("✅ Original app functionality working")
        
        return True
        
    except Exception as e:
        print(f"❌ Existing app test failed: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🦁 LMU Campus LLM 3D - Comprehensive Test Suite")
    print("=" * 50)
    
    # Test enhanced app
    enhanced_success = test_enhanced_app()
    
    # Test existing app compatibility
    existing_success = test_existing_app()
    
    print("\n" + "=" * 50)
    if enhanced_success and existing_success:
        print("🎉 All tests passed! Your enhanced app is ready to launch!")
        print("\n🚀 To run the enhanced app:")
        print("   python3 enhanced_lmu_3d.py")
        print("\n🚀 To run the original app:")
        print("   python3 app.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()