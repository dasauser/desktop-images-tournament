# Photo Tournament

A desktop application that implements a single-elimination tournament system for image comparison and ranking.

## Features

- **Single-elimination tournament** — standard bracket system with automatic progression
- **Odd participant support** — first match of odd-numbered rounds contains 3 participants instead of 2
- **Batch image loading** — load all images from a directory or select specific files
- **EXIF orientation correction** — automatic image rotation based on embedded metadata
- **Real-time tracking** — displays current round and match number
- **Multi-format support** — JPEG, PNG, GIF, and BMP
- **Automatic scaling** — intelligently resizes images for display

## Supported Platforms

Cross-platform compatibility verified on:

- Windows 10, Windows 11
- Windows Subsystem for Linux 2 (WSL2)
- macOS 10.14+
- Linux (Ubuntu 20.04+)

Requires Python 3.8 or higher.

## Requirements

- **Python** 3.8+
- **PyQt6** 6.7.0
- **Pillow** 9.0+

## Installation

### From source

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/photo-tournament.git
   cd photo-tournament
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python tournament_app.py
   ```

### Precompiled executable

Download `tournament_app.exe` for Windows and execute directly. No dependencies required.

## Usage

### Start tournament
1. Launch the application
2. Click **"Load Images from Folder"** to load all images from a directory, or **"Select Images"** to choose specific files
3. Click **"Start Tournament"**

### During tournament
1. Two (or three, in the first match of odd-numbered rounds) images are displayed
2. Click on the image you prefer
3. Selected image advances to the next round
4. Repeat until a single winner remains

### Tournament mechanics
- All participants are randomized before the first round
- Each round eliminates losing images
- First match of odd-numbered rounds contains 3 participants; subsequent matches contain 2
- Process continues until one image remains

## File Structure

```
photo-tournament/
├── tournament_app.py      — Main application
├── requirements.txt       — Python dependencies
└── README.md             — Documentation
```

## Technical Details

**GUI Framework:** PyQt6 — cross-platform desktop application framework

**Image Processing:** Pillow — handles image loading, scaling, and EXIF metadata extraction and application

**Architecture:** Single-window application using QStackedWidget for scene management (menu, tournament, results)

## Known Limitations

- Loading 1000+ images may require several seconds depending on average image size
- Images larger than 10000×10000 pixels are automatically scaled for display
- First match of odd-numbered rounds contains 3 participants instead of 2

## Building Executable

Using PyInstaller:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed tournament_app.py
```

Compiled executable will be in `dist/tournament_app.exe`.

## License

MIT License

---

*Proof-of-concept project provided as-is without warranty.*
