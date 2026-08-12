from Model.TurnManager import TurnManager

class TurnController:
    def __init__(self, players):
        self._turn_manager = TurnManager(players)

    def current_player(self):
        return self._turn_manager.obtenerJugadorActual()

    def next_turn(self):
        self._turn_manager.siguienteTurno()

    def reset(self):
        self._turn_manager.reiniciar()

    def get_turn_manager(self):
        return self._turn_manager