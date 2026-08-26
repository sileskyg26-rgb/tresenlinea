from abc import ABC, abstractmethod

from Model.IStrategy import IStrategy


class IQuantumStrategy(IStrategy, ABC):
    @abstractmethod
    def get_quantum_metrics(self) -> dict:
         pass

    @abstractmethod
    def reset_quantum_state(self) -> None:
        pass