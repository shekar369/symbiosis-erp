from fastapi import WebSocket
from typing import List, Dict


class NotificationWebSocket:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

    def disconnect(self, websocket: WebSocket, user_id: int):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)

    async def send_notification(self, message: dict, user_id: int):
        """
        Send notification to specific user
        """
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_json(message)

    async def broadcast_to_tenant(self, message: dict, tenant_id: int):
        """
        Broadcast notification to all users in a tenant
        """
        # TODO: Implement tenant-wide broadcast
        pass


notification_ws = NotificationWebSocket()
