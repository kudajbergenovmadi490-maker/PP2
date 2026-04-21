"""
main.py – Snake Game (Practice 11)
Extends Practice 10 Snake with:
  1. Randomly generating food with different weights (points)
  2. Foods disappear after a timer
  3. Full code comments

Controls:
  ← ↑ → ↓   Change direction
  R          Restart after game over
  ESC        Quit
"""

import sys
import random
import pygame

# ─────────────────────────────────────────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────────────────────────────────────────
CELL        = 20
COLS        = 25
ROWS        = 25
HUD_HEIGHT  = 50

WINDOW_WIDTH  = CELL * COLS
WINDOW_HEIGHT = CELL * ROWS + HUD_HEIGHT

FOODS_PER_LEVEL  = 3      # foods needed to level up
BASE_MOVE_DELAY  = 150    # ms between moves at level 1
SPEED_STEP       = 10     # ms reduction per level
MIN_MOVE_DELAY   = 40     # fastest possible speed

# ── Food types (Feature 1 – different weights) ────────────────────────────────
# Each food type: name, color, points, weight (probability), lifetime (ms)
FOOD_TYPES = [
    {"name": "Apple",   "color": (220,  50,  50), "points":  1,
     "weight": 60, "lifetime": 8000},   # common,   8 seconds
    {"name": "Cherry",  "color": (180,   0, 100), "points":  3,
     "weight": 30, "lifetime": 5000},   # uncommon, 5 seconds
    {"name": "Star",    "color": (255, 215,   0), "points": 10,
     "weight": 10, "lifetime": 3000},   # rare,     3 seconds
]

# Colours
BG_COLOR    = (15,  15,  25)
GRID_COLOR  = (30,  30,  45)
WALL_COLOR  = (80,  80, 110)
SNAKE_HEAD  = (80,  220,  80)
SNAKE_BODY  = (50,  170,  50)
TEXT_COLOR  = (230, 230, 230)
MUTED_COLOR = (120, 120, 150)
LEVEL_COLOR = (100, 180, 255)
HUD_BG      = (20,  20,  35)


# ─────────────────────────────────────────────────────────────────────────────
#  Helper
# ─────────────────────────────────────────────────────────────────────────────
def cell_rect(col, row):
    """Converts grid (col, row) to pixel Rect."""
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * CELL, CELL, CELL)


# ─────────────────────────────────────────────────────────────────────────────
#  Snake
# ─────────────────────────────────────────────────────────────────────────────
class Snake:
    """
    Manages the snake body, direction, and movement.
    Body is a list of (col, row) tuples; index 0 = head.
    """

    def __init__(self):
        mid_col = COLS // 2
        mid_row = ROWS // 2
        self.body = [(mid_col, mid_row),
                     (mid_col - 1, mid_row),
                     (mid_col - 2, mid_row)]
        self.direction         = (1, 0)
        self.pending_direction = (1, 0)
        self.grew = False

    def set_direction(self, dcol, drow):
        """Queue direction change; prevent reversing into self."""
        cur_dc, cur_dr = self.direction
        if (dcol, drow) != (-cur_dc, -cur_dr):
            self.pending_direction = (dcol, drow)

    def move(self):
        """Move snake one cell forward."""
        self.direction = self.pending_direction
        dc, dr = self.direction
        hc, hr = self.body[0]
        self.body.insert(0, (hc + dc, hr + dr))
        if self.grew:
            self.grew = False   # keep tail (snake grows)
        else:
            self.body.pop()     # remove tail (normal move)

    def grow(self):
        """Signal snake to grow on next move."""
        self.grew = True

    @property
    def head(self):
        return self.body[0]

    def check_self_collision(self):
        return self.head in self.body[1:]

    def draw(self, surface):
        for i, (col, row) in enumerate(self.body):
            rect  = cell_rect(col, row)
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(surface, color,
                             rect.inflate(-2, -2), border_radius=4)


