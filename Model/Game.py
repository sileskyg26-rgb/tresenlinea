class Game:
    def __init__(self, game_manager, turn_manager, board, history):
        # Constructor
        self._game_manager = game_manager
        self._turn_manager = turn_manager
        self._board = board
        self._history = history

    def __del__(self):
        # Destructor
        print("Ending the match and releasing game resources...")

    # --- GETTERS ---
    def get_game_manager(self):
        return self._game_manager

    def get_turn_manager(self):
        return self._turn_manager

    def get_board(self):
        return self._board

    def get_history(self):
        return self._history

    # --- SETTERS ---
    def set_game_manager(self, game_manager):
        self._game_manager = game_manager

    def set_turn_manager(self, turn_manager):
        self._turn_manager = turn_manager

    def set_board(self, board):
        self._board = board

    def set_history(self, history):
        self._history = history

    # --- METHODS ---
    def start(self):
        pass

    def execute(self):
        pass

    def finish(self):
        pass