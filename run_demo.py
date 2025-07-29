#!/usr/bin/env python3
"""
Quick demo runner for LMU Campus LLM
"""

import subprocess
import sys
import os

def main():
    print("🦁 Starting LMU Campus LLM Demo...")
    print("📱 Opening Streamlit app...")
    
    # Run streamlit
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_demo.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except KeyboardInterrupt:
        print("\n👋 Demo stopped by user")
    except Exception as e:
        print(f"❌ Error running demo: {e}")
        print("💡 Make sure you have streamlit installed: pip install streamlit")

if __name__ == "__main__":
    main()