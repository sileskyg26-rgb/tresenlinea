from typing import List, Tuple, Optional
import numpy as np

from Model.Symbol import Symbol
from Model.Board import Board
from Model.QuantumBot.QuantumBoardAnalyzer import QuantumBoardAnalyzer


class QuantumMinimaxEngine:
    MAX_DEPTH = 6
    WIN_SCORE = 10.0
    LOSE_SCORE = -10.0

    def __init__(self, my_symbol: Symbol, opponent_symbol: Symbol):
        self._my_symbol = my_symbol
        self._opp_symbol = opponent_symbol

    def evaluate(self, board: Board) -> complex:
        winner = self._check_winner(board)
        if winner == self._my_symbol:
            return self.WIN_SCORE + 0.0j
        if winner == self._opp_symbol:
            return self.LOSE_SCORE + 0.0j
        if board.is_full():
            return 0.0 + 0.0j

        analyzer = QuantumBoardAnalyzer(board, self._my_symbol, self._opp_symbol)
        probs = analyzer.evaluate_all_moves()

        real_score = (probs[1, 1] * 0.4 +
                     (probs[0, 0] + probs[0, 2] + probs[2, 0] + probs[2, 2]) * 0.15)

        imag_score = analyzer._calculate_entanglement(1, 1) * 0.3

        return complex(real_score, imag_score)

    def search(self, board: Board, depth: int = 0,
               is_maximizing: bool = True,
               alpha: complex = -1e9 + 0j,
               beta: complex = 1e9 + 0j) -> complex:

        winner = self._check_winner(board)
        if winner == self._my_symbol:
            return (self.WIN_SCORE - depth) + 0.0j
        if winner == self._opp_symbol:
            return (self.LOSE_SCORE + depth) + 0.0j
        if board.is_full() or depth >= self.MAX_DEPTH:
            return self.evaluate(board)

        empty_cells = self._get_empty_cells(board)
        if not empty_cells:
            return 0.0 + 0.0j

        if is_maximizing:
            max_eval = -1e9 + 0.0j
            for move in empty_cells:
                new_board = self._simulate_move(board, move, self._my_symbol)
                eval_val = self.search(new_board, depth + 1, False, alpha, beta)
                phase = self._move_phase(move)
                eval_val *= phase
                max_eval = self._quantum_max(max_eval, eval_val)
                alpha = self._quantum_max(alpha, eval_val)
                if self._quantum_greater(beta, alpha):
                    break
            return max_eval
        else:
            min_eval = 1e9 + 0.0j
            for move in empty_cells:
                new_board = self._simulate_move(board, move, self._opp_symbol)
                eval_val = self.search(new_board, depth + 1, True, alpha, beta)
                phase = self._move_phase(move)
                eval_val *= phase
                min_eval = self._quantum_min(min_eval, eval_val)
                beta = self._quantum_min(beta, eval_val)
                if self._quantum_greater(alpha, beta):
                    break
            return min_eval

    def find_best_move(self, board: Board) -> Optional[Tuple[int, int]]:
        empty_cells = self._get_empty_cells(board)
        if not empty_cells:
            return None

        best_move = empty_cells[0]
        best_score = -1e9 + 0.0j

        for move in empty_cells:
            new_board = self._simulate_move(board, move, self._my_symbol)
            score = self.search(new_board, depth=1, is_maximizing=False)
            if self._quantum_greater(score, best_score):
                best_score = score
                best_move = move

        return best_move

    def _check_winner(self, board: Board) -> Optional[Symbol]:
        cells = board.get_cells()
        lines = [
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)],
        ]
        for line in lines:
            syms = [cells[r][c].get_symbol() for r, c in line]
            if syms[0] is not None and syms[0] == syms[1] == syms[2]:
                return syms[0]
        return None

    def _get_empty_cells(self, board: Board) -> List[Tuple[int, int]]:
        cells = board.get_cells()
        empty = []
        for r in range(3):
            for c in range(3):
                if cells[r][c].is_empty():
                    empty.append((r, c))
        return empty

    def _simulate_move(self, board: Board, move: Tuple[int, int],
                       symbol: Symbol) -> Board:
        new_board = Board()
        orig_cells = board.get_cells()
        new_cells = new_board.get_cells()

        for r in range(3):
            for c in range(3):
                sym = orig_cells[r][c].get_symbol()
                if sym is not None:
                    new_cells[r][c].set_symbol(sym)

        new_board.place_symbol(move[0], move[1], symbol)
        return new_board

    def _move_phase(self, move: Tuple[int, int]) -> complex:
        row, col = move
        if row == 1 and col == 1:
            return np.exp(1j * np.pi / 4)
        if row in [0, 2] and col in [0, 2]:
            return np.exp(1j * np.pi / 6)
        return np.exp(-1j * np.pi / 8)

    def _quantum_max(self, a: complex, b: complex) -> complex:
        return a if np.abs(a) >= np.abs(b) else b

    def _quantum_min(self, a: complex, b: complex) -> complex:
        return a if np.abs(a) <= np.abs(b) else b

    def _quantum_greater(self, a: complex, b: complex) -> bool:
        return np.abs(a) > np.abs(b)