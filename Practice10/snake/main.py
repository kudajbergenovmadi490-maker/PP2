"""
main.py – Snake Game (Practice 10)

Features:
  1. Wall/border collision detection – game ends if snake leaves the area
  2. Food spawns at random positions that are not on a wall or the snake body
  3. Levels – every 3 foods eaten advances the level
  4. Speed increases with each level
  5. Score and level counter displayed on screen
  6. Full code comments

Controls:
  ← ↑ → ↓   Change snake direction
  ESC        Quit
  R          Restart (after game over)
"""

import sys
import random
import pygame

# ─────────────────────────────────────────────────────────────────────────────
#  Configuration constants
# ─────────────────────────────────────────────────────────────────────────────
CELL        = 20          # size of one grid cell in pixels
COLS        = 25          # number of columns in the play area
ROWS        = 25          # number of rows in the play area
HUD_HEIGHT  = 50          # pixels reserved at top for HUD

WINDOW_WIDTH  = CELL * COLS
WINDOW_HEIGHT = CELL * ROWS + HUD_HEIGHT

# How many foods eaten to advance one level
FOODS_PER_LEVEL = 3

# Base speed (frames between snake moves) and speed increase per level
BASE_MOVE_DELAY = 150     # milliseconds between moves at level 1
SPEED_STEP      = 10      # ms to reduce per level (min 40 ms)
MIN_MOVE_DELAY  = 40

# Score awarded per food
SCORE_PER_FOOD  = 10

# Colours
BG_COLOR        = (15,  15,  25)
GRID_COLOR      = (30,  30,  45)
WALL_COLOR      = (80,  80, 110)
SNAKE_HEAD      = (80,  220,  80)
SNAKE_BODY      = (50,  170,  50)
FOOD_COLOR      = (230,  60,  60)
TEXT_COLOR      = (230, 230, 230)
MUTED_COLOR     = (120, 120, 150)
LEVEL_COLOR     = (100, 180, 255)
HUD_BG          = (20,  20,  35)


# ─────────────────────────────────────────────────────────────────────────────
#  Helper: grid → pixel conversion
# ─────────────────────────────────────────────────────────────────────────────
def cell_rect(col: int, row: int) -> pygame.Rect:
    """
    Converts a grid cell (col, row) to the pixel Rect it occupies.
    Rows are offset downward by HUD_HEIGHT.
    """
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * CELL, CELL, CELL)


# ─────────────────────────────────────────────────────────────────────────────
#  Snake
# ─────────────────────────────────────────────────────────────────────────────
class Snake:
    """
    Manages the snake's body, direction, and movement.

    The body is a list of (col, row) tuples; index 0 is the head.
    """

    def __init__(self):
        # Start in the middle of the grid, moving right, length 3
        mid_col = COLS // 2
        mid_row = ROWS // 2
        self.body = [(mid_col, mid_row),
                     (mid_col - 1, mid_row),
                     (mid_col - 2, mid_row)]
        self.direction = (1, 0)     # (dcol, drow): right
        self.pending_direction = (1, 0)
        self.grew = False           # flag set when food was eaten this step

    def set_direction(self, dcol: int, drow: int):
        """
        Queues a direction change.
        Prevents reversing directly into the snake's own body.
        """
        # Ignore if the new direction is directly opposite current
        cur_dc, cur_dr = self.direction
        if (dcol, drow) != (-cur_dc, -cur_dr):
            self.pending_direction = (dcol, drow)

    def move(self):
        """
        Moves the snake one cell in the current direction.
        If the snake just ate food (grew=True) the tail is not removed.
        """
        self.direction = self.pending_direction
        dc, dr = self.direction
        head_col, head_row = self.body[0]
        new_head = (head_col + dc, head_row + dr)
        self.body.insert(0, new_head)

        if self.grew:
            # Keep the tail – snake grows by one segment
            self.grew = False
        else:
            self.body.pop()   # remove tail to keep length the same

    def grow(self):
        """Signal that the snake should grow on the next move."""
        self.grew = True

    @property
    def head(self) -> tuple:
        return self.body[0]

    def check_self_collision(self) -> bool:
        """Returns True if the head overlaps any body segment."""
        return self.head in self.body[1:]

    def draw(self, surface: pygame.Surface):
        """Draws the snake with a distinct head colour."""
        for i, (col, row) in enumerate(self.body):
            rect = cell_rect(col, row)
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(surface, color, rect.inflate(-2, -2), border_radius=4)


