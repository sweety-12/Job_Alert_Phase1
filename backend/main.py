from fastapi import FastAPI, HTTPException, Query
# from platforms.linkedin import search_linkedin
from platforms.linkedin_playwright import fetch_linkedin_jobs
from models.preferences import JobPreferences
from fastapi.middleware.cors import CORSMiddleware
from services.daily_alerts import send_daily_alerts
from database.db import init_db, get_db_connection
# from database import init_db, save_subscription
# from pydantic import BaseModel
from apscheduler.schedulers.background import BackgroundScheduler
import time
import json
import os

app = FastAPI()

#init DB when server starts
@app.on_event("startup")
def startup_event():
    init_db()

#scheduler setup
scheduler = BackgroundScheduler()

#scheduler send_daily_alerts to run everyday at 8 AM
scheduler.add_job(send_daily_alerts, 'cron', hour = 6, minute = 0)
scheduler.start()

@app.get("/")
def root():
    return {"message": "Job Alert Service Running"}

# @app.get("/send-daily-alerts")
# def trigger_alerts():
#     """Manually trigger daily alerts (for testing)"""
#     send_daily_alerts()
#     return {"message": "Daily alerts sent successfully!"}

SECRET_KEY = os.environ.get("CRON_SECRET")

@app.get("/send-daily-alerts")
def send_daily_alerts_api(key: str = Query(None)):
    if key != SECRET_KEY:
        raise HTTPException(status_code=403, detail="Unauthorized")

    send_daily_alerts()
    return {"message": "Daily alerts sent successfully!"}

# app = FastAPI()

# @app.get("/linkedin")
# def get_linkedin_jobs(query: str, location: str):
#     jobs = search_linkedin(query, location)
#     return {"count": len(jobs), "jobs": jobs}

@app.get("/linkedin")
def linkedin_route(query: str, location: str):
    try:
        jobs = fetch_linkedin_jobs(query, location)
        return {"count": len(jobs), "jobs": jobs}

    except Exception as e:
        return {"error": str(e)}


# CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DB PATH
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "database")
PREF_DB = os.path.join(DB_DIR, "preferences_db.json")

# Create DB directory + file
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)
if not os.path.exists(PREF_DB):
    with open(PREF_DB, "w") as f:
        json.dump([], f)

# @app.post("/save-preferences")
# async def save_preferences(pref: JobPreferences):
#     """Save user job alert preferences to JSON DB."""

#     # If file is empty → default to []
#     try:
#         with open(PREF_DB, "r") as f:
#             content = f.read().strip()
#             data = json.loads(content) if content else []
#     except json.JSONDecodeError:
#         data = []

#     data.append(pref.dict())

#     with open(PREF_DB, "w") as f:
#         json.dump(data, f, indent=4)

#     return {"message": "Preferences saved successfully!"}



@app.post("/save-preferences")
async def save_preferences(pref: JobPreferences):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO preferences (job_role, location, experience, work_mode, email)
        VALUES (?, ?, ?, ?, ?)
    """, (pref.job_role, pref.location, pref.experience, pref.work_mode, pref.email))

    conn.commit()
    conn.close()

    return {"message": "Preferences saved successfully!"}




@app.get("/send-daily-alerts")
def manual_send_daily_alerts():
    """
    Manual trigger to send all daily job alerts.
    Useful for testing.
    """
    try:
        send_daily_alerts()
        return {"message": "Daily alerts sent successfully!"}

    except Exception as e:
        return {"error": str(e)}



# @app.post("/save-preferences")
# async def save_preferences(pref: JobPreferences):
#     """Save job preference request to JSON DB"""
#     try:
#         with open(PREF_DB, "r") as f:
#             data = json.load(f)

#         data.append(pref.dict())

#         with open(PREF_DB, "w") as f:
#             json.dump(data, f, indent=4)

#         return {"message": "Preferences saved successfully!"}
#     except Exception as e:
#         return {"error": str(e)}










# from fastapi import FastAPI
# from models.preferences import JobPreferences
# import json
# import os

# app = FastAPI()

# PREF_DB = "database/preferences_db.json"

# # Create DB if missing
# if not os.path.exists("database"):
#     os.makedirs("database")
# if not os.path.exists(PREF_DB):
#     with open(PREF_DB, "w") as f:
#         json.dump([], f)


# @app.post("/save-preferences")
# async def save_preferences(pref: JobPreferences):
#     """Save user job alert preferences to JSON DB."""
    
#     with open(PREF_DB, "r") as f:
#         data = json.load(f)

#     data.append(pref.dict())

#     with open(PREF_DB, "w") as f:
#         json.dump(data, f, indent=4)

#     return {"message": "Preferences saved successfully!"}
