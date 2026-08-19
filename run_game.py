from Controller.GameController import GameController
from Controller.PlayerController import PlayerController
from Model.BotStrategy import BotStrategy


def print_board(cells):
    for row in cells:
        row_symbols = []
        for cell in row:
            # Support both implementations: attribute 'symbol' or internal _symbol/getter
            symbol = None
            if hasattr(cell, 'symbol'):
                symbol = cell.symbol
            elif hasattr(cell, 'get_symbol'):
                symbol = cell.get_symbol()
            elif hasattr(cell, '_symbol'):
                symbol = cell._symbol
            row_symbols.append(symbol if symbol is not None else '.')
        print(' '.join(str(s) for s in row_symbols))
    print()


def main():
    pc = PlayerController()
    p1 = pc.create_player("Bot1", "X", BotStrategy())
    p2 = pc.create_player("Bot2", "O", BotStrategy())

    players = pc.get_players()
    gc = GameController(players)
    game = gc.start()

    print("Starting headless match between two bots...")

    # loop until game ends
    while True:
        result = gc.play_turn()

        if not result.get("ok"):
            print("Turn result:", result)
            break

        print("Board after move:")
        cells = result.get("board")
        print_board(cells)

        state = result.get("state")
        if state in ("VICTORIA", "EMPATE"):
            print("Game finished:", result)
            break


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Error al ejecutar el juego: {e}")
