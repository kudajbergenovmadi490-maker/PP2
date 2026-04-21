import sys
import random
import pygame

CELL = 20
COLS = 25
ROWS = 25
HUD_HEIGHT = 50

WINDOW_WIDTH = CELL * COLS
WINDOW_HEIGHT = CELL * ROWS + HUD_HEIGHT

FOODS_PER_LEVEL = 3
BASE_MOVE_DELAY = 150
SPEED_STEP = 10
MIN_MOVE_DELAY = 40

FOOD_TYPES = [
    {"name": "Apple", "color": (220, 50, 50), "points": 1,
     "weight": 60, "lifetime": 8000},
    {"name": "Cherry", "color": (180, 0, 100), "points": 3,
     "weight": 30, "lifetime": 5000},
    {"name": "Star", "color": (255, 215, 0), "points": 10,
     "weight": 10, "lifetime": 3000},
]

BG_COLOR = (15, 15, 25)
GRID_COLOR = (30, 30, 45)
WALL_COLOR = (80, 80, 110)
SNAKE_HEAD = (80, 220, 80)
SNAKE_BODY = (50, 170, 50)
TEXT_COLOR = (230, 230, 230)
MUTED_COLOR = (120, 120, 150)
LEVEL_COLOR = (100, 180, 255)
HUD_BG = (20, 20, 35)

def cell_rect(col, row):
    return pygame.Rect(col * CELL, HUD_HEIGHT + row * CELL, CELL, CELL)

class Snake:
    def __init__(self):
        mid_col = COLS // 2
        mid_row = ROWS // 2
        self.body = [(mid_col, mid_row),
                     (mid_col - 1, mid_row),
                     (mid_col - 2, mid_row)]
        self.direction = (1, 0)
        self.pending_direction = (1, 0)
        self.grew = False

    def set_direction(self, dcol, drow):
        cur_dc, cur_dr = self.direction
        if (dcol, drow) != (-cur_dc, -cur_dr):
            self.pending_direction = (dcol, drow)

    def move(self):
        self.direction = self.pending_direction
        dc, dr = self.direction
        hc, hr = self.body[0]
        self.body.insert(0, (hc + dc, hr + dr))
        if self.grew:
            self.grew = False
        else:
            self.body.pop()

    def grow(self):
        self.grew = True

    @property
    def head(self):
        return self.body[0]

    def check_self_collision(self):
        return self.head in self.body[1:]

    def draw(self, surface):
        for i, (col, row) in enumerate(self.body):
            rect = cell_rect(col, row)
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(surface, color,
                             rect.inflate(-2, -2), border_radius=4)

