from fastapi import WebSocket
from typing import Optional
import logging
import asyncio

logging.basicConfig(
	filename='./logs/info.log',
	level=logging.INFO,
	format='%(asctime)s [%(levelname)s] %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S'
)

def logSync(msg: str):
	logging.info(msg)
	if connectionManager.isConnected():
		asyncio.run(connectionManager.sendLog(f"[SYNC]: {msg}"))

def logInfo(msg: str):
	logging.info(msg)
	if connectionManager.isConnected():
		asyncio.run(connectionManager.sendLog(f"[INFO]: {msg}"))

def logError(msg: str):
	logging.error(msg)
	if connectionManager.isConnected():
		asyncio.run(connectionManager.sendLog(f"[ERROR]: {msg}"))

class _ConnectionManager:
	def __init__(self):
		self.active_connection: Optional[WebSocket] = None

	async def connect(self, websocket: WebSocket):
		await websocket.accept()
		self.active_connection = websocket

	def disconnect(self):
		self.active_connection = None

	def isConnected(self) -> bool:
		return self.active_connection is not None

	async def sendLog(self, message: str):
		if self.active_connection:
			await self.active_connection.send_text(message)

connectionManager = _ConnectionManager()

del _ConnectionManager
