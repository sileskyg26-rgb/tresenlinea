class Move:
    def __init__(self, player, row, col):
        self._player = player
        self._row = row
        self._col = col

    def __del__(self):
        print("Releasing move resources...")

    # --- GETTERS ---
    def get_player(self):
        return self._player

    def get_row(self):
        return self._row

    def get_col(self):
        return self._col

    # --- SETTERS ---
    def set_player(self, player):
        self._player = player

    def set_row(self, row):
        self._row = row

    def set_col(self, col):
        self._col = col