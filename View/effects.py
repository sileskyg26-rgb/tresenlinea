"""
Efectos visuales reutilizables: fondo de "circuitos" animado,
sistema de partículas cuánticas y helpers de glow (resplandor)
para dibujar líneas / círculos con halo de luz.
"""

import math
import random

import pygame

from View import theme


# --------------------------------------------------------------------- #
# Helpers de "glow" (resplandor) usando superficies con alpha en capas
# --------------------------------------------------------------------- #
def draw_glow_line(surface, color, start, end, width, glow_layers=4, max_extra=10):
    """Dibuja una línea con halo de luz: varias líneas semitransparentes
    cada vez más anchas debajo de la línea nítida final."""
    x1, y1 = start
    x2, y2 = end
    for i in range(glow_layers, 0, -1):
        alpha = int(55 * (i / glow_layers))
        extra = int(max_extra * (i / glow_layers))
        glow_color = (*color, alpha)
        glow_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        pygame.draw.line(glow_surf, glow_color, start, end, width + extra)
        surface.blit(glow_surf, (0, 0))
    pygame.draw.line(surface, color, start, end, width)


def draw_glow_circle(surface, color, center, radius, width=0, glow_layers=5, max_extra=14):
    """Dibuja un círculo (relleno o contorno) con halo de luz alrededor."""
    for i in range(glow_layers, 0, -1):
        alpha = int(50 * (i / glow_layers))
        extra = int(max_extra * (i / glow_layers))
        glow_surf = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        glow_color = (*color, alpha)
        w = 0 if width == 0 else width + extra
        pygame.draw.circle(glow_surf, glow_color, center, radius + extra, w)
        surface.blit(glow_surf, (0, 0))
    pygame.draw.circle(surface, color, center, radius, width)


def draw_glow_text(surface, font, text, color, center, glow_color=None, glow_radius=6):
    """Renderiza texto con un leve halo detrás (varias copias desplazadas
    con transparencia) para dar sensación de luz de neón."""
    glow_color = glow_color or color
    base = font.render(text, True, color)
    rect = base.get_rect(center=center)

    glow_surf = pygame.Surface(
        (rect.width + glow_radius * 4, rect.height + glow_radius * 4), pygame.SRCALPHA
    )
    glow_text = font.render(text, True, glow_color)
    gx, gy = glow_surf.get_width() // 2, glow_surf.get_height() // 2
    for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)]:
        gt = glow_text.copy()
        gt.set_alpha(40)
        r = gt.get_rect(center=(gx + dx * 2, gy + dy * 2))
        glow_surf.blit(gt, r)
    glow_rect = glow_surf.get_rect(center=center)
    surface.blit(glow_surf, glow_rect)
    surface.blit(base, rect)


