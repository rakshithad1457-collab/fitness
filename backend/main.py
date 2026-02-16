from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

app = FastAPI(title="FitMood API")

# FORCED CORS: This stops the browser from blocking the connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# EMERGENCY LOGGER: This prints the REAL error to your terminal if the backend crashes
@app.middleware("http")
async def crash_catcher(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        print("\n!!! BACKEND CRASH DETECTED !!!")
        print(traceback.format_exc()) # Check your black terminal window for this!
        return JSONResponse(
            status_code=500,
            content={"detail": str(e)}
        )

from app.routers import auth, workouts, nutrition
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(workouts.router, prefix="/api/workouts", tags=["Workouts"])
app.include_router(nutrition.router, prefix="/api/nutrition", tags=["Nutrition"])

@app.get("/")
async def root():
    return {"message": "FitMood API is Running"}