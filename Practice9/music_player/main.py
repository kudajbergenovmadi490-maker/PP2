"""
main.py - Interactive Music Player with Keyboard Controls

Controls:
  P  → Play
  S  → Stop
  N  → Next track
  B  → Previous (Back) track
  Q  → Quit
"""

import sys
import pygame
from player import MusicPlayer

# ── Constants ────────────────────────────────────────────────────────────────
WINDOW_WIDTH  = 560
WINDOW_HEIGHT = 340
FPS           = 30
MUSIC_DIR     = "music"

# Colours
BG_COLOR       = (18,  18,  28)
PANEL_COLOR    = (30,  30,  46)
ACCENT_COLOR   = (100, 180, 255)
TEXT_COLOR     = (230, 230, 230)
MUTED_COLOR    = (120, 120, 140)
PLAY_COLOR     = (80,  200, 120)
STOP_COLOR     = (220,  90,  90)


def draw_ui(screen: pygame.Surface,
            player: MusicPlayer,
            fonts: dict) -> None:
    """
    Renders the entire player UI onto *screen*.

    Args:
        screen  : pygame display surface
        player  : MusicPlayer instance
        fonts   : dict with keys 'title', 'body', 'small'
    """
    screen.fill(BG_COLOR)

    # ── Decorative panel ─────────────────────────────────────────────────────
    panel_rect = pygame.Rect(20, 20, WINDOW_WIDTH - 40, WINDOW_HEIGHT - 40)
    pygame.draw.rect(screen, PANEL_COLOR, panel_rect, border_radius=14)
    pygame.draw.rect(screen, ACCENT_COLOR, panel_rect, width=2, border_radius=14)

    # ── Title bar ────────────────────────────────────────────────────────────
    title_surf = fonts["title"].render("🎵  Pygame Music Player", True, ACCENT_COLOR)
    screen.blit(title_surf, (40, 36))

    # ── Divider line ─────────────────────────────────────────────────────────
    pygame.draw.line(screen, ACCENT_COLOR, (40, 80), (WINDOW_WIDTH - 40, 80), 1)

    # ── Track info ───────────────────────────────────────────────────────────
    if player.track_count == 0:
        track_text = "No tracks found in music/"
        status_color = STOP_COLOR
    else:
        track_text = player.current_track_name
        status_color = PLAY_COLOR if player.is_playing else MUTED_COLOR

    track_surf = fonts["body"].render(track_text, True, TEXT_COLOR)
    screen.blit(track_surf, (40, 100))

    pos_surf = fonts["small"].render(
        f"Track  {player.position_label}", True, MUTED_COLOR)
    screen.blit(pos_surf, (40, 138))

    # ── Status indicator ─────────────────────────────────────────────────────
    status_label = "▶ PLAYING" if player.is_playing else "■ STOPPED"
    status_surf = fonts["body"].render(status_label, True, status_color)
    screen.blit(status_surf, (40, 172))

    # ── Playback position ────────────────────────────────────────────────────
    if player.is_playing:
        pos_ms  = player.get_playback_pos_ms()
        pos_sec = pos_ms // 1000
        elapsed = f"Elapsed: {pos_sec // 60:02d}:{pos_sec % 60:02d}"
        elapsed_surf = fonts["small"].render(elapsed, True, MUTED_COLOR)
        screen.blit(elapsed_surf, (200, 178))

    # ── Key hints ────────────────────────────────────────────────────────────
    pygame.draw.line(screen, MUTED_COLOR,
                     (40, WINDOW_HEIGHT - 100),
                     (WINDOW_WIDTH - 40, WINDOW_HEIGHT - 100), 1)

    hints = [
        ("[P] Play", PLAY_COLOR),
        ("[S] Stop", STOP_COLOR),
        ("[N] Next", ACCENT_COLOR),
        ("[B] Back", ACCENT_COLOR),
        ("[Q] Quit", MUTED_COLOR),
    ]
    x_offset = 40
    for label, color in hints:
        hint_surf = fonts["small"].render(label, True, color)
        screen.blit(hint_surf, (x_offset, WINDOW_HEIGHT - 80))
        x_offset += hint_surf.get_width() + 20

    pygame.display.flip()


def main() -> None:
    pygame.init()
    pygame.mixer.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Pygame Music Player")
    clock = pygame.time.Clock()

    # ── Fonts ────────────────────────────────────────────────────────────────
    fonts = {
        "title": pygame.font.SysFont("Segoe UI", 22, bold=True),
        "body" : pygame.font.SysFont("Segoe UI", 18),
        "small": pygame.font.SysFont("Segoe UI", 14),
    }

    # ── Player ───────────────────────────────────────────────────────────────
    player = MusicPlayer(MUSIC_DIR)

    # ── Main loop ────────────────────────────────────────────────────────────
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()

            # Auto-advance when a track finishes naturally
            elif event.type == pygame.USEREVENT:
                player.next_track()

        # Register end-of-track event so we know when to advance
        pygame.mixer.music.set_endevent(pygame.USEREVENT)

        draw_ui(screen, player, fonts)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
