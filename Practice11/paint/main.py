"""
main.py – Paint Application (Practice 11)
Extends Practice 10 Paint with:
  1. Draw square
  2. Draw right triangle
  3. Draw equilateral triangle
  4. Draw rhombus
  5. Full code comments

Controls:
  Left-click & drag  : draw with current tool
  Toolbar buttons    : select tool / colour
  Scroll wheel       : resize brush
  C                  : clear canvas
  ESC                : quit
"""

import sys
import math
import pygame

# ─────────────────────────────────────────────────────────────────────────────
#  Layout constants
# ─────────────────────────────────────────────────────────────────────────────
WINDOW_WIDTH   = 960
WINDOW_HEIGHT  = 680
TOOLBAR_WIDTH  = 160
CANVAS_X       = TOOLBAR_WIDTH
CANVAS_WIDTH   = WINDOW_WIDTH - TOOLBAR_WIDTH
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
MUTED_COLOR   = (100, 100, 130)

# Colour palette
PALETTE = [
    (0,     0,   0),
    (255, 255, 255),
    (220,  30,  30),
    (30,  220,  30),
    (30,  100, 220),
    (255, 220,   0),
    (255, 140,   0),
    (160,  30, 220),
    (0,   200, 200),
    (220,  30, 130),
    (80,   50,  20),
    (150, 150, 150),
]

# Tool names
TOOL_PENCIL    = "pencil"
TOOL_RECTANGLE = "rectangle"
TOOL_SQUARE    = "square"          # Feature 1
TOOL_CIRCLE    = "circle"
TOOL_RTRIANGLE = "right_triangle"  # Feature 2
TOOL_ETRIANGLE = "equil_triangle"  # Feature 3
TOOL_RHOMBUS   = "rhombus"         # Feature 4
TOOL_ERASER    = "eraser"


# ─────────────────────────────────────────────────────────────────────────────
#  Geometry helpers
# ─────────────────────────────────────────────────────────────────────────────
def right_triangle_points(start, end):
    """
    Returns 3 points of a right triangle.
    Right angle is at the bottom-left corner.

    Args:
        start : (x, y) drag start on canvas
        end   : (x, y) drag end on canvas
    """
    x1, y1 = start
    x2, y2 = end
    return [(x1, y2),   # bottom-left  (right angle here)
            (x2, y2),   # bottom-right
            (x1, y1)]   # top-left


def equilateral_triangle_points(start, end):
    """
    Returns 3 points of an equilateral triangle.
    Base is the horizontal line from start to end;
    apex is calculated using the equilateral triangle height formula.

    Height = (√3 / 2) × base

    Args:
        start : (x, y) drag start on canvas
        end   : (x, y) drag end on canvas
    """
    x1, y1 = start
    x2, y2 = end
    base    = x2 - x1
    height  = int(abs(base) * math.sqrt(3) / 2)
    # Apex is above the midpoint of the base
    mid_x   = (x1 + x2) // 2
    apex_y  = min(y1, y2) - height   # upward from the drag line
    return [(x1, max(y1, y2)),        # bottom-left
            (x2, max(y1, y2)),        # bottom-right
            (mid_x, apex_y)]          # apex


def rhombus_points(start, end):
    """
    Returns 4 points of a rhombus (diamond shape).
    The diagonals align with the bounding box of the drag.

    Args:
        start : (x, y) drag start on canvas
        end   : (x, y) drag end on canvas
    """
    x1, y1 = start
    x2, y2 = end
    mid_x   = (x1 + x2) // 2
    mid_y   = (y1 + y2) // 2
    return [(mid_x, y1),   # top
            (x2,   mid_y), # right
            (mid_x, y2),   # bottom
            (x1,   mid_y)] # left


