#!/usr/bin/env python3
"""
Force refresh script to clear caching and restart the application
"""

import os
import subprocess
import time
import signal

def kill_existing_processes():
    """Kill any existing Python app processes"""
    try:
        # Kill any existing python app.py processes
        subprocess.run(["pkill", "-f", "python app.py"], check=False)
        time.sleep(2)
        print("✅ Killed existing processes")
    except Exception as e:
        print(f"⚠️  Error killing processes: {e}")

def clear_cache():
    """Clear any potential cache files"""
    cache_dirs = [
        "__pycache__",
        ".gradio",
        "gradio_cached_examples"
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                subprocess.run(["rm", "-rf", cache_dir], check=False)
                print(f"✅ Cleared {cache_dir}")
            except Exception as e:
                print(f"⚠️  Error clearing {cache_dir}: {e}")

def start_application():
    """Start the application with fresh environment"""
    try:
        # Activate virtual environment and start app
        cmd = "source venv/bin/activate && python app.py --reload"
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("🚀 Starting application...")
        time.sleep(5)
        
        # Check if it's running
        result = subprocess.run(["curl", "-s", "http://localhost:7860"], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Application is running successfully!")
            print("🌐 Access at: http://localhost:7860")
            print("💡 If you still see old content, try:")
            print("   - Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)")
            print("   - Clear browser cache")
            print("   - Open in incognito/private mode")
        else:
            print("❌ Application failed to start")
            
    except Exception as e:
        print(f"❌ Error starting application: {e}")

if __name__ == "__main__":
    print("🔄 Force refreshing LMU Campus LLM...")
    print("=" * 50)
    
    kill_existing_processes()
    clear_cache()
    start_application()