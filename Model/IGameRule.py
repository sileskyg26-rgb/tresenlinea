from abc import ABC, abstractmethod

class IGameRule(ABC):
    @abstractmethod
    def verify(self, board) -> bool:
        pass

class VictoryVerifier(IGameRule):
    def verify(self, board) -> bool:
        cells = board.get_cells() # Assumes a method to get the 2D grid/matrix of cells
        
        for row in range(3):
            if cells[row][0].simbolo == cells[row][1].simbolo == cells[row][2].simbolo and not cells[row][0].estaVacia():
                return True

        for col in range(3):
            if cells[0][col].simbolo == cells[1][col].simbolo == cells[2][col].simbolo and not cells[0][col].estaVacia():
                return True

        if cells[0][0].simbolo == cells[1][1].simbolo == cells[2][2].simbolo and not cells[0][0].estaVacia():
            return True
            
        if cells[0][2].simbolo == cells[1][1].simbolo == cells[2][0].simbolo and not cells[0][2].estaVacia():
            return True

        return False

class DrawVerifier(IGameRule):
    def verify(self, board) -> bool:
        # A draw occurs if the board is full and there is no winner
        return board.estalleno()