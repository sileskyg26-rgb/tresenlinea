from Model.Player import Player
from View.ConsoleView import ConsoleView
from controller.GameController import GameController
from Model.HumanStrategy import HumanStrategy
from Model.BotStrategy import BotStrategy

class GameApp:
    def __init__(self):
        self.view = ConsoleView()

    def run(self):
        self.view.show_title()

        # Crear jugadores
        player1 = Player("Ana", "X", HumanStrategy())
        player2 = Player("Bot", "O", BotStrategy())

        game_controller = GameController([player1, player2])
        game_controller.start()

        while True:
            board = game_controller.get_board()
            self.view.show_board(board)

            state = game_controller.get_game_manager().get_state()
            if state in ["VICTORIA", "EMPATE", "FINALIZADO"]:
                break

            current_player = game_controller.get_turn_manager().obtenerJugadorActual()
            row, col = self.view.ask_move(current_player)

            result = game_controller.play_turn(row, col)

            if not result["ok"]:
                self.view.show_message(result["message"])
                continue

            self.view.show_message(f"Estado: {result['state']}")

        self.view.show_board(game_controller.get_board())
        if game_controller.get_game_manager().get_state() == "VICTORIA":
            self.view.show_message("¡Ganó un jugador!")
        else:
            self.view.show_message("¡Empate!")