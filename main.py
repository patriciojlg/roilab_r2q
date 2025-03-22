# main.py
from fastapi import FastAPI
from app.controllers.ftd_controllers import task_router

app = FastAPI()

# Registrar los routers
app.include_router(task_router, prefix="/ftd-queues")
