"""
app/api/workouts.py
--------------------
FastAPI router for mood + age-based workout generation.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from app.services.workout_service import get_mood_workout

router = APIRouter(tags=["workout"])

VALID_MOODS = ["happy", "stressed", "tired", "energetic", "anxious", "sad", "neutral", "motivated"]
VALID_AGE_CATEGORIES = ["teen", "young_adult", "adult", "senior"]


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class WorkoutRequest(BaseModel):
    mood: str
    available_time: int = Field(..., ge=5, description="Duration in minutes (min 5)")
    age_category: str = Field(default="young_adult", description="teen | young_adult | adult | senior")


class CaloriesBurned(BaseModel):
    per_exercise_total: int
    estimated_range: str
    note: str


class WorkoutResponse(BaseModel):
    mood: str
    age_category: str
    age_label: str
    title: str
    description: str
    duration_minutes: int
    rest_note: str
    exercises: list[dict]
    calories_burned: Optional[CaloriesBurned] = None
    youtube_url: str
    youtube_query: str


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.post("/mood-based", response_model=WorkoutResponse)
async def generate_workout(request: WorkoutRequest):
    mood         = request.mood.lower().strip()
    age_category = request.age_category.lower().strip()
    available_time = request.available_time

    if mood not in VALID_MOODS:
        raise HTTPException(
            status_code=400,
            detail=f"Mood '{mood}' is not supported. Choose from: {', '.join(VALID_MOODS)}"
        )

    if age_category not in VALID_AGE_CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Age category '{age_category}' is not supported. Choose from: {', '.join(VALID_AGE_CATEGORIES)}"
        )

    workout = get_mood_workout(mood, available_time, age_category)
    return workout


@router.get("/moods")
async def list_supported_moods():
    return {
        "moods": [
            {"value": "happy",     "label": "Happy 😊",    "description": "Upbeat cardio & dance workouts"},
            {"value": "stressed",  "label": "Stressed 😤", "description": "Yoga & breathing exercises"},
            {"value": "tired",     "label": "Tired 😴",    "description": "Gentle stretching & low-impact"},
            {"value": "energetic", "label": "Energetic ⚡", "description": "HIIT & power training"},
            {"value": "anxious",   "label": "Anxious 😰",  "description": "Mindful movement & meditation"},
            {"value": "sad",       "label": "Sad 😢",      "description": "Feel-good endorphin boosters"},
            {"value": "neutral",   "label": "Neutral 😐",  "description": "Balanced full-body workout"},
            {"value": "motivated", "label": "Motivated 💪","description": "Strength & performance training"},
        ]
    }


@router.get("/age-categories")
async def list_age_categories():
    return {
        "age_categories": [
            {
                "value": "teen",
                "label": "Teen (13–17)",
                "description": "Fun, energizing routines for developing bodies.",
                "calorie_note": "~10% higher burn rate"
            },
            {
                "value": "young_adult",
                "label": "Young Adult (18–35)",
                "description": "High-intensity sessions at peak metabolic rate.",
                "calorie_note": "Baseline burn rate"
            },
            {
                "value": "adult",
                "label": "Adult (36–55)",
                "description": "Smart training with joint-friendly modifications.",
                "calorie_note": "~10% lower burn rate"
            },
            {
                "value": "senior",
                "label": "Senior (56+)",
                "description": "Low-impact, chair-assisted movement for vitality.",
                "calorie_note": "~25% lower burn rate"
            },
        ]
    }