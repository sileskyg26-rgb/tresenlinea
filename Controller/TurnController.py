from Model.TurnManager import TurnManager

class TurnController:
    def __init__(self, players):
        self._turn_manager = TurnManager(players)

    def current_player(self):
        return self._turn_manager.get_current_player()

    def next_turn(self):
        self._turn_manager.next_turn()

    def reset(self):
        self._turn_manager.reset()

    def get_turn_manager(self):
        return self._turn_manager