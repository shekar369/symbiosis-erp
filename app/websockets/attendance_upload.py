from fastapi import WebSocket
from typing import List


class AttendanceUploadWebSocket:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_progress(self, message: dict, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast_progress(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)


attendance_ws = AttendanceUploadWebSocket()


async def handle_attendance_upload_progress(websocket: WebSocket):
    """
    WebSocket endpoint for real-time attendance upload progress
    """
    await attendance_ws.connect(websocket)
    try:
        while True:
            # Wait for messages from client
            data = await websocket.receive_text()
            # Process and send updates
            await attendance_ws.send_progress(
                {"status": "processing", "message": "Upload in progress"},
                websocket
            )
    except Exception as e:
        attendance_ws.disconnect(websocket)
