import asyncio
import json
from datetime import datetime
from zoneinfo import ZoneInfo
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session

from src.backend_checker import backend_checker
from src.database_manager import get_db, Message
from src.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, db: Session = Depends(get_db)):
    await websocket.accept()

    # Esperar a que el backend este disponible antes de registrar la conexion
    while not backend_checker.is_available:
        await websocket.send_json({"status": "waiting_for_backend", "message": "Servicio no disponible, esperando al backend...", "code": 2000})
        await asyncio.sleep(5)

    # Registrar la conexion una vez que el backend esta listo
    manager.active_connections[user_id] = websocket
    timestamp = datetime.now(ZoneInfo("UTC")).isoformat()
    logging.info(f"[{timestamp}] Usuario conectado: {user_id}")

    try:
        while True:
            # Bucle de espera si el backend se cae durante la operacion
            if not backend_checker.is_available:
                await websocket.send_json({"error": "Servicio no disponible temporalmente. Reintentando...", "code": 1000})
                while not backend_checker.is_available:
                    await asyncio.sleep(5)
                await websocket.send_json({"status": "service_restored", "message": "Servicio restablecido. Ya puedes enviar mensajes.", "code": 2001})

            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                recipient_id = message_data["recipient_id"]
                message_content = message_data["message"]
                
                db_message = Message(
                    senderId=user_id,
                    receiverId=recipient_id,
                    content=message_content
                )
                db.add(db_message)
                db.commit()

                await manager.send_personal_message(message_content, recipient_id, user_id)
            except (json.JSONDecodeError, KeyError):
                await websocket.send_json({"error": "Mensaje debe ser un JSON con 'recipient_id' y 'message'.", "code": 1001})
    except WebSocketDisconnect:
        manager.disconnect(user_id)