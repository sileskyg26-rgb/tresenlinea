import pygame

BG_DARK = (10, 22, 40)           
BG_DARKER = (6, 14, 28)          
CYAN = (0, 217, 255)             
CYAN_SOFT = (0, 150, 200)
CYAN_DIM = (0, 90, 130)
WHITE_GLOW = (210, 240, 255)     
BLUE_RING = (90, 180, 255)       
MAGENTA_ACCENT = (200, 60, 255)  
GRID_LINE = (0, 160, 210)
TEXT_PRIMARY = (200, 235, 255)
TEXT_DIM = (90, 140, 170)
WIN_GOLD = (255, 210, 90)
DRAW_PURPLE = (170, 120, 255)
DANGER = (255, 90, 110)

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 700
FPS = 60

BOARD_SIZE = 480
BOARD_MARGIN_TOP = 150
CELL_SIZE = BOARD_SIZE // 3

BOT_MOVE_DELAY_MS = 800


_fonts_cache = {}


def get_font(name, size, bold=False):
    
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
