from Model.Player import Player
from Model.HumanStrategy import HumanStrategy
from Model.BotStrategy import BotStrategy
from Controller.GameController import GameController
from View.ConsoleView import ConsoleView


def main():
    view = ConsoleView()

    view.show_title()

    player1 = Player("Jugador 1", "X", HumanStrategy())
    player2 = Player("Jugador 2", "O", BotStrategy())

    game = GameController([player1, player2])
    game.start()

    while True:
        view.show_board(game.get_board())

        state = game.get_game_manager().get_state()

        if state == "VICTORIA":
            winner = game.get_turn_manager().obtenerJugadorActual()
            view.show_message(f"¡Ganó {winner.get_name()}!")
            break

        if state == "EMPATE":
            view.show_message("¡Empate!")
            break

        if state == "FINALIZADO":
            view.show_message("La partida terminó.")
            break

        current_player = game.get_turn_manager().obtenerJugadorActual()
        row, col = view.ask_move(current_player)

        result = game.play_turn(row, col)

        if not result["ok"]:
            view.show_message(result["message"])
            continue

        if result["state"] == "VICTORIA":
            view.show_message(f"¡Ganó {result['winner']}!")
            view.show_board(game.get_board())
            break

        if result["state"] == "EMPATE":
            view.show_message("¡Empate!")
            view.show_board(game.get_board())
            break

    view.show_message("Gracias por jugar.")


if __name__ == "__main__":
    main()