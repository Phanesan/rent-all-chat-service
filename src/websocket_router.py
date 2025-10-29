import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.database_manager import SessionLocal
from src.models import Message
from src.websocket_manager import manager

router = APIRouter()

@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket, user_id)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                message_data = json.loads(data)
                recipient_id = message_data["recipient_id"]
                message = message_data["message"]

                # Save message to database
                db = SessionLocal()
                try:
                    db_message = Message(
                        sender_id=user_id,
                        recipient_id=recipient_id,
                        message=message
                    )
                    db.add(db_message)
                    db.commit()
                finally:
                    db.close()

                await manager.send_personal_message(message, recipient_id, user_id)
            except (json.JSONDecodeError, KeyError):
                await websocket.send_text("Error: Mensaje debe ser un JSON con 'recipient_id' y 'message'.")
    except WebSocketDisconnect:
        manager.disconnect(user_id)