from fastapi import APIRouter
from typing import Optional

router = APIRouter()

@router.get("/recipes")
async def get_recipes(goal: str, restrictions: Optional[str] = ""):
    # This logic ensures different recipes for different goals
    if goal == "weight_loss":
        recipes = [{"name": "Lean Green Salad", "calories": 250, "prep_time": 10, "servings": 1, "icon": "🥗", "dietary_tags": ["Vegan"]}]
    elif goal == "muscle_gain":
        recipes = [{"name": "Steak & Sweet Potato", "calories": 700, "prep_time": 25, "servings": 1, "icon": "🥩", "dietary_tags": ["High Protein"]}]
    else:
        recipes = [{"name": "Balanced Buddha Bowl", "calories": 450, "prep_time": 15, "servings": 1, "icon": "🥣", "dietary_tags": ["Healthy"]}]
    return {"recipes": recipes}

@router.get("/meal-plan")
async def get_meal_plan(goal: str, restrictions: Optional[str] = "", days: int = 7):
    plan = []
    for i in range(1, days + 1):
        plan.append({
            "day": i,
            "day_name": f"Day {i}",
            "total_calories": 2000,
            "meals": [{"meal_type": "Lunch", "name": "Chicken Wrap", "calories": 500, "icon": "🌯"}],
            "tips": "Stay hydrated!"
        })
    return {"meal_plan": plan}

@router.get("/healthy-swaps")
async def get_swaps(craving: str):
    swaps = {"sweet": [{"name": "Dark Chocolate", "icon": "🍫"}], "salty": [{"name": "Roasted Nuts", "icon": "🥜"}]}
    return {"swaps": swaps.get(craving.lower(), [])}