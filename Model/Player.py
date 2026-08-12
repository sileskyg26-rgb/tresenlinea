class Player:
    def __init__(self, name, symbol, strategy):
        self._name = name
        self._symbol = symbol
        self._strategy = strategy

    def __del__(self):
        print("Releasing player resources...")

    # --- GETTERS ---
    def get_name(self):
        return self._name

    def get_symbol(self):
        return self._symbol

    def get_strategy(self):
        return self._strategy

    # --- SETTERS ---
    def set_name(self, name):
        self._name = name

    def set_symbol(self, symbol):
        self._symbol = symbol

    def set_strategy(self, strategy):
        self._strategy = strategy

    # --- METHODS ---
    def hacerMovimiento(self, board):
        return self._strategy.ejecutarMovimiento(self, board)

    def obtenerSimbolo(self):
        return self._symbol

    def obtenerEstrategia(self):
        return self._strategy