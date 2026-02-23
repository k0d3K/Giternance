from fastapi import FastAPI, APIRouter, Body, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import List
from .models import Slot, RepoLinks
from .data import getCalendar, storeCalendar, getLinks, storeLinks
from .logs import connectionManager
from .RepoManager import repoManager
from .errors import BackendError, logException
import asyncio

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
	return JSONResponse(content=None)

# Calendar endpoints
@router.get("/calendar")
def get_calendar():
	return getCalendar()

@router.post("/calendar")
def post_calendar(calendar: List[Slot]):
	# parse data
	storeCalendar(calendar)
	return JSONResponse(content=None)

# Sync status endpoints
@router.post("/sync")
def set_status(status: bool = Body(..., embed=False)):
	try:
		if status == True:
			repoManager.start()
		elif status == False:
			repoManager.stop()
		return JSONResponse(content=None)
	except BackendError as e:
		return JSONResponse(content={"success": False, "error": str(e)}, status_code=400)
	except Exception as e:
		logException(e, context="Unexpected error in /sync")
		return JSONResponse(content={"success": False, "error": "Internal server error"}, status_code=500)

@router.get("/sync")
def get_status():
	return repoManager.isEnabled()

app.include_router(router)

# =========================
# WebSocket Manager
# =========================

@app.websocket("/ws/logs")
async def websocket_logs(websocket: WebSocket):
	if connectionManager.isConnected():
		await websocket.close(code=1008)
		return

	await connectionManager.connect(websocket)

	try:
		while True:
			await asyncio.sleep(10)
	except WebSocketDisconnect:
		connectionManager.disconnect()
