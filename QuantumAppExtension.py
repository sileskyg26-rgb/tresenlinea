import time
import pygame

from View.App import (
    TicTacToeApp,
    STATE_MENU,
    STATE_CHOOSE_FIRST,
    STATE_PLAYING,
    STATE_GAME_OVER,
)
from View import Theme, Theme
from View.Widgets import NeonButton
from View.board_view import SYMBOL_APPEAR_TIME

from Model.BotStrategy import BotStrategy
from Model.QuantumBot.QuantumBotStrategy import QuantumBotStrategy
from Model.Player import Player
from Model.Symbol import Symbol
from Model.HumanStrategy import HumanStrategy
 
_original_build_menu = TicTacToeApp._build_menu
_original_build_players = TicTacToeApp._build_players
_original_schedule_bot = TicTacToeApp._schedule_bot_if_needed
_original_handle_events = TicTacToeApp._handle_events
_original_update = TicTacToeApp._update
_original_draw = TicTacToeApp._draw
_original_maybe_run_bot = TicTacToeApp._maybe_run_bot
_original_handle_board_click = TicTacToeApp._handle_board_click
_original_draw_board = TicTacToeApp._draw_board

def _go_choose_first_quantum(self):
    self.state = "CHOOSE_FIRST_QUANTUM"

def _go_choose_first_qb(self):
    self.state = "CHOOSE_FIRST_QB"

