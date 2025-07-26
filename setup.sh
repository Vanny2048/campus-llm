#!/bin/bash

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service in the background
ollama serve &

# Wait for Ollama to start (adjust sleep time if needed )
sleep 5

# Download LLaMA 3.2 3B model
ollama pull llama3.2:3b

# Initialize the knowledge base
python scripts/setup_knowledge_base.py

echo "Ollama and LLaMA setup complete."
