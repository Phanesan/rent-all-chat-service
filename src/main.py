from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import os

from src.backend_checker import backend_checker
from src.database_manager import Base, engine
from src.websocket_router import router as websocket_router

app = FastAPI()

@app.on_event("startup")
def startup_event():
    backend_checker.start()

@app.on_event("shutdown")
def shutdown_event():
    backend_checker.stop()

# Logging configuration
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

log_filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".log"
log_filepath = os.path.join(LOGS_DIR, log_filename)

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[
        logging.FileHandler(log_filepath, mode='w'),
        logging.StreamHandler()
    ]
)

@app.get("/")
async def root():
    with open("index.html") as f:
        return HTMLResponse(f.read())

app.include_router(websocket_router)