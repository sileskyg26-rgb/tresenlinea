import math

import pygame

from View import theme
from View.effects import draw_glow_text


class NeonButton:
    def __init__(self, rect, text, on_click=None, accent=None):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.on_click = on_click
        self.accent = accent or theme.CYAN
        self.hovered = False
        self.enabled = True
        self._pulse = 0.0

    def update(self, dt, mouse_pos):
        self._pulse += dt
        self.hovered = self.enabled and self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                if self.on_click:
                    self.on_click()

    def _chamfered_points(self, rect, cut=14):
        x, y, w, h = rect
        return [
            (x + cut, y),
            (x + w - cut, y),
            (x + w, y + cut),
            (x + w, y + h - cut),
            (x + w - cut, y + h),
            (x + cut, y + h),
            (x, y + h - cut),
            (x, y + cut),
        ]

    def draw(self, surface):
        color = self.accent if self.enabled else theme.TEXT_DIM
        points = self._chamfered_points(self.rect)

        panel = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        local_points = [(px - self.rect.x, py - self.rect.y) for px, py in points]
        fill_alpha = 60 if self.hovered else 28
        pygame.draw.polygon(panel, (*color, fill_alpha), local_points)
        surface.blit(panel, self.rect.topleft)

        glow_strength = 1.0 if self.hovered else 0.0
        pulse = (math.sin(self._pulse * 4) + 1) / 2 if self.hovered else 0
        border_width = 2 + int(glow_strength * pulse)

        if self.hovered:
            halo = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
            pygame.draw.polygon(halo, (*color, 60), points, width=6)
            surface.blit(halo, (0, 0))

        pygame.draw.polygon(surface, color, points, width=max(2, border_width))

        x, y, w, h = self.rect
        tick = 6
        pygame.draw.line(surface, color, (x + tick, y), (x, y + tick), 1)
        pygame.draw.line(surface, color, (x + w - tick, y + h), (x + w, y + h - tick), 1)

        text_color = theme.TEXT_PRIMARY if self.enabled else theme.TEXT_DIM
        font = theme.font_button(24)
        if self.hovered:
            draw_glow_text(surface, font, self.text, text_color, self.rect.center, glow_color=color)
        else:
            label = font.render(self.text, True, text_color)
            surface.blit(label, label.get_rect(center=self.rect.center))
