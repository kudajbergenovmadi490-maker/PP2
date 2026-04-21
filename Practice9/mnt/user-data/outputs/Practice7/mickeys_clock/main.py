"""
main.py - Mickey's Clock Application
Displays current minutes and seconds using Mickey Mouse hand graphics.

Controls:
  Q / ESC  → Quit
"""

import sys
import pygame
from clock import get_current_time, get_hand_angle, degrees_to_pygame_angle

# ── Constants ────────────────────────────────────────────────────────────────
WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 500
FPS           = 10          # Refresh rate (10 fps is plenty for a clock)
BG_COLOR      = (240, 240, 240)

# Center of the clock face on screen
CENTER_X = WINDOW_WIDTH  // 2
CENTER_Y = WINDOW_HEIGHT // 2

# Where the hand "pivot point" sits within the hand image (as a fraction).
# Adjust these if your image's pivot is not at the bottom-center.
PIVOT_X_FRACTION = 0.5   # horizontal center
PIVOT_Y_FRACTION = 0.85  # near the bottom of the image


def load_hand_image(path: str, scale: tuple[int, int]) -> pygame.Surface:
    """
    Loads and scales the hand image.  Falls back to a plain rectangle
    if the image file is not found, so the app still runs during development.

    Args:
        path  : file path to the PNG image
        scale : (width, height) to scale the image to

    Returns:
        A pygame.Surface containing the hand graphic.
    """
    try:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.smoothscale(img, scale)
        print(f"[INFO] Loaded hand image from '{path}'")
    except FileNotFoundError:
        print(f"[WARN] '{path}' not found – using placeholder rectangle.")
        img = pygame.Surface(scale, pygame.SRCALPHA)
        img.fill((30, 30, 30))          # dark-grey rectangle as placeholder
    return img


def draw_hand(screen: pygame.Surface,
              image: pygame.Surface,
              angle_deg: float) -> None:
    """
    Rotates the hand image and blits it so that the pivot point sits
    exactly at the clock centre.

    Args:
        screen    : target pygame display surface
        image     : unrotated hand surface
        angle_deg : clockwise angle from 12 o'clock (degrees)
    """
    pygame_angle = degrees_to_pygame_angle(angle_deg)

    # Rotate around the image's own centre (pygame default)
    rotated = pygame.transform.rotozoom(image, pygame_angle, 1.0)

    # Calculate where the pivot point ends up in the rotated image
    orig_w, orig_h = image.get_size()
    pivot_in_orig = pygame.math.Vector2(
        orig_w * PIVOT_X_FRACTION,
        orig_h * PIVOT_Y_FRACTION,
    )

    # The same pivot point after rotation
    offset = pivot_in_orig.rotate(-pygame_angle)   # rotate() is CCW in pygame

    # Top-left corner so that pivot lands on clock centre
    rot_w, rot_h = rotated.get_size()
    blit_x = CENTER_X - rot_w // 2 + (rot_w // 2 - int(offset.x))
    blit_y = CENTER_Y - rot_h // 2 + (rot_h // 2 - int(offset.y))

    screen.blit(rotated, (blit_x, blit_y))


def draw_clock_face(screen: pygame.Surface) -> None:
    """Draws a simple decorative clock face (circle + hour dots)."""
    # Outer ring
    pygame.draw.circle(screen, (80, 80, 80), (CENTER_X, CENTER_Y), 180, 3)
    # 12 tick marks
    for i in range(12):
        angle_rad = (i / 12) * 2 * 3.14159 - 3.14159 / 2
        inner_r = 165
        outer_r = 178
        sx = int(CENTER_X + inner_r * pygame.math.Vector2(1, 0).rotate(-i * 30).x)
        sy = int(CENTER_Y + inner_r * pygame.math.Vector2(1, 0).rotate(-i * 30).y)
        ex = int(CENTER_X + outer_r * pygame.math.Vector2(1, 0).rotate(-i * 30).x)
        ey = int(CENTER_Y + outer_r * pygame.math.Vector2(1, 0).rotate(-i * 30).y)
        pygame.draw.line(screen, (60, 60, 60), (sx, sy), (ex, ey), 2)
    # Centre pin
    pygame.draw.circle(screen, (50, 50, 50), (CENTER_X, CENTER_Y), 6)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Mickey's Clock")
    clock_tick = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28, bold=True)

    # Load hand image – both hands use the same graphic
    hand_img = load_hand_image("images/mickey_hand.png", scale=(40, 160))

    # ── Main loop ────────────────────────────────────────────────────────────
    running = True
    while running:
        # ── Event handling ───────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False

        # ── Get time ─────────────────────────────────────────────────────────
        minutes, seconds = get_current_time()

        # ── Draw background & clock face ─────────────────────────────────────
        screen.fill(BG_COLOR)
        draw_clock_face(screen)

        # ── Draw minute hand (right hand) ─────────────────────────────────────
        minute_angle = get_hand_angle(minutes, 60)
        draw_hand(screen, hand_img, minute_angle)

        # ── Draw second hand (left hand) ──────────────────────────────────────
        second_angle = get_hand_angle(seconds, 60)
        draw_hand(screen, hand_img, second_angle)

        # ── Display time as text ──────────────────────────────────────────────
        time_str = f"{minutes:02d}:{seconds:02d}"
        text_surf = font.render(time_str, True, (40, 40, 40))
        text_rect = text_surf.get_rect(center=(CENTER_X, WINDOW_HEIGHT - 40))
        screen.blit(text_surf, text_rect)

        # ── Legend ────────────────────────────────────────────────────────────
        legend = font.render("Right=Minutes  Left=Seconds  |  Q: Quit", True, (120, 120, 120))
        screen.blit(legend, (10, 10))

        pygame.display.flip()
        clock_tick.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
