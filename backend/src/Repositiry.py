import os
import shutil
from git import Repo, GitCommandError
from .errors import BackendError
from .logs import logInfo

SSH_CMD = "ssh -o StrictHostKeyChecking=no"

class Repository:
	def __init__(self, repo_url: str, target_dir: str):
		self.target_dir = target_dir
		self.repo: Repo = self._clone_or_update_repo(repo_url, target_dir)

	def _clone_or_update_repo(self, repo_url: str, target_dir: str):
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
		repo = Repo.clone_from(repo_url, target_dir, env={"GIT_SSH_COMMAND": SSH_CMD})
		logInfo("Clone completed.")
		return repo

	def update_from_remote(self):
		try:
			with self.repo.git.custom_environment(
				SSH_AUTH_SOCK="/ssh-agent",
				GIT_SSH_COMMAND=SSH_CMD
			):
				self.repo.remotes.origin.fetch(prune=True)
				
		except Exception as e:
			logInfo(f"Error updating repository from remote: {str(e)}")

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
	
	def get_all_branches(self):
		'''
		Find all branches of the repo
		'''
		if not self.repo:
			return
		self.repo.remotes.origin
		local_branches = [branch.name for branch in self.repo.heads]
		return local_branches

	def get_root_commit(self):
		return list(self.repo.iter_commits("HEAD", reverse=True))[0]

	def get_commits_from_branch(self, branch: str = "origin/main"):
		"""
		Get all commits from a specific branch in chronological order (oldest first).
		Returns list of commit objects.
		Returns empty list if branch doesn't exist.
		"""
		try:
			target_ref = None
			for ref in self.repo.remotes.origin.refs:
				if ref.name.endswith(branch):
					target_ref = ref
					break
			
			if not target_ref:
				logInfo(f"Branch {branch} not found in remote. Repository might be empty {self.repo.remotes.origin.refs}.")
				return []
			
			commits = list(self.repo.iter_commits(branch))
			return commits[::-1]
		except Exception as e:
			logInfo(f"Error fetching commits from {branch}: {str(e)}")
			return []

	def cherry_pick_commit_with_new_time(self, commit_sha: str, new_timestamp: int, src_dir: str):
		"""
		Cherry-pick a commit from source repo and rewrite its timestamp.
		Preserves original author and committer identity per commit.
		new_timestamp: Unix timestamp in seconds
		Returns: hexsha of the new commit
		"""
		try:
			abs_src_dir = os.path.abspath(src_dir)
			if "local_src" not in [r.name for r in self.repo.remotes]:
				self.repo.create_remote("local_src", abs_src_dir)
			else:
				self.repo.git.remote("set-url", "local_src", abs_src_dir)

			self.repo.remotes.local_src.fetch()

			src_commit = self.repo.commit(commit_sha)
			author_name = src_commit.author.name
			author_email = src_commit.author.email
			committer_name = src_commit.committer.name
			committer_email = src_commit.committer.email
			formatted_date = f"@{new_timestamp}"

			with self.repo.git.custom_environment(
				GIT_AUTHOR_NAME=author_name,
				GIT_AUTHOR_EMAIL=author_email,
				GIT_COMMITTER_NAME=committer_name,
				GIT_COMMITTER_EMAIL=committer_email,
				GIT_AUTHOR_DATE=formatted_date,
				GIT_COMMITTER_DATE=formatted_date,
			):
				self.repo.git.cherry_pick(commit_sha, "--allow-empty", "--keep-redundant-commits")

			return self.repo.head.commit.hexsha
		except Exception as e:
			logInfo(f"Error cherry-picking commit {commit_sha}: {str(e)}")
			raise
