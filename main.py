import json
from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import logging
import os

app = FastAPI()

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

class ConnectionManager:
    def __init__(self):
        # Diccionario para almacenar las conexiones activas: {user_id: WebSocket}
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        """Acepta una nueva conexión WebSocket y la almacena."""
        await websocket.accept()
        self.active_connections[user_id] = websocket

        timestamp = datetime.now(ZoneInfo("UTC")).isoformat()
        log = f"[{timestamp}] Usuario conectado: {user_id}"
        logging.info(log)

    def disconnect(self, user_id: str):
        """Cierra y elimina una conexión WebSocket."""
        if user_id in self.active_connections:
            del self.active_connections[user_id]

            timestamp = datetime.now(ZoneInfo("UTC")).isoformat()
            log = f"[{timestamp}] Usuario desconectado: {user_id}"
            logging.info(log)

    async def send_personal_message(self, message: str, recipient_id: str, sender_id: str):
        """Envía un mensaje a un usuario específico."""
        if recipient_id in self.active_connections:
            websocket = self.active_connections[recipient_id]
            
            timestamp = datetime.now(ZoneInfo("UTC")).isoformat()

            payload = {
                "from": sender_id,
                "message": message,
                "timestamp": timestamp
            }
            
            await websocket.send_json(payload)
            log = f"[{timestamp}] {sender_id} >> {recipient_id}: {message}"
            logging.info(log)
        else:
            timestamp = datetime.now(ZoneInfo("UTC")).isoformat()
            log = f"[{timestamp}] Error: Usuario {recipient_id} no encontrado o no conectado."
            logging.info(log)

manager = ConnectionManager()

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)

                recipient_id = message_data["recipient_id"]
                message = message_data["message"]

                await manager.send_personal_message(message, recipient_id, user_id)

            except (json.JSONDecodeError, KeyError):
                await websocket.send_text("Error: Mensaje debe ser un JSON con 'recipient_id' y 'message'.")

    except WebSocketDisconnect:
        manager.disconnect(user_id)
