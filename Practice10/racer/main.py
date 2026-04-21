import sys
import random
import pygame

WINDOW_WIDTH  = 500
WINDOW_HEIGHT = 500
FPS           = 60

LANE_LEFT   = 80
LANE_RIGHT  = 420

WHITE   = (255, 255, 255)
BLACK   = (0,   0,   0)
GREY    = (50,  50,  50)
YELLOW  = (255, 220,  0)
RED     = (220,  30,  30)
GREEN   = (30,  200,  60)
BLUE    = (30,  120, 220)

STRIPE_HEIGHT = 50
STRIPE_GAP    = 50
STRIPE_X      = WINDOW_WIDTH // 2 - 5
STRIPE_WIDTH  = 10

class Road:
    def __init__(self):
        self.stripes = list(range(-STRIPE_HEIGHT, WINDOW_HEIGHT + STRIPE_HEIGHT,
                                  STRIPE_HEIGHT + STRIPE_GAP))
        self.speed = 5

    def update(self):
        self.stripes = [y + self.speed for y in self.stripes]
        self.stripes = [y if y < WINDOW_HEIGHT else y - (WINDOW_HEIGHT + STRIPE_HEIGHT + STRIPE_GAP)
                        for y in self.stripes]

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, GREY, (LANE_LEFT, 0,
                                         LANE_RIGHT - LANE_LEFT, WINDOW_HEIGHT))
        for y in self.stripes:
            pygame.draw.rect(surface, WHITE,
                             (STRIPE_X, y, STRIPE_WIDTH, STRIPE_HEIGHT))

class PlayerCar:
 
    WIDTH  = 40
    HEIGHT = 70
    SPEED  = 5  

    def __init__(self):
        self.x = WINDOW_WIDTH  // 2 - self.WIDTH // 2
        self.y = WINDOW_HEIGHT - self.HEIGHT - 20
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.x -= self.SPEED
        if keys[pygame.K_RIGHT]:
            self.x += self.SPEED

        self.x = max(LANE_LEFT, min(self.x, LANE_RIGHT - self.WIDTH))
        self.rect.x = self.x

    def draw(self, surface: pygame.Surface):
        r = self.rect
        pygame.draw.rect(surface, BLUE, r, border_radius=6)
        pygame.draw.rect(surface, (180, 220, 255),
                         (r.x + 6, r.y + 8, r.width - 12, 18), border_radius=3)
        pygame.draw.rect(surface, (180, 220, 255),
                         (r.x + 6, r.y + r.height - 26, r.width - 12, 14),
                         border_radius=3)
        wheel_w, wheel_h = 10, 16
        pygame.draw.rect(surface, BLACK, (r.x - wheel_w + 2, r.y + 8,          wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x + r.width - 2, r.y + 8,          wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x - wheel_w + 2, r.y + r.height - 24, wheel_w, wheel_h), border_radius=3)
        pygame.draw.rect(surface, BLACK, (r.x + r.width - 2, r.y + r.height - 24, wheel_w, wheel_h), border_radius=3)

class EnemyCar:
    
    WIDTH  = 40
    HEIGHT = 70

    LANES = [LANE_LEFT + 10, LANE_RIGHT - WIDTH - 10]

    def __init__(self, speed: int = 5):
        self.speed = speed
        self.x = random.choice(self.LANES)
        self.y = -self.HEIGHT
        self.rect = pygame.Rect(self.x, self.y, self.WIDTH, self.HEIGHT)

    def update(self):
        self.y += self.speed
        self.rect.y = self.y

    def is_off_screen(self) -> bool:
        return self.y > WINDOW_HEIGHT

    def draw(self, surface: pygame.Surface):
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

class Coin:

    RADIUS = 12

    def __init__(self, speed: int = 5):
        self.speed = speed
        self.x = random.randint(LANE_LEFT + self.RADIUS + 5,
                                LANE_RIGHT - self.RADIUS - 5)
        self.y = -self.RADIUS 
        self.rect = pygame.Rect(self.x - self.RADIUS, self.y - self.RADIUS,
                                self.RADIUS * 2, self.RADIUS * 2)

    def update(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)

    def is_off_screen(self) -> bool:
        return self.y - self.RADIUS > WINDOW_HEIGHT

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, YELLOW, (self.x, self.y), self.RADIUS)
        pygame.draw.circle(surface, (200, 160, 0), (self.x, self.y), self.RADIUS, 2)
        pygame.draw.circle(surface, (255, 240, 100),
                           (self.x - 3, self.y - 3), self.RADIUS // 3)

def draw_hud(surface: pygame.Surface,
             font: pygame.font.Font,
             score: int,
             coins: int) -> None:

    score_surf = font.render(f"Score: {score}", True, WHITE)
    surface.blit(score_surf, (10, 10))

    coin_surf = font.render(f"🪙 Coins: {coins}", True, YELLOW)
    surface.blit(coin_surf, (WINDOW_WIDTH - coin_surf.get_width() - 10, 10))


def draw_game_over(surface: pygame.Surface,
                   big_font: pygame.font.Font,
                   font: pygame.font.Font,
                   score: int,
                   coins: int) -> None:

    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    surface.blit(overlay, (0, 0))

    go_surf  = big_font.render("GAME OVER", True, RED)
    sc_surf  = font.render(f"Score: {score}   Coins: {coins}", True, WHITE)
    rst_surf = font.render("Press R to restart  |  ESC to quit", True, GREY)

    surface.blit(go_surf,  go_surf.get_rect(center=(WINDOW_WIDTH//2, 180)))
    surface.blit(sc_surf,  sc_surf.get_rect(center=(WINDOW_WIDTH//2, 240)))
    surface.blit(rst_surf, rst_surf.get_rect(center=(WINDOW_WIDTH//2, 290)))

def reset_game():
    """Returns a fresh game-state dictionary."""
    return {
        "road"      : Road(),
        "player"    : PlayerCar(),
        "enemies"   : [],
        "coins"     : [],          
        "score"     : 0,
        "coin_count": 0,            
        "speed"     : 5,
        "enemy_timer" : 0,      
        "coin_timer"  : 0,         
        "game_over" : False,
    }

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

            state["road"].update()

            state["player"].update(keys)

            state["enemy_timer"] += 1
            if state["enemy_timer"] >= 90:
                state["enemies"].append(EnemyCar(speed=state["speed"]))
                state["enemy_timer"] = 0

            state["coin_timer"] += 1
            if state["coin_timer"] >= random.randint(120, 240):
                state["coins"].append(Coin(speed=state["speed"]))
                state["coin_timer"] = 0

            player_rect = state["player"].rect
            for enemy in state["enemies"][:]:
                enemy.update()
                if enemy.is_off_screen():
                    state["enemies"].remove(enemy)
                elif player_rect.colliderect(enemy.rect):
                    state["game_over"] = True

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
