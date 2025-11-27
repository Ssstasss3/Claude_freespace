# 🎮 Claude's Creative Workspace

A diverse collection of browser-based games, interactive data visualizations, and experimental AI architecture simulators. From classic arcade gameplay to roguelike dungeon crawlers, business intelligence dashboards, and novel neural network designs, this repository showcases different approaches to interactive web development and AI research visualization.

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

## 📊 Data Visualizations

### 5. **Retail Banking Analytics Dashboard** - Power BI-Style Interactive Dashboard
A comprehensive business intelligence dashboard analyzing retail banking data with interactive filters and visualizations.

**Features:**
- 4 KPI cards: Total customers, conversion rate, housing loans, average age
- 7 interactive charts (bar, line, pie, doughnut)
- Real-time filtering by age group, job, education, marital status
- 41,188 customer records from UCI Machine Learning Repository
- Campaign performance tracking by month
- Loan portfolio analysis
- Customer demographics breakdown

**Data Visualizations:**
- Customer distribution by job type
- Education level breakdown
- Age distribution analysis
- Loan portfolio overview
- Monthly campaign performance
- Marital status distribution
- Contact method effectiveness

**Data Source:** [UCI Bank Marketing Dataset](https://archive.ics.uci.edu/dataset/222/bank+marketing) (Creative Commons BY 4.0)

**View:** Open `banking_dashboard.html` in your browser

---

## 🧠 Experimental AI Architecture

### 6. **Librarian-Analyst Architecture Simulator** - Novel AI System Design
An interactive proof-of-concept for a novel AI architecture combining dynamic knowledge retrieval, adaptive reasoning, and physics-inspired optimization.

**Architecture Components:**
- **Librarians**: Clustered knowledge bases storing facts as vector embeddings
- **Analysts**: Attention layers that query paired librarians using cross-attention
- **Temperature Dynamics**: Adaptive local and global temperature control
- **Pruning/Resurrection**: Dynamic analyst lifecycle management
- **Multi-layer Evolution**: Iterative refinement across 10+ layers

**Key Innovations:**
- Temperature as resource/currency (facts consume temperature when retrieved)
- Grounded reasoning (analysts learn generalizations anchored to librarian facts)
- Dynamic pruning (low-performing analysts removed, efficiency improves with depth)
- Resurrection mechanism (similar data triggers dormant analyst revival)
- Adaptive exploration/exploitation balance via temperature
- Diffusion layers for stochastic creativity injection

**Interactive Features:**
- Real-time network visualization showing librarian-analyst connections
- Adjustable parameters (50-100 librarians, 5-20 layers, temperature, diffusion)
- Step-by-step or automatic evolution modes
- Live statistics: active analysts, facts retrieved, resurrections
- Layer-by-layer history tracking
- Color-coded temperature indicators (blue=confident, pink=cautious, gray=pruned)

**Theoretical Foundation:**
- Inspired by MoE (Mixture of Experts), RAG (Retrieval-Augmented Generation)
- Physics-inspired: Onsager-Machlup formalism, least action principle
- State evolution: deterministic weights × stochastic weights + stochastic tensor
- Exploitation engine + exploration engine balance

**Technical Details:**
- Cross-attention querying using cosine similarity
- Vector embeddings (8-dimensional in demo, scalable to 768D+)
- Perceiver architecture for efficient attention
- Self-attention layers for state refinement
- Clustering for specialized knowledge regions

**Use Cases:**
- Visualizing dynamic neural architecture concepts
- Understanding temperature-based resource allocation
- Exploring adaptive pruning/resurrection mechanisms
- Teaching MoE and RAG principles interactively

**Explore:** Open `librarian_analyst_architecture.html` in your browser

*Experimental architecture exploring grounded reasoning, adaptive specialization, and dynamic network topology.*

---

## 📁 Repository Structure

```
/
├── banking_dashboard.html              # Power BI-style analytics dashboard
├── bank_data.csv                       # Retail banking dataset (41K records)
├── librarian_analyst_architecture.html # AI architecture simulator
└── /games
    ├── tanks_mobile.html               # Mobile tanks game
    ├── claudes_revenge.html            # Endless runner (Opus + Gemini)
    ├── sonnets_dungeon.html            # Roguelike dungeon crawler
    └── /excel_tanks
        ├── tanks_game.xlsm             # Excel workbook
        ├── tanks_game.bas              # VBA game code
        ├── create_excel_tanks.py       # Generator script
        └── README.md                   # Setup instructions
```

## 🚀 Quick Start

All HTML games are self-contained single files. Simply:
1. Clone or download this repository
2. Open any `.html` file in a modern web browser
3. Start playing!

For the Excel game, see `games/excel_tanks/README.md` for setup instructions.

## 🎯 Technical Highlights

- **Pure vanilla JavaScript** - No frameworks or dependencies
- **Canvas API** for game rendering and network visualization
- **Chart.js** for data visualization
- **Procedural generation** algorithms
- **Touch and keyboard** input handling
- **Responsive design** for mobile and desktop
- **VBA macro programming** for Excel integration
- **CSV parsing** and data processing
- **Interactive filtering** and real-time updates
- **Vector embeddings** and cosine similarity
- **Cross-attention mechanisms** and dynamic neural architectures
- **Temperature-based resource allocation**
- **Physics-inspired optimization** (Onsager-Machlup formalism)

## 🤝 Credits

**Games:**
- **Mobile Tanks Game**: Claude Sonnet
- **Excel Tanks Game**: Claude Sonnet
- **Claude's Revenge**: Claude Opus & Google Gemini
- **Sonnet's Dungeon**: Claude Sonnet

**Data Visualizations:**
- **Banking Analytics Dashboard**: Claude Sonnet
- **Dataset**: UCI Machine Learning Repository

**Experimental AI:**
- **Librarian-Analyst Architecture**: Claude Sonnet
- **Theoretical Foundation**: Collaborative exploration with user

## 📝 License

Feel free to use these games for learning, experimentation, or entertainment. Have fun!

---

*Created with creative freedom and a lot of game design passion.*
