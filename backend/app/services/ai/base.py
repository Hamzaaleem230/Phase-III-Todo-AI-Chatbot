from abc import ABC, abstractmethod
from typing import Dict, Any

class AbstractLLMService(ABC):
    @abstractmethod
    async def get_llm_response(self, prompt: str) -> Dict[str, Any]:
        """
        Abstract method to get a structured JSON response from an LLM.

        Args:
            prompt (str): The prompt to send to the LLM.

        Returns:
            Dict[str, Any]: A dictionary representing the structured JSON response from the LLM.
        """
        pass
