import json
from typing import List
from .models import Slot, RepoLinks

SRC="/app/logs/"

def storeCalendar(calendar: List[Slot]):
	with open(SRC+"calendar.json", "w") as f:
		json.dump([slot.dict() for slot in calendar], f, indent=4)

def getCalendar() -> List[Slot]:
	try:
		with open(SRC+"calendar.json", "r") as f:
			data = json.load(f)
		return [Slot(**item) for item in data]
	except FileNotFoundError:
		return []

def storeLinks(links: RepoLinks):
	with open(SRC+"links.json", "w") as f:
		json.dump(links.dict(), f, indent=4)

def getLinks() -> RepoLinks:
	try:
		with open(SRC+"links.json", "r") as f:
			links = json.load(f)
		return RepoLinks(**links)
	except FileNotFoundError:
		return []
