import time
from celery import Celery
from datetime import datetime

celery = Celery(broker="redis://redis:6379/0")

JOBS = ["scrape_canada", "update_forms", "refresh_laws"]


while True:
    print(f"[Scheduler] Lancement du cycle {datetime.utcnow()}")
    for job in JOBS:
        celery.send_task("workers.celery_worker.add_task", args=[job])
    time.sleep(6 * 3600)  # relance toutes les 6h
import os
from celery import Celery
from celery.schedules import crontab

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "celery_scheduler",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["api.workers.celery_worker"],
)

celery_app.conf.beat_schedule = {
    "ping-every-minute": {
        "task": "api.workers.celery_worker.ping",
        "schedule": crontab(minute="*/1"),
    }
}

celery_app.conf.timezone = "UTC"
