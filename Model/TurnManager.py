class TurnManager:
    # Constructor
    def __init__(self, players):
        self._players = players
        self._current_turn = 0

    # Destructor
    def __del__(self):
        print("Releasing turn manager resources...")

    # --- GETTERS ---
    def get_players(self):
        return self._players

    def get_current_turn(self):
        return self._current_turn

    def get_current_player(self):
        return self._players[self._current_turn]

    # --- SETTERS ---
    def set_players(self, players):
        self._players = players

    def set_current_turn(self, current_turn):
        self._current_turn = current_turn

    # --- METHODS ---
    def next_turn(self):
        self._current_turn = (self._current_turn + 1) % len(self._players)

    def reset(self):
        self._current_turn = 0
        print("Turns have been reset.")