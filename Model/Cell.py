from Model.Symbol import Symbol

class Cell:
    def __init__(self, symbol=None):
        self._symbol = symbol

    def __del__(self):
        print("Releasing cell resources...")

    # --- GETTERS ---
    def get_symbol(self):
        return self._symbol

    # Spanish alias for getter
    def obtenerSimbolo(self):
        return self._symbol

    # --- SETTERS ---
    def set_symbol(self, symbol):
        self._symbol = symbol

    # Spanish alias for setter
    def set_simbolo(self, symbol):
        self._symbol = symbol

    # Provide attribute-style access for 'symbol' and 'simbolo'
    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value):
        self._symbol = value

    @property
    def simbolo(self):
        return self._symbol

    @simbolo.setter
    def simbolo(self, value):
        self._symbol = value

    # --- METHODS ---
    def is_empty(self) -> bool:
        return self._symbol is None

    # Spanish alias for is_empty
    def estaVacia(self) -> bool:
        return self.is_empty()

    def clear(self):
        self._symbol = None

    # Spanish alias for clear
    def limpiar(self):
        self.clear()