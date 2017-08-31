import traceback

class GameCall(Exception):
    """Game call raise message"""

class IntCall(GameCall):
    def __init__(self):
        super(IntCall, self).__init__("Interruption request")

class GameError(GameCall):
    def __init__(self, error):
	super(GameError, self).__init__("An error occured")
	self.error = error

    def __str__(self):
	return str(self.error)

    def printStackTrace(self):
	traceback.print_exc()

# Other kinds of error
