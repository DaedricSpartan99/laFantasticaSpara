
class GameCall(Exception):
    """Game call raise message"""

class IntCall(GameCall):
    def __init__(self):
        super(IntCall, self).__init__("Interruption request")

class GameError(GameCall):
    pass

# Other kinds of error
