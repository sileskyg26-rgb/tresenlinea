from Model.IStrategy import IStrategy

class HumanStrategy(IStrategy):
    def execute_move(self, player, board):
        # Human strategy logic, typically requesting row and column via input
        try:
            row = int(input(f"Player {player.get_name()} ({player.get_symbol()}), enter row (0-2): "))
            col = int(input(f"Player {player.get_name()} ({player.get_symbol()}), enter column (0-2): "))
            return row, col
        except ValueError:
            print("Invalid input. Please enter numbers between 0 and 2.")
            return self.execute_move(player, board)