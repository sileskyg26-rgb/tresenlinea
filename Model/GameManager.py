class GameManager:
    def __init__(self, state, victory_rule, draw_rule):
        # Constructor
        self._state = state
        self._victory_rule = victory_rule
        self._draw_rule = draw_rule

    def __del__(self):
        # Destructor
        print("Releasing game manager resources...")

    # --- GETTERS ---
    def get_state(self):
        return self._state

    def get_victory_rule(self):
        return self._victory_rule

    def get_draw_rule(self):
        return self._draw_rule

    # --- SETTERS ---
    def set_state(self, state):
        self._state = state

    def set_victory_rule(self, victory_rule):
        self._victory_rule = victory_rule

    def set_draw_rule(self, draw_rule):
        self._draw_rule = draw_rule

    # --- METHODS ---
    def start_match(self):
        self._state = "IN_PROGRESS"
        print("Match started. Good luck!")

    def update_state(self, board):
        if self._victory_rule.verify(board):
            self._state = "WIN"
            return True
        
        if self._draw_rule.verify(board):
            self._state = "DRAW"
            return True
                
        return False

    def restart(self):
        self._state = "IN_PROGRESS"
        print("Match restarted.")

    def finish(self):
        self._state = "FINISHED"
        print("Match finished.")

    def get_state_info(self):
        return self._state