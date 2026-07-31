import os
import json
import re
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
        self.model = genai.GenerativeModel('gemini-flash-latest')

    async def get_llm_response(self, prompt: str) -> Dict[str, Any]:
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Robust JSON extraction
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            else:
                return {"error": "No JSON found in response", "raw_response": response_text}
                
        except json.JSONDecodeError as e:
            print(f"LLM response was not valid JSON: {e}")
            return {"error": "LLM response was not valid JSON", "details": str(e), "raw_response": response_text}
        except Exception as e:
            print(f"Error getting response from Gemini LLM: {e}")
            return {"error": "Error communicating with LLM", "details": str(e)}

