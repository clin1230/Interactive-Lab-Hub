#!/bin/bash
# Setup script for Gesture DJ project
# Run this script once to set up everything

set -e  # Exit on error

echo "=========================================="
echo "       Gesture DJ Setup Script"
echo "=========================================="
echo ""

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Create virtual environment
echo "[1/6] Creating Python virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "      Virtual environment created."
else
    echo "      Virtual environment already exists."
fi

# Activate virtual environment
source venv/bin/activate

# 2. Upgrade pip
echo ""
echo "[2/6] Upgrading pip..."
pip install --upgrade pip

# 3. Install Python dependencies
echo ""
echo "[3/6] Installing Python dependencies..."
pip install -r requirements.txt

# 4. Install lgpio (required for Raspberry Pi 5)
echo ""
echo "[4/6] Installing lgpio for Raspberry Pi 5..."
pip install lgpio 2>/dev/null || echo "      lgpio already installed or not needed."

# 5. Download Vosk speech recognition model
echo ""
echo "[5/6] Downloading Vosk speech recognition model..."
VOSK_MODEL_PATH="$HOME/.cache/vosk/vosk-model-small-en-us-0.15"
if [ ! -d "$VOSK_MODEL_PATH" ]; then
    echo "      Downloading model (this may take a minute)..."
    python3 -c "from vosk import Model; Model(lang='en-us')" 2>/dev/null || echo "      Model will download on first run."
    echo "      Vosk model downloaded."
else
    echo "      Vosk model already cached."
fi

# 6. Create directories and placeholder files
echo ""
echo "[6/6] Setting up project directories..."
mkdir -p tracks
mkdir -p effects

# Create tracks README
cat > tracks/README.md << 'EOF'
# Tracks Directory

Place your 10 MP3 track files here with the following naming:
- track01.mp3
- track02.mp3
- track03.mp3
- track04.mp3
- track05.mp3
- track06.mp3
- track07.mp3
- track08.mp3
- track09.mp3
- track10.mp3

## Suggested Track Sources:
- Free Music Archive (https://freemusicarchive.org/)
- Incompetech (https://incompetech.com/music/)
- YouTube Audio Library
- Bensound (https://www.bensound.com/)

## Track Guidelines:
- Format: MP3
- Length: 10-60 seconds works well for DJ loops
- Quality: 128kbps or higher
- License: Royalty-free or Creative Commons
EOF

# Create effects README
cat > effects/README.md << 'EOF'
# Effects Directory

Place your sound effect MP3 files here:
- beep.mp3 (track change confirmation)
- click.mp3 (volume change confirmation)
- swoosh.mp3 (theme change sound effect)
- scratch1.mp3 (DJ scratch effect)
- scratch2.mp3 (DJ scratch effect)
- scratch3.mp3 (DJ scratch effect)
- scratch4.mp3 (DJ scratch effect)

## Suggested Effect Sources:
- Freesound (https://freesound.org/)
- Zapsplat (https://www.zapsplat.com/)
- SoundBible (http://soundbible.com/)

## Effect Guidelines:
- Format: MP3
- Length: 0.1-1.0 seconds (short and punchy)
- Volume: Moderate (not too loud)
- License: Royalty-free or Creative Commons
EOF

echo ""
echo "=========================================="
echo "           Setup Complete!"
echo "=========================================="
echo ""
echo "Directory structure:"
echo "  tracks/     - Place 10 MP3 tracks (track01.mp3 - track10.mp3)"
echo "  effects/    - Place sound effects (beep.mp3, click.mp3, swoosh.mp3, scratch1-4.mp3)"
echo ""
echo "Hardware Setup:"
echo "  1. Enable I2C and SPI:"
echo "     sudo raspi-config"
echo "     -> Interface Options -> I2C -> Enable"
echo "     -> Interface Options -> SPI -> Enable"
echo ""
echo "  2. Verify sensors:"
echo "     sudo i2cdetect -y 1"
echo "     (Should show 39 for APDS, 5a for MPR121)"
echo ""
echo "To run the Gesture DJ:"
echo "  1. Activate virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. Run the application:"
echo "     python gesture_dj.py"
echo ""
echo "  3. Run with web visualization:"
echo "     python gesture_dj.py --web"
echo ""
echo "Controls:"
echo "  APDS-9960 Gestures:"
echo "    - Swipe RIGHT: Next track"
echo "    - Swipe LEFT:  Previous track"
echo "    - Swipe UP:    Volume up"
echo "    - Swipe DOWN:  Volume down"
echo ""
echo "  MPR121 Touch Pads (if connected):"
echo "    - Pads 0-9:    Select track 1-10"
echo "    - Pad 10:      Play/Pause"
echo "    - Pad 11:      Stop"
echo ""
echo "  Voice Commands:"
echo "    - Say 'play':  Start playback"
echo "    - Say 'pause': Pause playback"
echo ""
echo "  Hand Gestures (camera required):"
echo "    - Open Palm (5 fingers):   Light theme (hold 2.5s)"
echo "    - Closed Fist (0 fingers): Dark theme (hold 2.5s)"
echo "    - Peace Sign (2 fingers):  DJ scratch effect (instant)"
echo ""
echo "Done!"
