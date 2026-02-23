"""
app/services/workout_service.py
--------------------------------
Business logic for mood-based workout generation and YouTube URL building.
"""

import urllib.parse

# ---------------------------------------------------------------------------
# Mood -> workout profile mapping
# ---------------------------------------------------------------------------

MOOD_PROFILES = {
    "happy": {
        "title": "Feel-Good Cardio Blast",
        "description": "Channel that positive energy into an upbeat, fun cardio session!",
        "intensity": "moderate",
        "style": "cardio dance",
        "calories_per_minute": 8,
        "youtube_query_template": "{time} minute upbeat cardio dance workout",
        "exercises": [
            {"name": "Jumping Jacks",     "sets": 3, "reps_or_duration": "45 sec", "approx_calories": 15},
            {"name": "High Knees",        "sets": 3, "reps_or_duration": "40 sec", "approx_calories": 18},
            {"name": "Dance Cardio",      "sets": 2, "reps_or_duration": "2 min",  "approx_calories": 30},
            {"name": "Butt Kicks",        "sets": 3, "reps_or_duration": "40 sec", "approx_calories": 15},
            {"name": "Cool-down Stretch", "sets": 1, "reps_or_duration": "3 min",  "approx_calories": 8},
        ],
    },
    "stressed": {
        "title": "Stress-Release Yoga Flow",
        "description": "Let go of tension with calming yoga and deep breathing.",
        "intensity": "low",
        "style": "yoga",
        "calories_per_minute": 4,
        "youtube_query_template": "{time} minute yoga for stress relief",
        "exercises": [
            {"name": "Box Breathing",         "sets": 1, "reps_or_duration": "3 min", "approx_calories": 5},
            {"name": "Cat-Cow Stretch",       "sets": 2, "reps_or_duration": "1 min", "approx_calories": 6},
            {"name": "Child's Pose",          "sets": 2, "reps_or_duration": "1 min", "approx_calories": 4},
            {"name": "Seated Forward Fold",   "sets": 2, "reps_or_duration": "1 min", "approx_calories": 5},
            {"name": "Legs Up The Wall",      "sets": 1, "reps_or_duration": "3 min", "approx_calories": 4},
        ],
    },
    "tired": {
        "title": "Gentle Energy Restore",
        "description": "Low-impact movement to wake your body up without draining you.",
        "intensity": "low",
        "style": "gentle stretching",
        "calories_per_minute": 3,
        "youtube_query_template": "{time} minute gentle stretching for tired body",
        "exercises": [
            {"name": "Neck Rolls",            "sets": 2, "reps_or_duration": "30 sec", "approx_calories": 3},
            {"name": "Shoulder Rolls",        "sets": 2, "reps_or_duration": "30 sec", "approx_calories": 3},
            {"name": "Standing Side Stretch", "sets": 2, "reps_or_duration": "30 sec", "approx_calories": 4},
            {"name": "Hip Circles",           "sets": 2, "reps_or_duration": "45 sec", "approx_calories": 5},
            {"name": "Slow Walk in Place",    "sets": 1, "reps_or_duration": "5 min",  "approx_calories": 12},
        ],
    },
    "energetic": {
        "title": "Power HIIT Surge",
        "description": "You're fired up — let's push hard with explosive HIIT training!",
        "intensity": "high",
        "style": "HIIT",
        "calories_per_minute": 12,
        "youtube_query_template": "{time} minute intense HIIT workout full body",
        "exercises": [
            {"name": "Burpees",            "sets": 4, "reps_or_duration": "45 sec", "approx_calories": 35},
            {"name": "Jump Squats",        "sets": 4, "reps_or_duration": "40 sec", "approx_calories": 30},
            {"name": "Mountain Climbers",  "sets": 4, "reps_or_duration": "45 sec", "approx_calories": 30},
            {"name": "Push-up Variations", "sets": 3, "reps_or_duration": "12 reps","approx_calories": 20},
            {"name": "Sprint in Place",    "sets": 4, "reps_or_duration": "30 sec", "approx_calories": 25},
        ],
    },
    "anxious": {
        "title": "Mindful Movement Reset",
        "description": "Ground yourself with mindful movement and calming breathwork.",
        "intensity": "low",
        "style": "mindfulness yoga",
        "calories_per_minute": 4,
        "youtube_query_template": "{time} minute mindful yoga for anxiety",
        "exercises": [
            {"name": "4-7-8 Breathing",        "sets": 3, "reps_or_duration": "2 min", "approx_calories": 5},
            {"name": "Body Scan Walk",          "sets": 1, "reps_or_duration": "5 min", "approx_calories": 15},
            {"name": "Slow Sun Salutation",     "sets": 2, "reps_or_duration": "2 min", "approx_calories": 10},
            {"name": "Grounding Foot Stretch",  "sets": 2, "reps_or_duration": "1 min", "approx_calories": 5},
            {"name": "Meditation",              "sets": 1, "reps_or_duration": "3 min", "approx_calories": 4},
        ],
    },
    "sad": {
        "title": "Endorphin Lift Workout",
        "description": "Movement is medicine — let's boost those feel-good hormones!",
        "intensity": "moderate",
        "style": "cardio + light strength",
        "calories_per_minute": 7,
        "youtube_query_template": "{time} minute workout to boost mood and energy",
        "exercises": [
            {"name": "Brisk Walk / March", "sets": 1, "reps_or_duration": "5 min",  "approx_calories": 25},
            {"name": "Bodyweight Squats",  "sets": 3, "reps_or_duration": "15 reps","approx_calories": 20},
            {"name": "Arm Circles",        "sets": 2, "reps_or_duration": "1 min",  "approx_calories": 6},
            {"name": "Standing Punches",   "sets": 3, "reps_or_duration": "45 sec", "approx_calories": 18},
            {"name": "Happy Baby Pose",    "sets": 1, "reps_or_duration": "2 min",  "approx_calories": 5},
        ],
    },
    "neutral": {
        "title": "Balanced Full-Body Routine",
        "description": "A solid, well-rounded workout hitting all the major muscle groups.",
        "intensity": "moderate",
        "style": "full body",
        "calories_per_minute": 7,
        "youtube_query_template": "{time} minute full body workout beginner intermediate",
        "exercises": [
            {"name": "Warm-up Jog in Place", "sets": 1, "reps_or_duration": "3 min",       "approx_calories": 18},
            {"name": "Push-ups",             "sets": 3, "reps_or_duration": "10 reps",      "approx_calories": 15},
            {"name": "Bodyweight Squats",    "sets": 3, "reps_or_duration": "15 reps",      "approx_calories": 20},
            {"name": "Plank Hold",           "sets": 3, "reps_or_duration": "30 sec",       "approx_calories": 12},
            {"name": "Lunges",               "sets": 3, "reps_or_duration": "12 reps each", "approx_calories": 18},
            {"name": "Cool-down Stretch",    "sets": 1, "reps_or_duration": "3 min",        "approx_calories": 8},
        ],
    },
    "motivated": {
        "title": "Beast Mode Strength Session",
        "description": "You're unstoppable today — time to hit a serious strength session!",
        "intensity": "high",
        "style": "strength training",
        "calories_per_minute": 10,
        "youtube_query_template": "{time} minute strength training workout no equipment",
        "exercises": [
            {"name": "Pull-ups / Rows",        "sets": 4, "reps_or_duration": "10 reps",      "approx_calories": 30},
            {"name": "Diamond Push-ups",       "sets": 4, "reps_or_duration": "12 reps",      "approx_calories": 25},
            {"name": "Bulgarian Split Squat",  "sets": 3, "reps_or_duration": "10 reps each", "approx_calories": 28},
            {"name": "Pike Push-ups",          "sets": 3, "reps_or_duration": "10 reps",      "approx_calories": 20},
            {"name": "Single-Leg Deadlift",    "sets": 3, "reps_or_duration": "12 reps each", "approx_calories": 22},
            {"name": "Plank Shoulder Taps",    "sets": 3, "reps_or_duration": "20 taps",      "approx_calories": 15},
        ],
    },
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def scale_exercises_to_time(exercises: list, available_time: int) -> list:
    """Trim exercise list based on available time."""
    if available_time <= 10:
        scaled = [dict(ex) for ex in exercises[:3]]
        for ex in scaled:
            ex["sets"] = min(ex.get("sets", 2), 2)
        return scaled
    elif available_time <= 20:
        return [dict(ex) for ex in exercises[:4]]
    else:
        return [dict(ex) for ex in exercises]


def calculate_total_calories(exercises: list, available_time: int, calories_per_minute: int) -> dict:
    """
    Calculate calorie estimates — per exercise sum and a time-based total.
    Returns a dict with breakdown and total range.
    """
    exercise_total = sum(ex.get("approx_calories", 0) for ex in exercises)

    # Time-based estimate gives a range (lower = calories_per_minute, upper = +25%)
    time_based_low  = calories_per_minute * available_time
    time_based_high = round(time_based_low * 1.25)

    # Blend both methods for a realistic range
    blended_low  = round((exercise_total + time_based_low)  / 2)
    blended_high = round((exercise_total + time_based_high) / 2)

    return {
        "per_exercise_total": exercise_total,
        "estimated_range": f"{blended_low}–{blended_high} kcal",
        "note": "Estimates based on a ~70 kg person. Actual burn varies by weight, age, and intensity."
    }


def build_youtube_url(query: str) -> str:
    """Build a YouTube search URL from a query string."""
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.youtube.com/results?search_query={encoded}"


def build_youtube_query(mood: str, available_time: int) -> str:
    """Build targeted YouTube search query based on mood and time."""
    template = MOOD_PROFILES[mood]["youtube_query_template"]
    rounded_time = max(5, round(available_time / 5) * 5)
    return template.format(time=rounded_time)


# ---------------------------------------------------------------------------
# Main service function
# ---------------------------------------------------------------------------

def get_mood_workout(mood: str, available_time: int) -> dict:
    """
    Generate a complete mood-based workout plan with a YouTube redirect URL
    and calorie burn estimates.

    Args:
        mood: One of the supported mood strings.
        available_time: Time available in minutes.

    Returns:
        A dict matching the WorkoutResponse schema in workouts.py
    """
    if mood not in MOOD_PROFILES:
        raise ValueError(f"Unsupported mood: {mood}")

    profile  = MOOD_PROFILES[mood]
    exercises = scale_exercises_to_time(profile["exercises"], available_time)
    calories  = calculate_total_calories(exercises, available_time, profile["calories_per_minute"])
    youtube_query = build_youtube_query(mood, available_time)
    youtube_url   = build_youtube_url(youtube_query)

    return {
        "mood": mood,
        "title": profile["title"],
        "description": profile["description"],
        "duration_minutes": available_time,
        "exercises": exercises,
        "calories_burned": calories,
        "youtube_url": youtube_url,
        "youtube_query": youtube_query,
    }