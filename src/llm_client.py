"""
LMU Campus LLM - Ollama Client
Handles communication with the local LLaMA model via Ollama
"""

import requests
import json
from typing import Dict, List, Optional
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3.2:3b"):
        """
        Initialize Ollama client
        
        Args:
            base_url: Ollama API base URL
            model: Model name to use
        """
        self.base_url = base_url
        self.model = model
        self.api_url = f"{base_url}/api/generate"
        
    def check_model_availability(self) -> bool:
        """Check if the specified model is available"""
        try:
            response = requests.get(f"{self.base_url}/api/tags")
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(model["name"] == self.model for model in models)
            return False
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False
    
    def generate_response(self, prompt: str, context: str = "", max_tokens: int = 500) -> str:
        """
        Generate a response using the LLM
        
        Args:
            prompt: User's question
            context: Relevant context from RAG system
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated response
        """
        try:
            # Construct the full prompt with context
            if context:
                full_prompt = f"""You are LMU Campus Assistant, a helpful AI assistant for Loyola Marymount University students. 
Use the following context to answer the student's question accurately and helpfully:

Context: {context}

Student Question: {prompt}

Please provide a clear, accurate, and helpful response based on the context provided. If the context doesn't contain enough information to fully answer the question, acknowledge what you know and suggest where they can find more information.

Response:"""
            else:
                full_prompt = f"""You are LMU Campus Assistant, a helpful AI assistant for Loyola Marymount University students.

Student Question: {prompt}

Please provide a helpful response. If you don't have specific information about this topic, suggest where the student might find more information.

Response:"""
            
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "max_tokens": max_tokens
                }
            }
            
            response = requests.post(self.api_url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "I'm sorry, I couldn't generate a response at this time.")
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return "I'm sorry, I'm having trouble connecting to my knowledge base right now. Please try again later."
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            return "I'm sorry, the request timed out. Please try again."
        except requests.exceptions.ConnectionError:
            logger.error("Connection error - is Ollama running?")
            return "I'm sorry, I can't connect to my knowledge base. Please make sure Ollama is running and try again."
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return "I'm sorry, something went wrong. Please try again."
    
    def test_connection(self) -> Dict[str, any]:
        """Test the connection to Ollama and return status"""
        try:
            # Test basic connectivity
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_available = any(model["name"] == self.model for model in models)
                
                return {
                    "status": "connected",
                    "model_available": model_available,
                    "available_models": [model["name"] for model in models],
                    "selected_model": self.model
                }
            else:
                return {
                    "status": "error",
                    "error": f"HTTP {response.status_code}",
                    "selected_model": self.model
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "status": "disconnected",
                "error": "Cannot connect to Ollama. Is it running?",
                "selected_model": self.model
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "selected_model": self.model
            }

# Example usage and testing
if __name__ == "__main__":
    client = OllamaClient()
    
    # Test connection
    status = client.test_connection()
    print(f"Connection status: {status}")
    
    if status["status"] == "connected" and status["model_available"]:
        # Test response generation
        test_prompt = "What are the library hours?"
        response = client.generate_response(test_prompt)
        print(f"\nTest response: {response}")
    else:
        print("Model not available or connection failed")