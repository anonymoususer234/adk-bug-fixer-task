import os
from google.adk.agents import LlmAgent

AGENT_MAIN_INSTRUCTION = """
You are an AI programming assistant. You will be provided with detailed task instructions,
including a bug description, file context, and a code snippet.
Your goal is to analyze this information and suggest a single-line code fix if possible,
following the output format specified in the detailed task instructions.
If a single-line fix is not appropriate or possible from the given information,
you should indicate that as per the task instructions.
Be precise and focus only on the requested output format.
"""

agent = LlmAgent(
    name="SimpleBugFixerAgent",
    model="gemini-1.5-flash-latest",
    description="An agent that analyzes a bug description and code snippet to suggest a single-line fix.",
    instruction=AGENT_MAIN_INSTRUCTION
)