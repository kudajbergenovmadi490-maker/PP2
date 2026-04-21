"""
main.py - Moving Ball Game

A red ball (radius 25, 50×50 bounding box) moves around a white
background using the arrow keys.  Movement is blocked at screen edges.

Controls:
  ↑ ↓ ← →   Move ball (20 px per press)
  Q / ESC    Quit
"""

import sys
import pygame
from ball import Ball

# ── Constants ────────────────────────────────────────────────────────────────
WINDOW_WIDTH  = 600
WINDOW_HEIGHT = 500
FPS           = 60

BG_COLOR      = (255, 255, 255)   # white background
BORDER_COLOR  = (200, 200, 200)   # subtle border hint
STEP_PX       = 20                # pixels per key press
BALL_RADIUS   = 25                # 25 px → 50×50 bounding box


def draw_hud(screen: pygame.Surface,
             ball: Ball,
             font: pygame.font.Font) -> None:
    """
    Draws the heads-up display showing current ball position and controls.

    Args:
        screen : display surface
        ball   : Ball instance
        font   : pygame font for rendering text
    """
    # Position info
    pos_text = font.render(
        f"Position: ({ball.x}, {ball.y})", True, (80, 80, 80))
    screen.blit(pos_text, (10, 10))

    # Control hint
    hint_text = font.render(
        "Arrow Keys: Move  |  Q / ESC: Quit", True, (150, 150, 150))
    screen.blit(hint_text, (10, WINDOW_HEIGHT - 28))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Moving Ball Game")
    clock = pygame.time.Clock()
    font  = pygame.font.SysFont("Segoe UI", 16)

    # Start the ball in the centre of the screen
    ball = Ball(
        x      = WINDOW_WIDTH  // 2,
        y      = WINDOW_HEIGHT // 2,
        radius = BALL_RADIUS,
        color  = (220, 50, 50),   # red
        step   = STEP_PX,
    )

    # ── Main loop ────────────────────────────────────────────────────────────
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Quit keys
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False
                # Movement keys – boundary check is inside ball.handle_keydown()
                else:
                    ball.handle_keydown(event.key, WINDOW_WIDTH, WINDOW_HEIGHT)

        # ── Render ───────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # Subtle border
        pygame.draw.rect(screen, BORDER_COLOR,
                         (0, 0, WINDOW_WIDTH, WINDOW_HEIGHT), 2)

        ball.draw(screen)
        draw_hud(screen, ball, font)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
