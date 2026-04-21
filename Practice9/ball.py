"""
ball.py - Ball entity for the Moving Ball game.
Manages position, drawing, and boundary-checked movement.
"""

import pygame


class Ball:
    """
    A red circle that can be moved with arrow keys.

    Attributes:
        x, y    : centre position of the ball (pixels)
        radius  : radius in pixels (default 25 → 50×50 bounding box)
        color   : RGB colour tuple
        step    : pixels to move per key press
    """

    def __init__(self,
                 x: int, y: int,
                 radius: int = 25,
                 color: tuple = (220, 50, 50),
                 step: int = 20) -> None:
        self.x      = x
        self.y      = y
        self.radius = radius
        self.color  = color
        self.step   = step

    # ── Movement ──────────────────────────────────────────────────────────────

    def move(self,
             dx: int, dy: int,
             screen_width: int, screen_height: int) -> None:
        """
        Moves the ball by (dx, dy) pixels if the destination is fully
        within the screen boundaries.  Out-of-bounds moves are silently ignored.

        Args:
            dx, dy          : pixel delta (positive = right/down)
            screen_width    : width of the display surface
            screen_height   : height of the display surface
        """
        new_x = self.x + dx
        new_y = self.y + dy

        # Boundary check: the entire circle must stay inside the window
        if (self.radius <= new_x <= screen_width  - self.radius and
                self.radius <= new_y <= screen_height - self.radius):
            self.x = new_x
            self.y = new_y
        # else: do nothing (ignore the out-of-bounds input)

    def handle_keydown(self,
                       key: int,
                       screen_width: int,
                       screen_height: int) -> None:
        """
        Translates a pygame key constant into a directional move.

        Args:
            key           : pygame key constant (e.g. pygame.K_UP)
            screen_width  : width of the display surface
            screen_height : height of the display surface
        """
        step = self.step
        if key == pygame.K_UP:
            self.move(0, -step, screen_width, screen_height)
        elif key == pygame.K_DOWN:
            self.move(0,  step, screen_width, screen_height)
        elif key == pygame.K_LEFT:
            self.move(-step, 0, screen_width, screen_height)
        elif key == pygame.K_RIGHT:
            self.move( step, 0, screen_width, screen_height)

    # ── Drawing ───────────────────────────────────────────────────────────────

    def draw(self, surface: pygame.Surface) -> None:
        """
        Draws the ball on *surface* with a subtle shadow for depth.

        Args:
            surface : pygame.Surface to draw onto
        """
        # Shadow (slightly offset, semi-transparent dark circle)
        shadow_surf = pygame.Surface(
            (self.radius * 2 + 4, self.radius * 2 + 4), pygame.SRCALPHA)
        pygame.draw.circle(shadow_surf, (0, 0, 0, 60),
                           (self.radius + 2, self.radius + 4), self.radius)
        surface.blit(shadow_surf, (self.x - self.radius - 2,
                                   self.y - self.radius - 2))

        # Main ball
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)

        # Highlight (small white oval near top-left for 3-D look)
        highlight_surf = pygame.Surface(
            (self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.ellipse(highlight_surf, (255, 255, 255, 80),
                            (self.radius // 2 - 4,
                             self.radius // 2 - 6,
                             self.radius // 2,
                             self.radius // 3))
        surface.blit(highlight_surf, (self.x - self.radius, self.y - self.radius))
