import logging
from fastapi import WebSocket
from typing import List, Dict

logger = logging.getLogger(__name__)


class NotificationWebSocket:
    def __init__(self):
        # user_id → list of active WebSocket connections
        self.active_connections: Dict[int, List[WebSocket]] = {}
        # tenant_id → set of user_ids currently connected
        self.tenant_users: Dict[int, set] = {}

    async def connect(self, websocket: WebSocket, user_id: int, tenant_id: int = None):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)

        if tenant_id is not None:
            if tenant_id not in self.tenant_users:
                self.tenant_users[tenant_id] = set()
            self.tenant_users[tenant_id].add(user_id)

        logger.debug("WebSocket connected: user_id=%d", user_id)

    def disconnect(self, websocket: WebSocket, user_id: int, tenant_id: int = None):
        if user_id in self.active_connections:
            connections = self.active_connections[user_id]
            if websocket in connections:
                connections.remove(websocket)
            if not connections:
                del self.active_connections[user_id]
                if tenant_id is not None and tenant_id in self.tenant_users:
                    self.tenant_users[tenant_id].discard(user_id)

        logger.debug("WebSocket disconnected: user_id=%d", user_id)

    async def send_notification(self, message: dict, user_id: int):
        """Send a notification to all active connections for a single user."""
        connections = self.active_connections.get(user_id, [])
        dead = []
        for ws in connections:
            try:
                await ws.send_json(message)
            except Exception:
                dead.append(ws)
        for ws in dead:
            self.active_connections[user_id].remove(ws)

    async def broadcast_to_tenant(self, message: dict, tenant_id: int):
        """Broadcast a notification to every connected user in the given tenant."""
        user_ids = list(self.tenant_users.get(tenant_id, set()))
        for uid in user_ids:
            await self.send_notification(message, uid)
        logger.debug(
            "Broadcast to tenant %d sent to %d user(s)", tenant_id, len(user_ids)
        )

    async def broadcast_to_all(self, message: dict):
        """Send a notification to all currently connected users."""
        for uid in list(self.active_connections.keys()):
            await self.send_notification(message, uid)


notification_ws = NotificationWebSocket()
