from google.adk.agents import Agent 
import os
import sys
from my_agent_code import agent_logic

print(f"Current working directory: {os.getcwd()}")
print(f"Python sys.path: {sys.path}")
print("-" * 30)

if hasattr(agent_logic, 'agent'):
    print(f"SUCCESS: Found 'agent' attribute in 'agent_logic' module. Agent name: {agent_logic.agent.name}")
else:
    print("ERROR: 'agent_logic' module was imported, but it does NOT have an 'agent' attribute defined at its top level.")

class TestAgent(Agent): 
    def __init__(self):
        super().__init__(
            name="TestAgentInRoot",
            description="A very simple test agent in the project root."
        )

    async def run_async(self, message=None, **kwargs): 
        yield self.event_type.TEXT_RESPONSE(text="TestAgentInRoot loaded and responding!")
        yield self.event_type.FINAL_RESPONSE()

agent = TestAgent()