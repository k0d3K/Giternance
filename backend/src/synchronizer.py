import os
import shutil
from git import Repo, GitCommandError
from typing import List
from .models import Slot, RepoLinks
from .data import getCalendar, getLinks

import os
os.environ["SSH_AUTH_SOCK"] = "/ssh-agent"

class Synchronizer:
	def __init__(self):
		self.active: bool = False

	def start(self):
		calendar: List[Slot] = getCalendar()
		if len(calendar) == 0:
			raise  RuntimeError(f"No calendar.")
		repos: RepoLinks = getLinks()
		if not cloneRepos(repos):
			raise  RuntimeError(f"Invalid repos.")
		return 0

	def stop(self) -> bool:
		self.active_connection = None

	def isEnabled(self) -> bool:
		return self.active

def clone_or_update_repo(repo_url: str, target_dir: str):
	"""
	Clone a Git repo if missing, or check if the existing repo matches the URL.
	"""
	if os.path.exists(target_dir) and os.path.isdir(target_dir):
		try:
			repo = Repo(target_dir)
			origin_url = next((r.url for r in repo.remotes), None)
			if origin_url != repo_url:
				print(f"Remote URL mismatch for {target_dir}: {origin_url} != {repo_url}")
				print(f"Deleting {target_dir} and re-cloning...")
				shutil.rmtree(target_dir)
			else:
				print(f"Repository at {target_dir} already matches {repo_url}")
				return repo
		except GitCommandError:
			print(f"Existing folder at {target_dir} is not a git repo. Replacing...")
			shutil.rmtree(target_dir)

	print(f"Cloning {repo_url} into {target_dir} ...")
	repo = Repo.clone_from(repo_url, target_dir, env={"GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no"})
	print("Clone completed.")
	return repo
	
def cloneRepos(repos: RepoLinks) -> bool:
	try:
		clone_or_update_repo(repos.src, "./repos/src")
		clone_or_update_repo(repos.dst, "./repos/dst")
		return True
	except Exception as e:
		print("Error cloning repos:", e)
		return False
