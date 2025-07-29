#!/usr/bin/env python3
"""
Test script for LMU Campus LLM leaderboard and points system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.points_system import PointsSystem
from app import CampusLLMApp

def test_points_system():
    """Test the points system functionality"""
    print("🧪 Testing Points System...")
    
    # Initialize points system
    points_system = PointsSystem()
    
    # Test adding points
    print("📝 Adding test points...")
    points_system.add_points("12345", 10, "test", "Testing points")
    points_system.add_points("67890", 15, "test", "Testing points")
    points_system.add_points("11111", 20, "test", "Testing points")
    
    # Test getting leaderboard
    print("🏆 Getting leaderboard...")
    leaderboard = points_system.get_leaderboard(10)
    print(f"Found {len(leaderboard)} users in leaderboard")
    
    for entry in leaderboard:
        print(f"Rank {entry['rank']}: {entry['user_id']} - {entry['total_points']} pts ({entry['level']})")
    
    # Test user stats
    print("\n👤 Testing user stats...")
    stats = points_system.get_user_stats("12345")
    print(f"User 12345 stats: {stats}")
    
    # Test user rank
    rank_info = points_system.get_user_rank("12345")
    print(f"User 12345 rank: {rank_info}")

def test_app_leaderboard():
    """Test the app's leaderboard HTML generation"""
    print("\n🌐 Testing App Leaderboard HTML...")
    
    app = CampusLLMApp()
    
    # Test leaderboard HTML
    leaderboard_html = app.get_leaderboard_html(5)
    print("Leaderboard HTML generated successfully!")
    print(f"HTML length: {len(leaderboard_html)} characters")
    
    # Test prizes HTML
    prizes_html = app.get_prizes_html()
    print("Prizes HTML generated successfully!")
    print(f"Prizes HTML length: {len(prizes_html)} characters")
    
    # Test user points HTML
    points_html = app.get_user_points("12345")
    print("User points HTML generated successfully!")
    print(f"Points HTML length: {len(points_html)} characters")

if __name__ == "__main__":
    print("🚀 Starting LMU Campus LLM Tests...")
    print("=" * 50)
    
    try:
        test_points_system()
        test_app_leaderboard()
        print("\n✅ All tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()