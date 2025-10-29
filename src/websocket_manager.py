from datetime import datetime
from zoneinfo import ZoneInfo
from fastapi import WebSocket
import logging

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: str):
        await websocket.accept()
        self.active_connections[user_id] = websocket
        timestamp = datetime.now(ZoneInfo("UTC")).isoformat()
        log = f"[{timestamp}] Usuario conectado: {user_id}"
        logging.info(log)

    def disconnect(self, user_id: str):
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            timestamp = datetime.now(ZoneInfo("UTC")).isoformat()
            log = f"[{timestamp}] Usuario desconectado: {user_id}"
            logging.info(log)

    async def send_personal_message(self, message: str, recipient_id: str, sender_id: str):
        if recipient_id in self.active_connections:
            websocket = self.active_connections[recipient_id]
            timestamp = datetime.now(ZoneInfo("UTC")).isoformat()
            payload = {
                "from": sender_id,
                "to": recipient_id,
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
