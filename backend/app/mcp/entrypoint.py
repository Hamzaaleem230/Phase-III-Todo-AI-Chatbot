import os
import sys
import logging
from mcp.server.fastmcp import FastMCP

# Disable logging to avoid interference with MCP communication
logging.disable(logging.CRITICAL)

# Set Groq API key for the MCP tool environment
if "GROQ_API_KEY" in os.environ:
    os.environ["OPENAI_API_KEY"] = os.environ["GROQ_API_KEY"]
    os.environ["OPENAI_BASE_URL"] = "https://api.groq.com/openai/v1"

# This script is meant to be run by the Agents SDK to start the MCP server.
# Ensure the root 'backend' directory is in the path to import 'app'.
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from app.mcp.tools import mcp

if __name__ == "__main__":
    mcp.run()
