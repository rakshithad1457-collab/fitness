from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.services.workout_service import get_mood_workout

router = APIRouter(tags=["workout"])


class WorkoutRequest(BaseModel):
    mood: str
    available_time: int


class CaloriesBurned(BaseModel):
    per_exercise_total: int
    estimated_range: str
    note: str


class WorkoutResponse(BaseModel):
    mood: str
    title: str
    description: str
    duration_minutes: int
    exercises: list[dict]
    calories_burned: Optional[CaloriesBurned] = None
    youtube_url: str
    youtube_query: str


# POST /api/workouts/mood-based
@router.post("/mood-based", response_model=WorkoutResponse)
async def generate_workout(request: WorkoutRequest):
    mood = request.mood.lower().strip()
    available_time = request.available_time

    if available_time < 5:
        raise HTTPException(status_code=400, detail="Available time must be at least 5 minutes.")

    valid_moods = ["happy", "stressed", "tired", "energetic", "anxious", "sad", "neutral", "motivated"]
    if mood not in valid_moods:
        raise HTTPException(
            status_code=400,
            detail=f"Mood '{mood}' is not supported. Choose from: {', '.join(valid_moods)}"
        )

    workout = get_mood_workout(mood, available_time)
    return workout


# GET /api/workouts/moods
@router.get("/moods")
async def list_supported_moods():
    return {
        "moods": [
            {"value": "happy",     "label": "Happy 😊",       "description": "Upbeat cardio & dance workouts"},
            {"value": "stressed",  "label": "Stressed 😤",    "description": "Yoga & breathing exercises"},
            {"value": "tired",     "label": "Tired 😴",       "description": "Gentle stretching & low-impact"},
            {"value": "energetic", "label": "Energetic ⚡",   "description": "HIIT & power training"},
            {"value": "anxious",   "label": "Anxious 😰",     "description": "Mindful movement & meditation"},
            {"value": "sad",       "label": "Sad 😢",         "description": "Feel-good endorphin boosters"},
            {"value": "neutral",   "label": "Neutral 😐",     "description": "Balanced full-body workout"},
            {"value": "motivated", "label": "Motivated 💪",   "description": "Strength & performance training"},
        ]
    }