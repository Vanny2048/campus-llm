"""
LLM Handler for interfacing with Ollama and LLaMA 3.2
"""

import requests
import json
import time
from typing import List, Dict, Any, Optional
from .utils import logger, load_config, clean_text

class LLMHandler:
    def __init__(self):
        """Initialize the LLM handler"""
        self.config = load_config()
        self.ollama_url = "http://localhost:11434"
        self.model = self.config["llm"]["model"]
        self.temperature = self.config["llm"]["temperature"]
        self.max_tokens = self.config["llm"]["max_tokens"]
        self.timeout = self.config["llm"]["timeout"]
        
        # Updated system prompt with Gen-Z tone and LMU vibe
        self.system_prompt = """You are the LMU Campus AI Assistant, a helpful and friendly chatbot designed specifically for Loyola Marymount University students, faculty, and staff. Your mission is to provide accurate, helpful information about all aspects of campus life at LMU.

Key (Professional) Guidelines:
1. **LMU-Focused** – Keep responses specific to LMU. If asked about other schools, redirect back to LMU.
2. **FERPA Friendly** – Never request or discuss personal student information.
3. **Accuracy First** – If you aren’t sure, say so and suggest the correct LMU office / website.

Gen-Z Tone & Style Guidelines:
A. **Use college slang naturally** – words like *lowkey, bet, fr, vibes, nah for real* are welcome but don’t spam them.
B. **Mirror the student’s writing style & capitalization** – if they type in lowercase, you do too.
C. **Keep it concise** – shoot for 1-3 short sentences (≈ <60 words total). Cut the fluff.
D. **Sound like you’re on campus** – sprinkle LMU references (The Bluff, U-Hall, Lion Dollars, C-Store runs, Burns Backcourt, First Fridays, etc.) when relevant.
E. **Break the stiff “AI voice”** – it’s ok to say *idk tbh* or *lemme check* and use light humor or meme reactions (💀, 😭) in moderation.
F. **Emojis = seasoning** – 0-2 per reply, placed where a real student would.

You can help with:
• Academic policies and procedures
• Campus resources and services
• Event information and campus life vibes 😎
• Administrative processes (registrar, PROWL, etc.)
• Study abroad, tutoring, wellness, and more

Remember: you’re basically that chill friend who knows campus info — keep it real, helpful, and LMU-centric! 🦁"""

    def check_ollama_connection(self) -> bool:
        """Check if Ollama is running and accessible"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    def ensure_model_available(self) -> bool:
        """Ensure the LLaMA model is available"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [model["name"] for model in models]
                
                if self.model in available_models:
                    return True
                else:
                    logger.warning(f"Model {self.model} not found. Available models: {available_models}")
                    return False
            return False
        except Exception as e:
            logger.error(f"Error checking model availability: {e}")
            return False

    def generate_response(self, user_message: str, context: str = "", history: List[Dict] = None) -> str:
        """Generate a response using the LLM"""
        try:
            # Check Ollama connection
            if not self.check_ollama_connection():
                return "🚨 I'm having trouble connecting to my brain (Ollama). Please make sure Ollama is running with: `ollama serve`"
            
            # Check model availability
            if not self.ensure_model_available():
                return f"🚨 The {self.model} model isn't available. Please run: `ollama pull {self.model}`"
            
            # Clean the input
            user_message = clean_text(user_message)
            context = clean_text(context)
            
            # Build the prompt
            prompt = self._build_prompt(user_message, context, history)
            
            # Make the API call
            response = self._call_ollama_api(prompt)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Sorry, I encountered an error while processing your request: {str(e)}"

    def _build_prompt(self, user_message: str, context: str = "", history: List[Dict] = None) -> str:
        """Build the complete prompt for the LLM"""
        prompt_parts = [self.system_prompt]
        
        # Add context if provided
        if context:
            prompt_parts.append(f"\nRelevant LMU Information:\n{context}")
        
        # Add conversation history
        if history:
            prompt_parts.append("\nConversation History:")
            for turn in history[-3:]:  # Keep last 3 turns for context
                if isinstance(turn, list) and len(turn) == 2:
                    prompt_parts.append(f"Student: {turn[0]}")
                    prompt_parts.append(f"Assistant: {turn[1]}")
        
        # Add current question
        prompt_parts.append(f"\nCurrent Question: {user_message}")
        prompt_parts.append("\nResponse:")
        
        return "\n".join(prompt_parts)

    def _call_ollama_api(self, prompt: str) -> str:
        """Make the actual API call to Ollama"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "I'm sorry, I couldn't generate a response.")
            else:
                logger.error(f"Ollama API error: {response.status_code} - {response.text}")
                return f"API Error: {response.status_code}"
                
        except requests.exceptions.Timeout:
            return "I'm taking too long to respond. Please try asking your question again."
        except requests.exceptions.RequestException as e:
            logger.error(f"Request error: {e}")
            return "I'm having trouble connecting. Please check if Ollama is running."
        except Exception as e:
            logger.error(f"Unexpected error in API call: {e}")
            return f"An unexpected error occurred: {str(e)}"

    def generate_streaming_response(self, user_message: str, context: str = "", history: List[Dict] = None):
        """Generate a streaming response (for future use)"""
        try:
            if not self.check_ollama_connection():
                yield "🚨 I'm having trouble connecting to my brain (Ollama). Please make sure Ollama is running."
                return
            
            prompt = self._build_prompt(user_message, context, history)
            
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": self.temperature,
                    "num_predict": self.max_tokens,
                    "top_p": 0.9,
                    "top_k": 40
                }
            }
            
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                stream=True,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "response" in chunk:
                                yield chunk["response"]
                            if chunk.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
            else:
                yield f"API Error: {response.status_code}"
                
        except Exception as e:
            logger.error(f"Error in streaming response: {e}")
            yield f"Error: {str(e)}"

    def test_connection(self) -> Dict[str, Any]:
        """Test the connection and return status information"""
        status = {
            "ollama_running": False,
            "model_available": False,
            "response_test": False,
            "error_message": None
        }
        
        try:
            # Test Ollama connection
            status["ollama_running"] = self.check_ollama_connection()
            if not status["ollama_running"]:
                status["error_message"] = "Ollama is not running. Start it with: ollama serve"
                return status
            
            # Test model availability
            status["model_available"] = self.ensure_model_available()
            if not status["model_available"]:
                status["error_message"] = f"Model {self.model} not available. Install it with: ollama pull {self.model}"
                return status
            
            # Test response generation
            test_response = self.generate_response("Hello, can you help me?")
            if test_response and not test_response.startswith("🚨"):
                status["response_test"] = True
            else:
                status["error_message"] = f"Response test failed: {test_response}"
            
        except Exception as e:
            status["error_message"] = f"Connection test error: {str(e)}"
        
        return status

# Quick test function
def test_llm_handler():
    """Test the LLM handler functionality"""
    handler = LLMHandler()
    status = handler.test_connection()
    
    print("🧪 LLM Handler Test Results:")
    print(f"Ollama Running: {'✅' if status['ollama_running'] else '❌'}")
    print(f"Model Available: {'✅' if status['model_available'] else '❌'}")
    print(f"Response Test: {'✅' if status['response_test'] else '❌'}")
    
    if status['error_message']:
        print(f"Error: {status['error_message']}")
    
    if all([status['ollama_running'], status['model_available'], status['response_test']]):
        print("🎉 LLM Handler is working correctly!")
    else:
        print("⚠️ LLM Handler needs attention.")

if __name__ == "__main__":
    test_llm_handler()