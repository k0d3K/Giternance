import os
import shutil
from git import Repo, GitCommandError
from typing import List
from .models import Slot, RepoLinks
from .data import getCalendar, getLinks
from .errors import BackendError
from .logs import logInfo

import os
os.environ["SSH_AUTH_SOCK"] = "/ssh-agent"

class _Synchronizer:
	def __init__(self):
		self.active: bool = False

	def start(self):
		"""
		Resume
		----------
		Start syncrhonisation from local files configuration
		
		Raises
		----------
			BackendError: If a misconfiguration happens.
			OtherError: If something unexpected happens.
		"""
		calendar: List[Slot] = getCalendar()
		if len(calendar) == 0:
			raise BackendError(f"No slot in the given calendar")
		repos: RepoLinks = getLinks()
		clone_or_update_repo(repos.src, "./repos/src")
		clone_or_update_repo(repos.dst, "./repos/dst")

	def stop(self):
		self.active_connection = None

	def isEnabled(self) -> bool:
		return self.active

synchronizer = _Synchronizer()
del _Synchronizer

def clone_or_update_repo(repo_url: str, target_dir: str):
	"""
	Clone a Git repo if missing, or check if the existing repo matches the URL.
	"""
	if os.path.exists(target_dir) and os.path.isdir(target_dir):
		try:
			repo = Repo(target_dir)
			origin_url = next((r.url for r in repo.remotes), None)
			if origin_url != repo_url:
				logInfo(f"Remote URL mismatch for {target_dir}: {origin_url} != {repo_url}")
				logInfo(f"Deleting {target_dir} and re-cloning...")
				shutil.rmtree(target_dir)
			else:
				logInfo(f"Repository at {target_dir} already matches {repo_url}")
				return repo
		except GitCommandError:
			logInfo(f"Existing folder at {target_dir} is not a git repo. Replacing...")
			shutil.rmtree(target_dir)

	logInfo(f"Cloning {repo_url} into {target_dir} ...")
	repo = Repo.clone_from(repo_url, target_dir, env={"GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no"})
	logInfo("Clone completed.")
	return repo
