from Model.IGameRule import IGameRule
class DrawVerifier(IGameRule):
    def verify(self, board) -> bool:
        return board.is_full()