# ─────────────────────────────────────────────────────────────────────────────
#  Food
# ─────────────────────────────────────────────────────────────────────────────
class Food:
    """
    A single food item placed at a random valid grid cell.

    A 'valid' cell is one that is:
      - not occupied by the snake body
      - not on the border wall (col 0, col COLS-1, row 0, row ROWS-1)
    """

    def __init__(self, snake_body: list):
        self.pos = self._random_pos(snake_body)

    def _random_pos(self, snake_body: list) -> tuple:
        """
        Picks a random cell that is not a wall and not occupied by the snake.
        Feature #2: food cannot appear on a wall or on the snake.
        """
        # Inner cells only (exclude the 1-cell border)
        available = [
            (c, r)
            for c in range(1, COLS - 1)
            for r in range(1, ROWS - 1)
            if (c, r) not in snake_body
        ]
        if not available:
            # Extremely unlikely – board is full; return a fallback
            return (COLS // 2, ROWS // 2)
        return random.choice(available)

    def draw(self, surface: pygame.Surface):
        """Draw the food as a red circle."""
        rect = cell_rect(*self.pos)
        center = rect.center
        radius = CELL // 2 - 2
        pygame.draw.circle(surface, FOOD_COLOR, center, radius)
        # Shine highlight
        pygame.draw.circle(surface, (255, 140, 140),
                           (center[0] - 3, center[1] - 3), radius // 3)


# ─────────────────────────────────────────────────────────────────────────────
#  Drawing helpers
# ─────────────────────────────────────────────────────────────────────────────
def draw_grid(surface: pygame.Surface):
    """Draw the background grid and border wall."""
    surface.fill(BG_COLOR)

    # Faint grid lines
    for c in range(COLS):
        for r in range(ROWS):
            rect = cell_rect(c, r)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

    # Border wall cells (feature #1 – these are the 'walls')
    for c in range(COLS):
        for r in range(ROWS):
            if c == 0 or c == COLS - 1 or r == 0 or r == ROWS - 1:
                pygame.draw.rect(surface, WALL_COLOR,
                                 cell_rect(c, r), border_radius=2)


def draw_hud(surface: pygame.Surface,
             font: pygame.font.Font,
             score: int,
             level: int,
             foods_in_level: int):
    """
    Draws the HUD bar at the top of the window.

    Args:
        surface        : display surface
        font           : pygame font
        score          : total score
        level          : current level number
        foods_in_level : foods eaten within the current level
    """
    pygame.draw.rect(surface, HUD_BG, (0, 0, WINDOW_WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, WALL_COLOR, (0, HUD_HEIGHT), (WINDOW_WIDTH, HUD_HEIGHT), 2)

    score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
    level_surf = font.render(f"Level: {level}", True, LEVEL_COLOR)
    prog_surf  = font.render(
        f"Next level: {foods_in_level}/{FOODS_PER_LEVEL}", True, MUTED_COLOR)

    surface.blit(score_surf, (10, 12))
    surface.blit(level_surf, (WINDOW_WIDTH // 2 - level_surf.get_width() // 2, 12))
    surface.blit(prog_surf,  (WINDOW_WIDTH - prog_surf.get_width() - 10, 12))


def draw_game_over(surface: pygame.Surface,
                   big_font: pygame.font.Font,
                   font: pygame.font.Font,
                   score: int,
                   level: int):
    """Semi-transparent game-over overlay."""
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 170))
    surface.blit(overlay, (0, 0))

    go  = big_font.render("GAME OVER", True, (220, 50, 50))
    sc  = font.render(f"Score: {score}   Level: {level}", True, TEXT_COLOR)
    rst = font.render("R – Restart   |   ESC – Quit", True, MUTED_COLOR)

    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2
    surface.blit(go,  go.get_rect(center=(cx, cy - 50)))
    surface.blit(sc,  sc.get_rect(center=(cx, cy + 10)))
    surface.blit(rst, rst.get_rect(center=(cx, cy + 50)))


# ─────────────────────────────────────────────────────────────────────────────
#  Game state helpers
# ─────────────────────────────────────────────────────────────────────────────
def move_delay_for_level(level: int) -> int:
    """
    Returns the millisecond delay between snake moves for a given level.
    Speed increases (delay decreases) with each level. (Feature #4)
    """
    return max(MIN_MOVE_DELAY, BASE_MOVE_DELAY - (level - 1) * SPEED_STEP)


def reset_game() -> dict:
    """Returns a fresh game-state dictionary."""
    snake = Snake()
    return {
        "snake"          : snake,
        "food"           : Food(snake.body),
        "score"          : 0,
        "level"          : 1,      # Feature #3 & #5
        "foods_in_level" : 0,      # foods eaten in the current level
        "last_move_time" : pygame.time.get_ticks(),
        "game_over"      : False,
    }


# ─────────────────────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake")
    clock    = pygame.time.Clock()
    font     = pygame.font.SysFont("Segoe UI", 18, bold=True)
    big_font = pygame.font.SysFont("Segoe UI", 48, bold=True)

    state = reset_game()

    running = True
    while running:
        now = pygame.time.get_ticks()   # current time in ms

        # ── Events ───────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and state["game_over"]:
                    state = reset_game()
                # Direction controls
                elif event.key == pygame.K_UP:
                    state["snake"].set_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    state["snake"].set_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    state["snake"].set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    state["snake"].set_direction(1, 0)

        # ── Game logic (runs on a timer, not every frame) ─────────────────
        if not state["game_over"]:
            delay = move_delay_for_level(state["level"])   # Feature #4
            if now - state["last_move_time"] >= delay:
                state["last_move_time"] = now
                snake = state["snake"]
                snake.move()

                head = snake.head
                col, row = head

                # Feature #1 – wall (border) collision
                if col <= 0 or col >= COLS - 1 or row <= 0 or row >= ROWS - 1:
                    state["game_over"] = True

                # Self-collision
                elif snake.check_self_collision():
                    state["game_over"] = True

                # Food collection
                elif head == state["food"].pos:
                    snake.grow()
                    state["score"]          += SCORE_PER_FOOD   # Feature #5
                    state["foods_in_level"] += 1

                    # Feature #3 – level up every FOODS_PER_LEVEL foods
                    if state["foods_in_level"] >= FOODS_PER_LEVEL:
                        state["level"]          += 1
                        state["foods_in_level"]  = 0

                    # Feature #2 – new food at a valid random position
                    state["food"] = Food(snake.body)

        # ── Draw ─────────────────────────────────────────────────────────────
        draw_grid(screen)
        state["food"].draw(screen)
        state["snake"].draw(screen)
        draw_hud(screen, font,
                 state["score"], state["level"], state["foods_in_level"])

        if state["game_over"]:
            draw_game_over(screen, big_font, font,
                           state["score"], state["level"])

        pygame.display.flip()
        clock.tick(60)   # render at 60 fps; game logic is timer-gated

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
