import os
import sys
import time

from Model.Board import Board
from Model.Cell import Cell  # noqa: F401  (imported for completeness/integration)
from Model.Symbol import Symbol
from Model.Player import Player
from Model.PlayerType import PlayerType
from Model.TurnManager import TurnManager
from Model.MatchHistory import MatchHistory
from Model.GameManager import GameManager
from Model.VictoryVerifier import VictoryVerifier
from Model.DrawVerifier import DrawVerifier
from Model.HumanStrategy import HumanStrategy
from Model.BotStrategy import BotStrategy
from Model.InvalidMoveException import InvalidMoveException  # noqa: F401


BOT_MOVE_DELAY_SECONDS = 0.8


# --------------------------------------------------------------------------- #
# Board rendering (attached to Board since Board.py has no __str__)
# --------------------------------------------------------------------------- #
def _board_to_string(self: Board) -> str:
    cells = self.get_cells()
    col_header = "     0   1   2"
    sep = "   " + "-" * 13
    lines = [col_header]
    for row in range(3):
        row_symbols = []
        for col in range(3):
            symbol = cells[row][col].get_symbol()
            row_symbols.append(str(symbol) if symbol is not None else " ")
        lines.append(f" {row} | " + " | ".join(row_symbols) + " |")
        lines.append(sep)
    return "\n".join(lines)


Board.__str__ = _board_to_string


# --------------------------------------------------------------------------- #
# Small CLI helpers
# --------------------------------------------------------------------------- #
def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def print_title():
    print("=" * 40)
    print("           TIC-TAC-TOE  (3 en raya)")
    print("=" * 40)


def print_menu():
    print("\nMain Menu")
    print("-" * 40)
    print("1. Human vs Human")
    print("2. Human vs Bot")
    print("3. Bot vs Bot")
    print("4. Exit")
    print("-" * 40)


def prompt_int(message, valid_values):
    while True:
        raw = input(message).strip()
        if raw.isdigit() and int(raw) in valid_values:
            return int(raw)
        print(f"Invalid input. Please enter one of: {valid_values}")


# --------------------------------------------------------------------------- #
# Player / game setup
# --------------------------------------------------------------------------- #
def build_players(mode: str, human_goes_first: bool = True):
    """
    mode: "hh" (human vs human), "hb" (human vs bot), "bb" (bot vs bot)
    Returns a list of two Player objects, in turn order.
    """
    symbol_x = Symbol("X")
    symbol_o = Symbol("O")

    if mode == "hh":
        return [
            Player("Player 1", symbol_x, HumanStrategy()),
            Player("Player 2", symbol_o, HumanStrategy()),
        ]

    if mode == "hb":
        human = Player("Human", symbol_x, HumanStrategy())
        bot = Player("Bot", symbol_o, BotStrategy())
        return [human, bot] if human_goes_first else [bot, human]

    if mode == "bb":
        return [
            Player("Bot 1", symbol_x, BotStrategy()),
            Player("Bot 2", symbol_o, BotStrategy()),
        ]

    raise ValueError(f"Unknown mode: {mode}")


def build_game_components(players):
    board = Board()
    turn_manager = TurnManager(players)
    history = MatchHistory()
    game_manager = GameManager(
        state="READY",
        victory_rule=VictoryVerifier(),
        draw_rule=DrawVerifier(),
    )
    return board, turn_manager, history, game_manager


# --------------------------------------------------------------------------- #
# Game loop
# --------------------------------------------------------------------------- #
def play(players, bot_vs_bot: bool = False):
    board, turn_manager, history, game_manager = build_game_components(players)

    board.reset()
    turn_manager.reset()
    history.clear_history()
    game_manager.start_match()

    print(f"\nPlayer '{players[0].get_name()}' is {players[0].get_symbol()}")
    print(f"Player '{players[1].get_name()}' is {players[1].get_symbol()}\n")

    while game_manager.get_state() == "IN_PROGRESS":
        clear_screen()
        print_title()
        print(board)

        current_player = turn_manager.get_current_player()
        print(f"\nTurn: {current_player.get_name()} ({current_player.get_symbol()})")

        if bot_vs_bot:
            time.sleep(BOT_MOVE_DELAY_SECONDS)

        strategy = current_player.get_strategy()

        try:
            movement = strategy.execute_move(current_player, board)
        except Exception as exc:
            print(f"Error while computing move: {exc}")
            continue

        if movement is None:
            print("No move was returned. Ending match early.")
            break

        row, col = movement

        if not (isinstance(row, int) and isinstance(col, int) and 0 <= row < 3 and 0 <= col < 3):
            print("Move out of bounds. Row and column must be between 0 and 2.")
            input("Press Enter to try again...")
            continue

        placed = board.place_symbol(row, col, current_player.get_symbol())

        if not placed:
            print("Invalid move: that cell is already occupied.")
            input("Press Enter to try again...")
            continue

        history.add_match((current_player.get_name(), row, col))

        if game_manager.update_state(board):
            break

        turn_manager.next_turn()

    clear_screen()
    print_title()
    print(board)

    final_state = game_manager.get_state()
    print()
    if final_state == "WIN":
        winner = turn_manager.get_current_player()
        print(f"*** {winner.get_name()} ({winner.get_symbol()}) wins! ***")
    elif final_state == "DRAW":
        print("*** It's a draw! ***")
    else:
        print("Match ended.")

    game_manager.finish()
    input("\nPress Enter to return to the main menu...")


# --------------------------------------------------------------------------- #
# Menu flows
# --------------------------------------------------------------------------- #
def human_vs_human():
    players = build_players("hh")
    play(players, bot_vs_bot=False)


def human_vs_bot():
    print("\nWho should go first?")
    print("1. Human")
    print("2. Bot")
    choice = prompt_int("Choose (1-2): ", [1, 2])
    human_first = choice == 1
    players = build_players("hb", human_goes_first=human_first)
    play(players, bot_vs_bot=False)


def bot_vs_bot():
    players = build_players("bb")
    print("\nStarting Bot vs Bot match (moves are delayed for readability)...")
    play(players, bot_vs_bot=True)


def main():
    while True:
        clear_screen()
        print_title()
        print_menu()
        choice = prompt_int("Select an option (1-4): ", [1, 2, 3, 4])

        if choice == 1:
            human_vs_human()
        elif choice == 2:
            human_vs_bot()
        elif choice == 3:
            bot_vs_bot()
        elif choice == 4:
            print("\nThanks for playing! Goodbye.")
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGame interrupted. Goodbye!")
        sys.exit(0)