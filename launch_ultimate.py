#!/usr/bin/env python3
"""
Launch Script for LMU Campus LLM Ultimate 3D
Quick setup and launch for the ultimate school spirit platform
"""

import os
import sys
import subprocess
import time

def print_banner():
    """Print the ultimate LMU banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║  🦁 LMU Campus LLM Ultimate 3D 🦁                           ║
    ║                                                              ║
    ║  Your Ultimate School Spirit Platform                       ║
    ║  Making School Spirit Iconic Since 2024                     ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'gradio',
        'pillow', 
        'qrcode',
        'requests',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("✅ All dependencies installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run:")
            print(f"pip install -r ultimate_requirements.txt")
            return False
    
    return True

def launch_app():
    """Launch the ultimate LMU app"""
    print("\n🚀 Launching LMU Campus LLM Ultimate 3D...")
    print("✨ Features:")
    print("   • Ultimate 3D Design with Glassmorphism Effects")
    print("   • Gen Z Chatbot with Authentic LMU Knowledge")
    print("   • Interactive Event Calendar with High-Quality Images")
    print("   • Live Game Day Engagement with QR Code Check-ins")
    print("   • Dynamic Leaderboard with Real-time Updates")
    print("   • Premium Prize Showcase with Exclusive Experiences")
    print("   • User Profile & Progress Tracking")
    print("   • Community Feedback & Event Suggestions")
    print("   • Smart Notifications & Streak System")
    
    try:
        # Import and run the app
        from lmu_ultimate_3d import UltimateLMUApp, main
        
        print("\n🎯 Starting the ultimate experience...")
        time.sleep(2)
        
        main()
        
    except ImportError as e:
        print(f"❌ Error importing app: {e}")
        print("Make sure lmu_ultimate_3d.py is in the current directory")
        return False
    except Exception as e:
        print(f"❌ Error launching app: {e}")
        return False
    
    return True

def main():
    """Main launch function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Setup failed. Please install dependencies manually.")
        return
    
    # Launch the app
    if launch_app():
        print("\n🎉 LMU Campus LLM Ultimate 3D launched successfully!")
        print("🌐 Open your browser and navigate to the provided URL")
        print("🦁 Enjoy the ultimate school spirit experience!")
    else:
        print("\n❌ Failed to launch the app. Please check the error messages above.")

if __name__ == "__main__":
    main()