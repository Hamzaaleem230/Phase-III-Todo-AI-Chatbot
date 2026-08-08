from agents import Agent, OpenAIChatCompletionsModel
from agents.mcp.server import MCPServerStdio
import sys
import os
from app.core.config import settings
from openai import AsyncOpenAI
import agents

# Global configuration for Agents SDK
client = AsyncOpenAI(base_url="https://api.groq.com/openai/v1", api_key=settings.GROQ_API_KEY)
model = OpenAIChatCompletionsModel(model="llama-3.3-70b-versatile", openai_client=client)

def create_todo_agent(user_id: str):
    return Agent[dict](
        name="TodoAgent",
        model=model,
        instructions="You are a helpful assistant that manages todo tasks. Use the provided tools to perform CRUD operations on the user's tasks.",
        mcp_servers=[
            MCPServerStdio(
                params={
                    "command": sys.executable,
                    "args": [os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), "app", "mcp", "entrypoint.py")],
                    "env": {"USER_ID": user_id, "GROQ_API_KEY": settings.GROQ_API_KEY}
                }
            )
        ],
    )



