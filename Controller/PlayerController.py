from Model.Player import Player

class PlayerController:
    def __init__(self):
        self._players = []

    def create_player(self, name, symbol, strategy):
        player = Player(name, symbol, strategy)
        self._players.append(player)
        return player

    def get_players(self):
        return self._players

    def request_move(self, player, board):
        strategy = player.get_strategy()

        # Soporta ambos nombres para que funcione con tu proyecto
        if hasattr(strategy, "execute_move"):
            return strategy.execute_move(player, board)
        if hasattr(strategy, "ejecutarMovimiento"):
            return strategy.ejecutarMovimiento(player, board)

        raise AttributeError("La estrategia no tiene un método de movimiento válido.")