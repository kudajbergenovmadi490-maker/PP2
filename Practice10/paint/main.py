"""
main.py – Paint Application (Practice 10)
Based on: https://nerdparadise.com/programming/pygame/part6

Added features:
  1. Draw rectangle (click & drag)
  2. Draw circle (click & drag)
  3. Eraser tool
  4. Colour picker palette

Controls:
  Left-click & drag  : draw with current tool
  Toolbar buttons    : select tool / colour
  C                  : clear canvas
  ESC                : quit
"""

import sys
import pygame

# ─────────────────────────────────────────────────────────────────────────────
#  Layout constants
# ─────────────────────────────────────────────────────────────────────────────
WINDOW_WIDTH   = 900
WINDOW_HEIGHT  = 650
TOOLBAR_WIDTH  = 140     # left-side toolbar width
CANVAS_X       = TOOLBAR_WIDTH
CANVAS_Y       = 0
CANVAS_WIDTH   = WINDOW_WIDTH  - TOOLBAR_WIDTH
CANVAS_HEIGHT  = WINDOW_HEIGHT

# ─────────────────────────────────────────────────────────────────────────────
#  Colours
# ─────────────────────────────────────────────────────────────────────────────
BG_COLOR      = (240, 240, 245)
TOOLBAR_BG    = (45,  45,  60)
CANVAS_BG     = (255, 255, 255)
BORDER_COLOR  = (80,  80, 100)
SELECTED_RING = (100, 200, 255)
TEXT_COLOR    = (230, 230, 230)

# Colour palette (feature #4)
PALETTE = [
    (0,     0,   0),   # black
    (255, 255, 255),   # white
    (220,  30,  30),   # red
    (30,  220,  30),   # green
    (30,  100, 220),   # blue
    (255, 220,   0),   # yellow
    (255, 140,   0),   # orange
    (160,  30, 220),   # purple
    (0,   200, 200),   # cyan
    (220,  30, 130),   # pink
    (80,   50,  20),   # brown
    (150, 150, 150),   # grey
]

# Tool identifiers
TOOL_PENCIL    = "pencil"
TOOL_RECTANGLE = "rectangle"   # feature #1
TOOL_CIRCLE    = "circle"      # feature #2
TOOL_ERASER    = "eraser"      # feature #3


# ─────────────────────────────────────────────────────────────────────────────
#  Button helper
# ─────────────────────────────────────────────────────────────────────────────
class Button:
    """A simple clickable rectangle button for the toolbar."""

    def __init__(self, rect: pygame.Rect, label: str, value):
        self.rect  = rect
        self.label = label
        self.value = value        # the tool name or colour this button selects

    def draw(self, surface: pygame.Surface,
             font: pygame.font.Font,
             selected: bool):
        # Background
        colour = (70, 70, 90) if not selected else (90, 90, 120)
        pygame.draw.rect(surface, colour, self.rect, border_radius=6)

        # Selection ring
        if selected:
            pygame.draw.rect(surface, SELECTED_RING, self.rect,
                             width=2, border_radius=6)

        # Label
        text = font.render(self.label, True, TEXT_COLOR)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, pos: tuple) -> bool:
        return self.rect.collidepoint(pos)


class ColourSwatch:
    """A clickable colour square in the palette."""

    SIZE = 24

    def __init__(self, rect: pygame.Rect, colour: tuple):
        self.rect   = rect
        self.colour = colour

    def draw(self, surface: pygame.Surface, selected: bool):
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=4)
        ring_color = SELECTED_RING if selected else BORDER_COLOR
        pygame.draw.rect(surface, ring_color, self.rect,
                         width=2, border_radius=4)

    def is_clicked(self, pos: tuple) -> bool:
        return self.rect.collidepoint(pos)


