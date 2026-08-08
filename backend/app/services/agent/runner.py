from agents import Runner
from app.services.agent.agent import create_todo_agent

class TodoRunner:
    async def run(self, user_id: str, prompt: str):
        # Create a fresh agent for each request with the authenticated user_id
        agent = create_todo_agent(user_id=user_id)
        
        # Connect to MCP servers before execution
        for server in agent.mcp_servers:
            await server.connect()

        # Execute the agent
        # The agent is the first argument to runner.run
        runner = Runner()
        result = await runner.run(agent, prompt, context={"user_id": user_id})
        return result

