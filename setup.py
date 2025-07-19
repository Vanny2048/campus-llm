#!/usr/bin/env python3
"""
LMU Campus LLM - Setup Script
Helps with installation and setup of the campus assistant
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_ollama():
    """Install Ollama if not already installed"""
    print("🔍 Checking if Ollama is installed...")
    
    # Check if ollama command exists
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Ollama is already installed: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("📦 Ollama not found. Installing...")
    
    system = platform.system().lower()
    
    if system == "darwin":  # macOS
        return run_command(
            "curl -fsSL https://ollama.ai/install.sh | sh",
            "Installing Ollama on macOS"
        )
    elif system == "linux":
        return run_command(
            "curl -fsSL https://ollama.ai/install.sh | sh",
            "Installing Ollama on Linux"
        )
    elif system == "windows":
        print("❌ Windows installation not supported in this script")
        print("Please install Ollama manually from: https://ollama.ai/download")
        return False
    else:
        print(f"❌ Unsupported operating system: {system}")
        return False

def download_llama_model():
    """Download the LLaMA 3.2 3B model"""
    print("🔍 Checking if LLaMA 3.2 3B model is available...")
    
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if "llama3.2:3b" in result.stdout:
            print("✅ LLaMA 3.2 3B model is already downloaded")
            return True
    except Exception as e:
        print(f"❌ Error checking models: {e}")
        return False
    
    print("📥 Downloading LLaMA 3.2 3B model...")
    return run_command(
        "ollama pull llama3.2:3b",
        "Downloading LLaMA 3.2 3B model"
    )

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    
    # Check if requirements.txt exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        return False
    
    return run_command(
        f"{sys.executable} -m pip install -r requirements.txt",
        "Installing Python dependencies"
    )

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = ["data", "src", "ui", "tests"]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def test_installation():
    """Test the installation"""
    print("🧪 Testing installation...")
    
    # Test Python imports
    try:
        import requests
        import gradio
        import numpy
        import sentence_transformers
        print("✅ Python dependencies imported successfully")
    except ImportError as e:
        print(f"❌ Python dependency import failed: {e}")
        return False
    
    # Test Ollama connection
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama connection successful")
        else:
            print("❌ Ollama connection failed")
            return False
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        return False
    
    return True

def create_config_file():
    """Create a configuration file"""
    config = {
        "ollama_url": "http://localhost:11434",
        "model": "llama3.2:3b",
        "data_dir": "data",
        "web_port": 7860,
        "max_tokens": 500,
        "temperature": 0.7
    }
    
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    print("✅ Created config.json")
    return True

def main():
    """Main setup function"""
    print("🦁 LMU Campus LLM Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Create directories
    if not create_directories():
        return False
    
    # Install Ollama
    if not install_ollama():
        print("⚠️ Ollama installation failed. You may need to install it manually.")
        print("Visit: https://ollama.ai/download")
    
    # Download model
    if not download_llama_model():
        print("⚠️ Model download failed. You can try again later with: ollama pull llama3.2:3b")
    
    # Install Python dependencies
    if not install_python_dependencies():
        print("❌ Python dependencies installation failed")
        return False
    
    # Create config file
    create_config_file()
    
    # Test installation
    if not test_installation():
        print("⚠️ Installation test failed. Some components may not work properly.")
    
    print("\n🎉 Setup completed!")
    print("\n🚀 Next steps:")
    print("1. Start Ollama: ollama serve")
    print("2. Run the assistant: python app.py --interactive")
    print("3. Or start the web interface: python ui/gradio_app.py")
    print("\n📚 For more information, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)