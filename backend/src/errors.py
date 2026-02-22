from .logs import logError

class BackendError(Exception):
	def __init__(self, msg: str):
		super().__init__(msg)
		logError(msg)

def logException(e: Exception, context: str = ""):
	msg = f"{context}: {str(e)}" if context else str(e)
	logError(msg)
