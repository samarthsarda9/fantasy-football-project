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


def _fetch_recent_stats(player_display_name: str) -> str:
    """
    Calls this project's FastAPI backend for a player's most recent game plus
    the rolling/season-to-date features the model uses, so the LLM can answer
    "how has usage changed recently" from real numbers instead of guessing.
    """
    response = requests.get(f"{API_BASE_URL}/players/{player_display_name}")

    if response.status_code == 404:
        return f"No stats found for player: {player_display_name}"

    response.raise_for_status()
    data = response.json()

    return (
        f"{data['player_display_name']}'s most recent game was season {data['season']}, "
        f"week {data['week']} vs {data['opponent_team']}: "
        f"{data['receptions']} receptions on {data['targets']} targets, "
        f"{data['receiving_yards']} receiving yards, {data['receiving_tds']} receiving TDs, "
        f"{data['calculated_ppr']} full-PPR points. "
        f"Recent form: {data['prev_rolling_3_ppr']} PPR average over the previous 3 games, "
        f"{data['prev_season_avg_ppr']} PPR average for the season before this game."
    )


@function_tool
def get_recent_stats(player_display_name: str) -> str:
    """
    Look up a wide receiver's most recent game stats and recent usage trend.

    Parameters:
    player_display_name: The player's full display name, e.g. "CeeDee Lamb".
    """
    return _fetch_recent_stats(player_display_name)


def _compare_players(player_a: str, player_b: str) -> str:
    """
    Fetches both players' projections from the FastAPI backend and decides who
    is projected higher. The comparison itself (which number is bigger) is a
    deterministic calculation, so it's done here in plain Python rather than
    leaving an LLM to eyeball two numbers and possibly get it wrong.
    """
    response_a = requests.get(f"{API_BASE_URL}/predictions/{player_a}")
    if response_a.status_code == 404:
        return f"No projection found for player: {player_a}"
    response_a.raise_for_status()
    data_a = response_a.json()

    response_b = requests.get(f"{API_BASE_URL}/predictions/{player_b}")
    if response_b.status_code == 404:
        return f"No projection found for player: {player_b}"
    response_b.raise_for_status()
    data_b = response_b.json()

    projection_a = data_a["projected_ppr"]
    projection_b = data_b["projected_ppr"]

    if projection_a == projection_b:
        return (
            f"{data_a['player_display_name']} and {data_b['player_display_name']} have the same "
            f"projection: {projection_a} full-PPR points each."
        )

    higher, lower = (data_a, data_b) if projection_a > projection_b else (data_b, data_a)
    return (
        f"{higher['player_display_name']} is projected higher ({higher['projected_ppr']} full-PPR points) "
        f"than {lower['player_display_name']} ({lower['projected_ppr']} full-PPR points)."
    )


@function_tool
def compare_players(player_a: str, player_b: str) -> str:
    """
    Compare two wide receivers' next-week full-PPR projections, e.g. to help
    decide who to start.

    Parameters:
    player_a: First player's full display name.
    player_b: Second player's full display name.
    """
    return _compare_players(player_a, player_b)


fantasy_analyst_agent = Agent(
    name="Fantasy Analyst",
    model=OpenAIChatCompletionsModel(model=GEMINI_MODEL_NAME, openai_client=gemini_client),
    instructions=(
        "You are a fantasy football analyst for full-PPR wide receiver scoring. "
        "Always use get_player_projection for projections, get_recent_stats for "
        "recent performance/usage questions, and compare_players for start/sit "
        "questions between two players. Never invent or estimate stats or "
        "projections yourself, and never decide a start/sit comparison yourself "
        "without calling compare_players."
    ),
    tools=[get_player_projection, get_recent_stats, compare_players],
)


if __name__ == "__main__":
    result = Runner.run_sync(
        fantasy_analyst_agent,
        "Should I start CeeDee Lamb or Puka Nacua this week?",
    )
    print(result.final_output)
