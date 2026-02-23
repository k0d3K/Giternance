
class Synchronizer:
	def __init__(self):
		self.active: bool = False

	def synchronise(self):
		pass

	def stop(self):
		pass

	def isActive(self) -> bool:
		return self.active