# --------------------------------------------------------------------- #
# Fondo de circuitos cuántico animado
# --------------------------------------------------------------------- #
class CircuitBackground:
    """
    Genera una red de líneas tipo 'circuito impreso' sobre el fondo,
    con nodos que pulsan suavemente (efecto de energía viajando por
    las trazas) y estrellas/partículas de fondo tipo 'campo cuántico'.
    """

    def __init__(self, width, height, node_count=26, seed=None):
        self.width = width
        self.height = height
        rng = random.Random(seed)

        # Genera nodos en una grilla ligeramente perturbada, luego
        # conecta cada nodo con 1-2 vecinos cercanos para simular pistas.
        cols, rows = 7, 6
        self.nodes = []
        for r in range(rows):
            for c in range(cols):
                x = (c + 0.5) * width / cols + rng.uniform(-25, 25)
                y = (r + 0.5) * height / rows + rng.uniform(-25, 25)
                self.nodes.append([x, y])

        self.edges = []
        for i, (x1, y1) in enumerate(self.nodes):
            dists = []
            for j, (x2, y2) in enumerate(self.nodes):
                if i == j:
                    continue
                d = math.hypot(x1 - x2, y1 - y2)
                dists.append((d, j))
            dists.sort()
            for _, j in dists[:2]:
                edge = tuple(sorted((i, j)))
                if edge not in self.edges:
                    self.edges.append(edge)

        # Pequeñas partículas de "polvo cuántico" flotando de fondo
        self.dust = [
            {
                "x": rng.uniform(0, width),
                "y": rng.uniform(0, height),
                "r": rng.uniform(0.6, 1.8),
                "speed": rng.uniform(4, 14),
                "phase": rng.uniform(0, math.tau),
            }
            for _ in range(70)
        ]

        self.time = 0.0

    def update(self, dt):
        self.time += dt
        for d in self.dust:
            d["y"] -= d["speed"] * dt
            if d["y"] < -5:
                d["y"] = self.height + 5
                d["x"] = random.uniform(0, self.width)

    def draw(self, surface):
        surface.fill(theme.BG_DARK)

        # Sutil viñeta / degradado radial simulado con círculos
        # (barato en rendimiento, evita crear superficies nuevas cada frame)

        # Trazas de circuito
        for (i, j) in self.edges:
            x1, y1 = self.nodes[i]
            x2, y2 = self.nodes[j]
            pygame.draw.line(surface, theme.CYAN_DIM, (x1, y1), (x2, y2), 1)

        # Pulso de energía viajando por algunas trazas
        pulse_edges = self.edges[:: max(1, len(self.edges) // 10)]
        for (i, j) in pulse_edges:
            x1, y1 = self.nodes[i]
            x2, y2 = self.nodes[j]
            t = (math.sin(self.time * 1.5 + i * 0.7) + 1) / 2
            px = x1 + (x2 - x1) * t
            py = y1 + (y2 - y1) * t
            pygame.draw.circle(surface, theme.CYAN, (int(px), int(py)), 2)

        # Nodos con leve pulso de brillo
        for idx, (x, y) in enumerate(self.nodes):
            pulse = (math.sin(self.time * 2 + idx) + 1) / 2
            radius = 2 + pulse * 1.5
            alpha = 60 + int(pulse * 90)
            node_surf = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(node_surf, (*theme.CYAN, alpha), (5, 5), radius)
            surface.blit(node_surf, (x - 5, y - 5))

        # Polvo cuántico
        for d in self.dust:
            tw = (math.sin(self.time * 3 + d["phase"]) + 1) / 2
            alpha = int(40 + tw * 90)
            dust_surf = pygame.Surface((6, 6), pygame.SRCALPHA)
            pygame.draw.circle(dust_surf, (*theme.WHITE_GLOW, alpha), (3, 3), d["r"])
            surface.blit(dust_surf, (d["x"] - 3, d["y"] - 3))


# --------------------------------------------------------------------- #
# Sistema de partículas para "explosión" cuántica al colocar una ficha
# --------------------------------------------------------------------- #
class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "max_life", "color", "radius")

    def __init__(self, x, y, vx, vy, life, color, radius):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.life = life
        self.max_life = life
        self.color = color
        self.radius = radius

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.96
        self.vy *= 0.96
        self.life -= dt
        return self.life > 0

    def draw(self, surface):
        t = max(0.0, self.life / self.max_life)
        alpha = int(255 * t)
        radius = max(1, int(self.radius * t))
        p_surf = pygame.Surface((radius * 4, radius * 4), pygame.SRCALPHA)
        pygame.draw.circle(
            p_surf, (*self.color, alpha), (radius * 2, radius * 2), radius
        )
        surface.blit(p_surf, (self.x - radius * 2, self.y - radius * 2))


class ParticleSystem:
    def __init__(self):
        self.particles = []

    def burst(self, x, y, color, count=24, speed_range=(60, 220), life_range=(0.4, 0.9)):
        for _ in range(count):
            angle = random.uniform(0, math.tau)
            speed = random.uniform(*speed_range)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            life = random.uniform(*life_range)
            radius = random.uniform(1.5, 4.0)
            self.particles.append(Particle(x, y, vx, vy, life, color, radius))

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
