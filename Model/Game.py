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
        self._board.inicializar()
        self._history.limpiar()
        self._game_manager.start_match()
        print("Welcome to Tic-Tac-Toe!")

    def execute(self):
        self.start()
        
        while self._game_manager.get_state() == "EN_CURSO":
            print(self._board)
            
            current_player = self._turn_manager.obtenerJugadorActual()
            print(f"Turn of player: {current_player.nombre} ({current_player.simbolo})")
            
            try:
                movement = current_player.realizarMovimiento(self._board)
                
                # Validar y colocar en el tablero
                if self._board.validarMovimiento(movement):
                    self._board.colocarFicha(movement)
                    self._history.agregarMovimiento(movement)

                    if self._game_manager.update_state(self._board):
                        break    

                    self._turn_manager.siguienteTurno()
                else:
                    print("Invalid movement. The cell is already occupied or out of bounds.")
            except Exception as e:
                print(f"Error during movement: {e}")

        print(self._board)
        self.finish()

    def finish(self):
        state = self._game_manager.get_state()
        if state == "VICTORIA":
            current_player = self._turn_manager.obtenerJugadorActual()
            print(f"The game is over! Winner: {current_player.nombre}")
        elif state == "EMPATE":
            print("The game ended in a draw!")
        
        self._game_manager.finish()