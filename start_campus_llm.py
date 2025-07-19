#!/usr/bin/env python3
"""
LMU Campus LLM Startup Script
Handles setup and launches the application
"""

import os
import sys
import subprocess
import time
import platform
from pathlib import Path

def print_banner():
    """Print the LMU Campus LLM banner"""
    banner = """
🦁 ═══════════════════════════════════════════════════════════════ 🦁
                        LMU CAMPUS LLM
              Your AI Assistant for Everything LMU
                Built by Students, For Students
🦁 ═══════════════════════════════════════════════════════════════ 🦁
"""
    print(banner)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {sys.version}")
        return False
    
    print(f"✅ Python {sys.version.split()[0]} is compatible")
    return True

def check_ollama_installation():
    """Check if Ollama is installed"""
    print("🤖 Checking Ollama installation...")
    
    try:
        result = subprocess.run(["ollama", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Ollama not found")
    return False

def install_ollama():
    """Install Ollama"""
    print("📦 Installing Ollama...")
    
    system = platform.system().lower()
    
    if system == "linux":
        try:
            subprocess.run([
                "curl", "-fsSL", "https://ollama.ai/install.sh"
            ], check=True, text=True, capture_output=True)
            print("✅ Ollama installation script downloaded")
            
            # Run installation
            subprocess.run(["sh", "-c", "curl -fsSL https://ollama.ai/install.sh | sh"], 
                          check=True)
            print("✅ Ollama installed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install Ollama: {e}")
            return False
    
    elif system == "darwin":  # macOS
        print("💡 Please install Ollama manually:")
        print("   1. Visit https://ollama.ai")
        print("   2. Download the macOS installer")
        print("   3. Run the installer")
        return False
    
    elif system == "windows":
        print("💡 Please install Ollama manually:")
        print("   1. Visit https://ollama.ai")
        print("   2. Download the Windows installer")
        print("   3. Run the installer")
        return False
    
    else:
        print(f"❌ Unsupported system: {system}")
        return False

def check_ollama_service():
    """Check if Ollama service is running"""
    print("🔄 Checking Ollama service...")
    
    try:
        result = subprocess.run(["curl", "-s", "http://localhost:11434/api/tags"], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama service is running")
            return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        pass
    
    print("❌ Ollama service not running")
    return False

def start_ollama_service():
    """Start Ollama service"""
    print("🚀 Starting Ollama service...")
    
    try:
        # Start Ollama in the background
        subprocess.Popen(["ollama", "serve"], 
                        stdout=subprocess.DEVNULL, 
                        stderr=subprocess.DEVNULL)
        
        # Wait a bit for service to start
        time.sleep(3)
        
        # Check if it's running
        if check_ollama_service():
            return True
        else:
            print("❌ Failed to start Ollama service")
            return False
            
    except Exception as e:
        print(f"❌ Error starting Ollama: {e}")
        return False

def check_llama_model():
    """Check if LLaMA model is available"""
    print("🧠 Checking LLaMA 3.2 model...")
    
    try:
        result = subprocess.run(["ollama", "list"], 
                              capture_output=True, text=True)
        
        if "llama3.2:3b" in result.stdout or "llama3.2" in result.stdout:
            print("✅ LLaMA 3.2 model is available")
            return True
        else:
            print("❌ LLaMA 3.2 model not found")
            return False
            
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False

def download_llama_model():
    """Download LLaMA 3.2 model"""
    print("📥 Downloading LLaMA 3.2 3B model...")
    print("   This may take several minutes...")
    
    try:
        process = subprocess.Popen(
            ["ollama", "pull", "llama3.2:3b"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            universal_newlines=True
        )
        
        # Show progress
        for line in process.stdout:
            if "downloading" in line.lower() or "%" in line:
                print(f"   {line.strip()}")
        
        process.wait()
        
        if process.returncode == 0:
            print("✅ LLaMA 3.2 model downloaded successfully")
            return True
        else:
            print("❌ Failed to download LLaMA model")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--break-system-packages"
        ], check=True, capture_output=True)
        
        print("✅ Python dependencies installed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print("💡 Try running: pip install -r requirements.txt --break-system-packages")
        return False

def setup_knowledge_base():
    """Set up the knowledge base"""
    print("📚 Setting up knowledge base...")
    
    try:
        subprocess.run([
            sys.executable, "scripts/setup_knowledge_base.py"
        ], check=True)
        
        print("✅ Knowledge base setup completed")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Knowledge base setup failed: {e}")
        return False

def run_tests():
    """Run basic tests"""
    print("🧪 Running basic tests...")
    
    try:
        result = subprocess.run([
            sys.executable, "tests/test_basic_functionality.py", "--quick"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Basic tests passed")
            return True
        else:
            print("❌ Some tests failed")
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def launch_application():
    """Launch the Gradio application"""
    print("🚀 Launching LMU Campus LLM...")
    print("\n" + "="*50)
    print("🌐 The application will open in your browser")
    print("🔗 Default URL: http://localhost:7860")
    print("🛑 Press Ctrl+C to stop the application")
    print("="*50 + "\n")
    
    try:
        # Launch the app
        subprocess.run([sys.executable, "app.py"], check=True)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Application stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Error launching application: {e}")
        return False

def main():
    """Main setup and launch function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Step 2: Install Python dependencies
    if not install_python_dependencies():
        sys.exit(1)
    
    # Step 3: Check/install Ollama
    if not check_ollama_installation():
        print("\n💡 Installing Ollama...")
        if not install_ollama():
            print("\n📝 Manual Ollama installation required:")
            print("   1. Visit https://ollama.ai")
            print("   2. Download and install Ollama for your system")
            print("   3. Run this script again")
            sys.exit(1)
    
    # Step 4: Start Ollama service
    if not check_ollama_service():
        if not start_ollama_service():
            print("\n💡 Please start Ollama manually:")
            print("   Run: ollama serve")
            print("   Then run this script again")
            sys.exit(1)
    
    # Step 5: Check/download LLaMA model
    if not check_llama_model():
        if not download_llama_model():
            print("\n💡 Please download the model manually:")
            print("   Run: ollama pull llama3.2:3b")
            sys.exit(1)
    
    # Step 6: Setup knowledge base
    if not setup_knowledge_base():
        print("⚠️ Continuing without full knowledge base setup")
    
    # Step 7: Run tests
    if not run_tests():
        print("⚠️ Some tests failed, but continuing...")
    
    # Step 8: Launch application
    print("\n🎉 Setup completed! Launching application...")
    launch_application()

if __name__ == "__main__":
    main()