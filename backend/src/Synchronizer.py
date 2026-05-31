import asyncio
import json
import time
from pathlib import Path
import random
from .logs import logInfo
from .Repositiry import Repository

class Synchronizer:
	def __init__(self, src_repo: Repository, dst_repo: Repository, state_path: str = "./logs/sync_state.json"):
		self.active: bool = False
		self.src: Repository = src_repo
		self.dst: Repository = dst_repo
		self.state_path = Path(state_path)
		self.modification_stack = []

	def _load_last_sync_sha(self) -> str:
		if self.state_path.exists():
			try:
				with open(self.state_path, "r") as f:
					data = json.load(f)
					return data.get("last_source_sha", "")
			except Exception as e:
				logInfo(f"Error reading state file: {str(e)}")
		return ""

	def _save_sync_state(self, source_sha: str):
		"""Save the last successfully synchronized source SHA to disk inside the logs volume."""
		try:
			self.state_path.parent.mkdir(parents=True, exist_ok=True)
			with open(self.state_path, "w") as f:
				json.dump({"last_source_sha": source_sha}, f, indent=4)
			logInfo(f"Saved tracking state to disk: {source_sha}")
		except Exception as e:
			logInfo(f"Error writing state file: {str(e)}")

	def _get_commit_stats(self, commit_sha: str) -> tuple[int, int, int]:
		try:
			commit = self.src.repo.commit(commit_sha)
			stats = commit.stats.total
			return stats['files'], stats['insertions'], stats['deletions']
		except Exception as e:
			logInfo(f"Error reading stats for commit {commit_sha}: {str(e)}")
			return 1, 1, 0

	def _estimate_human_effort_seconds(self, files_changed: int, lines_added: int, lines_deleted: int) -> int:
		base_context_switch_seconds = 60  # add in advanced settings
		time_per_added_line_seconds = 12
		time_per_deleted_line_seconds = 4

		total_seconds = (
			(files_changed * base_context_switch_seconds) +
			(lines_added * time_per_added_line_seconds) +
			(lines_deleted * time_per_deleted_line_seconds)
		)

		if total_seconds < 90:  # add in advanced settings
			total_seconds = random.randint(90, 300)

		variance_factor = random.uniform(0.85, 1.15)
		final_estimated_seconds = int(total_seconds * variance_factor)

		return final_estimated_seconds

	def _setup_missing_commits(self) -> list[dict]:
		"""
		Analyze histories and schedule target human timestamps.
		"""
		logInfo("Analyzing histories to setup missing commits...")
		src_commits = self.src.get_commits_from_branch("origin/main")
		dst_commit_shas = self.dst.get_all_commits()
		# dst_commits = self.dst.get_commits_from_branch("origin/main")

		if not src_commits:
			logInfo("Source repository has no commits.")
			return []

		last_sync_sha = self._load_last_sync_sha()
		missing_src_commits = []
		if last_sync_sha:
			found_marker = False
			for c in src_commits:
				if found_marker:
					missing_src_commits.append(c)
				elif c.hexsha == last_sync_sha:
					found_marker = True
			
			if not found_marker:
				logInfo("Saved sync marker missing from source. Falling back to history length comparison.")
				missing_src_commits = [c for c in src_commits if c.hexsha not in dst_commit_shas]
		else:
			missing_src_commits = [c for c in src_commits if c.hexsha not in dst_commit_shas]

		if not missing_src_commits:
			logInfo("No missing commits found. Everything is synchronized.")
			return []

		dst_commits = self.dst.get_commits_from_branch("origin/main")
		if dst_commits:
			last_dst_timestamp = dst_commits[-1].committed_date
		else:
			last_dst_timestamp = missing_src_commits[0].committed_date - 3600

		timeline_stack = []
		current_timeline_pointer = max(last_dst_timestamp, int(time.time()))

		for commit in missing_src_commits:
			files, added, deleted = self._get_commit_stats(commit.hexsha)
			effort_seconds = self._estimate_human_effort_seconds(files, added, deleted)

			target_timestamp = current_timeline_pointer + effort_seconds

			timeline_stack.append({
				"src_sha": commit.hexsha,
				"target_timestamp": target_timestamp,
				"effort_seconds": effort_seconds
			})

			current_timeline_pointer = target_timestamp

		logInfo(f"Successfully staged {len(timeline_stack)} commits into the modification stack.")
		return timeline_stack

	def _sync_single_commit(self, job: dict):
		logInfo(f"Target timestamp met for commit {job['src_sha']}. Executing sync...")

		src_commit = self.src.repo.commit(job["src_sha"])

		# Clean working tree — handle empty repo (no HEAD yet)
		try:
			self.dst.repo.git.reset("--hard", "HEAD")
			logInfo("Destination working tree reset to clean state.")
		except Exception:
			# No commits yet — just remove untracked files
			logInfo("No HEAD found (empty repo), cleaning untracked files only.")
			try:
				self.dst.repo.git.clean("-fd")
			except Exception as e:
				logInfo(f"Warning: could not clean destination repo: {str(e)}")

		new_dst_sha = self.dst.cherry_pick_commit_with_new_time(
			commit_sha=job["src_sha"],
			new_timestamp=job["target_timestamp"],
			src_dir=self.src.target_dir,
		)

		logInfo(f"Successfully applied commit to destination workspace. New SHA: {new_dst_sha}")

		self.dst.repo.remotes.origin.push()
		logInfo("Changes successfully pushed to destination remote repository.")

		self._save_sync_state(job["src_sha"])

	def synchronise(self):
		"""
		Asynchronous, infinite execution loop. Consumes the modification stack.
		"""
		self.active = True
		logInfo("Entering live asynchronous synchronization execution loop.")

		while self.active:
			if not self.modification_stack:
				logInfo("Modification stack is empty. Fetching remote updates to check for new commits...")
				try:
					# with self.src.repo.git.custom_environment(SSH_AUTH_SOCK="/ssh-agent"):
					self.src.update_from_remote()
					
					# with self.dst.repo.git.custom_environment(SSH_AUTH_SOCK="/ssh-agent"):
					self.dst.update_from_remote()
					
					self.modification_stack = self._setup_missing_commits()
				except Exception as e:
					logInfo(f"Error checking for new commits: {str(e)}")

				# Check if still empty, if so sleep safely and loop back to the top
				if not self.modification_stack:
					logInfo("No new commits found upstream. Sleeping for 60 seconds before next check...")
					for _ in range(12):
						if not self.active:
							break
						time.sleep(5)
					continue 

			current_time = int(time.time())
			next_job = self.modification_stack[0]
			
			if current_time >= next_job["target_timestamp"]:
				try:
					# with self.dst.repo.git.custom_environment(SSH_AUTH_SOCK="/ssh-agent"):
					self._sync_single_commit(next_job)
					self.modification_stack.pop(0)
				except Exception as e:
					logInfo(f"Critical error processing commit {next_job['src_sha']}: {str(e)}")
					logInfo("Retrying this commit in 10 seconds...")
					time.sleep(10)
			else:
				seconds_remaining = next_job["target_timestamp"] - current_time
				logInfo(f"Commit {next_job['src_sha']} queued. Simulating human delay: {seconds_remaining}s remaining.")
				
				sleep_chunk = min(seconds_remaining, 5)
				time.sleep(sleep_chunk)

		logInfo("Synchronization loop exited cleanly.")

	def stop(self):
		self.active = False
		logInfo("Synchronization process stopped.")

	def isActive(self) -> bool:
		return self.active
