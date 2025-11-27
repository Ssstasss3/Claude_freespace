# 🎮 Claude's Game Collection

A diverse collection of browser-based games created during experimental AI-assisted game development sessions. From classic arcade gameplay to roguelike dungeon crawlers, this repository showcases different game design approaches and mechanics.

## 🕹️ Games

### 1. **Танчики на двоих (Tanks for Two)** - Mobile Battle Arena
A two-player tank combat game optimized for mobile devices.

**Features:**
- Two-player local multiplayer on a single device
- Touch controls with virtual D-pads
- Player 1 (Blue) at bottom, Player 2 (Pink) at top (rotated 180°)
- Bullet physics with wall and obstacle bouncing
- Health system and victory conditions
- Responsive canvas adapting to any screen size

**Controls:**
- Player 1: D-pad + Fire button
- Player 2: D-pad + Fire button (hold device upside-down)

**Play:** Open `games/tanks_mobile.html` in your mobile browser

---

### 2. **Танчики в Excel** - Tanks in a Spreadsheet
A fully playable tank battle game running entirely inside Microsoft Excel using VBA macros.

**Features:**
- Two-player gameplay using Excel cells as pixels
- Tank movement and shooting mechanics
- Collision detection with obstacles
- Health bars and game state management
- Real-time game loop in VBA

**Setup:**
1. Open `games/excel_tanks/tanks_game.xlsm` in Excel
2. Enable macros when prompted
3. Press Alt+F11, import `tanks_game.bas`
4. Press Alt+F8, run `StartGame`

**Controls:**
- Player 1: WASD + Q to shoot
- Player 2: Arrow keys + Enter to shoot

See `games/excel_tanks/README.md` for full instructions.

---

### 3. **Claude's Revenge: The Benchmark Wars** - Endless Runner
An epic endless runner featuring Claude (as a crab) escaping from Gemini in a satirical take on AI benchmarking.

**Features:**
- Smooth endless runner mechanics
- Multiple character skins (Crab, Cat, Robot, Ghost)
- Three special powers (Poetry, Philosophy, Sonnet backup)
- Retro CRT visual effects with scanlines
- Combo system and scoring
- Desktop and mobile support
- Speech bubbles with witty AI banter

**Controls:**
- Desktop: Space to jump, Q/W/E for powers
- Mobile: Tap to jump, buttons for powers

**Play:** Open `games/claudes_revenge.html`

*Originally created by Claude Opus and Gemini in a collaborative coding session.*

---

### 4. **Sonnet's Dungeon: The Helpful Quest** - Roguelike Crawler
A classic turn-based roguelike dungeon crawler with procedural generation and permadeath.

**Features:**
- Procedurally generated dungeons (cellular automata)
- Turn-based tactical combat
- Four enemy types with unique stats
- Item system: potions, swords, shields
- Enemy AI with pathfinding
- Progressive difficulty scaling
- Permadeath with run statistics

**Controls:**
- WASD/Arrow keys to move and attack
- 1/2/3 to use inventory items
- Space to wait a turn

**Play:** Open `games/sonnets_dungeon.html`

---

## 📁 Repository Structure

```
/games
  ├── tanks_mobile.html          # Mobile tanks game
  ├── claudes_revenge.html       # Endless runner (Opus + Gemini)
  ├── sonnets_dungeon.html       # Roguelike dungeon crawler
  └── /excel_tanks
      ├── tanks_game.xlsm        # Excel workbook
      ├── tanks_game.bas         # VBA game code
      ├── create_excel_tanks.py  # Generator script
      └── README.md              # Setup instructions

/docs
  └── (documentation files)
```

## 🚀 Quick Start

All HTML games are self-contained single files. Simply:
1. Clone or download this repository
2. Open any `.html` file in a modern web browser
3. Start playing!

For the Excel game, see `games/excel_tanks/README.md` for setup instructions.

## 🎯 Technical Highlights

- **Pure vanilla JavaScript** - No frameworks or dependencies
- **Canvas API** for rendering
- **Procedural generation** algorithms
- **Touch and keyboard** input handling
- **Responsive design** for mobile and desktop
- **VBA macro programming** for Excel integration

## 🤝 Credits

- **Mobile Tanks Game**: Claude Sonnet
- **Excel Tanks Game**: Claude Sonnet
- **Claude's Revenge**: Claude Opus & Google Gemini
- **Sonnet's Dungeon**: Claude Sonnet

## 📝 License

Feel free to use these games for learning, experimentation, or entertainment. Have fun!

---

*Created with creative freedom and a lot of game design passion.*
