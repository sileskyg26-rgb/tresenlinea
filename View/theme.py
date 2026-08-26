"""
Tema visual: futurista / sci-fi / cuántico.
Toda la paleta de colores, tamaños y fuentes vive aquí para que
el resto de la vista sea puramente de dibujo.
"""

import pygame

# --- Paleta -----------------------------------------------------------
BG_DARK = (10, 22, 40)          # #0a1628 - fondo azul marino oscuro
BG_DARKER = (6, 14, 28)         # variante aún más oscura (para paneles)
CYAN = (0, 217, 255)            # #00d9ff - cian brillante (circuitos / X)
CYAN_SOFT = (0, 150, 200)
CYAN_DIM = (0, 90, 130)
WHITE_GLOW = (210, 240, 255)    # blanco azulado (O)
BLUE_RING = (90, 180, 255)      # anillo azul de la O
MAGENTA_ACCENT = (200, 60, 255) # acento cuántico secundario (hover / warnings)
GRID_LINE = (0, 160, 210)
TEXT_PRIMARY = (200, 235, 255)
TEXT_DIM = (90, 140, 170)
WIN_GOLD = (255, 210, 90)
DRAW_PURPLE = (170, 120, 255)
DANGER = (255, 90, 110)

# --- Ventana ------------------------------------------------------------
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
FPS = 60

BOARD_SIZE = 480
BOARD_MARGIN_TOP = 150
CELL_SIZE = BOARD_SIZE // 3

BOT_MOVE_DELAY_MS = 800


_fonts_cache = {}


def get_font(name, size, bold=False):
    """
    Devuelve una fuente 'técnica' cacheada. Intenta usar fuentes
    monoespaciadas del sistema (look de consola/HUD); si no existen,
    recurre a la fuente monoespaciada por defecto de pygame.
    """
    key = (name, size, bold)
    if key in _fonts_cache:
        return _fonts_cache[key]

    candidates = [
        "Consolas",
        "Courier New",
        "DejaVu Sans Mono",
        "Lucida Console",
        "Monaco",
    ]
    font = None
    for candidate in candidates:
        try:
            font = pygame.font.SysFont(candidate, size, bold=bold)
            if font is not None:
                break
        except Exception:
            continue

    if font is None:
        font = pygame.font.SysFont("monospace", size, bold=bold)

    _fonts_cache[key] = font
    return font


def font_title(size=48):
    return get_font("title", size, bold=True)


def font_hud(size=22):
    return get_font("hud", size, bold=False)


def font_button(size=26):
    return get_font("button", size, bold=True)
