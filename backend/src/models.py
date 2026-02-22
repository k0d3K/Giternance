from pydantic import BaseModel

class Slot(BaseModel):
	start: str
	end: str

class RepoLinks(BaseModel):
	src: str
	dst: str
