"""
app/services/workout_service.py
--------------------------------
Business logic for mood + age-based workout generation and YouTube URL building.
"""

import urllib.parse

# ---------------------------------------------------------------------------
# Age category definitions
# ---------------------------------------------------------------------------

AGE_CATEGORIES = {
    "teen": {
        "label": "Teen (13–17)",
        "calorie_multiplier": 1.10,       # teens burn slightly more
        "intensity_cap": "high",          # no restriction on intensity
        "rest_note": "Rest 30–45 sec between sets. Focus on form over speed.",
        "youtube_age_modifier": "for teens beginners",
    },
    "young_adult": {
        "label": "Young Adult (18–35)",
        "calorie_multiplier": 1.0,        # baseline
        "intensity_cap": "high",
        "rest_note": "Rest 30–60 sec between sets. Push hard and recover well.",
        "youtube_age_modifier": "",
    },
    "adult": {
        "label": "Adult (36–55)",
        "calorie_multiplier": 0.90,       # slightly lower metabolic rate
        "intensity_cap": "moderate",      # cap energetic/motivated at moderate
        "rest_note": "Rest 45–75 sec between sets. Prioritize joint mobility.",
        "youtube_age_modifier": "for adults over 40",
    },
    "senior": {
        "label": "Senior (56+)",
        "calorie_multiplier": 0.75,       # lower metabolic rate
        "intensity_cap": "low",           # cap everything at low intensity
        "rest_note": "Rest 60–90 sec between sets. Move gently, listen to your body.",
        "youtube_age_modifier": "for seniors over 60 low impact",
    },
}

# ---------------------------------------------------------------------------
# Senior-safe exercise overrides (replaces high-impact exercises for seniors)
# ---------------------------------------------------------------------------

SENIOR_EXERCISE_OVERRIDES = {
    "happy": [
        {"name": "Seated March",          "sets": 3, "reps_or_duration": "1 min",  "approx_calories": 8},
        {"name": "Standing Side Steps",   "sets": 3, "reps_or_duration": "45 sec", "approx_calories": 7},
        {"name": "Gentle Arm Swings",     "sets": 2, "reps_or_duration": "1 min",  "approx_calories": 5},
        {"name": "Seated Toe Taps",       "sets": 2, "reps_or_duration": "45 sec", "approx_calories": 6},
        {"name": "Cool-down Breathing",   "sets": 1, "reps_or_duration": "3 min",  "approx_calories": 4},
    ],
    "energetic": [
        {"name": "Chair Squats",          "sets": 3, "reps_or_duration": "12 reps", "approx_calories": 18},
        {"name": "Wall Push-ups",         "sets": 3, "reps_or_duration": "12 reps", "approx_calories": 14},
        {"name": "Step Touch Side-to-Side","sets": 3,"reps_or_duration": "1 min",  "approx_calories": 12},
        {"name": "Seated Leg Extensions", "sets": 2, "reps_or_duration": "15 reps","approx_calories": 8},
        {"name": "Standing Balance Hold", "sets": 2, "reps_or_duration": "30 sec", "approx_calories": 5},
    ],
    "motivated": [
        {"name": "Chair Squats",          "sets": 4, "reps_or_duration": "12 reps", "approx_calories": 20},
        {"name": "Wall Push-ups",         "sets": 4, "reps_or_duration": "15 reps", "approx_calories": 16},
        {"name": "Standing Row (band)",   "sets": 3, "reps_or_duration": "12 reps", "approx_calories": 14},
        {"name": "Heel Raises",           "sets": 3, "reps_or_duration": "15 reps", "approx_calories": 10},
        {"name": "Bird Dog Hold",         "sets": 3, "reps_or_duration": "20 sec",  "approx_calories": 8},
        {"name": "Seated Bicep Curls",    "sets": 3, "reps_or_duration": "12 reps", "approx_calories": 8},
    ],
    "sad": [
        {"name": "Gentle Walk in Place",  "sets": 1, "reps_or_duration": "5 min",  "approx_calories": 18},
        {"name": "Seated Arm Circles",    "sets": 2, "reps_or_duration": "1 min",  "approx_calories": 5},
        {"name": "Chair Squats",          "sets": 2, "reps_or_duration": "10 reps","approx_calories": 14},
        {"name": "Shoulder Rolls",        "sets": 2, "reps_or_duration": "30 sec", "approx_calories": 3},
        {"name": "Seated Meditation",     "sets": 1, "reps_or_duration": "3 min",  "approx_calories": 3},
    ],
    "neutral": [
        {"name": "March in Place",        "sets": 1, "reps_or_duration": "3 min",  "approx_calories": 12},
        {"name": "Wall Push-ups",         "sets": 3, "reps_or_duration": "12 reps","approx_calories": 12},
        {"name": "Chair Squats",          "sets": 3, "reps_or_duration": "12 reps","approx_calories": 16},
        {"name": "Seated Leg Lifts",      "sets": 3, "reps_or_duration": "12 reps","approx_calories": 8},
        {"name": "Standing Calf Raises",  "sets": 3, "reps_or_duration": "15 reps","approx_calories": 7},
        {"name": "Seated Spinal Twist",   "sets": 1, "reps_or_duration": "2 min",  "approx_calories": 4},
    ],
}

