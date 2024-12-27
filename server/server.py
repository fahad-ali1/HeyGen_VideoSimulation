"""
FastAPI Video Translation Simulation Service.

This module provides a simple API to simulate video translation jobs with async processing.
It includes endpoints for starting translation jobs and checking their status.
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import random
import time
import threading
import uuid

# Create a FastAPI instance
app = FastAPI()

# Simulated job storage
jobs = {}

# NOTE: Not sure if the HR wanted a random delay or configurable fixed delay
# DELAY = random.randint(1, 12)
# Configurable time (seconds)
DELAY = 5

SPECIAL_JOB_ID = "special-pending-job"

def simulate_translation(job_id):
    """
    Simulate a video translation process.

    Args:
        job_id (str): Unique identifier for the translation job.
    Note:
        This function simulates processing by waiting for DELAY seconds
        and then randomly sets the job status to either "completed" or "error".
    """
    time.sleep(DELAY)
    # Randomized completed or error
    jobs[job_id] = random.choice(["error", "completed"])

@app.post("/start")
async def start_translation():
    """
    Start a translation job.

    Returns:
        Dict[str, str]: Dictionary containing the job_id.
    Example:
        Response: {"job_id": "example-job-id"}
    """
    job_id = str(uuid.uuid4())
    jobs[job_id] = "pending"
    threading.Thread(target=simulate_translation, args=(job_id,)).start()
    return {"job_id": job_id}

@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """
    Get status of job.

    Args:
        job_id (str): Unique identifier for the translation job.
    Returns:
        Dict[str, str]: Dictionary containing the job_id and result.
    Example:
        Response: {"job_id": "example-job-id", "result": "completed"}
    """
    if job_id == SPECIAL_JOB_ID:
        # Always returns "pending" to test exponential backoff in client
        return JSONResponse(content={"job_id": job_id, "result": "pending"})
    
    if job_id in jobs:
        return JSONResponse(content={"job_id": job_id, "result": jobs[job_id]})
    
    raise HTTPException(status_code=404, detail="Job not found")