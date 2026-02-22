from fastapi import FastAPI, WebSocket
from typing import Optional

app = FastAPI()

class ConnectionManager:
	def __init__(self):
		self.active_connection: Optional[WebSocket] = None

	async def connect(self, websocket: WebSocket):
		await websocket.accept()
		self.active_connection = websocket

	def disconnect(self):
		self.active_connection = None

	def is_connected(self) -> bool:
		return self.active_connection is not None

	async def send_log(self, message: str):
		if self.active_connection:
			await self.active_connection.send_text(message)

