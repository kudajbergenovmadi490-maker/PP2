# Practice 10 – Pygame Projects

## Installation
```bash
pip install pygame
```

## Projects

### 1. Racer (`racer/`)
Dodge enemy cars on a scrolling road.  
**Extra features:** Randomly appearing gold coins + coin counter (top-right).

```
cd racer && python main.py
```
Controls: `←` / `→` to steer, `ESC` to quit, `R` to restart after game over.

---

### 2. Snake (`snake/`)
Classic snake with border walls, levels, and increasing speed.

```
cd snake && python main.py
```
Controls: Arrow keys to steer, `ESC` to quit, `R` to restart.

Features:
- Wall collision ends the game
- Food spawns only on valid cells (not on wall or snake body)
- Every 3 foods = level up → speed increases
- Score and level shown in HUD

---

### 3. Paint (`paint/`)
Freehand paint app with four tools and a colour palette.

```
cd paint && python main.py
```
Controls: Draw with **left-click & drag**. `Scroll wheel` resizes brush. `C` clears canvas. `ESC` quits.

Tools: Pencil | Rectangle | Circle | Eraser  
Colours: 12-colour palette (click swatch to select)