# Adult overrides for high-impact exercises (moderate intensity substitutions)
ADULT_EXERCISE_OVERRIDES = {
    "energetic": [
        {"name": "Squat to Overhead Press", "sets": 4, "reps_or_duration": "12 reps", "approx_calories": 28},
        {"name": "Reverse Lunges",           "sets": 4, "reps_or_duration": "10 reps each","approx_calories": 25},
        {"name": "Modified Mountain Climbers","sets": 3,"reps_or_duration": "40 sec", "approx_calories": 22},
        {"name": "Push-up Variations",       "sets": 3, "reps_or_duration": "10 reps","approx_calories": 18},
        {"name": "Step Jacks",               "sets": 3, "reps_or_duration": "45 sec", "approx_calories": 18},
    ],
    "motivated": [
        {"name": "Dumbbell / Band Rows",     "sets": 4, "reps_or_duration": "12 reps",      "approx_calories": 26},
        {"name": "Push-ups",                 "sets": 4, "reps_or_duration": "12 reps",      "approx_calories": 22},
        {"name": "Reverse Lunges",           "sets": 3, "reps_or_duration": "10 reps each", "approx_calories": 24},
        {"name": "Pike Push-ups",            "sets": 3, "reps_or_duration": "10 reps",      "approx_calories": 18},
        {"name": "Romanian Deadlift (band)", "sets": 3, "reps_or_duration": "12 reps",      "approx_calories": 20},
        {"name": "Plank Hold",               "sets": 3, "reps_or_duration": "30 sec",       "approx_calories": 12},
    ],
}

# ---------------------------------------------------------------------------
# Mood -> workout profile mapping (base — used for young adults)
# ---------------------------------------------------------------------------

