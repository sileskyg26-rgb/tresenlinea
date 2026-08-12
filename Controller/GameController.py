from Model.Board import Board
from Model.GameManager import GameManager
from Model.Game import Game
from Model.TurnManager import TurnManager
from Model.VictoryVerifier import VictoryVerifier
from Model.DrawVerifier import DrawVerifier

class GameController:
    def __init__(self, players):
        self._board = Board()
        self._game_manager = GameManager("EN_CURSO", None, None)
        self._turn_manager = TurnManager(players)
        self._game = Game(self._game_manager, self._turn_manager, self._board, None)

        # Se asignan las reglas reales del juego
        self._game_manager.set_victory_rule(VictoryVerifier())
        self._game_manager.set_draw_rule(DrawVerifier())

    def start(self):
        self._board.reset()
        self._turn_manager.reiniciar()
        self._game_manager.start_match()
        return self._game

    def play_turn(self):
        player = self._turn_manager.obtenerJugadorActual()

        # Obtener movimiento desde la estrategia
        strategy = player.get_strategy()
        if hasattr(strategy, "execute_move"):
            move = strategy.execute_move(player, self._board)
        elif hasattr(strategy, "ejecutarMovimiento"):
            move = strategy.ejecutarMovimiento(player, self._board)
        else:
            raise AttributeError("La estrategia no define un movimiento válido.")

        if move is None:
            return {"ok": False, "message": "No hay movimientos disponibles."}

        row, col = move

        # Validar y ubicar ficha
        if self._board.place_symbol(row, col, player.get_symbol()):
            self._game_manager.update_state(self._board)

            # Estado final
            if self._game_manager.get_state() == "VICTORIA":
                return {
                    "ok": True,
                    "winner": player.get_name(),
                    "state": "VICTORIA",
                    "board": self._board.get_cells()
                }

            if self._game_manager.get_state() == "EMPATE":
                return {
                    "ok": True,
                    "winner": None,
                    "state": "EMPATE",
                    "board": self._board.get_cells()
                }

            # Si sigue en curso, cambia de turno
            self._turn_manager.siguienteTurno()
            return {
                "ok": True,
                "winner": None,
                "state": "EN_CURSO",
                "board": self._board.get_cells()
            }

        return {"ok": False, "message": "Movimiento inválido."}

    def get_board(self):
        return self._board

    def get_game_manager(self):
        return self._game_manager

    def get_turn_manager(self):
        return self._turn_manager