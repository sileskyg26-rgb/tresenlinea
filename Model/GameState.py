from enum import Enum
class GameState(Enum):
    IN_PROGRESS = "IN_PROGRESS"
    VICTORY = "VICTORY"
    DRAW = "DRAW"
    FINISHED = "FINISHED"