# ─────────────────────────────────────────────────────────────────────────────
#  Button / Swatch
# ─────────────────────────────────────────────────────────────────────────────
class Button:
    """Clickable toolbar button."""

    def __init__(self, rect, label, value):
        self.rect  = rect
        self.label = label
        self.value = value

    def draw(self, surface, font, selected):
        color = (90, 90, 120) if selected else (60, 60, 80)
        pygame.draw.rect(surface, color, self.rect, border_radius=5)
        if selected:
            pygame.draw.rect(surface, SELECTED_RING, self.rect,
                             width=2, border_radius=5)
        text = font.render(self.label, True, TEXT_COLOR)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class ColourSwatch:
    """Clickable colour square."""

    SIZE = 22

    def __init__(self, rect, colour):
        self.rect   = rect
        self.colour = colour

    def draw(self, surface, selected):
        pygame.draw.rect(surface, self.colour, self.rect, border_radius=3)
        ring = SELECTED_RING if selected else BORDER_COLOR
        pygame.draw.rect(surface, ring, self.rect, width=2, border_radius=3)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


# ─────────────────────────────────────────────────────────────────────────────
#  Build toolbar
# ─────────────────────────────────────────────────────────────────────────────
def build_toolbar():
    """Creates and returns (tool_buttons, colour_swatches)."""
    bw, bh = 140, 30
    bx = 10
    y  = 50

    # All tools including new shapes (Features 1–4)
    tools = [
        ("✏ Pencil",      TOOL_PENCIL),
        ("▭ Rectangle",   TOOL_RECTANGLE),
        ("■ Square",      TOOL_SQUARE),       # Feature 1
        ("○ Circle",      TOOL_CIRCLE),
        ("◺ Right Tri",   TOOL_RTRIANGLE),    # Feature 2
        ("△ Equil Tri",   TOOL_ETRIANGLE),    # Feature 3
        ("◇ Rhombus",     TOOL_RHOMBUS),      # Feature 4
        ("◻ Eraser",     TOOL_ERASER),
    ]

    buttons = []
    for label, value in tools:
        buttons.append(Button(pygame.Rect(bx, y, bw, bh), label, value))
        y += bh + 4

    # Colour palette – 2 columns
    swatches = []
    sw  = ColourSwatch.SIZE
    pad = 5
    py  = y + 20
    for idx, colour in enumerate(PALETTE):
        col = idx % 2
        row = idx // 2
        rx  = bx + col * (sw + pad)
        ry  = py + row * (sw + pad)
        swatches.append(ColourSwatch(pygame.Rect(rx, ry, sw, sw), colour))

    return buttons, swatches


# ─────────────────────────────────────────────────────────────────────────────
#  Draw toolbar
# ─────────────────────────────────────────────────────────────────────────────
def draw_toolbar(surface, font, small_font, buttons, swatches,
                 current_tool, current_colour, brush_size):
    """Renders the full left toolbar."""
    pygame.draw.rect(surface, TOOLBAR_BG, (0, 0, TOOLBAR_WIDTH, WINDOW_HEIGHT))
    pygame.draw.line(surface, BORDER_COLOR,
                     (TOOLBAR_WIDTH - 1, 0), (TOOLBAR_WIDTH - 1, WINDOW_HEIGHT), 2)

    title = font.render("Paint", True, (150, 200, 255))
    surface.blit(title, (10, 12))

    for btn in buttons:
        btn.draw(surface, small_font, selected=(btn.value == current_tool))

    # Palette label
    pal_y = buttons[-1].rect.bottom + 24
    pal_l = small_font.render("Colours:", True, TEXT_COLOR)
    surface.blit(pal_l, (10, pal_y - 18))

    for sw in swatches:
        sw.draw(surface, selected=(sw.colour == current_colour))

    # Current colour preview
    preview = pygame.Rect(10, WINDOW_HEIGHT - 80, 140, 30)
    pygame.draw.rect(surface, current_colour, preview, border_radius=5)
    pygame.draw.rect(surface, BORDER_COLOR,  preview, width=2, border_radius=5)

    size_l = small_font.render(f"Brush: {brush_size}px", True, TEXT_COLOR)
    surface.blit(size_l, (10, WINDOW_HEIGHT - 42))
    hint = small_font.render("Scroll to resize", True, MUTED_COLOR)
    surface.blit(hint, (10, WINDOW_HEIGHT - 24))