# ─────────────────────────────────────────────────────────────────────────────
#  Food  (Features 1 & 2)
# ─────────────────────────────────────────────────────────────────────────────
class Food:
    """
    A food item with a random type based on weighted probability.
    Disappears after its lifetime expires. (Feature 2)

    Types:
      Apple  (60% chance) = 1 pt,  8 seconds
      Cherry (30% chance) = 3 pts, 5 seconds
      Star   (10% chance) = 10 pts, 3 seconds
    """

    def __init__(self, snake_body):
        # Feature 1 – pick type by weight
        weights    = [ft["weight"] for ft in FOOD_TYPES]
        self.ftype = random.choices(FOOD_TYPES, weights=weights, k=1)[0]

        self.color    = self.ftype["color"]
        self.points   = self.ftype["points"]
        self.name     = self.ftype["name"]
        self.lifetime = self.ftype["lifetime"]   # total ms before disappearing

        # Spawn time (ms) – used to track remaining lifetime
        self.spawn_time = pygame.time.get_ticks()

        # Random valid position (not on wall, not on snake)
        self.pos = self._random_pos(snake_body)

    def _random_pos(self, snake_body):
        """Pick a cell that is not a wall and not on the snake."""
        available = [
            (c, r)
            for c in range(1, COLS - 1)
            for r in range(1, ROWS - 1)
            if (c, r) not in snake_body
        ]
        return random.choice(available) if available else (COLS // 2, ROWS // 2)

    def is_expired(self):
        """
        Feature 2 – returns True if the food's lifetime has run out.
        """
        elapsed = pygame.time.get_ticks() - self.spawn_time
        return elapsed >= self.lifetime

    def time_remaining_fraction(self):
        """Returns a 0.0–1.0 fraction of lifetime remaining (1 = fresh)."""
        elapsed = pygame.time.get_ticks() - self.spawn_time
        return max(0.0, 1.0 - elapsed / self.lifetime)

    def draw(self, surface):
        """
        Draw food as a circle. It blinks when almost expired to warn the player.
        """
        fraction = self.time_remaining_fraction()

        # Blink fast when less than 25% lifetime left
        if fraction < 0.25:
            # Blink every 200ms
            if (pygame.time.get_ticks() // 200) % 2 == 0:
                return   # skip drawing (blink effect)

        rect   = cell_rect(*self.pos)
        center = rect.center
        radius = CELL // 2 - 2

        # Draw food circle
        pygame.draw.circle(surface, self.color, center, radius)

        # Timer bar below the food (shrinks as time runs out)
        bar_w = int(CELL * fraction)
        bar_rect = pygame.Rect(rect.x, rect.bottom - 4, bar_w, 3)
        bar_color = (80, 255, 80) if fraction > 0.5 else (255, 80, 80)
        pygame.draw.rect(surface, bar_color, bar_rect)

        # Points label
        # (only draw if cell is big enough)
        if CELL >= 20:
            pts_font = pygame.font.SysFont("Arial", 10, bold=True)
            pts_surf = pts_font.render(str(self.points), True, (255, 255, 255))
            surface.blit(pts_surf, pts_surf.get_rect(center=center))


# ─────────────────────────────────────────────────────────────────────────────
#  Drawing helpers
# ─────────────────────────────────────────────────────────────────────────────
def draw_grid(surface):
    """Draw background grid and border walls."""
    surface.fill(BG_COLOR)
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(surface, GRID_COLOR, cell_rect(c, r), 1)
            if c == 0 or c == COLS - 1 or r == 0 or r == ROWS - 1:
                pygame.draw.rect(surface, WALL_COLOR,
                                 cell_rect(c, r), border_radius=2)


def draw_hud(surface, font, score, level, foods_in_level):
    """Draw HUD bar at top showing score, level, and progress."""
    pygame.draw.rect(surface, HUD_BG, (0, 0, WINDOW_WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, WALL_COLOR,
                     (0, HUD_HEIGHT), (WINDOW_WIDTH, HUD_HEIGHT), 2)

    score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
    level_surf = font.render(f"Level: {level}", True, LEVEL_COLOR)
    prog_surf  = font.render(
        f"Next: {foods_in_level}/{FOODS_PER_LEVEL}", True, MUTED_COLOR)

    # Food type legend
    legend_parts = []
    for ft in FOOD_TYPES:
        legend_parts.append((ft["name"][0], ft["color"], ft["points"]))

    surface.blit(score_surf, (10, 14))
    surface.blit(level_surf, (WINDOW_WIDTH // 2 - level_surf.get_width() // 2, 14))
    surface.blit(prog_surf,  (WINDOW_WIDTH - prog_surf.get_width() - 10, 14))


def draw_food_legend(surface, small_font):
    """Draw food type legend in the corner."""
    x, y = 10, HUD_HEIGHT + 5
    for ft in FOOD_TYPES:
        pygame.draw.circle(surface, ft["color"], (x + 6, y + 6), 5)
        label = small_font.render(
            f"{ft['name']} = {ft['points']}pt ({ft['lifetime']//1000}s)",
            True, ft["color"])
        surface.blit(label, (x + 16, y))
        y += 18


def draw_game_over(surface, big_font, font, score, level):
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))
    go  = big_font.render("GAME OVER", True, (220, 50, 50))
    sc  = font.render(f"Score: {score}   Level: {level}", True, TEXT_COLOR)
    rst = font.render("R – Restart   |   ESC – Quit", True, MUTED_COLOR)
    cx  = WINDOW_WIDTH // 2
    cy  = WINDOW_HEIGHT // 2
    surface.blit(go,  go.get_rect(center=(cx, cy - 50)))
    surface.blit(sc,  sc.get_rect(center=(cx, cy + 10)))
    surface.blit(rst, rst.get_rect(center=(cx, cy + 50)))


# ─────────────────────────────────────────────────────────────────────────────
#  Game helpers
# ─────────────────────────────────────────────────────────────────────────────
def move_delay_for_level(level):
    """Returns ms delay between moves. Decreases with each level."""
    return max(MIN_MOVE_DELAY, BASE_MOVE_DELAY - (level - 1) * SPEED_STEP)


def reset_game():
    snake = Snake()
    return {
        "snake"          : snake,
        "foods"          : [Food(snake.body)],   # list of active foods
        "score"          : 0,
        "level"          : 1,
        "foods_in_level" : 0,
        "last_move_time" : pygame.time.get_ticks(),
        "food_spawn_time": pygame.time.get_ticks(),
        "game_over"      : False,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen   = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake – Practice 11")
    clock    = pygame.time.Clock()
    font     = pygame.font.SysFont("Segoe UI", 18, bold=True)
    small    = pygame.font.SysFont("Segoe UI", 13)
    big_font = pygame.font.SysFont("Segoe UI", 48, bold=True)

    state = reset_game()

    running = True
    while running:
        now = pygame.time.get_ticks()

        # ── Events ───────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and state["game_over"]:
                    state = reset_game()
                elif event.key == pygame.K_UP:
                    state["snake"].set_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    state["snake"].set_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    state["snake"].set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    state["snake"].set_direction(1, 0)

        # ── Game logic ────────────────────────────────────────────────────────
        if not state["game_over"]:

            # Feature 2 – remove expired foods
            state["foods"] = [f for f in state["foods"] if not f.is_expired()]

            # Spawn a new food every 4 seconds if fewer than 3 on screen
            if now - state["food_spawn_time"] >= 4000:
                if len(state["foods"]) < 3:
                    state["foods"].append(Food(state["snake"].body))
                state["food_spawn_time"] = now

            # Ensure at least 1 food is always present
            if len(state["foods"]) == 0:
                state["foods"].append(Food(state["snake"].body))

            # Move snake on timer
            delay = move_delay_for_level(state["level"])
            if now - state["last_move_time"] >= delay:
                state["last_move_time"] = now
                snake = state["snake"]
                snake.move()

                col, row = snake.head

                # Wall collision check
                if col <= 0 or col >= COLS-1 or row <= 0 or row >= ROWS-1:
                    state["game_over"] = True

                # Self collision check
                elif snake.check_self_collision():
                    state["game_over"] = True

                else:
                    # Check food collection
                    for food in state["foods"][:]:
                        if snake.head == food.pos:
                            snake.grow()
                            state["score"]          += food.points   # Feature 1
                            state["foods_in_level"] += 1
                            state["foods"].remove(food)

                            # Spawn replacement food
                            state["foods"].append(Food(snake.body))

                            # Level up every FOODS_PER_LEVEL foods
                            if state["foods_in_level"] >= FOODS_PER_LEVEL:
                                state["level"]         += 1
                                state["foods_in_level"] = 0

        # ── Draw ─────────────────────────────────────────────────────────────
        draw_grid(screen)
        for food in state["foods"]:
            food.draw(screen)
        state["snake"].draw(screen)
        draw_hud(screen, font,
                 state["score"], state["level"], state["foods_in_level"])
        draw_food_legend(screen, small)

        if state["game_over"]:
            draw_game_over(screen, big_font, font,
                           state["score"], state["level"])

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
