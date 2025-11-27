# ТАНЧИКИ В EXCEL (Tanks in Excel)

A fully playable two-player tank battle game inside Microsoft Excel using VBA macros!

## 📦 What's Included

- **tanks_game.xlsm** - Excel workbook with pre-configured game board
- **tanks_game.bas** - VBA macro code with game logic
- **README_EXCEL_TANKS.md** - This file

## 🎮 How to Play

### Setup Instructions

1. **Open the Excel File**
   - Open `tanks_game.xlsm` in Microsoft Excel
   - You'll see a security warning about macros

2. **Enable Macros**
   - Click "Enable Content" or "Enable Macros" in the security banner
   - This is required for the game to work

3. **Import the VBA Code**
   - Press `Alt+F11` to open the VBA Editor
   - Go to `File` > `Import File...`
   - Select `tanks_game.bas`
   - Close the VBA Editor (`Alt+Q` or click the X)

4. **Start the Game**
   - Press `Alt+F8` to open the Macros dialog
   - Select `StartGame` from the list
   - Click `Run`

### Controls

**Player 1 (Blue Tank) - Left Side**
- `W` - Move Up
- `A` - Move Left
- `S` - Move Down
- `D` - Move Right
- `Q` - Shoot

**Player 2 (Pink Tank) - Right Side**
- `↑` Arrow - Move Up
- `←` Arrow - Move Left
- `↓` Arrow - Move Down
- `→` Arrow - Move Right
- `Enter` - Shoot

**General**
- `ESC` - Stop/Exit Game

## 🎯 Game Rules

- Each player starts with **100 HP**
- Bullets deal **20 damage** per hit
- Bullets bounce off walls and obstacles
- Gray obstacles block movement and bullets
- First player to reach 0 HP loses
- Health is displayed at the bottom of the game board

## 🏗️ How It Works

The game uses:
- **Excel cells as pixels** - Each cell represents one game unit
- **Cell colors** - Different colors for tanks, bullets, obstacles
- **VBA macros** - Game logic, collision detection, movement
- **Keyboard events** - Capture player input
- **Game loop** - Updates at ~10 FPS

## ⚠️ Technical Notes

- The game runs in real-time using VBA's game loop
- Due to Excel's single-threaded nature, performance may vary
- Tested on Excel 2016+ (Windows/Mac)
- The .xlsm file preserves the game board layout
- VBA code must be imported manually due to security restrictions

## 🎨 Features

- Two-player local multiplayer
- Bullet physics with bouncing
- Strategic obstacle placement
- Real-time health tracking
- Visual feedback with colored cells
- Classic arcade-style gameplay

## 🔧 Troubleshooting

**"Macros are disabled"**
- Go to File > Options > Trust Center > Trust Center Settings
- Select "Enable all macros" (or add the folder to Trusted Locations)

**"StartGame macro not found"**
- Make sure you imported tanks_game.bas correctly
- Check the VBA Editor (Alt+F11) - you should see a "TanksGame" module

**Game is slow**
- Close other Excel workbooks
- Reduce the number of active bullets on screen
- Ensure your Excel is up to date

**Keys not responding**
- Make sure the Game sheet is active
- Try clicking on the worksheet first
- Ensure no other cells are selected

## 🎉 Enjoy!

This is a creative experiment pushing Excel beyond its typical use case. Have fun battling in the world's most unexpected gaming platform!

---

**Created with creative freedom by Claude**
*"Because why not?"*
