from enum import Enum

class GameState(Enum):
    IN_PROGRESS = "EN_CURSO"
    VICTORY = "VICTORIA"
    DRAW = "EMPATE"
    FINISHED = "FINALIZADO"