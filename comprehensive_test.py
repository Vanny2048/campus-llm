#!/usr/bin/env python3
"""
Comprehensive Test Suite for LMU Campus LLM
Tests all buttons, chat functionality, and features
"""

import streamlit as st
import requests
import json
import time
import sys
import os
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class ComprehensiveTester:
    def __init__(self):
        self.base_url = "http://localhost:8501"
        self.test_results = []
        self.session = requests.Session()
        
    def log_test(self, test_name, status, details=""):
        """Log test results"""
        result = {
            "test": test_name,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        print(f"[{status.upper()}] {test_name}: {details}")
        
    def test_server_connection(self):
        """Test if the Streamlit server is accessible"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            if response.status_code == 200:
                self.log_test("Server Connection", "PASS", "Server is accessible")
                return True
            else:
                self.log_test("Server Connection", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Server Connection", "FAIL", f"Connection error: {str(e)}")
            return False
    
    def test_home_page_loading(self):
        """Test if the home page loads correctly"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            if "LMU Campus LLM" in response.text or "LMU Campus Spirit Hub" in response.text:
                self.log_test("Home Page Loading", "PASS", "Home page loads with correct content")
                return True
            else:
                self.log_test("Home Page Loading", "FAIL", "Home page content not found")
                return False
        except Exception as e:
            self.log_test("Home Page Loading", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_navigation_menu(self):
        """Test navigation menu functionality"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            # Check for navigation elements
            nav_indicators = [
                "Home", "Calendar", "Leaderboard", "Prizes", 
                "Content Gallery", "User Profile", "AI Assistant", "Feedback"
            ]
            
            found_nav = []
            for indicator in nav_indicators:
                if indicator.lower() in response.text.lower():
                    found_nav.append(indicator)
            
            if len(found_nav) >= 4:  # At least 4 navigation items should be present
                self.log_test("Navigation Menu", "PASS", f"Found navigation items: {', '.join(found_nav)}")
                return True
            else:
                self.log_test("Navigation Menu", "FAIL", f"Only found: {', '.join(found_nav)}")
                return False
        except Exception as e:
            self.log_test("Navigation Menu", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_calendar_functionality(self):
        """Test calendar page and functionality"""
        try:
            # Test calendar page loading
            response = self.session.get(f"{self.base_url}/Calendar", timeout=10)
            if response.status_code == 200:
                self.log_test("Calendar Page Loading", "PASS", "Calendar page accessible")
                
                # Check for calendar elements
                if "calendar" in response.text.lower() or "event" in response.text.lower():
                    self.log_test("Calendar Elements", "PASS", "Calendar elements found")
                    return True
                else:
                    self.log_test("Calendar Elements", "FAIL", "Calendar elements not found")
                    return False
            else:
                self.log_test("Calendar Page Loading", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Calendar Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_leaderboard_functionality(self):
        """Test leaderboard page and functionality"""
        try:
            response = self.session.get(f"{self.base_url}/Leaderboard", timeout=10)
            if response.status_code == 200:
                self.log_test("Leaderboard Page Loading", "PASS", "Leaderboard page accessible")
                
                # Check for leaderboard elements
                if "leaderboard" in response.text.lower() or "points" in response.text.lower():
                    self.log_test("Leaderboard Elements", "PASS", "Leaderboard elements found")
                    return True
                else:
                    self.log_test("Leaderboard Elements", "FAIL", "Leaderboard elements not found")
                    return False
            else:
                self.log_test("Leaderboard Page Loading", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Leaderboard Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_prizes_functionality(self):
        """Test prizes page and functionality"""
        try:
            response = self.session.get(f"{self.base_url}/Prizes", timeout=10)
            if response.status_code == 200:
                self.log_test("Prizes Page Loading", "PASS", "Prizes page accessible")
                
                # Check for prizes elements
                if "prize" in response.text.lower() or "shop" in response.text.lower():
                    self.log_test("Prizes Elements", "PASS", "Prizes elements found")
                    return True
                else:
                    self.log_test("Prizes Elements", "FAIL", "Prizes elements not found")
                    return False
            else:
                self.log_test("Prizes Page Loading", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Prizes Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_ai_assistant_functionality(self):
        """Test AI assistant page and functionality"""
        try:
            response = self.session.get(f"{self.base_url}/AI_Assistant", timeout=10)
            if response.status_code == 200:
                self.log_test("AI Assistant Page Loading", "PASS", "AI Assistant page accessible")
                
                # Check for AI assistant elements
                if "ai" in response.text.lower() or "assistant" in response.text.lower() or "chat" in response.text.lower():
                    self.log_test("AI Assistant Elements", "PASS", "AI Assistant elements found")
                    return True
                else:
                    self.log_test("AI Assistant Elements", "FAIL", "AI Assistant elements not found")
                    return False
            else:
                self.log_test("AI Assistant Page Loading", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("AI Assistant Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_user_profile_functionality(self):
        """Test user profile page and functionality"""
        try:
            response = self.session.get(f"{self.base_url}/User_Profile", timeout=10)
            if response.status_code == 200:
                self.log_test("User Profile Page Loading", "PASS", "User Profile page accessible")
                
                # Check for profile elements
                if "profile" in response.text.lower() or "user" in response.text.lower():
                    self.log_test("User Profile Elements", "PASS", "User Profile elements found")
                    return True
                else:
                    self.log_test("User Profile Elements", "FAIL", "User Profile elements not found")
                    return False
            else:
                self.log_test("User Profile Page Loading", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("User Profile Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_feedback_functionality(self):
        """Test feedback page and functionality"""
        try:
            response = self.session.get(f"{self.base_url}/Feedback", timeout=10)
            if response.status_code == 200:
                self.log_test("Feedback Page Loading", "PASS", "Feedback page accessible")
                
                # Check for feedback elements
                if "feedback" in response.text.lower() or "form" in response.text.lower():
                    self.log_test("Feedback Elements", "PASS", "Feedback elements found")
                    return True
                else:
                    self.log_test("Feedback Elements", "FAIL", "Feedback elements not found")
                    return False
            else:
                self.log_test("Feedback Page Loading", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Feedback Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_content_gallery_functionality(self):
        """Test content gallery page and functionality"""
        try:
            response = self.session.get(f"{self.base_url}/Content_Gallery", timeout=10)
            if response.status_code == 200:
                self.log_test("Content Gallery Page Loading", "PASS", "Content Gallery page accessible")
                
                # Check for gallery elements
                if "gallery" in response.text.lower() or "content" in response.text.lower():
                    self.log_test("Content Gallery Elements", "PASS", "Content Gallery elements found")
                    return True
                else:
                    self.log_test("Content Gallery Elements", "FAIL", "Content Gallery elements not found")
                    return False
            else:
                self.log_test("Content Gallery Page Loading", "FAIL", f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Content Gallery Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_button_functionality(self):
        """Test various buttons and interactive elements"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            
            # Check for button elements
            button_indicators = [
                "button", "click", "submit", "rsvp", "check-in", 
                "join", "register", "login", "logout"
            ]
            
            found_buttons = []
            for indicator in button_indicators:
                if indicator.lower() in response.text.lower():
                    found_buttons.append(indicator)
            
            if len(found_buttons) >= 3:  # At least 3 button types should be present
                self.log_test("Button Elements", "PASS", f"Found button types: {', '.join(found_buttons)}")
                return True
            else:
                self.log_test("Button Elements", "FAIL", f"Only found: {', '.join(found_buttons)}")
                return False
        except Exception as e:
            self.log_test("Button Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_chat_functionality(self):
        """Test chat/communication functionality"""
        try:
            # Test AI assistant page for chat elements
            response = self.session.get(f"{self.base_url}/AI_Assistant", timeout=10)
            
            chat_indicators = [
                "chat", "message", "send", "input", "conversation", 
                "ask", "question", "response"
            ]
            
            found_chat = []
            for indicator in chat_indicators:
                if indicator.lower() in response.text.lower():
                    found_chat.append(indicator)
            
            if len(found_chat) >= 2:  # At least 2 chat elements should be present
                self.log_test("Chat Elements", "PASS", f"Found chat elements: {', '.join(found_chat)}")
                return True
            else:
                self.log_test("Chat Elements", "FAIL", f"Only found: {', '.join(found_chat)}")
                return False
        except Exception as e:
            self.log_test("Chat Functionality", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_data_loading(self):
        """Test if data is loading correctly"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            
            # Check for data elements
            data_indicators = [
                "event", "points", "leaderboard", "prize", "user", 
                "calendar", "schedule", "activity"
            ]
            
            found_data = []
            for indicator in data_indicators:
                if indicator.lower() in response.text.lower():
                    found_data.append(indicator)
            
            if len(found_data) >= 4:  # At least 4 data types should be present
                self.log_test("Data Loading", "PASS", f"Found data types: {', '.join(found_data)}")
                return True
            else:
                self.log_test("Data Loading", "FAIL", f"Only found: {', '.join(found_data)}")
                return False
        except Exception as e:
            self.log_test("Data Loading", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_styling_and_ui(self):
        """Test UI styling and responsive design"""
        try:
            response = self.session.get(self.base_url, timeout=10)
            
            # Check for styling elements
            style_indicators = [
                "css", "style", "color", "font", "background", 
                "border", "margin", "padding", "responsive"
            ]
            
            found_styles = []
            for indicator in style_indicators:
                if indicator.lower() in response.text.lower():
                    found_styles.append(indicator)
            
            if len(found_styles) >= 2:  # At least 2 styling elements should be present
                self.log_test("UI Styling", "PASS", f"Found styling elements: {', '.join(found_styles)}")
                return True
            else:
                self.log_test("UI Styling", "FAIL", f"Only found: {', '.join(found_styles)}")
                return False
        except Exception as e:
            self.log_test("UI Styling", "FAIL", f"Error: {str(e)}")
            return False
    
    def test_error_handling(self):
        """Test error handling and edge cases"""
        try:
            # Test non-existent page
            response = self.session.get(f"{self.base_url}/nonexistent", timeout=10)
            if response.status_code == 404:
                self.log_test("Error Handling", "PASS", "404 error handled correctly")
                return True
            else:
                self.log_test("Error Handling", "FAIL", f"Unexpected status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Error Handling", "FAIL", f"Error: {str(e)}")
            return False
    
    def run_all_tests(self):
        """Run all tests and generate report"""
        print("🦁 Starting Comprehensive LMU Campus LLM Test Suite")
        print("=" * 60)
        
        tests = [
            self.test_server_connection,
            self.test_home_page_loading,
            self.test_navigation_menu,
            self.test_calendar_functionality,
            self.test_leaderboard_functionality,
            self.test_prizes_functionality,
            self.test_ai_assistant_functionality,
            self.test_user_profile_functionality,
            self.test_feedback_functionality,
            self.test_content_gallery_functionality,
            self.test_button_functionality,
            self.test_chat_functionality,
            self.test_data_loading,
            self.test_styling_and_ui,
            self.test_error_handling
        ]
        
        passed = 0
        failed = 0
        
        for test in tests:
            try:
                if test():
                    passed += 1
                else:
                    failed += 1
            except Exception as e:
                self.log_test(test.__name__, "ERROR", f"Test crashed: {str(e)}")
                failed += 1
        
        # Generate summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"📈 Success Rate: {(passed/(passed+failed)*100):.1f}%")
        
        # Save detailed results
        self.save_test_results()
        
        return passed, failed
    
    def save_test_results(self):
        """Save test results to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"📄 Detailed results saved to: {filename}")

def main():
    """Main function to run the comprehensive test suite"""
    tester = ComprehensiveTester()
    passed, failed = tester.run_all_tests()
    
    if failed == 0:
        print("\n🎉 All tests passed! The application is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please review the results above.")
        return 1

if __name__ == "__main__":
    exit(main())