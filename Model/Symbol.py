class Symbol:
    def __init__(self, value):
        self._value = value

    def __del__(self):
        print("Releasing symbol resources...")

    # --- GETTERS ---
    def get_value(self):
        return self._value

    # --- SETTERS ---
    def set_value(self, value):
        self._value = value

    # --- METHODS ---
    def __str__(self):
        return str(self._value)

    def __eq__(self, other):
        if isinstance(other, Symbol):
            return self._value == other._value
        return self._value == other