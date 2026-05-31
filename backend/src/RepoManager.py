import os
from threading import Thread
from typing import Optional, List
from .models import Slot, RepoLinks
from .data import getCalendar, getLinks
from .errors import BackendError
from .logs import logInfo
from .Synchronizer import Synchronizer
from .Repositiry import Repository

os.environ["SSH_AUTH_SOCK"] = "/ssh-agent"

class _RepoManager:
	def __init__(self):
		self.synchronizer: Optional[Synchronizer] = None
		self.src: Optional[Repository] = None
		self.dst: Optional[Repository] = None

	def _validate(self):
		src_has = self.src.has_any_commits()
		dst_has = self.dst.has_any_commits()

		if not dst_has:
			return

		if not src_has and dst_has:
			raise BackendError("Repositories are different projects.")

		src_root_message = self.src.get_root_commit().message
		dst_root_message = self.dst.get_root_commit().message

		if src_root_message == dst_root_message:
			return

		raise BackendError("Repositories are different projects.")

	def _setup_and_run(self):
		try:
			repos = getLinks()

			logInfo("Setting up source repository...")
			self.src = Repository(repos.src, "./repos/src")
			logInfo("Setting up destination repository...")
			self.dst = Repository(repos.dst, "./repos/dst")
			self._validate()
			logInfo("Valid configuration verified, starting synchronizer loop.")
			self.synchronizer = Synchronizer(src_repo=self.src, dst_repo=self.dst)

			self.synchronizer.synchronise()
			
		except BackendError as be:
			logInfo(f"[ERROR] Configuration verification failed: {str(be)}")
		except Exception as e:
			logInfo(f"[ERROR] Target workspace activation crashed: {str(e)}")

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
		if self.synchronizer and self.synchronizer.isActive():
			logInfo("Synchronization is already running.")
			return

		calendar: List[Slot] = getCalendar()
		if len(calendar) == 0:
			raise BackendError(f"No slot in the given calendar")

		worker = Thread(target=self._setup_and_run, daemon=True)
		worker.start()

	def stop(self):
		"""
		Signal the loop to stop and wait for clean exit.
		"""
		if self.synchronizer:
			self.synchronizer.stop()
		logInfo("Synchronisation loop requested to stop.")

	def isEnabled(self) -> bool:
		if self.synchronizer:
			return self.synchronizer.isActive()
		return False

repoManager = _RepoManager()
del _RepoManager
