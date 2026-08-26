import math

import pygame

from View import theme
from View.effects import draw_glow_line, draw_glow_circle

SYMBOL_APPEAR_TIME = 0.28  # segundos que tarda una ficha en "materializarse"


def ease_out_back(t):
    """Pequeño 'overshoot' para que la ficha aparezca con un ligero rebote,
    reforzando la sensación de energía condensándose de golpe."""
    c1 = 1.70158
    c3 = c1 + 1
    t = max(0.0, min(1.0, t))
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2


class BoardView:
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        self.cell = self.rect.width // 3

    def cell_rect(self, row, col):
        x = self.rect.x + col * self.cell
        y = self.rect.y + row * self.cell
        return pygame.Rect(x, y, self.cell, self.cell)

    def cell_at_pos(self, pos):
        if not self.rect.collidepoint(pos):
            return None
        x, y = pos
        col = (x - self.rect.x) // self.cell
        row = (y - self.rect.y) // self.cell
        if 0 <= row < 3 and 0 <= col < 3:
            return int(row), int(col)
        return None

    # ------------------------------------------------------------------ #
    def draw_grid(self, surface, time_elapsed):
        r = self.rect
        # Panel de fondo del tablero, ligeramente más oscuro que el resto
        panel = pygame.Surface(r.size, pygame.SRCALPHA)
        pygame.draw.rect(panel, (*theme.BG_DARKER, 160), panel.get_rect(), border_radius=10)
        surface.blit(panel, r.topleft)

        # Líneas internas del grid con glow
        for i in (1, 2):
            x = r.x + i * self.cell
            draw_glow_line(surface, theme.CYAN, (x, r.y + 6), (x, r.bottom - 6), 2, glow_layers=3, max_extra=8)
            y = r.y + i * self.cell
            draw_glow_line(surface, theme.CYAN, (r.x + 6, y), (r.right - 6, y), 2, glow_layers=3, max_extra=8)

        # Marco exterior tipo circuito con esquinas marcadas
        pygame.draw.rect(surface, theme.CYAN_SOFT, r, width=2, border_radius=10)
        corner = 16
        for cx, cy, dx, dy in [
            (r.left, r.top, 1, 1),
            (r.right, r.top, -1, 1),
            (r.left, r.bottom, 1, -1),
            (r.right, r.bottom, -1, -1),
        ]:
            pygame.draw.line(surface, theme.CYAN, (cx, cy), (cx + dx * corner, cy), 3)
            pygame.draw.line(surface, theme.CYAN, (cx, cy), (cx, cy + dy * corner), 3)

        # Nodos pulsantes en las intersecciones internas
        for i in (1, 2):
            for j in (1, 2):
                x = r.x + i * self.cell
                y = r.y + j * self.cell
                pulse = (math.sin(time_elapsed * 3 + i + j) + 1) / 2
                draw_glow_circle(surface, theme.CYAN, (x, y), 3 + int(pulse * 2), glow_layers=3, max_extra=6)

    def draw_cell_hover(self, surface, row, col):
        rect = self.cell_rect(row, col)
        hover_surf = pygame.Surface(rect.size, pygame.SRCALPHA)
        pygame.draw.rect(hover_surf, (*theme.CYAN, 30), hover_surf.get_rect(), border_radius=6)
        pygame.draw.rect(hover_surf, (*theme.CYAN, 120), hover_surf.get_rect(), width=2, border_radius=6)
        surface.blit(hover_surf, rect.topleft)

    # ------------------------------------------------------------------ #
    def draw_symbol(self, surface, row, col, symbol_str, appear_elapsed):
        rect = self.cell_rect(row, col)
        cx, cy = rect.center
        pad = int(self.cell * 0.22)
        size = self.cell - pad * 2

        t = min(1.0, appear_elapsed / SYMBOL_APPEAR_TIME) if appear_elapsed is not None else 1.0
        scale = ease_out_back(t)
        current_size = max(2, size * scale)
        alpha_fade = min(1.0, appear_elapsed / (SYMBOL_APPEAR_TIME * 0.6)) if appear_elapsed is not None else 1.0

        if symbol_str == "X":
            self._draw_x(surface, (cx, cy), current_size, alpha_fade)
        elif symbol_str == "O":
            self._draw_o(surface, (cx, cy), current_size, alpha_fade)

    def _draw_x(self, surface, center, size, alpha_fade):
        cx, cy = center
        half = size / 2
        thickness = max(3, int(size * 0.11))

        temp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        draw_glow_line(
            temp, theme.CYAN, (cx - half, cy - half), (cx + half, cy + half),
            thickness, glow_layers=5, max_extra=16,
        )
        draw_glow_line(
            temp, theme.CYAN, (cx + half, cy - half), (cx - half, cy + half),
            thickness, glow_layers=5, max_extra=16,
        )
        # núcleo blanco muy brillante en el centro de cada trazo
        pygame.draw.line(temp, theme.WHITE_GLOW, (cx - half, cy - half), (cx + half, cy + half), max(1, thickness - 3))
        pygame.draw.line(temp, theme.WHITE_GLOW, (cx + half, cy - half), (cx - half, cy + half), max(1, thickness - 3))

        temp.set_alpha(int(255 * alpha_fade))
        surface.blit(temp, (0, 0))

    def _draw_o(self, surface, center, size, alpha_fade):
        radius = int(size / 2)
        thickness = max(3, int(size * 0.14))

        temp = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        draw_glow_circle(temp, theme.BLUE_RING, center, radius, width=thickness, glow_layers=5, max_extra=18)
        # anillo interior blanco brillante, más fino, para el "núcleo" de luz
        pygame.draw.circle(temp, theme.WHITE_GLOW, center, radius - thickness // 3, width=max(1, thickness - 4))

        temp.set_alpha(int(255 * alpha_fade))
        surface.blit(temp, (0, 0))

    # ------------------------------------------------------------------ #
    def draw_winning_line(self, surface, line_cells, time_elapsed):
        """line_cells: lista de (row, col) de las 3 celdas ganadoras, en orden."""
        if not line_cells:
            return
        start_cell = line_cells[0]
        end_cell = line_cells[-1]
        start = self.cell_rect(*start_cell).center
        end = self.cell_rect(*end_cell).center

        pulse = (math.sin(time_elapsed * 6) + 1) / 2
        width = 4 + int(pulse * 3)
        draw_glow_line(surface, theme.WIN_GOLD, start, end, width, glow_layers=6, max_extra=20)
