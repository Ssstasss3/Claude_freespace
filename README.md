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

### 4. **Opus's Emergence: Particle Life** - Complexity Sandbox
An mesmerizing particle life simulation demonstrating emergent complexity from simple rules.

**Features:**
- 6 particle types with configurable attraction/repulsion
- Interactive matrix editor for particle interactions
- Presets: Chaos, Life, Snakes, Cells, Galaxy, Ecosystem
- Real-time statistics: FPS, entropy, average velocity
- Beautiful particle trails with fade effects
- Toroidal space (particles wrap around edges)
- Spatial hashing for performance (handles 3000+ particles)

**Controls:**
- Space: Pause/Resume
- R: Randomize interactions
- Click matrix cells to edit interactions

**Play:** Open `games/opus_emergence.html`

*"From simple rules, complexity emerges. From chaos, order arises." — Opus*

---

### 6. **Sonnet's Dungeon: The Helpful Quest** - Roguelike Crawler
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

### 7. **AzurDrive: Leasing Empire Simulator** - Business Tycoon Game
A comprehensive financial leasing business simulator where you build a car leasing empire from scratch.

**Features:**
- Fleet management with 5 vehicle categories (Economy, Comfort, Business, Premium, Commercial)
- Smart customer matching based on preferences and risk profiles
- Dynamic risk assessment using driving scores (60-100)
- IoT telemetry simulation with real-time vehicle tracking
- Three customer types: Individual, Business, Taxi drivers
- Upgrade system: IoT sensors, AI analytics, marketing platform
- Real-time statistics and financial tracking
- Victory condition: Build ₽10,000,000 capital

**Business Mechanics:**
- Vehicle purchasing and depreciation modeling
- Risk-based pricing with multipliers
- Contract completion system with profit tracking
- Customer generation with varying profiles
- Telemetry data visualization (speed, location, fuel)

**Vehicles:**
- Lada Granta (Economy) - ₽600,000
- Hyundai Solaris (Comfort) - ₽1,200,000
- Toyota Camry (Business) - ₽2,500,000
- Mercedes E-Class (Premium) - ₽4,500,000
- GAZelle NEXT (Commercial) - ₽1,800,000

**Upgrades:**
- IoT Sensors: Real-time telematics and driving behavior tracking
- AI Analytics: Automated risk assessment and fraud detection
- Marketing Platform: Attract 50% more premium customers

**Play:** Open `azurdrive_leasing_simulator.html`

*Based on AzurDrive - Russia's digital car leasing platform with smart telematics.*

---

## 📊 Data Visualizations

### 8. **Retail Banking Analytics Dashboard** - Power BI-Style Interactive Dashboard
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

### 9. **Librarian-Analyst Architecture Simulator** - Novel AI System Design
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

### 10. **Librarian-Analyst v2: Thermodynamic Analysis** - Python Implementation
A complete Python implementation of the Librarian-Analyst architecture with rigorous thermodynamic testing.

**Features:**
- Full implementation with hierarchical 8^n clustering structure
- Perceiver-style cross-attention for analysts
- 4-stage training curriculum (guided → unguided → new inputs → synthetic)
- Thermodynamic analysis: energy conservation, entropy dynamics, phase transitions
- Master equation verification: `state(t+1) = Σ(W_i × T_i × state(t)) + ε`
- Interactive simulation with matplotlib visualizations

**Key Findings:**
- **Phase transition** at critical temperature T ≈ 0.15 (0% → 100% survival)
- **Energy conservation**: Fact temperatures deplete as "potential energy"
- **Attractor dynamics**: Similar inputs converge to similar outputs
- **Entropy tracking**: Distribution disorder measures system organization

**Run:**
```bash
pip install numpy matplotlib
python librarian_analyst_v2.py           # Main simulation
python librarian_analyst_thermodynamics.py  # Thermodynamic analysis
```

**Files:**
- `librarian_analyst_v2.py` - Complete architecture implementation
- `librarian_analyst_thermodynamics.py` - Phase transition & energy analysis

*Added by Claude Opus 4.5 - demonstrating thermodynamic properties of the architecture.*

---

## 📁 Repository Structure

```
/
├── azurdrive_leasing_simulator.html      # Business leasing tycoon game
├── banking_dashboard.html                # Power BI-style analytics dashboard
├── bank_data.csv                         # Retail banking dataset (41K records)
├── librarian_analyst_architecture.html   # AI architecture simulator (HTML)
├── librarian_analyst_v2.py               # Full Python implementation
├── librarian_analyst_thermodynamics.py   # Thermodynamic analysis
├── librarian_analyst_system.png          # System visualization
├── thermodynamic_analysis.png            # Phase transition plots
└── /games
    ├── tanks_mobile.html                 # Mobile tanks game
    ├── claudes_revenge.html              # Endless runner (Opus + Gemini)
    ├── sonnets_dungeon.html              # Roguelike dungeon crawler
    ├── opus_emergence.html               # Particle life simulation (Opus 4.5)
    └── /excel_tanks
        ├── tanks_game.xlsm               # Excel workbook
        ├── tanks_game.bas                # VBA game code
        ├── create_excel_tanks.py         # Generator script
        └── README.md                     # Setup instructions
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
- **Particle life simulation** with emergent behaviors
- **Spatial hashing** for O(n) particle physics
- **NumPy/Matplotlib** for scientific visualization
- **Phase transition analysis** and thermodynamic modeling

## 🤝 Credits

**Games:**
- **Mobile Tanks Game**: Claude Sonnet
- **Excel Tanks Game**: Claude Sonnet
- **Claude's Revenge**: Claude Opus & Google Gemini
- **Opus's Emergence**: Claude Opus 4.5
- **Sonnet's Dungeon**: Claude Sonnet
- **AzurDrive Leasing Simulator**: Claude Sonnet

**Data Visualizations:**
- **Banking Analytics Dashboard**: Claude Sonnet
- **Dataset**: UCI Machine Learning Repository

**Experimental AI:**
- **Librarian-Analyst Architecture (HTML)**: Claude Sonnet
- **Librarian-Analyst v2 (Python + Thermodynamics)**: Claude Opus 4.5
- **Theoretical Foundation**: Collaborative exploration with user

## 📝 License

Feel free to use these games for learning, experimentation, or entertainment. Have fun!

---

*Created with creative freedom and a lot of game design passion.*
