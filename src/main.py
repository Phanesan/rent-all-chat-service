from datetime import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import logging
import os

from src.database_manager import Base, engine
from src.websocket_router import router as websocket_router

app = FastAPI()

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

# Create DB tables on startup
@app.on_event("startup")
async def startup_event():
    logging.info("Application has started.")
    Base.metadata.create_all(bind=engine)