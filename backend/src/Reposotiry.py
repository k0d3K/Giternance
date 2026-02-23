import os
import shutil
from git import Repo, GitCommandError
from .errors import BackendError
from .logs import logInfo

class Repository:
	def __init__(self, repo_url: str, target_dir: str):
		self.repo: Repo = self.__clone_or_update_repo(repo_url, target_dir)

	def __clone_or_update_repo(sefl, repo_url: str, target_dir: str):
		"""
		Clone a Git repo if missing, or check if the existing repo matches the URL.
		"""
		if os.path.exists(target_dir) and os.path.isdir(target_dir):
			try:
				repo = Repo(target_dir)
				origin = repo.remotes.origin
				origin_url = origin.url
				if origin_url != repo_url:
					logInfo(f"Remote URL mismatch for {target_dir}: {origin_url} != {repo_url}")
					logInfo(f"Deleting {target_dir} and re-cloning...")
					shutil.rmtree(target_dir)
				else:
					logInfo(f"Repository at {target_dir} already matches {repo_url}")
					logInfo("Pulling latest changes...")
					origin.pull()
					logInfo("Pull completed.")
					return repo
			except GitCommandError:
				logInfo(f"Existing folder at {target_dir} is not a git repo. Replacing...")
				shutil.rmtree(target_dir)

		logInfo(f"Cloning {repo_url} into {target_dir} ...")
		repo = Repo.clone_from(repo_url, target_dir, env={"GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=no"})
		logInfo("Clone completed.")
		return repo

	def has_any_commits(self):
		return len(list(self.repo.refs)) > 0

	def get_all_commits(self):
		roots = set()

		for ref in self.repo.refs:
			try:
				for commit in self.repo.iter_commits(ref, max_parents=0):
					roots.add(commit.hexsha)
			except Exception:
				continue

		return roots
