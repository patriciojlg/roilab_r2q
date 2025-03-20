
from fastapi import APIRouter, HTTPException
from redis import Redis
from rq import Queue
import time
import uuid

# Conectar con Redis
redis_conn = Redis(host='localhost', port=6379, db=0)
queue = Queue('default', connection=redis_conn)

task_router = APIRouter()

def update_task_status(job_id: str, status: str):
    redis_conn.hset(f"task:{job_id}", mapping={"status": status})

def example_task(job_id: str, duration: int, payload: dict):
    update_task_status(job_id, "running")
    time.sleep(duration)
    update_task_status(job_id, "completed")
    return {"job_id": job_id, "status": "completed", "payload": payload}

@task_router.post("/tasks/")
def create_task(duration: int, payload: dict):
    job_id = str(uuid.uuid4())
    update_task_status(job_id, "queued")
    queue.enqueue(example_task, job_id, duration, payload)
    return {"job_id": job_id, "status": "queued", "payload": payload}

@task_router.get("/tasks/{job_id}")
def get_task_status(job_id: str):
    status = redis_conn.hget(f"task:{job_id}", "status")
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"job_id": job_id, "status": status.decode(), "payload": {}}

@task_router.get("/tasks/")
def list_tasks():
    keys = redis_conn.keys("task:*")
    tasks = []
    for key in keys:
        job_id = key.decode().split(":")[1]
        status = redis_conn.hget(key, "status").decode()
        tasks.append({"job_id": job_id, "status": status, "payload": {}})
    return tasks

@task_router.delete("/tasks/{job_id}")
def cancel_task(job_id: str):
    update_task_status(job_id, "cancelled")
    return {"job_id": job_id, "status": "cancelled"}