# ─────────────────────────────────────────────────────────────────────────────
#  Canvas helpers
# ─────────────────────────────────────────────────────────────────────────────
def canvas_pos(pos):
    """Convert screen position to canvas-relative position."""
    return (pos[0] - CANVAS_X, pos[1])


def to_screen(pt):
    """Convert canvas-relative point to screen position."""
    return (pt[0] + CANVAS_X, pt[1])


def commit_shape(canvas, tool, colour, brush_size, start, end):
    """
    Permanently draws a completed shape onto the canvas surface.

    Args:
        canvas     : pygame.Surface (the drawing canvas)
        tool       : current tool string
        colour     : current drawing colour
        brush_size : line thickness
        start      : canvas-relative drag start (x, y)
        end        : canvas-relative drag end (x, y)
    """
    if tool == TOOL_RECTANGLE:
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = abs(end[0] - start[0])
        h = abs(end[1] - start[1])
        pygame.draw.rect(canvas, colour, (x, y, w, h), brush_size)

    elif tool == TOOL_SQUARE:
        # Feature 1 – force equal width and height
        side = min(abs(end[0] - start[0]), abs(end[1] - start[1]))
        x    = start[0] if end[0] >= start[0] else start[0] - side
        y    = start[1] if end[1] >= start[1] else start[1] - side
        pygame.draw.rect(canvas, colour, (x, y, side, side), brush_size)

    elif tool == TOOL_CIRCLE:
        cx = (start[0] + end[0]) // 2
        cy = (start[1] + end[1]) // 2
        r  = max(1, int(((end[0]-start[0])**2 + (end[1]-start[1])**2)**0.5 / 2))
        pygame.draw.circle(canvas, colour, (cx, cy), r, brush_size)

    elif tool == TOOL_RTRIANGLE:
        # Feature 2 – right triangle
        pts = right_triangle_points(start, end)
        if len(set(pts)) >= 3:
            pygame.draw.polygon(canvas, colour, pts, brush_size)

    elif tool == TOOL_ETRIANGLE:
        # Feature 3 – equilateral triangle
        pts = equilateral_triangle_points(start, end)
        if len(set(pts)) >= 3:
            pygame.draw.polygon(canvas, colour, pts, brush_size)

    elif tool == TOOL_RHOMBUS:
        # Feature 4 – rhombus
        pts = rhombus_points(start, end)
        if len(set(pts)) >= 3:
            pygame.draw.polygon(canvas, colour, pts, brush_size)


def draw_preview(screen, tool, colour, brush_size, start, end):
    """
    Draws a live preview on the screen (not the canvas) while dragging.
    Converts canvas-relative coordinates to screen coordinates.
    """
    # Convert to screen coords
    ss = to_screen(start)
    se = to_screen(end)

    if tool == TOOL_RECTANGLE:
        x = min(ss[0], se[0])
        y = min(ss[1], se[1])
        w = abs(se[0] - ss[0])
        h = abs(se[1] - ss[1])
        pygame.draw.rect(screen, colour, (x, y, w, h), brush_size)

    elif tool == TOOL_SQUARE:
        side = min(abs(se[0] - ss[0]), abs(se[1] - ss[1]))
        x    = ss[0] if se[0] >= ss[0] else ss[0] - side
        y    = ss[1] if se[1] >= ss[1] else ss[1] - side
        pygame.draw.rect(screen, colour, (x, y, side, side), brush_size)

    elif tool == TOOL_CIRCLE:
        cx = (ss[0] + se[0]) // 2
        cy = (ss[1] + se[1]) // 2
        r  = max(1, int(((se[0]-ss[0])**2 + (se[1]-ss[1])**2)**0.5 / 2))
        pygame.draw.circle(screen, colour, (cx, cy), r, brush_size)

    elif tool == TOOL_RTRIANGLE:
        pts = right_triangle_points(ss, se)
        if len(set(pts)) >= 3:
            pygame.draw.polygon(screen, colour, pts, brush_size)

    elif tool == TOOL_ETRIANGLE:
        # Convert canvas pts to screen pts
        cpts = equilateral_triangle_points(start, end)
        spts = [to_screen(p) for p in cpts]
        if len(set(spts)) >= 3:
            pygame.draw.polygon(screen, colour, spts, brush_size)

    elif tool == TOOL_RHOMBUS:
        cpts = rhombus_points(start, end)
        spts = [to_screen(p) for p in cpts]
        if len(set(spts)) >= 3:
            pygame.draw.polygon(screen, colour, spts, brush_size)


