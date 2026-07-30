import os
import json
from typing import Dict, Any
from dotenv import load_dotenv

import google.generativeai as genai

from app.services.ai.base import AbstractLLMService

load_dotenv()

class GeminiLLMService(AbstractLLMService):
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables.")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    async def get_llm_response(self, prompt: str) -> Dict[str, Any]:
        try:
            # For simplicity, using generate_content directly.
            # In a real async FastAPI app, this might be offloaded to a thread pool
            # or use an async client if available.
            response = self.model.generate_content(prompt)
            
            # Assuming LLM is prompted to return JSON in a specific format
            # We need to extract text and parse it as JSON
            response_text = response.text.strip()
            
            # Attempt to parse as JSON
            json_response = json.loads(response_text)
            return json_response
        except ValueError as e:
            # Handle JSON decoding errors
            print(f"LLM response was not valid JSON: {e}")
            print(f"Raw LLM response: {response_text}")
            return {"error": "LLM response was not valid JSON", "details": str(e), "raw_response": response_text}
        except Exception as e:
            # Handle other potential errors during API call
            print(f"Error getting response from Gemini LLM: {e}")
            return {"error": "Error communicating with LLM", "details": str(e)}

