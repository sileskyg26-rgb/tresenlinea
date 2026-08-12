from Model.Cell import Cell


class Board:
    def __init__(self):
         self._cells = [[Cell() for _ in range(3)] for _ in range(3)]

    def __del__(self):
        print("Releasing board resources...")

    # --- GETTERS ---
    def get_cells(self):
        return self._cells

    # --- SETTERS ---
    def set_cells(self, cells):
        self._cells = cells

    # --- METHODS ---
    def is_full(self) -> bool:
        for row in range(3):
            for col in range(3):
                if self._cells[row][col].is_empty():
                    return False
        return True

    def place_symbol(self, row, col, symbol):
        if 0 <= row < 3 and 0 <= col < 3:
            if self._cells[row][col].is_empty():
                self._cells[row][col].symbol = symbol
                return True
        return False

    def reset(self):
        for row in range(3):
            for col in range(3):
                self._cells[row][col].clear()