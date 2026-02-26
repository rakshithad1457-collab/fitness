from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import json
import os
from app.models.user import UserCreate, Token, UserResponse

router = APIRouter()

# File to store users permanently
DB_FILE = "users_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            return json.load(f)
    return {}

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "fitmood-secret-key-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# ─────────────────────────────────────────
#  REGISTER
# ─────────────────────────────────────────
@router.post("/register", response_model=Token)
async def register(user: UserCreate):
    users_db = load_db()

    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    new_user = {
        "id":              len(users_db) + 1,
        "email":           user.email,
        "hashed_password": hashed_password,
        "workouts":        0,
        "lastMood":        "neutral",
        "joined":          datetime.utcnow().strftime("%Y-%m-%d"),
    }

    users_db[user.email] = new_user
    save_db(users_db)

    expire     = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode  = {"sub": user.email, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": encoded_jwt,
        "token_type":   "bearer",
        "user":         {"id": new_user["id"], "email": new_user["email"]},
    }


# ─────────────────────────────────────────
#  LOGIN
# ─────────────────────────────────────────
@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    users_db    = load_db()
    stored_user = users_db.get(user.email)

    if not stored_user or not pwd_context.verify(user.password, stored_user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    expire      = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode   = {"sub": stored_user["email"], "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return {
        "access_token": encoded_jwt,
        "token_type":   "bearer",
        "user":         {"id": stored_user["id"], "email": stored_user["email"]},
    }


# ─────────────────────────────────────────
#  ADMIN — GET ALL USERS
#  Called by your Next.js /admin page
#  GET /auth/admin/users
# ─────────────────────────────────────────
@router.get("/admin/users")
async def get_all_users():
    users_db = load_db()

    # Never send hashed passwords to the frontend
    safe_users = [
        {
            "id":        u["id"],
            "email":     u["email"],
            "joined":    u.get("joined",   "N/A"),
            "workouts":  u.get("workouts",  0),
            "lastMood":  u.get("lastMood", "neutral"),
        }
        for u in users_db.values()
    ]

    # Sort by id so newest users appear at the bottom
    safe_users.sort(key=lambda x: x["id"])

    return safe_users


# ─────────────────────────────────────────
#  ADMIN — GET STATS SUMMARY
#  GET /auth/admin/stats
# ─────────────────────────────────────────
@router.get("/admin/stats")
async def get_stats():
    users_db = load_db()
    users    = list(users_db.values())

    total_users    = len(users)
    total_workouts = sum(u.get("workouts", 0) for u in users)
    avg_workouts   = round(total_workouts / total_users, 1) if total_users > 0 else 0

    # Count how many users have each mood
    mood_counts = {}
    for u in users:
        mood = u.get("lastMood", "neutral")
        mood_counts[mood] = mood_counts.get(mood, 0) + 1

    top_mood = max(mood_counts, key=mood_counts.get) if mood_counts else "neutral"

    return {
        "total_users":    total_users,
        "total_workouts": total_workouts,
        "avg_workouts":   avg_workouts,
        "top_mood":       top_mood,
        "mood_counts":    mood_counts,
    }


# ─────────────────────────────────────────
#  ADMIN — DELETE A USER
#  DELETE /auth/admin/users/{email}
# ─────────────────────────────────────────
@router.delete("/admin/users/{email}")
async def delete_user(email: str):
    users_db = load_db()

    if email not in users_db:
        raise HTTPException(status_code=404, detail="User not found")

    del users_db[email]
    save_db(users_db)

    return {"message": f"User {email} deleted successfully"}