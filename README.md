# 🎩 Tycoon Monopoly

A feature-rich, visually polished Monopoly game implementation in Python using `tkinter`. This project brings the classic board game experience to your desktop with a modern "Tycoon" aesthetic, including custom property names, interactive UI, and full game logic.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![UI](https://img.shields.io/badge/UI-Tkinter-orange)

---

## ✨ Features

- **🎮 Full Game Logic:** Complete implementation of Monopoly rules including trading, auctions, mortgages, and building houses/hotels.
- **🎨 Modern UI:** A custom-styled `tkinter` interface with a dark theme and vibrant property colors.
- **🤖 AI Players:** Play solo against intelligent AI opponents or with friends in local multiplayer.
- **🎲 Dynamic Events:** Full implementation of "Fate" (Chance) and "Vault" (Community Chest) cards.
- **🏠 Property Management:** Detailed management of your portfolio, including color-group tracking and house building.
- **🚀 Portable:** Can be easily bundled into a standalone executable using the included `.spec` file.

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher installed on your system.

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/monopoly.git
   cd monopoly
   ```

2. **No external dependencies required!**
   The game uses `tkinter`, which is included in most standard Python installations.

## 🚀 How to Play

1. **Start the game:**
   ```bash
   python monopoly.py
   ```
2. **Setup:** Choose the number of players (Human and AI) and pick your tokens.
3. **Roll & Move:** Click the "Roll Dice" button to move your token around the board.
4. **Win:** Bankrupt your opponents to become the ultimate Tycoon!

## 📦 Building Standalone Executable

If you want to create a `.exe` for Windows:
1. Install PyInstaller: `pip install pyinstaller`
2. Run the build command:
   ```bash
   pyinstaller monopoly.spec
   ```
3. The executable will be in the `dist/` folder.

## 🗺️ Board Preview

The game features unique locations like:
- **Neon Blvd** & **Cyber St** (Pink Group)
- **Billion Row** & **Tycoon Twr** (Dark Blue Group)
- **Slum St** (Brown Group)
- **North/East/South/West Railroads**

## 🤝 Contributing

Contributions are welcome! If you have ideas for new features or find a bug, feel free to:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

Distributed under the MIT License. See `LICENSE` (to be added) for more information.

---
*Created with ❤️ for the gaming community.*
