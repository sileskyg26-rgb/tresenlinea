"""QuantumBotStrategy - Quantum-inspired Tic-Tac-Toe bot.

OCP: Extends behavior without modifying existing code.
SRP: Delegates to specialized classes.
ISP: Implements IQuantumStrategy.
DIP: Depends on abstractions.
"""
import random
from typing import List, Tuple, Optional
import numpy as np

from Model.IQuantumStrategy import IQuantumStrategy
from Model.Symbol import Symbol
from Model.QuantumState import QuantumState
from Model.QuantumBoardAnalyzer import QuantumBoardAnalyzer
from Model.QuantumMinimaxEngine import QuantumMinimaxEngine


class QuantumBotStrategy(IQuantumStrategy):
    def __init__(self, difficulty: float = 1.0):
        self._difficulty = max(0.0, min(1.0, difficulty))
        self._quantum_state = QuantumState()
        self._move_history: List[Tuple[int, int]] = []
        self._quantum_noise = 0.05
        self._last_metrics = {}

    def execute_move(self, player, board) -> Optional[Tuple[int, int]]:
        cells = board.get_cells()
        my_symbol = player.get_symbol()
        opponent_symbol = self._detect_opponent_symbol(cells, my_symbol)

        empty_cells = self._get_empty_cells(cells)
        if not empty_cells:
            return None

        if self._difficulty <= 0:
            return random.choice(empty_cells)

        chosen = self._quantum_decision(board, empty_cells, my_symbol, opponent_symbol)

        self._update_state_after_move(chosen[0], chosen[1])
        self._move_history.append(chosen)
        self._last_metrics = self._build_metrics(player, chosen)
        self._log_move(player, chosen)

        return chosen

    def get_quantum_metrics(self) -> dict:
        metrics = self._quantum_state.get_metrics()
        metrics["move_history_length"] = len(self._move_history)
        metrics["difficulty"] = self._difficulty
        metrics.update(self._last_metrics)
        return metrics

    def reset_quantum_state(self) -> None:
        self._quantum_state.reset()
        self._move_history.clear()
        self._last_metrics = {}

    def _quantum_decision(self, board, empty_cells: List[Tuple[int, int]],
                          my_symbol: Symbol, opponent_symbol: Symbol) -> Tuple[int, int]:
        analyzer = QuantumBoardAnalyzer(board, my_symbol, opponent_symbol)
        interference = analyzer.evaluate_all_moves()

        engine = QuantumMinimaxEngine(my_symbol, opponent_symbol)
        best_minimax = engine.find_best_move(board)

        combined = self._combine_scores(empty_cells, interference, best_minimax)

        total = sum(combined.values())
        if total > 0:
            for key in combined:
                combined[key] /= total

        return self._collapse_wavefunction(empty_cells, combined)

    def _combine_scores(self, empty_cells: List[Tuple[int, int]],
                        interference: np.ndarray,
                        best_minimax: Optional[Tuple[int, int]]) -> dict:
        scores = {}

        for row, col in empty_cells:
            q_prob = max(0.0, interference[row, col])
            mm_bonus = 0.5 if best_minimax == (row, col) else 0.0

            combined = (q_prob * 0.4 + mm_bonus * 0.4 +
                       self._quantum_state.get_probability(row * 3 + col, 0) * 0.2)
            combined *= self._difficulty

            noise = random.gauss(0, self._quantum_noise)
            scores[(row, col)] = max(0.0, combined + noise)

        return scores

    def _collapse_wavefunction(self, empty_cells: List[Tuple[int, int]],
                               probabilities: dict) -> Tuple[int, int]:
        if random.random() < self._difficulty * 0.9:
            return max(probabilities, key=probabilities.get)
        else:
            moves = list(probabilities.keys())
            weights = [probabilities[m] for m in moves]
            return random.choices(moves, weights=weights, k=1)[0]

    def _update_state_after_move(self, row: int, col: int) -> None:
        cell_idx = row * 3 + col
        self._quantum_state.collapse_to_state(cell_idx, QuantumState.STATE_X)
        self._entangle_neighbors(row, col)

    def _entangle_neighbors(self, row: int, col: int) -> None:
        neighbors = [
            (row - 1, col), (row + 1, col),
            (row, col - 1), (row, col + 1),
            (row - 1, col - 1), (row - 1, col + 1),
            (row + 1, col - 1), (row + 1, col + 1)
        ]
        for nr, nc in neighbors:
            if 0 <= nr < 3 and 0 <= nc < 3:
                idx = nr * 3 + nc
                self._quantum_state.apply_phase_shift(idx, np.exp(1j * 0.1))

    def _detect_opponent_symbol(self, cells, my_symbol: Symbol) -> Symbol:
        for r in range(3):
            for c in range(3):
                sym = cells[r][c].get_symbol()
                if sym is not None and sym != my_symbol:
                    return sym
        return Symbol("O") if str(my_symbol) == "X" else Symbol("X")

    def _get_empty_cells(self, cells) -> List[Tuple[int, int]]:
        empty = []
        for r in range(3):
            for c in range(3):
                if cells[r][c].is_empty():
                    empty.append((r, c))
        return empty

    def _build_metrics(self, player, chosen: Tuple[int, int]) -> dict:
        return {
            "player": player.get_name(),
            "symbol": str(player.get_symbol()),
            "move": chosen,
            "quantum_entropy": self._quantum_state.calculate_entropy()
        }

    def _log_move(self, player, chosen: Tuple[int, int]) -> None:
        row, col = chosen
        print(f"[QUANTUM] Bot {player.get_name()} ({player.get_symbol()})")
        print(f"[QUANTUM]   Collapsed wavefunction at: row {row}, col {col}")
        print(f"[QUANTUM]   Quantum state entropy: {self._quantum_state.calculate_entropy():.4f}")
        print(f"[QUANTUM]   Move history length: {len(self._move_history)}")