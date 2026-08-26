from Model.IGameRule import IGameRule

class VictoryVerifier(IGameRule):
    def verify(self, board) -> bool:
        cells = board.get_cells()
        
        for row in range(3):
            if (cells[row][0].symbol == cells[row][1].symbol == cells[row][2].symbol 
                and not cells[row][0].is_empty()):
                return True

        for col in range(3):
            if (cells[0][col].symbol == cells[1][col].symbol == cells[2][col].symbol 
                and not cells[0][col].is_empty()):
                return True

        if (cells[0][0].symbol == cells[1][1].symbol == cells[2][2].symbol 
            and not cells[0][0].is_empty()):
            return True
            
        if (cells[0][2].symbol == cells[1][1].symbol == cells[2][0].symbol 
            and not cells[0][2].is_empty()):
            return True

        return False