class Food:
    def __init__(self, snake_body):
        weights = [ft["weight"] for ft in FOOD_TYPES]
        self.ftype = random.choices(FOOD_TYPES, weights=weights, k=1)[0]
        self.color = self.ftype["color"]
        self.points = self.ftype["points"]
        self.name = self.ftype["name"]
        self.lifetime = self.ftype["lifetime"]
        self.spawn_time = pygame.time.get_ticks()
        self.pos = self._random_pos(snake_body)

    def _random_pos(self, snake_body):
        available = [
            (c, r)
            for c in range(1, COLS - 1)
            for r in range(1, ROWS - 1)
            if (c, r) not in snake_body
        ]
        return random.choice(available) if available else (COLS // 2, ROWS // 2)

    def is_expired(self):
        elapsed = pygame.time.get_ticks() - self.spawn_time
        return elapsed >= self.lifetime

    def time_remaining_fraction(self):
        elapsed = pygame.time.get_ticks() - self.spawn_time
        return max(0.0, 1.0 - elapsed / self.lifetime)

    def draw(self, surface):
        fraction = self.time_remaining_fraction()
        if fraction < 0.25:
            if (pygame.time.get_ticks() // 200) % 2 == 0:
                return

        rect = cell_rect(*self.pos)
        center = rect.center
        radius = CELL // 2 - 2
        pygame.draw.circle(surface, self.color, center, radius)

        bar_w = int(CELL * fraction)
        bar_rect = pygame.Rect(rect.x, rect.bottom - 4, bar_w, 3)
        bar_color = (80, 255, 80) if fraction > 0.5 else (255, 80, 80)
        pygame.draw.rect(surface, bar_color, bar_rect)

        if CELL >= 20:
            pts_font = pygame.font.SysFont("Arial", 10, bold=True)
            pts_surf = pts_font.render(str(self.points), True, (255, 255, 255))
            surface.blit(pts_surf, pts_surf.get_rect(center=center))

def draw_grid(surface):
    surface.fill(BG_COLOR)
    for c in range(COLS):
        for r in range(ROWS):
            pygame.draw.rect(surface, GRID_COLOR, cell_rect(c, r), 1)
            if c == 0 or c == COLS - 1 or r == 0 or r == ROWS - 1:
                pygame.draw.rect(surface, WALL_COLOR,
                                 cell_rect(c, r), border_radius=2)

def draw_hud(surface, font, score, level, foods_in_level):
    pygame.draw.rect(surface, HUD_BG, (0, 0, WINDOW_WIDTH, HUD_HEIGHT))
    pygame.draw.line(surface, WALL_COLOR,
                     (0, HUD_HEIGHT), (WINDOW_WIDTH, HUD_HEIGHT), 2)
    score_surf = font.render(f"Score: {score}", True, TEXT_COLOR)
    level_surf = font.render(f"Level: {level}", True, LEVEL_COLOR)
    prog_surf = font.render(
        f"Next: {foods_in_level}/{FOODS_PER_LEVEL}", True, MUTED_COLOR)
    surface.blit(score_surf, (10, 14))
    surface.blit(level_surf, (WINDOW_WIDTH // 2 - level_surf.get_width() // 2, 14))
    surface.blit(prog_surf, (WINDOW_WIDTH - prog_surf.get_width() - 10, 14))

def draw_food_legend(surface, small_font):
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
    go = big_font.render("GAME OVER", True, (220, 50, 50))
    sc = font.render(f"Score: {score}   Level: {level}", True, TEXT_COLOR)
    rst = font.render("R – Restart   |   ESC – Quit", True, MUTED_COLOR)
    cx = WINDOW_WIDTH // 2
    cy = WINDOW_HEIGHT // 2
    surface.blit(go, go.get_rect(center=(cx, cy - 50)))
    surface.blit(sc, sc.get_rect(center=(cx, cy + 10)))
    surface.blit(rst, rst.get_rect(center=(cx, cy + 50)))

def move_delay_for_level(level):
    return max(MIN_MOVE_DELAY, BASE_MOVE_DELAY - (level - 1) * SPEED_STEP)

def reset_game():
    snake = Snake()
    return {
        "snake": snake,
        "foods": [Food(snake.body)],
        "score": 0,
        "level": 1,
        "foods_in_level": 0,
        "last_move_time": pygame.time.get_ticks(),
        "food_spawn_time": pygame.time.get_ticks(),
        "game_over": False,
    }

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake – Practice 11")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Segoe UI", 18, bold=True)
    small = pygame.font.SysFont("Segoe UI", 13)
    big_font = pygame.font.SysFont("Segoe UI", 48, bold=True)
    state = reset_game()
    running = True
    while running:
        now = pygame.time.get_ticks()
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

        if not state["game_over"]:
            state["foods"] = [f for f in state["foods"] if not f.is_expired()]
            if now - state["food_spawn_time"] >= 4000:
                if len(state["foods"]) < 3:
                    state["foods"].append(Food(state["snake"].body))
                state["food_spawn_time"] = now
            if len(state["foods"]) == 0:
                state["foods"].append(Food(state["snake"].body))

            delay = move_delay_for_level(state["level"])
            if now - state["last_move_time"] >= delay:
                state["last_move_time"] = now
                snake = state["snake"]
                snake.move()
                col, row = snake.head
                if col <= 0 or col >= COLS-1 or row <= 0 or row >= ROWS-1:
                    state["game_over"] = True
                elif snake.check_self_collision():
                    state["game_over"] = True
                else:
                    for food in state["foods"][:]:
                        if snake.head == food.pos:
                            snake.grow()
                            state["score"] += food.points
                            state["foods_in_level"] += 1
                            state["foods"].remove(food)
                            state["foods"].append(Food(snake.body))
                            if state["foods_in_level"] >= FOODS_PER_LEVEL:
                                state["level"] += 1
                                state["foods_in_level"] = 0

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