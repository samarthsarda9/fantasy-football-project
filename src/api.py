from contextlib import asynccontextmanager

import polars as pl
from agents import Runner
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent import fantasy_analyst_agent, summarize_tool_calls
from src.data import load_wr_weekly_stats
from src.scoring import calculate_ppr
from src.features import create_features, create_defensive_features
from src.modeling import load_model
from src.predict import get_latest_player_row, predict_player_projection

SEASONS = [2021, 2022, 2023, 2024, 2025]

model = None
features_df: pl.DataFrame | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Builds the same feature table used in notebooks/03_further_engineering.ipynb
    and loads the trained model once, at startup, instead of per-request.
    """
    global model, features_df

    raw_stats = load_wr_weekly_stats(SEASONS)
    scored_stats = calculate_ppr(raw_stats)
    stats_with_features = create_features(scored_stats)
    features_df = create_defensive_features(stats_with_features)

    model = load_model()

    yield


app = FastAPI(title="Fantasy Football AI Predictor", lifespan=lifespan)

# Allows the Next.js dev server (a different origin) to call this API directly
# from the browser. Local dev origins only; revisit before deploying either app.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/players")
def list_players() -> list[str]:
    """
    Returns the sorted list of WR display names from the most recent season in
    the dataset, for populating a player selector in the frontend.
    """
    latest_season = features_df.select(pl.col("season").max()).item()
    names = (
        features_df
        .filter(pl.col("season") == latest_season)
        .select("player_display_name")
        .unique()
        .sort("player_display_name")
        .to_series()
        .to_list()
    )
    return names


@app.get("/players/{player_display_name}")
def get_player_stats(player_display_name: str) -> dict:
    """
    Returns a player's most recent computed feature row (recent stats used for projection).
    """
    try:
        player_row = get_latest_player_row(features_df, player_display_name)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Player not found: {player_display_name}")

    return player_row.to_dicts()[0]


@app.get("/predictions/{player_display_name}")
def get_player_projection(player_display_name: str) -> dict:
    """
    Returns a player's projected next-week full-PPR points from the trained model.
    """
    try:
        player_row = get_latest_player_row(features_df, player_display_name)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Player not found: {player_display_name}")

    projection = predict_player_projection(model, player_row)
    return {
        "player_display_name": player_display_name,
        "projected_ppr": projection,
    }


class AgentQuestion(BaseModel):
    question: str


class AgentAnswer(BaseModel):
    answer: str
    trace: list[str]


@app.post("/agent/ask")
async def ask_agent(payload: AgentQuestion) -> AgentAnswer:
    """
    Runs the Fantasy Analyst Agent (src/agent.py) on a natural-language question
    and returns its answer plus a trace of which tools it called, so the frontend
    can show the answer is grounded in this project's real data rather than an
    invented number.
    """
    try:
        result = await Runner.run(fantasy_analyst_agent, payload.question)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Agent request failed: {exc}")

    return AgentAnswer(answer=result.final_output, trace=summarize_tool_calls(result))
