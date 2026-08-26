import numpy as np


class QuantumState:
    STATE_EMPTY = 0
    STATE_X = 1
    STATE_O = 2

    def __init__(self, board_size: int = 3):
        self._board_size = board_size
        self._num_cells = board_size * board_size
        self._amplitudes = np.zeros((self._num_cells, 3), dtype=np.complex128)
        self._initialize_empty()

    def _initialize_empty(self) -> None:
         for i in range(self._num_cells):
            self._amplitudes[i, self.STATE_EMPTY] = 1.0 + 0j

    def get_amplitude(self, cell_idx: int, state: int) -> complex:
         return self._amplitudes[cell_idx, state]

    def set_amplitude(self, cell_idx: int, state: int, value: complex) -> None:
         self._amplitudes[cell_idx, state] = value

    def get_probability(self, cell_idx: int, state: int) -> float:
        amp = self._amplitudes[cell_idx, state]
        return float(np.abs(amp) ** 2)

    def collapse_to_state(self, cell_idx: int, state: int) -> None:
        self._amplitudes[cell_idx] = np.zeros(3, dtype=np.complex128)
        self._amplitudes[cell_idx, state] = 1.0 + 0j

    def apply_phase_shift(self, cell_idx: int, phase: complex) -> None:
        self._amplitudes[cell_idx] *= phase

    def normalize_cell(self, cell_idx: int) -> None:
        probs = np.abs(self._amplitudes[cell_idx]) ** 2
        total = np.sum(probs)
        if total > 0:
            self._amplitudes[cell_idx] /= np.sqrt(total)

    def calculate_entropy(self) -> float:
        entropy = 0.0
        for i in range(self._num_cells):
            probs = np.abs(self._amplitudes[i]) ** 2
            for p in probs:
                if p > 1e-10:
                    entropy -= float(p * np.log2(p))
        return entropy

    def reset(self) -> None:
        self._amplitudes.fill(0j)
        self._initialize_empty()

    def get_metrics(self) -> dict:
        return {
            "entropy": self.calculate_entropy(),
            "num_cells": self._num_cells,
            "total_amplitude_magnitude": float(np.sum(np.abs(self._amplitudes)))
        }