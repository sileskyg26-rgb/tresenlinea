import random
from Model.IStrategy import IStrategy

class BotStrategy(IStrategy):
    def execute_move(self, player, board):
        cells = board.get_cells()
        empty_cells = []
        
        for row in range(3):
            for col in range(3):
                if cells[row][col].is_empty():
                    empty_cells.append((row, col))
                    
        if empty_cells:
            chosen_row, chosen_col = random.choice(empty_cells)
            print(f"Bot {player.get_name()} ({player.get_symbol()}) chose position: row {chosen_row}, col {chosen_col}")
            return chosen_row, chosen_col
            
        return None