# ─────────────────────────────────────────────────────────────────────────────
#  Build toolbar layout
# ─────────────────────────────────────────────────────────────────────────────
def build_toolbar(font: pygame.font.Font) -> tuple:
    """
    Creates and returns (tool_buttons, colour_swatches).

    Args:
        font : pygame font for button labels

    Returns:
        Tuple of (list[Button], list[ColourSwatch])
    """
    btn_w, btn_h = 120, 36
    btn_x = 10
    start_y = 60

    tool_buttons = [
        Button(pygame.Rect(btn_x, start_y,       btn_w, btn_h), "✏  Pencil",    TOOL_PENCIL),
        Button(pygame.Rect(btn_x, start_y + 50,  btn_w, btn_h), "▭  Rectangle", TOOL_RECTANGLE),
        Button(pygame.Rect(btn_x, start_y + 100, btn_w, btn_h), "○  Circle",    TOOL_CIRCLE),
        Button(pygame.Rect(btn_x, start_y + 150, btn_w, btn_h), "◻  Eraser",   TOOL_ERASER),
    ]

    # Colour palette – 2 columns × 6 rows
    swatches = []
    sw = ColourSwatch.SIZE
    pad = 6
    pal_start_y = 280
    for idx, colour in enumerate(PALETTE):
        col = idx % 2
        row = idx // 2
        x = btn_x + col * (sw + pad)
        y = pal_start_y + row * (sw + pad)
        swatches.append(ColourSwatch(pygame.Rect(x, y, sw, sw), colour))

    return tool_buttons, swatches


