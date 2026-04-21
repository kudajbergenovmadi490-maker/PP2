"""
main.py – Racer Game (Practice 10)
Based on: https://coderslegacy.com/python/python-pygame-tutorial/ (Parts 1-3)

Extra features added:
  • Randomly appearing coins on the road
  • Coin counter displayed in the top-right corner
  • Full code comments

Controls:
  ← / →   Move car left / right
  ESC      Quit
"""

import sys
import random
import pygame

# ─────────────────────────────────────────────────────────────────────────────
#  Constants
# ─────────────────────────────────────────────────────────────────────────────
WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 500
FPS           = 60

# Road lane boundaries (pixels from left edge)
LANE_LEFT   = 80
LANE_RIGHT  = 420

# Colours
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GREY    = (50,  50,  50)
YELLOW  = (255, 220,  0)
RED     = (220,  30,  30)
GREEN   = (30,  200,  60)
BLUE    = (30,  120, 220)

# Road stripe animation
STRIPE_HEIGHT = 50
STRIPE_GAP    = 50
STRIPE_X      = WINDOW_WIDTH // 2 - 5   # centre line x-position
STRIPE_WIDTH  = 10


# ─────────────────────────────────────────────────────────────────────────────
#  Road / background
# ─────────────────────────────────────────────────────────────────────────────
class Road:
    """
    Draws the scrolling road with animated dashed centre-line stripes.
    """

    def __init__(self):
        # Starting y positions for all visible stripes
        self.stripes = list(range(-STRIPE_HEIGHT, WINDOW_HEIGHT + STRIPE_HEIGHT,
                                  STRIPE_HEIGHT + STRIPE_GAP))
        self.speed = 5   # pixels per frame the road scrolls down

    def update(self):
        """Move all stripes downward to simulate forward motion."""
        self.stripes = [y + self.speed for y in self.stripes]
        # Recycle stripe back to top when it goes off-screen
        self.stripes = [y if y < WINDOW_HEIGHT else y - (WINDOW_HEIGHT + STRIPE_HEIGHT + STRIPE_GAP)
                        for y in self.stripes]

    def draw(self, surface: pygame.Surface):
        # Grey road surface
        pygame.draw.rect(surface, GREY, (LANE_LEFT, 0,
                                         LANE_RIGHT - LANE_LEFT, WINDOW_HEIGHT))
        # White dashed centre-line stripes
        for y in self.stripes:
            pygame.draw.rect(surface, WHITE,
                             (STRIPE_X, y, STRIPE_WIDTH, STRIPE_HEIGHT))


# ─────────────────────────────────────────────────────────────────────────────
#  Player car
# ─────────────────────────────────────────────────────────────────────────────
class PlayerCar:
    """
    The player-controlled car.  Moves left/right with arrow keys.
    """

    WIDTH  = 40
    HEIGHT = 70
    SPEED  = 5   # pixels per frame

    def __init__(self):
        # Start in the centre of the road at the bottom
        self.x = WINDOW_WIDTH  // 2 - self.WIDTH // 2
        self.y = WINDOW_HEIGHT - self.HEIGHT - 20
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def update(self, keys):
        """
        Move left or right based on held keys.
        Clamps position to road boundaries.

        Args:
            keys : result of pygame.key.get_pressed()
        """
        if keys[pygame.K_LEFT]:
            self.x -= self.SPEED
        if keys[pygame.K_RIGHT]:
            self.x += self.SPEED

        # Boundary clamping – car stays inside the road
        self.x = max(LANE_LEFT, min(self.x, LANE_RIGHT - self.WIDTH))
        self.rect.x = self.x

    def draw(self, surface: pygame.Surface):
        """Draw the player car as a simple blue rectangle with details."""
        r = self.rect
        # Car body
        pygame.draw.rect(surface, BLUE, r, border_radius=6)
        # Windshield
        pygame.draw.rect(surface, (180, 220, 255),
                         (r.x + 6, r.y + 8, r.width - 12, 18), border_radius=3)
        # Rear window
        pygame.draw.rect(surface, (180, 220, 255),
                         (r.x + 6, r.y + r.height - 26, r.width - 12, 14),
                         border_radius=3)
        # Wheels (4 black rectangles)
        wheel_w, wheel_h = 10, 16
        pygame.draw.rect(surface, BLACK, (r.x - wheel_w + 2, r.y + 8,          wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x + r.width - 2, r.y + 8,          wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x - wheel_w + 2, r.y + r.height - 24, wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x + r.width - 2, r.y + r.height - 24, wheel_w, wheel_h), border_radius=3)