MOOD_PROFILES = {
    "happy": {
        "title": "Feel-Good Cardio Blast",
        "description": "Channel that positive energy into an upbeat, fun cardio session!",
        "intensity": "moderate",
        "style": "cardio dance",
        "calories_per_minute": 8,
        "youtube_query_template": "{time} minute upbeat cardio dance workout {age_mod}",
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
        "youtube_query_template": "{time} minute yoga for stress relief {age_mod}",
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
        "youtube_query_template": "{time} minute gentle stretching for tired body {age_mod}",
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
        "youtube_query_template": "{time} minute intense HIIT workout full body {age_mod}",
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
        "youtube_query_template": "{time} minute mindful yoga for anxiety {age_mod}",
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
        "youtube_query_template": "{time} minute workout to boost mood and energy {age_mod}",
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
        "youtube_query_template": "{time} minute full body workout beginner intermediate {age_mod}",
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
        "youtube_query_template": "{time} minute strength training workout no equipment {age_mod}",
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

def get_exercises_for_age_and_mood(mood: str, age_category: str) -> list:
    """Return the appropriate exercise list based on age category and mood."""
    if age_category == "senior":
        return SENIOR_EXERCISE_OVERRIDES.get(mood, MOOD_PROFILES[mood]["exercises"])
    elif age_category == "adult":
        return ADULT_EXERCISE_OVERRIDES.get(mood, MOOD_PROFILES[mood]["exercises"])
    else:
        # teen and young_adult use base exercises
        return MOOD_PROFILES[mood]["exercises"]


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


def calculate_total_calories(
    exercises: list,
    available_time: int,
    calories_per_minute: int,
    calorie_multiplier: float,
) -> dict:
    """
    Calculate age-adjusted calorie estimates.
    Returns a dict with breakdown and total range.
    """
    exercise_total = sum(ex.get("approx_calories", 0) for ex in exercises)

    time_based_low  = calories_per_minute * available_time * calorie_multiplier
    time_based_high = round(time_based_low * 1.25)
    time_based_low  = round(time_based_low)

    blended_low  = round((exercise_total * calorie_multiplier + time_based_low)  / 2)
    blended_high = round((exercise_total * calorie_multiplier + time_based_high) / 2)

    return {
        "per_exercise_total": round(exercise_total * calorie_multiplier),
        "estimated_range": f"{blended_low}–{blended_high} kcal",
        "note": "Age-adjusted estimate for a ~70 kg person. Actual burn varies by fitness level and intensity.",
    }


def build_youtube_url(query: str) -> str:
    """Build a YouTube search URL from a query string."""
    encoded = urllib.parse.quote_plus(query)
    return f"https://www.youtube.com/results?search_query={encoded}"


def build_youtube_query(mood: str, available_time: int, age_category: str) -> str:
    """Build age-and-mood-targeted YouTube search query."""
    template = MOOD_PROFILES[mood]["youtube_query_template"]
    rounded_time = max(5, round(available_time / 5) * 5)
    age_mod = AGE_CATEGORIES[age_category]["youtube_age_modifier"]
    return template.format(time=rounded_time, age_mod=age_mod).strip()


# ---------------------------------------------------------------------------
# Main service function
# ---------------------------------------------------------------------------

def get_mood_workout(mood: str, available_time: int, age_category: str = "young_adult") -> dict:
    """
    Generate a complete mood + age-based workout plan with a YouTube redirect
    URL and age-adjusted calorie burn estimates.

    Args:
        mood:           One of the supported mood strings.
        available_time: Time available in minutes.
        age_category:   One of: teen | young_adult | adult | senior.

    Returns:
        A dict matching the WorkoutResponse schema in workouts.py
    """
    if mood not in MOOD_PROFILES:
        raise ValueError(f"Unsupported mood: {mood}")
    if age_category not in AGE_CATEGORIES:
        raise ValueError(f"Unsupported age_category: {age_category}")

    profile        = MOOD_PROFILES[mood]
    age_profile    = AGE_CATEGORIES[age_category]
    raw_exercises  = get_exercises_for_age_and_mood(mood, age_category)
    exercises      = scale_exercises_to_time(raw_exercises, available_time)
    calories       = calculate_total_calories(
        exercises,
        available_time,
        profile["calories_per_minute"],
        age_profile["calorie_multiplier"],
    )
    youtube_query  = build_youtube_query(mood, available_time, age_category)
    youtube_url    = build_youtube_url(youtube_query)

    return {
        "mood": mood,
        "age_category": age_category,
        "age_label": age_profile["label"],
        "title": profile["title"],
        "description": profile["description"],
        "duration_minutes": available_time,
        "rest_note": age_profile["rest_note"],
        "exercises": exercises,
        "calories_burned": calories,
        "youtube_url": youtube_url,
        "youtube_query": youtube_query,
    }