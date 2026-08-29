import os

import requests
from dotenv import load_dotenv
from openai import AsyncOpenAI
from agents import Agent, Runner, function_tool, OpenAIChatCompletionsModel

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Gemini exposes an OpenAI-compatible endpoint, so the existing openai-agents
# SDK can talk to it directly through a custom client instead of requiring a
# different agent framework or an extra provider-specific dependency.
GEMINI_MODEL_NAME = "gemini-3.6-flash"
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def _fetch_projection(player_display_name: str) -> str:
    """
    Calls this project's FastAPI backend for a player's projection instead of
    letting the LLM guess a number. Kept separate from the @function_tool
    wrapper below so it can be unit tested without going through the agent.
    """
    response = requests.get(f"{API_BASE_URL}/predictions/{player_display_name}")

    if response.status_code == 404:
        return f"No projection found for player: {player_display_name}"

    response.raise_for_status()
    data = response.json()
    return f"{data['player_display_name']} is projected for {data['projected_ppr']} full-PPR points next week."


@function_tool
def get_player_projection(player_display_name: str) -> str:
    """
    Look up a wide receiver's projected full-PPR fantasy points for next week.

    Parameters:
    player_display_name: The player's full display name, e.g. "CeeDee Lamb".
    """
    return _fetch_projection(player_display_name)


fantasy_analyst_agent = Agent(
    name="Fantasy Analyst",
    model=OpenAIChatCompletionsModel(model=GEMINI_MODEL_NAME, openai_client=gemini_client),
    instructions=(
        "You are a fantasy football analyst for full-PPR wide receiver scoring. "
        "Always use the get_player_projection tool to get a player's projection. "
        "Never invent or estimate a projection yourself."
    ),
    tools=[get_player_projection],
)


if __name__ == "__main__":
    result = Runner.run_sync(
        fantasy_analyst_agent,
        "How many points is CeeDee Lamb projected to score next week?",
    )
    print(result.final_output)
