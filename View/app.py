"""
App principal de la interfaz gráfica (pygame).

Reutiliza tal cual el backend ya existente (Model/*): Board, Player,
Symbol, TurnManager, MatchHistory, GameManager, VictoryVerifier,
DrawVerifier, HumanStrategy y BotStrategy. La vista NO reimplementa
reglas del juego: solo dibuja el estado y traduce clics de mouse en
llamadas a `board.place_symbol(...)`, igual que el bucle de main.py
traduce `strategy.execute_move(...)` a esa misma llamada.

Para el jugador humano, en vez de invocar HumanStrategy.execute_move
(que bloquea con input() por consola), la vista captura el clic sobre
la celda y coloca el símbolo directamente sobre el tablero -- el mismo
punto de entrada que usa main.py tras obtener la jugada.
Para el bot, sí se usa BotStrategy.execute_move tal cual, porque no
depende de la consola.
"""

import sys
import time

import pygame

from Model.Board import Board
from Model.Symbol import Symbol
from Model.Player import Player
from Model.TurnManager import TurnManager
from Model.MatchHistory import MatchHistory
from Model.GameManager import GameManager
from Model.VictoryVerifier import VictoryVerifier
from Model.DrawVerifier import DrawVerifier
from Model.HumanStrategy import HumanStrategy
from Model.BotStrategy import BotStrategy

from View import theme
from View.effects import CircuitBackground, ParticleSystem, draw_glow_text
from View.widgets import NeonButton
from View.board_view import BoardView, SYMBOL_APPEAR_TIME


STATE_MENU = "MENU"
STATE_CHOOSE_FIRST = "CHOOSE_FIRST"
STATE_PLAYING = "PLAYING"
STATE_GAME_OVER = "GAME_OVER"


def find_winning_line(board):
    """Determina qué 3 celdas forman la línea ganadora (si existe), solo
    para poder resaltarla visualmente. No altera ni sustituye la lógica
    de VictoryVerifier, que sigue siendo la única fuente de verdad sobre
    si hay o no victoria."""
    cells = board.get_cells()

    lines = []
    for row in range(3):
        lines.append([(row, 0), (row, 1), (row, 2)])
    for col in range(3):
        lines.append([(0, col), (1, col), (2, col)])
    lines.append([(0, 0), (1, 1), (2, 2)])
    lines.append([(0, 2), (1, 1), (2, 0)])

    for line in lines:
        symbols = [cells[r][c].get_symbol() for r, c in line]
        if symbols[0] is not None and symbols[0] == symbols[1] == symbols[2]:
            return line
    return None


