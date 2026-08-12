from Model.IGameRule import IGameRule

class DrawVerifier(IGameRule):
    def verify(self, board) -> bool:
        # A draw occurs if the board is full and the victory rule hasn't been met
        return board.estalleno()