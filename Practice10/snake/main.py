import sys
import random
import pygame

CELL        = 20          
COLS        = 25          
ROWS        = 25         
HUD_HEIGHT  = 50         

WINDOW_WIDTH  = CELL * COLS
WINDOW_HEIGHT = CELL * ROWS + HUD_HEIGHT

FOODS_PER_LEVEL = 3

BASE_MOVE_DELAY = 150    
SPEED_STEP      = 10     
MIN_MOVE_DELAY  = 40

SCORE_PER_FOOD  = 10

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


def cell_rect(col: int, row: int) -> pygame.Rect:
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

    def set_direction(self, dcol: int, drow: int):
        cur_dc, cur_dr = self.direction
        if (dcol, drow) != (-cur_dc, -cur_dr):
            self.pending_direction = (dcol, drow)

    def move(self):
        self.direction = self.pending_direction
        dc, dr = self.direction
        head_col, head_row = self.body[0]
        new_head = (head_col + dc, head_row + dr)
        self.body.insert(0, new_head)

        if self.grew:
            self.grew = False
        else:
            self.body.pop()   

    def grow(self):
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


class Food:
    def __init__(self, snake_body: list):
        self.pos = self._random_pos(snake_body)

    def _random_pos(self, snake_body: list) -> tuple:
        available = [
            (c, r)
            for c in range(1, COLS - 1)
            for r in range(1, ROWS - 1)
            if (c, r) not in snake_body
        ]
        if not available:
            return (COLS // 2, ROWS // 2)
        return random.choice(available)

    def draw(self, surface: pygame.Surface):
        """Draw the food as a red circle."""
        rect = cell_rect(*self.pos)
        center = rect.center
        radius = CELL // 2 - 2
        pygame.draw.circle(surface, FOOD_COLOR, center, radius)
        pygame.draw.circle(surface, (255, 140, 140),
                           (center[0] - 3, center[1] - 3), radius // 3)

def draw_grid(surface: pygame.Surface):
    surface.fill(BG_COLOR)

    for c in range(COLS):
        for r in range(ROWS):
            rect = cell_rect(c, r)
            pygame.draw.rect(surface, GRID_COLOR, rect, 1)

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

def move_delay_for_level(level: int) -> int:
    return max(MIN_MOVE_DELAY, BASE_MOVE_DELAY - (level - 1) * SPEED_STEP)


def reset_game() -> dict:
    snake = Snake()
    return {
        "snake"          : snake,
        "food"           : Food(snake.body),
        "score"          : 0,
        "level"          : 1,      
        "foods_in_level" : 0,      
        "last_move_time" : pygame.time.get_ticks(),
        "game_over"      : False,
    }



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
        now = pygame.time.get_ticks()   

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

        if not state["game_over"]:
            delay = move_delay_for_level(state["level"])   
            if now - state["last_move_time"] >= delay:
                state["last_move_time"] = now
                snake = state["snake"]
                snake.move()

                head = snake.head
                col, row = head

                if col <= 0 or col >= COLS - 1 or row <= 0 or row >= ROWS - 1:
                    state["game_over"] = True

                elif snake.check_self_collision():
                    state["game_over"] = True

                elif head == state["food"].pos:
                    snake.grow()
                    state["score"]          += SCORE_PER_FOOD   
                    state["foods_in_level"] += 1

                    if state["foods_in_level"] >= FOODS_PER_LEVEL:
                        state["level"]          += 1
                        state["foods_in_level"]  = 0

                    state["food"] = Food(snake.body)

        draw_grid(screen)
        state["food"].draw(screen)
        state["snake"].draw(screen)
        draw_hud(screen, font,
                 state["score"], state["level"], state["foods_in_level"])

        if state["game_over"]:
            draw_game_over(screen, big_font, font,
                           state["score"], state["level"])

        pygame.display.flip()
        clock.tick(60)   

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