# ─────────────────────────────────────────────────────────────────────────────
#  Drawing helpers
# ─────────────────────────────────────────────────────────────────────────────
def draw_toolbar(surface: pygame.Surface,
                 font: pygame.font.Font,
                 small_font: pygame.font.Font,
                 tool_buttons: list,
                 swatches: list,
                 current_tool: str,
                 current_colour: tuple,
                 brush_size: int):
    """Renders the entire left toolbar."""
    pygame.draw.rect(surface, TOOLBAR_BG,
                     (0, 0, TOOLBAR_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(surface, BORDER_COLOR,
                     (TOOLBAR_WIDTH - 1, 0), (TOOLBAR_WIDTH - 1, WINDOW_HEIGHT), 2)

    # Title
    title = font.render("Paint", True, (150, 200, 255))
    surface.blit(title, (10, 14))

    # Tool buttons
    for btn in tool_buttons:
        btn.draw(surface, small_font, selected=(btn.value == current_tool))

    # Colour palette label
    pal_label = small_font.render("Colours:", True, TEXT_COLOR)
    surface.blit(pal_label, (10, 256))

    # Swatches
    for sw in swatches:
        sw.draw(surface, selected=(sw.colour == current_colour))

    # Current colour preview
    preview_rect = pygame.Rect(10, WINDOW_HEIGHT - 90, 120, 36)
    pygame.draw.rect(surface, current_colour, preview_rect, border_radius=6)
    pygame.draw.rect(surface, BORDER_COLOR,  preview_rect, width=2, border_radius=6)

    # Brush size display
    size_label = small_font.render(f"Brush: {brush_size}px", True, TEXT_COLOR)
    surface.blit(size_label, (10, WINDOW_HEIGHT - 46))
    hint = small_font.render("Scroll ↑↓ to resize", True, (100, 100, 130))
    surface.blit(hint, (10, WINDOW_HEIGHT - 28))


def canvas_pos(pos: tuple) -> tuple:
    """Converts screen (x, y) to canvas-relative (x, y)."""
    return (pos[0] - CANVAS_X, pos[1] - CANVAS_Y)


def draw_preview(screen: pygame.Surface,
                 tool: str,
                 colour: tuple,
                 brush_size: int,
                 start: tuple,
                 end: tuple):
    """
    Draws a live preview of the shape being dragged (rectangle or circle).
    This is drawn on the screen surface directly, not the canvas, so it
    disappears each frame without permanently marking the canvas.
    """
    if tool == TOOL_RECTANGLE:
        x = min(start[0], end[0]) + CANVAS_X
        y = min(start[1], end[1]) + CANVAS_Y
        w = abs(end[0] - start[0])
        h = abs(end[1] - start[1])
        pygame.draw.rect(screen, colour, (x, y, w, h), brush_size)

    elif tool == TOOL_CIRCLE:
        cx = (start[0] + end[0]) // 2 + CANVAS_X
        cy = (start[1] + end[1]) // 2 + CANVAS_Y
        radius = max(1, int(((end[0] - start[0])**2 + (end[1] - start[1])**2) ** 0.5 / 2))
        pygame.draw.circle(screen, colour, (cx, cy), radius, brush_size)


# ─────────────────────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()

    font       = pygame.font.SysFont("Segoe UI", 20, bold=True)
    small_font = pygame.font.SysFont("Segoe UI", 14)

    # The canvas is a separate surface; shapes are committed here permanently
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(CANVAS_BG)

    tool_buttons, swatches = build_toolbar(font)

    # State
    current_tool   = TOOL_PENCIL
    current_colour = PALETTE[0]   # black
    brush_size     = 4

    drawing     = False           # True while LMB is held
    drag_start  = None            # canvas-relative start position of drag
    last_pos    = None            # for pencil/eraser continuous line

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_c:
                    # Clear canvas
                    canvas.fill(CANVAS_BG)

            elif event.type == pygame.MOUSEWHEEL:
                # Adjust brush size with scroll wheel
                brush_size = max(1, min(50, brush_size + event.y))

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # ── Toolbar click ─────────────────────────────────────────
                if mouse_pos[0] < TOOLBAR_WIDTH:
                    for btn in tool_buttons:
                        if btn.is_clicked(mouse_pos):
                            current_tool = btn.value
                    for sw in swatches:
                        if sw.is_clicked(mouse_pos):
                            current_colour = sw.colour
                else:
                    # ── Canvas click – begin drawing ──────────────────────
                    cp = canvas_pos(mouse_pos)
                    drawing    = True
                    drag_start = cp
                    last_pos   = cp

                    # Pencil/eraser start dot
                    if current_tool in (TOOL_PENCIL, TOOL_ERASER):
                        color = CANVAS_BG if current_tool == TOOL_ERASER else current_colour
                        pygame.draw.circle(canvas, color, cp, brush_size // 2)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and mouse_pos[0] >= TOOLBAR_WIDTH:
                    cp = canvas_pos(mouse_pos)

                    # Commit shape to canvas when mouse is released
                    if current_tool == TOOL_RECTANGLE:   # feature #1
                        x = min(drag_start[0], cp[0])
                        y = min(drag_start[1], cp[1])
                        w = abs(cp[0] - drag_start[0])
                        h = abs(cp[1] - drag_start[1])
                        pygame.draw.rect(canvas, current_colour,
                                         (x, y, w, h), brush_size)

                    elif current_tool == TOOL_CIRCLE:    # feature #2
                        cx = (drag_start[0] + cp[0]) // 2
                        cy = (drag_start[1] + cp[1]) // 2
                        radius = max(1, int(((cp[0] - drag_start[0])**2 +
                                             (cp[1] - drag_start[1])**2) ** 0.5 / 2))
                        pygame.draw.circle(canvas, current_colour,
                                           (cx, cy), radius, brush_size)

                drawing    = False
                drag_start = None
                last_pos   = None

            elif event.type == pygame.MOUSEMOTION:
                if drawing and mouse_pos[0] >= TOOLBAR_WIDTH:
                    cp = canvas_pos(mouse_pos)

                    # Pencil and eraser draw continuously as mouse moves
                    if current_tool == TOOL_PENCIL and last_pos:
                        pygame.draw.line(canvas, current_colour,
                                         last_pos, cp, brush_size)
                    elif current_tool == TOOL_ERASER and last_pos:  # feature #3
                        pygame.draw.line(canvas, CANVAS_BG,
                                         last_pos, cp, brush_size * 3)

                    last_pos = cp

        # ── Render ───────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # Blit canvas
        screen.blit(canvas, (CANVAS_X, CANVAS_Y))

        # Live preview for rect/circle while dragging (feature #1 & #2)
        if drawing and drag_start and current_tool in (TOOL_RECTANGLE, TOOL_CIRCLE):
            cp = canvas_pos(mouse_pos)
            draw_preview(screen, current_tool, current_colour,
                         brush_size, drag_start, cp)

        # Cursor preview circle for pencil/eraser
        if mouse_pos[0] >= TOOLBAR_WIDTH:
            preview_r = brush_size // 2 if current_tool != TOOL_ERASER else brush_size * 3 // 2
            preview_c = CANVAS_BG if current_tool == TOOL_ERASER else current_colour
            pygame.draw.circle(screen, preview_c, mouse_pos, max(1, preview_r), 1)

        draw_toolbar(screen, font, small_font,
                     tool_buttons, swatches,
                     current_tool, current_colour, brush_size)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
