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

    # --- METHODS---
    def start(self):
        # Normalize to English API
        if hasattr(self._board, 'reset'):
            self._board.reset()
        elif hasattr(self._board, 'inicializar'):
            self._board.inicializar()

        if self._history is not None:
            if hasattr(self._history, 'clear_history'):
                self._history.clear_history()
            elif hasattr(self._history, 'limpiar'):
                self._history.limpiar()

        self._game_manager.start_match()
        print("Welcome to Tic-Tac-Toe!")

    def execute(self):
        self.start()
        
        while self._game_manager.get_state() == "EN_CURSO":
            print(self._board)
            
            # Use English API from TurnManager/Player
            current_player = self._turn_manager.get_current_player()
            # Use getters for name and symbol
            try:
                player_name = current_player.get_name()
            except AttributeError:
                player_name = getattr(current_player, 'nombre', 'Player')
            try:
                player_symbol = current_player.get_symbol()
            except AttributeError:
                player_symbol = getattr(current_player, 'simbolo', None)

            print(f"Turn of player: {player_name} ({player_symbol})")
            
            try:
                # Ask strategy for move — prefer English API
                strategy = current_player.get_strategy()
                if hasattr(strategy, 'execute_move'):
                    movement = strategy.execute_move(current_player, self._board)
                elif hasattr(current_player, 'realizarMovimiento'):
                    movement = current_player.realizarMovimiento(self._board)
                elif hasattr(strategy, 'ejecutarMovimiento'):
                    movement = strategy.ejecutarMovimiento(current_player, self._board)
                else:
                    raise AttributeError('No valid movement method found')
                
                # Validate and place on board using Board's API
                if movement is None:
                    print('No movement returned by strategy')
                else:
                    row, col = movement
                    if hasattr(self._board, 'place_symbol'):
                        valid = self._board.place_symbol(row, col, player_symbol)
                    elif hasattr(self._board, 'colocarFicha'):
                        valid = self._board.colocarFicha(movement)
                    else:
                        valid = False

                    if valid:
                        if self._history is not None:
                            if hasattr(self._history, 'add_match'):
                                self._history.add_match(movement)
                            elif hasattr(self._history, 'agregarMovimiento'):
                                self._history.agregarMovimiento(movement)

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
        if state == "VICTORIA":
            current_player = self._turn_manager.get_current_player()
            try:
                name = current_player.get_name()
            except AttributeError:
                name = getattr(current_player, 'nombre', 'Player')
            print(f"The game is over! Winner: {name}")
        elif state == "EMPATE":
            print("The game ended in a draw!")
        
        self._game_manager.finish()