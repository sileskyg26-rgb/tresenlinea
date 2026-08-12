from abc import ABC, abstractmethod

class IGameRule(ABC):
    @abstractmethod
    def verify(self, board) -> bool:
        pass