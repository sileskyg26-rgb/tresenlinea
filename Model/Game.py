class Game:
    # --- Constructor ---
    def __init__(self, game_manager, turn_manager, board, history):
        self._game_manager = game_manager
        self._turn_manager = turn_manager
        self._board = board
        self._history = history

    # --- Destructor ---
    def __del__(self):
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
        if hasattr(self._board, 'reset'):
            self._board.reset()

        if self._history is not None and hasattr(self._history, 'clear_history'):
            self._history.clear_history()

        self._game_manager.start_match()
        print("Welcome to Tic-Tac-Toe!")

    def execute(self):
        self.start()

        while self._game_manager.get_state() == "IN_PROGRESS":
            print(self._board)

            current_player = self._turn_manager.get_current_player()
            player_name = current_player.get_name()
            player_symbol = current_player.get_symbol()

            print(f"Turn of player: {player_name} ({player_symbol})")

            try:
                strategy = current_player.get_strategy()
                movement = strategy.execute_move(current_player, self._board)

                if movement is None:
                    print('No movement returned by strategy')
                else:
                    row, col = movement
                    valid = self._board.place_symbol(row, col, player_symbol)

                    if valid:
                        if self._history is not None:
                            self._history.add_match(movement)

                        if self._game_manager.update_state(self._board):
                            break

                        self._turn_manager.next_turn()
                    else:
                        print("Invalid movement. The cell is already occupied or out of bounds.")
            except Exception as e:
                print(f"Error during movement: {e}")

        print(self._board)
        self.finish()

    def finish(self):
        state = self._game_manager.get_state()
        if state == "WIN":
            current_player = self._turn_manager.get_current_player()
            name = current_player.get_name()
            print(f"The game is over! Winner: {name}")
        elif state == "DRAW":
            print("The game ended in a draw!")

        self._game_manager.finish()