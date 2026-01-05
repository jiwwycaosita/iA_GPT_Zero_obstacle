from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from connectors.supabase_connector import SupabaseConnector
from workers.celery_worker import add_task
from agents.profile_agent import ProfileAgent

load_dotenv()
app = FastAPI(title="Zéro Obstacle Canada – API de base")

db = SupabaseConnector(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))


class JobRequest(BaseModel):
    job_name: str


@app.get("/")
def root():
    return {"status": "ok", "message": "API Zéro Obstacle prête"}


@app.post("/run_job")
def run_job(request: JobRequest):
    add_task.delay(request.job_name)
    return {"status": "queued", "job": request.job_name}


@app.post("/analyze_profile")
def analyze_profile(profile: dict):
    agent = ProfileAgent()
    result = agent.analyze_profile(profile, mode="precision")
    return result
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from api.workers.celery_worker import celery_app, add

app = FastAPI(title="Example Celery API", version="0.1.0")


class AddJobRequest(BaseModel):
    first_number: int
    second_number: int


@app.get("/")
async def health_check() -> dict:
    """Simple health check endpoint."""
    return {"status": "ok", "service": app.title}


@app.post("/enqueue")
async def enqueue_job(job_request: AddJobRequest) -> dict:
    """Enqueue a simple addition task for the Celery worker."""
    if not os.getenv("REDIS_URL"):
        raise HTTPException(status_code=500, detail="Missing REDIS_URL configuration")

    task = add.delay(job_request.first_number, job_request.second_number)
    return {"task_id": task.id, "status": "queued"}