# ─────────────────────────────────────────────────────────────────────────────
#  Enemy car
# ─────────────────────────────────────────────────────────────────────────────
class EnemyCar:
    """
    An oncoming enemy car that scrolls down the screen.
    Spawns at a random lane position near the top of the road.
    """

    WIDTH  = 40
    HEIGHT = 70

    # Two lane x-positions for enemies
    LANES = [LANE_LEFT + 10, LANE_RIGHT - WIDTH - 10]

    def __init__(self, speed: int = 5):
        self.speed = speed
        self.x = random.choice(self.LANES)
        self.y = -self.HEIGHT   # start just above the screen
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def update(self):
        """Move the enemy car downward."""
        self.y += self.speed
        self.rect.y = self.y

    def is_off_screen(self) -> bool:
        return self.y > WINDOW_HEIGHT

    def draw(self, surface: pygame.Surface):
        """Draw the enemy car as a red rectangle with details."""
        r = self.rect
        pygame.draw.rect(surface, RED, r, border_radius=6)
        pygame.draw.rect(surface, (255, 160, 160),
                         (r.x + 6, r.y + 8, r.width - 12, 18), border_radius=3)
        pygame.draw.rect(surface, (255, 160, 160),
                         (r.x + 6, r.y + r.height - 26, r.width - 12, 14),
                         border_radius=3)
        wheel_w, wheel_h = 10, 16
        pygame.draw.rect(surface, BLACK, (r.x - wheel_w + 2, r.y + 8,              wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x + r.width - 2, r.y + 8,              wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x - wheel_w + 2, r.y + r.height - 24,  wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x + r.width - 2, r.y + r.height - 24,  wheel_w, wheel_h), border_radius=3)


# ─────────────────────────────────────────────────────────────────────────────
#  Coin  (Extra feature #1 – randomly appearing coins)
# ─────────────────────────────────────────────────────────────────────────────
class Coin:
    """
    A gold coin that appears randomly on the road.
    Collected when the player car overlaps it.
    """

    RADIUS = 12

    def __init__(self, speed: int = 5):
        self.speed = speed
        # Random x inside the road, clear of the edges
        self.x = random.randint(LANE_LEFT + self.RADIUS + 5,
                                LANE_RIGHT - self.RADIUS - 5)
        self.y = -self.RADIUS   # start just above the screen
        self.rect = pygame.Rect(self.x - self.RADIUS, self.y - self.RADIUS,
                                self.RADIUS * 2, self.RADIUS * 2)

    def update(self):
        """Scroll the coin downward."""
        self.y += self.speed
        self.rect.center = (self.x, self.y)

    def is_off_screen(self) -> bool:
        return self.y - self.RADIUS > WINDOW_HEIGHT

    def draw(self, surface: pygame.Surface):
        """Draw the coin as a shiny gold circle."""
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.RADIUS)
        pygame.draw.circle(surface, (200, 160, 0), (self.x, self.y), self.RADIUS, 2)
        # Inner shine
        pygame.draw.circle(surface, (255, 240, 100),
                           (self.x - 3, self.y - 3), self.RADIUS // 3)


# ─────────────────────────────────────────────────────────────────────────────
#  HUD
# ─────────────────────────────────────────────────────────────────────────────
def draw_hud(surface: pygame.Surface,
             font: pygame.font.Font,
             score: int,
             coins: int) -> None:
    """
    Draws the heads-up display.

    Args:
        surface : display surface
        font    : pygame font object
        score   : distance-based score
        coins   : number of collected coins  (Extra feature #2)
    """
    # Score – top left
    score_surf = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_surf, (10, 10))

    # Coin counter – top right  (Extra feature #2)
    coin_surf = font.render(f"🪙 Coins: {coins}", True, YELLOW)
    surface.blit(coin_surf, (WINDOW_WIDTH - coin_surf.get_width() - 10, 10))