class TicTacToeApp:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("TIC-TAC-TOE // QUANTUM GRID")
        self.screen = pygame.display.set_mode((theme.WINDOW_WIDTH, theme.WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.background = CircuitBackground(theme.WINDOW_WIDTH, theme.WINDOW_HEIGHT, seed=7)
        self.particles = ParticleSystem()

        self.time_elapsed = 0.0
        self.running = True

        self.state = STATE_MENU
        self.mode = None  # "hh" | "hb" | "bb"
        self.human_first = True

        self.board = None
        self.turn_manager = None
        self.history = None
        self.game_manager = None
        self.board_view = None
        self.players = None

        self.symbol_appear_times = {}  # (row, col) -> timestamp de colocación
        self.bot_move_deadline = None
        self.winning_line = None
        self.status_message = ""

        self._build_menu()

    # ------------------------------------------------------------------ #
    # Construcción de menús
    # ------------------------------------------------------------------ #
    def _build_menu(self):
        cx = theme.WINDOW_WIDTH // 2
        w, h, gap = 340, 56, 20
        start_y = 300
        self.menu_buttons = [
            NeonButton(
                (cx - w // 2, start_y, w, h),
                "HUMANO vs HUMANO",
                on_click=lambda: self._start_mode("hh"),
            ),
            NeonButton(
                (cx - w // 2, start_y + (h + gap), w, h),
                "HUMANO vs BOT",
                on_click=lambda: self._go_choose_first(),
            ),
            NeonButton(
                (cx - w // 2, start_y + 2 * (h + gap), w, h),
                "BOT vs BOT",
                on_click=lambda: self._start_mode("bb"),
            ),
            NeonButton(
                (cx - w // 2, start_y + 3 * (h + gap), w, h),
                "SALIR",
                on_click=self._quit,
                accent=theme.DANGER,
            ),
        ]

        self.choose_first_buttons = [
            NeonButton(
                (cx - w // 2, start_y, w, h),
                "EMPIEZA HUMANO",
                on_click=lambda: self._start_mode("hb", human_first=True),
            ),
            NeonButton(
                (cx - w // 2, start_y + (h + gap), w, h),
                "EMPIEZA BOT",
                on_click=lambda: self._start_mode("hb", human_first=False),
            ),
            NeonButton(
                (cx - w // 2, start_y + 2 * (h + gap), w, h),
                "VOLVER",
                on_click=self._go_menu,
                accent=theme.MAGENTA_ACCENT,
            ),
        ]

        self.game_over_buttons = [
            NeonButton((cx - 190, 600, 180, 50), "REVANCHA", on_click=self._rematch),
            NeonButton((cx + 10, 600, 180, 50), "MENU", on_click=self._go_menu, accent=theme.MAGENTA_ACCENT),
        ]

    def _go_menu(self):
        self.state = STATE_MENU
        self.mode = None

    def _go_choose_first(self):
        self.state = STATE_CHOOSE_FIRST

    def _quit(self):
        self.running = False

    # ------------------------------------------------------------------ #
    # Configuración de partida (equivalente a build_players / build_game_components)
    # ------------------------------------------------------------------ #
    def _build_players(self, mode, human_first=True):
        symbol_x = Symbol("X")
        symbol_o = Symbol("O")

        if mode == "hh":
            return [
                Player("JUGADOR 1", symbol_x, HumanStrategy()),
                Player("JUGADOR 2", symbol_o, HumanStrategy()),
            ]
        if mode == "hb":
            human = Player("HUMANO", symbol_x, HumanStrategy())
            bot = Player("BOT", symbol_o, BotStrategy())
            return [human, bot] if human_first else [bot, human]
        if mode == "bb":
            return [
                Player("BOT 1", symbol_x, BotStrategy()),
                Player("BOT 2", symbol_o, BotStrategy()),
            ]
        raise ValueError(f"Modo desconocido: {mode}")

    def _start_mode(self, mode, human_first=True):
        self.mode = mode
        self.human_first = human_first
        self.players = self._build_players(mode, human_first)
        self._setup_match()
        self.state = STATE_PLAYING

    def _rematch(self):
        self.players = self._build_players(self.mode, self.human_first)
        self._setup_match()
        self.state = STATE_PLAYING

    def _setup_match(self):
        self.board = Board()
        self.turn_manager = TurnManager(self.players)
        self.history = MatchHistory()
        self.game_manager = GameManager(
            state="READY",
            victory_rule=VictoryVerifier(),
            draw_rule=DrawVerifier(),
        )

        self.board.reset()
        self.turn_manager.reset()
        self.history.clear_history()
        self.game_manager.start_match()

        board_x = (theme.WINDOW_WIDTH - theme.BOARD_SIZE) // 2
        board_y = theme.BOARD_MARGIN_TOP
        self.board_view = BoardView((board_x, board_y, theme.BOARD_SIZE, theme.BOARD_SIZE))

        self.symbol_appear_times = {}
        self.winning_line = None
        self.status_message = ""
        self._schedule_bot_if_needed()

    def _schedule_bot_if_needed(self):
        current = self.turn_manager.get_current_player()
        if isinstance(current.get_strategy(), BotStrategy):
            self.bot_move_deadline = time.time() + theme.BOT_MOVE_DELAY_MS / 1000.0
        else:
            self.bot_move_deadline = None

    # ------------------------------------------------------------------ #
    # Colocar una jugada (usado tanto por clic humano como por el bot)
    # ------------------------------------------------------------------ #
    def _apply_move(self, row, col):
        current_player = self.turn_manager.get_current_player()
        placed = self.board.place_symbol(row, col, current_player.get_symbol())
        if not placed:
            return

        self.symbol_appear_times[(row, col)] = time.time()
        self.history.add_match((current_player.get_name(), row, col))

        cell_rect = self.board_view.cell_rect(row, col)
        color = theme.CYAN if str(current_player.get_symbol()) == "X" else theme.BLUE_RING
        self.particles.burst(*cell_rect.center, color, count=30)

        if self.game_manager.update_state(self.board):
            self.winning_line = find_winning_line(self.board)
            final_state = self.game_manager.get_state()
            if final_state == "WIN":
                self.status_message = f"{current_player.get_name()} ({current_player.get_symbol()}) GANA"
            elif final_state == "DRAW":
                self.status_message = "EMPATE"
            self.game_manager.finish()
            self.state = STATE_GAME_OVER
            return

        self.turn_manager.next_turn()
        self._schedule_bot_if_needed()

    def _handle_board_click(self, pos):
        current_player = self.turn_manager.get_current_player()
        if isinstance(current_player.get_strategy(), BotStrategy):
            return  # el bot mueve solo
        cell = self.board_view.cell_at_pos(pos)
        if cell is None:
            return
        row, col = cell
        self._apply_move(row, col)

    def _maybe_run_bot(self):
        if self.state != STATE_PLAYING or self.bot_move_deadline is None:
            return
        if time.time() < self.bot_move_deadline:
            return

        current_player = self.turn_manager.get_current_player()
        strategy = current_player.get_strategy()
        if not isinstance(strategy, BotStrategy):
            self.bot_move_deadline = None
            return

        movement = strategy.execute_move(current_player, self.board)
        self.bot_move_deadline = None
        if movement is None:
            return
        row, col = movement
        self._apply_move(row, col)

    # ------------------------------------------------------------------ #
    # Bucle principal
    # ------------------------------------------------------------------ #
    def run(self):
        while self.running:
            dt = self.clock.tick(theme.FPS) / 1000.0
            self.time_elapsed += dt
            self._handle_events()
            self._update(dt)
            self._draw()
            pygame.display.flip()

        pygame.quit()
        sys.exit(0)

    def _handle_events(self):
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
            elif self.state == STATE_PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self._handle_board_click(event.pos)
            elif self.state == STATE_GAME_OVER:
                for b in self.game_over_buttons:
                    b.handle_event(event)

        buttons = {
            STATE_MENU: self.menu_buttons,
            STATE_CHOOSE_FIRST: self.choose_first_buttons,
            STATE_GAME_OVER: self.game_over_buttons,
        }.get(self.state, [])
        for b in buttons:
            b.update(0.0, mouse_pos)

    def _update(self, dt):
        self.background.update(dt)
        self.particles.update(dt)
        mouse_pos = pygame.mouse.get_pos()

        buttons = {
            STATE_MENU: self.menu_buttons,
            STATE_CHOOSE_FIRST: self.choose_first_buttons,
            STATE_GAME_OVER: self.game_over_buttons,
        }.get(self.state, [])
        for b in buttons:
            b.update(dt, mouse_pos)

        if self.state == STATE_PLAYING:
            self._maybe_run_bot()

    # ------------------------------------------------------------------ #
    # Dibujo
    # ------------------------------------------------------------------ #
    def _draw(self):
        self.background.draw(self.screen)

        if self.state == STATE_MENU:
            self._draw_title("TIC-TAC-TOE")
            self._draw_subtitle("RED CUANTICA // SELECCIONA UN MODO")
            for b in self.menu_buttons:
                b.draw(self.screen)

        elif self.state == STATE_CHOOSE_FIRST:
            self._draw_title("HUMANO vs BOT")
            self._draw_subtitle("QUIEN INICIA LA SECUENCIA?")
            for b in self.choose_first_buttons:
                b.draw(self.screen)

        elif self.state == STATE_PLAYING:
            self._draw_game_hud()
            self._draw_board()

        elif self.state == STATE_GAME_OVER:
            self._draw_board()
            self._draw_game_over_overlay()
            for b in self.game_over_buttons:
                b.draw(self.screen)

        self.particles.draw(self.screen)

    def _draw_title(self, text):
        draw_glow_text(
            self.screen, theme.font_title(52), text, theme.TEXT_PRIMARY,
            (theme.WINDOW_WIDTH // 2, 130), glow_color=theme.CYAN,
        )

    def _draw_subtitle(self, text):
        font = theme.font_hud(20)
        label = font.render(text, True, theme.TEXT_DIM)
        rect = label.get_rect(center=(theme.WINDOW_WIDTH // 2, 190))
        self.screen.blit(label, rect)

    def _draw_game_hud(self):
        current_player = self.turn_manager.get_current_player()
        turn_text = f"TURNO: {current_player.get_name()} [{current_player.get_symbol()}]"
        draw_glow_text(
            self.screen, theme.font_hud(26), turn_text, theme.TEXT_PRIMARY,
            (theme.WINDOW_WIDTH // 2, 70), glow_color=theme.CYAN,
        )
        hint_font = theme.font_hud(16)
        hint = hint_font.render("ESC: MENU", True, theme.TEXT_DIM)
        self.screen.blit(hint, (16, 16))

    def _draw_board(self):
        self.board_view.draw_grid(self.screen, self.time_elapsed)

        if self.state == STATE_PLAYING:
            mouse_pos = pygame.mouse.get_pos()
            current_player = self.turn_manager.get_current_player()
            if not isinstance(current_player.get_strategy(), BotStrategy):
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

    def _draw_game_over_overlay(self):
        overlay = pygame.Surface((theme.WINDOW_WIDTH, 130), pygame.SRCALPHA)
        pygame.draw.rect(overlay, (*theme.BG_DARKER, 210), overlay.get_rect())
        self.screen.blit(overlay, (0, 40))

        color = theme.WIN_GOLD if "GANA" in self.status_message else theme.DRAW_PURPLE
        draw_glow_text(
            self.screen, theme.font_title(40), self.status_message, theme.TEXT_PRIMARY,
            (theme.WINDOW_WIDTH // 2, 95), glow_color=color,
        )
