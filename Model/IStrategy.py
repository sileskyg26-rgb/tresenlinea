from abc import ABC, abstractmethod

class IStrategy(ABC):
    @abstractmethod
    def execute_move(self, player, board):
        pass