def draw_game_over(surface: pygame.Surface,
                   big_font: pygame.font.Font,
                   font: pygame.font.Font,
                   score: int,
                   coins: int) -> None:
    """Renders a semi-transparent game-over overlay."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    go_surf  = big_font.render("GAME OVER", True, RED)
    sc_surf  = font.render(f"Score: {score}   Coins: {coins}", True, WHITE)
    rst_surf = font.render("Press R to restart  |  ESC to quit", True, GREY)

    surface.blit(go_surf,  go_surf.get_rect(center=(WINDOW_WIDTH//2, 180)))
    surface.blit(sc_surf,  sc_surf.get_rect(center=(WINDOW_WIDTH//2, 240)))
    surface.blit(rst_surf, rst_surf.get_rect(center=(WINDOW_WIDTH//2, 290)))


# ─────────────────────────────────────────────────────────────────────────────
#  Game state reset
# ─────────────────────────────────────────────────────────────────────────────
def reset_game():
    """Returns a fresh game-state dictionary."""
    return {
        "road"      : Road(),
        "player"    : PlayerCar(),
        "enemies"   : [],
        "coins"     : [],           # list of active Coin objects
        "score"     : 0,
        "coin_count": 0,            # collected coins
        "speed"     : 5,
        "enemy_timer" : 0,          # frames since last enemy spawn
        "coin_timer"  : 0,          # frames since last coin spawn
        "game_over" : False,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Racer")
    clock  = pygame.time.Clock()

    font     = pygame.font.SysFont("Segoe UI", 20, bold=True)
    big_font = pygame.font.SysFont("Segoe UI", 48, bold=True)

    state = reset_game()

    running = True
    while running:
        # ── Events ───────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_r and state["game_over"]:
                    state = reset_game()

        if not state["game_over"]:
            keys = pygame.key.get_pressed()

            # ── Update road ──────────────────────────────────────────────────
            state["road"].update()

            # ── Update player ────────────────────────────────────────────────
            state["player"].update(keys)

            # ── Spawn enemies every ~90 frames ──────────────────────────────
            state["enemy_timer"] += 1
            if state["enemy_timer"] >= 90:
                state["enemies"].append(EnemyCar(speed=state["speed"]))
                state["enemy_timer"] = 0

            # ── Spawn coins randomly every 120–240 frames  (Extra feature #1)
            state["coin_timer"] += 1
            if state["coin_timer"] >= random.randint(120, 240):
                state["coins"].append(Coin(speed=state["speed"]))
                state["coin_timer"] = 0

            # ── Update enemies & check collision ────────────────────────────
            player_rect = state["player"].rect
            for enemy in state["enemies"][:]:
                enemy.update()
                if enemy.is_off_screen():
                    state["enemies"].remove(enemy)
                elif player_rect.colliderect(enemy.rect):
                    state["game_over"] = True

            # ── Update coins & check collection  (Extra feature #1) ─────────
            for coin in state["coins"][:]:
                coin.update()
                if coin.is_off_screen():
                    state["coins"].remove(coin)
                elif player_rect.colliderect(coin.rect):
                    state["coin_count"] += 1   # collect coin
                    state["coins"].remove(coin)

            # ── Score increases every frame ──────────────────────────────────
            state["score"] += 1

            # ── Gradually increase difficulty ────────────────────────────────
            if state["score"] % 500 == 0:
                state["speed"] = min(state["speed"] + 1, 15)
                state["road"].speed = state["speed"]

        # ── Draw ─────────────────────────────────────────────────────────────
        screen.fill((34, 139, 34))   # green grass on sides
        state["road"].draw(screen)

        for enemy in state["enemies"]:
            enemy.draw(screen)
        for coin in state["coins"]:
            coin.draw(screen)
        state["player"].draw(screen)

        draw_hud(screen, font, state["score"], state["coin_count"])

        if state["game_over"]:
            draw_game_over(screen, big_font, font,
                           state["score"], state["coin_count"])

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
