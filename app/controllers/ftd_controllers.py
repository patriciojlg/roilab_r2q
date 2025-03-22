
from fastapi import APIRouter, Body, HTTPException
from redis import Redis
from rq import Queue
import time
import uuid
import boto3

import json

# Conectar con Redis
redis_conn = Redis(host='localhost', port=6379, db=0)
queue = Queue('default', connection=redis_conn)

task_router = APIRouter()

def update_task_status(job_id: str, status: str):
    redis_conn.hset(f"task:{job_id}", mapping={"status": status})

def example_task(payload: dict):
    job_id = payload["job_id"]
    task = payload["task"]
    update_task_status(job_id, "running")

    # Nombre del ARN de tu Step Function
    STATE_MACHINE_ARN = "arn:aws:states:us-east-1:963485456147:stateMachine:FTC-Codelco-MachineState"



    # Crear cliente
    sfn = boto3.client("stepfunctions")

    # Ejecutar la Step Function
    response = sfn.start_execution(
        stateMachineArn=STATE_MACHINE_ARN,
        input=json.dumps(task)
    )

    ok = False
    while not ok:
        response = sfn.describe_execution(
            executionArn=response["executionArn"]
        )
        if response["status"] == "RUNNING":
            time.sleep(5)
            # Imprimir resultado    
            print("Ejecución iniciada:")
            print(response["status"])

        else:
            ok = True


    update_task_status(job_id, "completed")
    return {"job_id": job_id, "status": "completed", "payload": payload}

@task_router.post("/tasks/")
def create_task(payload: list  = Body(...)):
    job_id = str(uuid.uuid4())
    payload = {"task": payload, "job_id": job_id}
    update_task_status(job_id, "queued")
    queue.enqueue(example_task, payload)
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