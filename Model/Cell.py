from Model.Symbol import Symbol

class Cell:
    def __init__(self, symbol=None):
        self._symbol = symbol

    def __del__(self):
        print("Releasing cell resources...")

    # --- GETTERS ---
    def get_symbol(self):
        return self._symbol

    # --- SETTERS ---
    def set_symbol(self, symbol):
        self._symbol = symbol

    # --- METHODS ---
    def is_empty(self) -> bool:
        return self._symbol is None

    def clear(self):
        self._symbol = None