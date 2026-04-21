"""
main.py – Racer Game (Practice 11)
Extends Practice 10 Racer with:
  1. Randomly generating coins with different weights (Bronze/Silver/Gold)
  2. Enemy speed increases every N coins collected
  3. Full code comments

Controls:
  ← / →   Move car left / right
  ESC      Quit
  R        Restart after game over
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

# Road boundaries
LANE_LEFT   = 80
LANE_RIGHT  = 420

# Colours
WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GREY    = (50,  50,  50)
RED     = (220,  30,  30)
GREEN   = (34, 139,  34)
BLUE    = (30,  120, 220)

# Road stripe settings
STRIPE_HEIGHT = 50
STRIPE_GAP    = 50
STRIPE_X      = WINDOW_WIDTH // 2 - 5
STRIPE_WIDTH  = 10

# ── Coin settings ─────────────────────────────────────────────────────────────
# Each coin type has: (name, color, points, probability weight)
# Higher weight = appears more often
COIN_TYPES = [
    {"name": "Bronze", "color": (205, 127,  50), "points":  1, "weight": 60},
    {"name": "Silver", "color": (192, 192, 192), "points":  3, "weight": 30},
    {"name": "Gold",   "color": (255, 215,   0), "points": 10, "weight": 10},
]

# Enemy speed increases every N coins collected
SPEED_UP_EVERY_N_COINS = 5


# ─────────────────────────────────────────────────────────────────────────────
#  Road
# ─────────────────────────────────────────────────────────────────────────────
class Road:
    """Scrolling road with animated dashed centre-line stripes."""

    def __init__(self):
        self.stripes = list(range(-STRIPE_HEIGHT, WINDOW_HEIGHT + STRIPE_HEIGHT,
                                  STRIPE_HEIGHT + STRIPE_GAP))
        self.speed = 5

    def update(self):
        """Move stripes downward to simulate forward motion."""
        self.stripes = [y + self.speed for y in self.stripes]
        self.stripes = [y if y < WINDOW_HEIGHT
                        else y - (WINDOW_HEIGHT + STRIPE_HEIGHT + STRIPE_GAP)
                        for y in self.stripes]

    def draw(self, surface):
        # Grey road
        pygame.draw.rect(surface, GREY,
                         (LANE_LEFT, 0, LANE_RIGHT - LANE_LEFT, WINDOW_HEIGHT))
        # Dashed centre line
        for y in self.stripes:
            pygame.draw.rect(surface, WHITE,
                             (STRIPE_X, y, STRIPE_WIDTH, STRIPE_HEIGHT))


# ─────────────────────────────────────────────────────────────────────────────
#  Player car
# ─────────────────────────────────────────────────────────────────────────────
class PlayerCar:
    """Player-controlled car. Moves left/right with arrow keys."""

    WIDTH  = 40
    HEIGHT = 70
    SPEED  = 5

    def __init__(self):
        self.x = WINDOW_WIDTH  // 2 - self.WIDTH // 2
        self.y = WINDOW_HEIGHT - self.HEIGHT - 20
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def update(self, keys):
        """Move left or right, clamped to road boundaries."""
        if keys[pygame.K_LEFT]:
            self.x -= self.SPEED
        if keys[pygame.K_RIGHT]:
            self.x += self.SPEED
        self.x = max(LANE_LEFT, min(self.x, LANE_RIGHT - self.WIDTH))
        self.rect.x = self.x

    def draw(self, surface):
        r = self.rect
        pygame.draw.rect(surface, BLUE, r, border_radius=6)
        pygame.draw.rect(surface, (180, 220, 255),
                         (r.x + 6, r.y + 8, r.width - 12, 18), border_radius=3)
        pygame.draw.rect(surface, (180, 220, 255),
                         (r.x + 6, r.y + r.height - 26, r.width - 12, 14),
                         border_radius=3)
        ww, wh = 10, 16
        for cx in [r.x - ww + 2, r.x + r.width - 2]:
            for cy in [r.y + 8, r.y + r.height - 24]:
                pygame.draw.rect(surface, BLACK, (cx, cy, ww, wh), border_radius=3)


# ─────────────────────────────────────────────────────────────────────────────
#  Enemy car
# ─────────────────────────────────────────────────────────────────────────────
class EnemyCar:
    """Oncoming enemy car that scrolls down the screen."""

    WIDTH  = 40
    HEIGHT = 70
    LANES  = [LANE_LEFT + 10, LANE_RIGHT - 50]

    def __init__(self, speed=5):
        self.speed = speed
        self.x = random.choice(self.LANES)
        self.y = -self.HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def update(self):
        """Move enemy downward."""
        self.y += self.speed
        self.rect.y = self.y

    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT

    def draw(self, surface):
        r = self.rect
        pygame.draw.rect(surface, RED, r, border_radius=6)
        pygame.draw.rect(surface, (255, 160, 160),
                         (r.x + 6, r.y + 8, r.width - 12, 18), border_radius=3)
        pygame.draw.rect(surface, (255, 160, 160),
                         (r.x + 6, r.y + r.height - 26, r.width - 12, 14),
                         border_radius=3)
        ww, wh = 10, 16
        for cx in [r.x - ww + 2, r.x + r.width - 2]:
            for cy in [r.y + 8, r.y + r.height - 24]:
                pygame.draw.rect(surface, BLACK, (cx, cy, ww, wh), border_radius=3)


# ─────────────────────────────────────────────────────────────────────────────
#  Coin  (Feature 1 – different weights)
# ─────────────────────────────────────────────────────────────────────────────
class Coin:
    """
    A coin with a random type based on weighted probability.

    Types:
      Bronze (60% chance) = 1 point
      Silver (30% chance) = 3 points
      Gold   (10% chance) = 10 points
    """

    RADIUS = 12

    def __init__(self, speed=5):
        self.speed = speed

        # Pick coin type based on weights (Feature 1)
        weights     = [ct["weight"] for ct in COIN_TYPES]
        self.ctype  = random.choices(COIN_TYPES, weights=weights, k=1)[0]
        self.color  = self.ctype["color"]
        self.points = self.ctype["points"]
        self.name   = self.ctype["name"]

        # Random x position inside the road
        self.x = random.randint(LANE_LEFT + self.RADIUS + 5,
                                LANE_RIGHT - self.RADIUS - 5)
        self.y = -self.RADIUS
        self.rect = pygame.Rect(self.x - self.RADIUS, self.y - self.RADIUS,
                                self.RADIUS * 2, self.RADIUS * 2)

    def update(self):
        """Scroll coin downward."""
        self.y += self.speed
        self.rect.center = (self.x, self.y)

    def is_off_screen(self):
        return self.y - self.RADIUS > WINDOW_HEIGHT

    def draw(self, surface):
        """Draw coin with its type colour and a shine highlight."""
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.RADIUS)
        pygame.draw.circle(surface, BLACK, (self.x, self.y), self.RADIUS, 2)
        # Shine
        pygame.draw.circle(surface, (255, 255, 255),
                           (self.x - 3, self.y - 3), self.RADIUS // 4)


# ─────────────────────────────────────────────────────────────────────────────
#  HUD
# ─────────────────────────────────────────────────────────────────────────────
def draw_hud(surface, font, small_font, score, coin_points,
             coin_count, enemy_speed):
    """
    Draws the heads-up display.

    Args:
        score       : distance-based score
        coin_points : total points from coins
        coin_count  : number of coins collected
        enemy_speed : current enemy speed (shown so player knows difficulty)
    """
    # Score top left
    score_surf = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_surf, (10, 10))

    # Coin points top right
    coin_surf = font.render(f"Coins: {coin_points} pts", True, (255, 215, 0))
    surface.blit(coin_surf, (WINDOW_WIDTH - coin_surf.get_width() - 10, 10))

    # Coin legend below
    legend_y = 34
    for ct in COIN_TYPES:
        leg = small_font.render(
            f"{ct['name']}: {ct['points']}pt", True, ct["color"])
        surface.blit(leg, (WINDOW_WIDTH - leg.get_width() - 10, legend_y))
        legend_y += 18

    # Next speed-up progress
    next_speedup = SPEED_UP_EVERY_N_COINS - (coin_count % SPEED_UP_EVERY_N_COINS)
    prog = small_font.render(
        f"Speed up in: {next_speedup} coins | Enemy spd: {enemy_speed}",
        True, (200, 200, 200))
    surface.blit(prog, (10, 34))


def draw_game_over(surface, big_font, font, score, coin_points):
    """Semi-transparent game-over overlay."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))
    go  = big_font.render("GAME OVER", True, RED)
    sc  = font.render(f"Score: {score}   Coin Points: {coin_points}", True, WHITE)
    rst = font.render("R – Restart  |  ESC – Quit", True, (150, 150, 150))
    surface.blit(go,  go.get_rect(center=(WINDOW_WIDTH//2, 180)))
    surface.blit(sc,  sc.get_rect(center=(WINDOW_WIDTH//2, 240)))
    surface.blit(rst, rst.get_rect(center=(WINDOW_WIDTH//2, 290)))


# ─────────────────────────────────────────────────────────────────────────────
#  Game state
# ─────────────────────────────────────────────────────────────────────────────
def reset_game():
    """Returns a fresh game-state dictionary."""
    return {
        "road"        : Road(),
        "player"      : PlayerCar(),
        "enemies"     : [],
        "coins"       : [],
        "score"       : 0,
        "coin_points" : 0,   # total points from collected coins
        "coin_count"  : 0,   # total number of coins collected
        "enemy_speed" : 5,   # current enemy speed (Feature 2)
        "enemy_timer" : 0,
        "coin_timer"  : 0,
        "game_over"   : False,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen   = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Racer – Practice 11")
    clock    = pygame.time.Clock()
    font     = pygame.font.SysFont("Segoe UI", 18, bold=True)
    small    = pygame.font.SysFont("Segoe UI", 13)
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

            # Update road scroll
            state["road"].update()

            # Update player position
            state["player"].update(keys)

            # Spawn enemy every ~90 frames
            state["enemy_timer"] += 1
            if state["enemy_timer"] >= 90:
                state["enemies"].append(EnemyCar(speed=state["enemy_speed"]))
                state["enemy_timer"] = 0

            # Spawn coin every 120–240 frames randomly
            state["coin_timer"] += 1
            if state["coin_timer"] >= random.randint(120, 240):
                state["coins"].append(Coin(speed=state["enemy_speed"]))
                state["coin_timer"] = 0

            player_rect = state["player"].rect

            # Update enemies & collision check
            for enemy in state["enemies"][:]:
                enemy.update()
                if enemy.is_off_screen():
                    state["enemies"].remove(enemy)
                elif player_rect.colliderect(enemy.rect):
                    state["game_over"] = True

            # Update coins & collection check
            for coin in state["coins"][:]:
                coin.update()
                if coin.is_off_screen():
                    state["coins"].remove(coin)
                elif player_rect.colliderect(coin.rect):
                    # Add points based on coin type (Feature 1)
                    state["coin_points"] += coin.points
                    state["coin_count"]  += 1
                    state["coins"].remove(coin)

                    # Feature 2 – increase enemy speed every N coins
                    if state["coin_count"] % SPEED_UP_EVERY_N_COINS == 0:
                        state["enemy_speed"] = min(state["enemy_speed"] + 1, 15)
                        state["road"].speed  = state["enemy_speed"]

            # Increase score every frame (distance based)
            state["score"] += 1

        # ── Draw ─────────────────────────────────────────────────────────────
        screen.fill(GREEN)
        state["road"].draw(screen)
        for enemy in state["enemies"]:
            enemy.draw(screen)
        for coin in state["coins"]:
            coin.draw(screen)
        state["player"].draw(screen)
        draw_hud(screen, font, small,
                 state["score"], state["coin_points"],
                 state["coin_count"], state["enemy_speed"])

        if state["game_over"]:
            draw_game_over(screen, big_font, font,
                           state["score"], state["coin_points"])

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
