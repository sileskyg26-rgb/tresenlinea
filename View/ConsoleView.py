class ConsoleView:
    def show_title(self):
        print("=== Tres en Línea ===")

    def show_board(self, board):
        cells = board.get_cells()
        print()
        for row in range(3):
            line = " | ".join(
                cell.simbolo if not cell.estaVacia() else " "
                for cell in cells[row]
            )
            print(line)
            if row < 2:
                print("--+---+--")
        print()

    def show_message(self, message):
        print(message)

    def ask_move(self, player):
        while True:
            try:
                row = int(input(f"{player.get_name()} ({player.get_symbol()}), ingresa fila (0-2): "))
                col = int(input(f"{player.get_name()} ({player.get_symbol()}), ingresa columna (0-2): "))
                return row, col
            except ValueError:
                print("Entrada inválida. Debes ingresar números del 0 al 2.")