from fastapi import FastAPI, APIRouter, Body, Response, WebSocket, WebSocketDisconnect
from typing import List
from .models import Slot, RepoLinks
from .data import getCalendar, storeCalendar, getLinks, storeLinks
from .logs import ConnectionManager
from .synchronizer import Synchronizer

app = FastAPI()

router = APIRouter(prefix="/api")

# =========================
# REST API ROUTES
# =========================

# Repo endpoints
@router.get("/repos")
def get_repos():
	return getLinks()

@router.post("/repos")
def post_repos(repos: RepoLinks):
	# parse data
	storeLinks(repos)
	return Response(content=None)

# Calendar endpoints
@router.get("/calendar")
def get_calendar():
	return getCalendar()

@router.post("/calendar")
def post_calendar(calendar: List[Slot]):
	# parse data
	storeCalendar(calendar)
	return Response(content=None)

# Sync status endpoints
synchronizer = Synchronizer()

@router.post("/sync")
def set_status(status: bool = Body(..., embed=False)):
	try:
		if status == True:
			synchronizer.start()
		elif status == False:
			synchronizer.stop()
		return Response(content=None)
	except Exception as e:
		return Response(content=f"Error: {str(e)}", status_code=500)

@router.get("/sync")
def get_status():
	return synchronizer.isEnabled()

app.include_router(router)

# =========================
# WebSocket Manager
# =========================

manager = ConnectionManager()

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
	if manager.is_connected():
		await websocket.close(code=1008)
		return

	await manager.connect(websocket)

	try:
		while True:
			await websocket.receive_text()
	except WebSocketDisconnect:
		manager.disconnect()
