class MatchHistory:
    def __init__(self):
        self._matches = []

    def __del__(self):
        print("Releasing match history resources...")

    # --- GETTERS ---
    def get_matches(self):
        return self._matches

    # --- SETTERS ---
    def set_matches(self, matches):
        self._matches = matches

    # --- METHODS ---
    def add_match(self, match_info):
        self._matches.append(match_info)

    def get_history(self):
        return self._matches

    def clear_history(self):
        self._matches.clear()