def _new_build_menu(self):
    _original_build_menu(self)

    cx = Theme.WINDOW_WIDTH // 2
    w, h, gap = 340, 48, 10
    start_y = 200

    self.menu_buttons = [
        NeonButton(
            (cx - w // 2, start_y, w, h),
            "HUMANO vs HUMANO",
            on_click=lambda: self._start_mode("hh"),
        ),
        NeonButton(
            (cx - w // 2, start_y + 1 * (h + gap), w, h),
            "HUMANO vs BOT",
            on_click=self._go_choose_first,
        ),
        NeonButton(
            (cx - w // 2, start_y + 2 * (h + gap), w, h),
            "HUMANO vs QUANTUM BOT",
            on_click=self._go_choose_first_quantum,
            accent=Theme.MAGENTA_ACCENT,
        ),
        NeonButton(
            (cx - w // 2, start_y + 3 * (h + gap), w, h),
            "BOT vs BOT",
            on_click=lambda: self._start_mode("bb"),
        ),
        NeonButton(
            (cx - w // 2, start_y + 4 * (h + gap), w, h),
            "QUANTUM BOT vs QUANTUM BOT",
            on_click=lambda: self._start_mode("qq"),
            accent=Theme.MAGENTA_ACCENT,
        ),
        NeonButton(
            (cx - w // 2, start_y + 5 * (h + gap), w, h),
            "QUANTUM BOT vs BOT",
            on_click=self._go_choose_first_qb,
            accent=Theme.MAGENTA_ACCENT,
        ),
        NeonButton(
            (cx - w // 2, start_y + 6 * (h + gap), w, h),
            "SALIR",
            on_click=self._quit,
            accent=Theme.DANGER,
        ),
    ]

    self.choose_first_quantum_buttons = [
        NeonButton(
            (cx - w // 2, start_y, w, h),
            "EMPIEZA HUMANO",
            on_click=lambda: self._start_mode("hq", human_first=True),
        ),
        NeonButton(
            (cx - w // 2, start_y + 1 * (h + gap), w, h),
            "EMPIEZA QUANTUM BOT",
            on_click=lambda: self._start_mode("hq", human_first=False),
        ),
        NeonButton(
            (cx - w // 2, start_y + 2 * (h + gap), w, h),
            "VOLVER",
            on_click=self._go_menu,
            accent=Theme.MAGENTA_ACCENT,
        ),
    ]

    self.choose_first_qb_buttons = [
        NeonButton(
            (cx - w // 2, start_y, w, h),
            "EMPIEZA QUANTUM BOT",
            on_click=lambda: self._start_mode("qb", human_first=True),
        ),
        NeonButton(
            (cx - w // 2, start_y + 1 * (h + gap), w, h),
            "EMPIEZA BOT",
            on_click=lambda: self._start_mode("qb", human_first=False),
        ),
        NeonButton(
            (cx - w // 2, start_y + 2 * (h + gap), w, h),
            "VOLVER",
            on_click=self._go_menu,
            accent=Theme.MAGENTA_ACCENT,
        ),
    ]

def _new_build_players(self, mode, human_first=True):
    if mode == "hq":
        symbol_x = Symbol("X")
        symbol_o = Symbol("O")
        human = Player("HUMANO", symbol_x, HumanStrategy())
        q_bot = Player("QUANTUM BOT", symbol_o, QuantumBotStrategy(difficulty=1.0))
        return [human, q_bot] if human_first else [q_bot, human]

    if mode == "qq":
        symbol_x = Symbol("X")
        symbol_o = Symbol("O")
        return [
            Player("QUANTUM BOT 1", symbol_x, QuantumBotStrategy(difficulty=1.0)),
            Player("QUANTUM BOT 2", symbol_o, QuantumBotStrategy(difficulty=1.0)),
        ]

    if mode == "qb":
        symbol_x = Symbol("X")
        symbol_o = Symbol("O")
        q_bot = Player("QUANTUM BOT", symbol_x, QuantumBotStrategy(difficulty=1.0))
        bot = Player("BOT", symbol_o, BotStrategy())
        return [q_bot, bot] if human_first else [bot, q_bot]

    return _original_build_players(self, mode, human_first)
 
def _new_schedule_bot_if_needed(self):
    current = self.turn_manager.get_current_player()
    strategy = current.get_strategy()
    if isinstance(strategy, (BotStrategy, QuantumBotStrategy)):
        self.bot_move_deadline = time.time() + Theme.BOT_MOVE_DELAY_MS / 1000.0
    else:
        self.bot_move_deadline = None
 
def _new_handle_events(self):
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False
            return
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state in (STATE_PLAYING, STATE_GAME_OVER):
                self._go_menu()
            else:
                self.running = False
            return

        if self.state == STATE_MENU:
            for b in self.menu_buttons:
                b.handle_event(event)
        elif self.state == STATE_CHOOSE_FIRST:
            for b in self.choose_first_buttons:
                b.handle_event(event)
        elif self.state == "CHOOSE_FIRST_QUANTUM":
            for b in getattr(self, "choose_first_quantum_buttons", []):
                b.handle_event(event)
        elif self.state == "CHOOSE_FIRST_QB":
            for b in getattr(self, "choose_first_qb_buttons", []):
                b.handle_event(event)
        elif self.state == STATE_PLAYING:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._handle_board_click(event.pos)
        elif self.state == STATE_GAME_OVER:
            for b in self.game_over_buttons:
                b.handle_event(event)

    buttons_map = {
        STATE_MENU: getattr(self, "menu_buttons", []),
        STATE_CHOOSE_FIRST: getattr(self, "choose_first_buttons", []),
        "CHOOSE_FIRST_QUANTUM": getattr(self, "choose_first_quantum_buttons", []),
        "CHOOSE_FIRST_QB": getattr(self, "choose_first_qb_buttons", []),
        STATE_GAME_OVER: getattr(self, "game_over_buttons", []),
    }
    buttons = buttons_map.get(self.state, [])
    for b in buttons:
        b.update(0.0, mouse_pos)
 
def _new_update(self, dt):
    _original_update(self, dt)
    extra_states = ("CHOOSE_FIRST_QUANTUM", "CHOOSE_FIRST_QB")
    if self.state in extra_states:
        mouse_pos = pygame.mouse.get_pos()
        buttons_map = {
            "CHOOSE_FIRST_QUANTUM": getattr(self, "choose_first_quantum_buttons", []),
            "CHOOSE_FIRST_QB": getattr(self, "choose_first_qb_buttons", []),
        }
        for b in buttons_map.get(self.state, []):
            b.update(dt, mouse_pos)
 
def _new_draw(self):
    if self.state == "CHOOSE_FIRST_QUANTUM":
        self.background.draw(self.screen)
        self._draw_title("HUMANO vs QUANTUM BOT")
        self._draw_subtitle("QUIEN INICIA LA SECUENCIA CUANTICA?")
        for b in getattr(self, "choose_first_quantum_buttons", []):
            b.draw(self.screen)
        self.particles.draw(self.screen)
        return

    if self.state == "CHOOSE_FIRST_QB":
        self.background.draw(self.screen)
        self._draw_title("QUANTUM BOT vs BOT")
        self._draw_subtitle("QUIEN INICIA LA SECUENCIA?")
        for b in getattr(self, "choose_first_qb_buttons", []):
            b.draw(self.screen)
        self.particles.draw(self.screen)
        return

    _original_draw(self)

def _new_maybe_run_bot(self):
    if self.state != STATE_PLAYING or self.bot_move_deadline is None:
        return
    if time.time() < self.bot_move_deadline:
        return

    current_player = self.turn_manager.get_current_player()
    strategy = current_player.get_strategy()
    if not isinstance(strategy, (BotStrategy, QuantumBotStrategy)):
        self.bot_move_deadline = None
        return

    movement = strategy.execute_move(current_player, self.board)
    self.bot_move_deadline = None
    if movement is None:
        return
    row, col = movement
    self._apply_move(row, col)

def _new_handle_board_click(self, pos):
    current_player = self.turn_manager.get_current_player()
    strategy = current_player.get_strategy()
    if isinstance(strategy, (BotStrategy, QuantumBotStrategy)):
        return
    cell = self.board_view.cell_at_pos(pos)
    if cell is None:
        return
    row, col = cell
    self._apply_move(row, col)
 
def _new_draw_board(self):
    self.board_view.draw_grid(self.screen, self.time_elapsed)

    if self.state == STATE_PLAYING:
        mouse_pos = pygame.mouse.get_pos()
        current_player = self.turn_manager.get_current_player()
        strategy = current_player.get_strategy()
        if not isinstance(strategy, (BotStrategy, QuantumBotStrategy)):
            cell = self.board_view.cell_at_pos(mouse_pos)
            if cell is not None:
                r, c = cell
                if self.board.get_cells()[r][c].is_empty():
                    self.board_view.draw_cell_hover(self.screen, r, c)

    cells = self.board.get_cells()
    for row in range(3):
        for col in range(3):
            symbol = cells[row][col].get_symbol()
            if symbol is None:
                continue
            placed_at = self.symbol_appear_times.get((row, col))
            elapsed = (time.time() - placed_at) if placed_at else SYMBOL_APPEAR_TIME
            self.board_view.draw_symbol(self.screen, row, col, str(symbol), elapsed)

    if self.winning_line:
        self.board_view.draw_winning_line(self.screen, self.winning_line, self.time_elapsed)
 
TicTacToeApp._build_menu = _new_build_menu
TicTacToeApp._go_choose_first_quantum = _go_choose_first_quantum
TicTacToeApp._go_choose_first_qb = _go_choose_first_qb
TicTacToeApp._build_players = _new_build_players
TicTacToeApp._schedule_bot_if_needed = _new_schedule_bot_if_needed
TicTacToeApp._handle_events = _new_handle_events
TicTacToeApp._update = _new_update
TicTacToeApp._draw = _new_draw
TicTacToeApp._maybe_run_bot = _new_maybe_run_bot
TicTacToeApp._handle_board_click = _new_handle_board_click
TicTacToeApp._draw_board = _new_draw_board
 
if __name__ == "__main__":
    app = TicTacToeApp()
    app.run()