# ─────────────────────────────────────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────────────────────────────────────
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Paint – Practice 11")
    clock = pygame.time.Clock()

    font       = pygame.font.SysFont("Segoe UI", 18, bold=True)
    small_font = pygame.font.SysFont("Segoe UI", 13)

    # Canvas is a separate surface – shapes are committed here permanently
    canvas = pygame.Surface((CANVAS_WIDTH, CANVAS_HEIGHT))
    canvas.fill(CANVAS_BG)

    buttons, swatches = build_toolbar()

    # State
    current_tool   = TOOL_PENCIL
    current_colour = PALETTE[0]
    brush_size     = 4

    drawing    = False
    drag_start = None
    last_pos   = None

    # Tools that use click-drag-release (not continuous drawing)
    SHAPE_TOOLS = {TOOL_RECTANGLE, TOOL_SQUARE, TOOL_CIRCLE,
                   TOOL_RTRIANGLE, TOOL_ETRIANGLE, TOOL_RHOMBUS}

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
                    canvas.fill(CANVAS_BG)   # clear canvas

            elif event.type == pygame.MOUSEWHEEL:
                # Scroll wheel resizes brush
                brush_size = max(1, min(60, brush_size + event.y))

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if mouse_pos[0] < TOOLBAR_WIDTH:
                    # Toolbar click – select tool or colour
                    for btn in buttons:
                        if btn.is_clicked(mouse_pos):
                            current_tool = btn.value
                    for sw in swatches:
                        if sw.is_clicked(mouse_pos):
                            current_colour = sw.colour
                else:
                    # Canvas click – start drawing
                    cp         = canvas_pos(mouse_pos)
                    drawing    = True
                    drag_start = cp
                    last_pos   = cp
                    if current_tool == TOOL_PENCIL:
                        pygame.draw.circle(canvas, current_colour,
                                           cp, brush_size // 2)
                    elif current_tool == TOOL_ERASER:
                        pygame.draw.circle(canvas, CANVAS_BG,
                                           cp, brush_size)

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if drawing and mouse_pos[0] >= TOOLBAR_WIDTH:
                    cp = canvas_pos(mouse_pos)
                    # Commit shape tools on mouse release
                    if current_tool in SHAPE_TOOLS:
                        commit_shape(canvas, current_tool,
                                     current_colour, brush_size,
                                     drag_start, cp)
                drawing    = False
                drag_start = None
                last_pos   = None

            elif event.type == pygame.MOUSEMOTION:
                if drawing and mouse_pos[0] >= TOOLBAR_WIDTH:
                    cp = canvas_pos(mouse_pos)
                    # Pencil and eraser draw continuously
                    if current_tool == TOOL_PENCIL and last_pos:
                        pygame.draw.line(canvas, current_colour,
                                         last_pos, cp, brush_size)
                    elif current_tool == TOOL_ERASER and last_pos:
                        pygame.draw.line(canvas, CANVAS_BG,
                                         last_pos, cp, brush_size * 3)
                    last_pos = cp

        # ── Render ───────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)
        screen.blit(canvas, (CANVAS_X, 0))

        # Live shape preview while dragging
        if drawing and drag_start and current_tool in SHAPE_TOOLS:
            cp = canvas_pos(mouse_pos)
            draw_preview(screen, current_tool, current_colour,
                         brush_size, drag_start, cp)

        # Cursor preview circle
        if mouse_pos[0] >= TOOLBAR_WIDTH:
            r = brush_size if current_tool == TOOL_ERASER else brush_size // 2
            c = CANVAS_BG if current_tool == TOOL_ERASER else current_colour
            pygame.draw.circle(screen, c, mouse_pos, max(1, r), 1)

        draw_toolbar(screen, font, small_font, buttons, swatches,
                     current_tool, current_colour, brush_size)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
