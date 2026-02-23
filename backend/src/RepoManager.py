import os
from typing import Optional
from typing import List
from .models import Slot, RepoLinks
from .data import getCalendar, getLinks
from .errors import BackendError
from .logs import logInfo
from .Synchronizer import Synchronizer
from .Reposotiry import Repository

import os
os.environ["SSH_AUTH_SOCK"] = "/ssh-agent"

class _RepoManager:
	def __init__(self):
		self.synchs: List[Synchronizer] = []
		self.src: Optional[Repository] = None
		self.dst: Optional[Repository] = None

	def __validate(self):
		src_has = self.src.has_any_commits()
		dst_has = self.dst.has_any_commits()

		if not dst_has:
			return

		if not src_has and dst_has:
			raise BackendError("Repositories are different projects.")

		src_roots = self.src.get_all_commits()
		dst_roots = self.dst.get_all_commits()

		if src_roots.intersection(dst_roots):
			return

		raise BackendError("Repositories are different projects.")

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
		self.src = Repository(repos.src, "./repos/src")
		self.dst = Repository(repos.dst, "./repos/dst")
		self.__validate()
		logInfo("Valid configuration, initiating synchronisation")

	def stop(self):
		self.active_connection = None

	def isEnabled(self) -> bool:
		return self.active

repoManager = _RepoManager()
del _RepoManager
