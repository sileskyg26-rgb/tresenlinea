from typing import List, Tuple, Optional
import numpy as np

from Model.Symbol import Symbol


class QuantumBoardAnalyzer:
    WIN_LINES: List[List[Tuple[int, int]]] = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]

    def __init__(self, board, my_symbol: Symbol, opponent_symbol: Symbol):
        self._board = board
        self._my_symbol = my_symbol
        self._opp_symbol = opponent_symbol
        self._cells = board.get_cells()

    def evaluate_all_moves(self) -> np.ndarray:
        probs = np.zeros((3, 3), dtype=np.float64)

        for row in range(3):
            for col in range(3):
                if not self._cells[row][col].is_empty():
                    probs[row, col] = -1.0
                    continue

                amplitude = self._evaluate_move_amplitude(row, col)
                entanglement = self._calculate_entanglement(row, col)
                prob = np.abs(amplitude) ** 2 + entanglement * 0.1
                probs[row, col] = max(0.0, prob)

        valid_probs = probs[probs >= 0]
        total = np.sum(valid_probs)
        if total > 0:
            probs = np.where(probs >= 0, probs / total, -1.0)

        return probs

    def _evaluate_move_amplitude(self, row: int, col: int) -> complex:
        amplitude = 0.0 + 0.0j

        for line in self.WIN_LINES:
            if (row, col) not in line:
                continue
            line_amp = self._line_amplitude(line, row, col)
            amplitude += line_amp

        return amplitude

    def _line_amplitude(self, line: List[Tuple[int, int]],
                        move_row: int, move_col: int) -> complex:
        my_count = 0
        opp_count = 0
        empty_count = 0

        for r, c in line:
            if (r, c) == (move_row, move_col):
                my_count += 1
                continue

            sym = self._cells[r][c].get_symbol()
            if sym is None:
                empty_count += 1
            elif sym == self._my_symbol:
                my_count += 1
            else:
                opp_count += 1

        if my_count == 3:
            return 1.0 + 0.0j
        if opp_count == 2 and empty_count == 1 and my_count == 1:
            return 0.8 + 0.0j
        if my_count == 2 and empty_count == 1:
            return 0.0 + 0.6j
        if my_count == 1 and empty_count == 2:
            return 0.3 + 0.2j
        if opp_count == 1 and empty_count == 2:
            return 0.1 + 0.0j
        return 0.0 + 0.0j

    def _calculate_entanglement(self, row: int, col: int) -> float:
        score = 0.0
        cell_lines = [line for line in self.WIN_LINES if (row, col) in line]

        for line in cell_lines:
            for other_line in self.WIN_LINES:
                if other_line == line:
                    continue
                shared = set(line) & set(other_line)
                if shared and (row, col) in shared:
                    score += 0.5

        return score

    def get_winning_line(self, symbol: Symbol) -> Optional[List[Tuple[int, int]]]:
        for line in self.WIN_LINES:
            syms = [self._cells[r][c].get_symbol() for r, c in line]
            if all(s == symbol for s in syms):
                return line
        return None