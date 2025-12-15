# Gesture DJ 🎵

A multi-modal DJ controller for Raspberry Pi that uses gesture sensors, touch input, voice commands, and hand tracking to control music playback with real-time web visualizations.

**Project Team:**
- Eva Huang (lh764)
- Zoe Tseng (yzt2)
- Charlotte Lin (hl2575)

## 📹 Demo Video

<a href="https://youtube.com/shorts/_Esceg73g3c"><img src="https://img.youtube.com/vi/_Esceg73g3c/hqdefault.jpg" alt="Demo Video" width="500"></a>

<a href="https://youtube.com/shorts/_wjvhvSJUlQ"><img src="https://img.youtube.com/vi/_wjvhvSJUlQ/hqdefault.jpg" alt="Demo Video" width="500"></a>

*▶️ Click above to watch someone using Gesture DJ!*

## 📸 Project Photos

### The Complete Device
<!-- Add photo of your finished device -->
<img src="https://hackmd.io/_uploads/rJWBAaTfZl.jpg" alt="Gesture DJ Device" width="400">

### Hardware Setup
<img src="https://hackmd.io/_uploads/rk_srCTMZx.jpg" alt="Full Setup" width="400">

### Web Interface Screenshots
| Light Theme | Dark Theme |
|-------------|------------|
| ![Light Theme](YOUR_SCREENSHOT_URL) | <img src="https://hackmd.io/_uploads/Sy0avApfZe.png" alt="Dark Theme" width="300"> |


## Deliverables

| Deliverable | Link/Status |
|-------------|-------------|
| 📋 Project Plan | [View Plan](https://github.com/zyt02/Interactive-Lab-Hub/blob/Fall2025/final_project_plan.md) |
| 📝 Design Documentation | See [Design Documentation](#design-documentation) below |
| 💻 Code Archive | This repository |
| 💭 Reflections | See [Reflection](#reflection) below |

## Features

### 1. APDS-9960 Gesture Sensor
Navigate music library intuitively with proximity-based gesture control:
- **Track Navigation**
  - ➡️ Swipe RIGHT → Next track (auto-play)
  - ⬅️ Swipe LEFT → Previous track (auto-play)
- **Volume Control**
  - ⬆️ Swipe UP → Volume up (+10%)
  - ⬇️ Swipe DOWN → Volume down (-10%)

### 2. MPR121 Capacitive Touch Pads
Direct track selection at your fingertips:
- **Track Selection**
  - 🔢 Pads 0-9 → Instant access to tracks 1-10
- **Playback Control**
  - ▶️ Pad 10 → Play/Pause toggle
  - ⏹️ Pad 11 → Stop playback

### 3.  Voice Commands
Control playback with natural voice commands using Vosk offline speech recognition:
- **Play Commands**
  - 🗣️ Say "play", "start", "go", or "resume" → Begin/resume playback
- **Pause Commands**
  - 🗣️ Say "pause", "stop", "wait", or "hold" → Pause playback
- Works with any USB microphone
- No internet connection required

### 4. MediaPipe Hand Gesture Recognition
Advanced computer vision-based controls using Google's MediaPipe framework. A USB camera captures video that's processed in real-time to detect hand landmarks and classify gestures.

#### Theme Control
Hold gesture for 2.5 seconds to change theme:
- **Light Theme**
  - ✋ Open Palm (5 fingers) → Baby blue gradient UI
- **Dark Theme**
  - ✊ Closed Fist (0 fingers) → Midnight cyberpunk UI
- Hold requirement prevents accidental triggers
- Swoosh sound effect confirms theme change

#### DJ Effects
- **Scratch Effect**
  - ✌️ Peace Sign (2 fingers) → Instant DJ scratch
  - Randomly selects from 4 scratch samples
  - Plays over music without interrupting
  - 0.5 second cooldown between triggers

### 5. PiTFT Display
Immersive visual feedback directly on the device:
- **Retro vaporwave aesthetic** with 80s-inspired graphics
- Real-time track info and system status
- Volume level bars
- Playback status icons

### 6. Web Interface
Access music system from any device on your network:
- **Real-time camera feed** showing hand gesture recognition
- **Playback controls** for play/pause functionality
- **Volume slider** for precise audio level adjustment
- **Theme indicator** showing current light/dark mode
- **Track information** with current track name and progress
- WebSocket-based real-time updates (20 FPS)

#### Dynamic Audio Visualizations
Multiple visualization modes that respond to music in real-time:

| Mode | Description |
|------|-------------|
| **WAVEFORM** | Oscilloscope-style amplitude display with beat-reactive glow effects |
| **SPECTRUM** | Frequency spectrum analyzer with gradient coloring from bass (red) to treble (blue) |
| **AUDIENCE** | RGB bar visualization that bounces with bass levels, simulating a crowd at a concert |
| **PARTICLES** | Pulsing rings and particle burst effects synchronized to beat detection |

**Technical Details:**
- Visualizations use simulated audio data with beat detection algorithms
- Bass/mid/high frequency separation for reactive effects
- Smooth CSS transitions for theme changes
- MJPEG streaming for camera feed (same approach as standard webcam servers)


## Quick Start

```bash
# 1. Navigate to project directory
cd ~/Interactive-Lab-Hub/Final\ Project

# 2. Run setup (first time only)
chmod +x setup.sh && ./setup.sh

# 3. Add your MP3 files to tracks/ directory (track01.mp3 - track10.mp3)

# 4. Start the DJ!
source venv/bin/activate
python gesture_dj.py --web
```

Then open `http://<your-pi-ip>:5000` in a browser to see visualizations and camera feed.

## Hardware Requirements

### Required
- Raspberry Pi 5 (or Pi 4)
- APDS-9960 Gesture Sensor (I2C address: 0x39)
- PiTFT Display (SPI)
- USB Microphone (for voice control)
- USB Camera (for MediaPipe hand tracking)
- Speakers or headphones (3.5mm audio output)
- MPR121 Capacitive Touch Sensor (I2C address: 0x5A)
- Desktop or Laptop for Web Interface
- Wood boards and arcrylic materials for physical device design 

## Wiring

### APDS-9960 (I2C)
| APDS-9960 | Raspberry Pi |
|-----------|--------------|
| VCC       | 3.3V         |
| GND       | GND          |
| SDA       | GPIO 2 (SDA) |
| SCL       | GPIO 3 (SCL) |

### MPR121 (I2C)
| MPR121    | Raspberry Pi |
|-----------|--------------|
| VCC       | 3.3V         |
| GND       | GND          |
| SDA       | GPIO 2 (SDA) |
| SCL       | GPIO 3 (SCL) |

### PiTFT Display (SPI)
| PiTFT     | Raspberry Pi |
|-----------|--------------|
| CS        | GPIO 5 (CE0) |
| DC        | GPIO 25      |
| SPI       | Hardware SPI |

## Installation

### 1. Clone the Repository
```bash
cd ~/Interactive-Lab-Hub
cd "Final Project"
```

### 2. Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Create a Python virtual environment (`venv`)
- Install all required Python packages from `requirements.txt`
- Install lgpio for Raspberry Pi 5 GPIO support
- Download the Vosk speech recognition model (~50MB)
- Create `tracks/` and `effects/` directories with README files

### 3. Add Music Files

Place your MP3 tracks in the `tracks/` directory:
```
tracks/
├── track01.mp3
├── track02.mp3
├── track03.mp3
├── track04.mp3
├── track05.mp3
├── track06.mp3
├── track07.mp3
├── track08.mp3
├── track09.mp3
└── track10.mp3
```

Add sound effects in `effects/` (some are included):
```
effects/
├── beep.mp3       (track change sound)
├── click.mp3      (volume change sound)
├── swoosh.mp3     (theme change sound)
├── scratch1.mp3   (DJ scratch effect)
├── scratch2.mp3   (DJ scratch effect)
├── scratch3.mp3   (DJ scratch effect)
└── scratch4.mp3   (DJ scratch effect)
```

### 4. Enable I2C and SPI
```bash
sudo raspi-config
# Navigate to: Interface Options -> I2C -> Enable
# Navigate to: Interface Options -> SPI -> Enable
```

### 5. Verify Sensors
```bash
sudo i2cdetect -y 1
```
You should see:
- `39` - APDS-9960 gesture sensor
- `5a` - MPR121 touch sensor

## Usage

### Start the Application
```bash
cd ~/Interactive-Lab-Hub/Final\ Project
source venv/bin/activate
python gesture_dj.py
```

### Start with Web Visualization
```bash
python gesture_dj.py --web
```
Then open `http://<raspberry-pi-ip>:5000` in any browser to see the visualizations.

### Start with Web (No Auto-Browser)
```bash
python gesture_dj.py --web --no-browser
```

### Quick Reference

**All controls are detailed in the [Features](#features) section above.** 

Quick summary:
- **APDS Gestures**: Swipe RIGHT/LEFT (tracks), UP/DOWN (volume)
- **MPR121 Touch**: Pads 0-9 (tracks), Pad 10 (play/pause), Pad 11 (stop)
- **Voice**: Say "play" or "pause" (plus alternatives)
- **Hand Gestures**: Palm (light theme), Fist (dark theme), Peace (scratch)
- **Web Interface**: Access at `http://<pi-ip>:5000` for visualizations and remote control

### Stop the Application
Press `Ctrl+C` to exit gracefully.

## File Structure
<details>
<summary>Click to expand file structure</summary>
```
Final Project/
├── gesture_dj.py       # Main application with display and web
├── gesture_dj_core.py  # Core business logic
├── audio_engine.py     # Audio playback and track management
├── apds_gesture.py     # APDS-9960 gesture sensor interface
├── mpr121_touch.py     # MPR121 touch sensor interface
├── voice_control.py    # Vosk-based voice recognition
├── hand_tracker.py     # MediaPipe hand tracking module
├── mood_lighting.py    # Theme/mood management (light/dark)
├── display.py          # PiTFT display interface (retro style)
├── web_server.py       # Flask web server with WebSocket
├── demo.py             # Demo/test script
├── requirements.txt    # Python dependencies
├── setup.sh            # Setup script
├── README.md           # This file
├── tracks/             # MP3 track files
│   └── track01-10.mp3
└── effects/            # Sound effect files
    ├── beep.mp3
    ├── click.mp3
    ├── swoosh.mp3
    ├── scratch1.mp3
    ├── scratch2.mp3
    ├── scratch3.mp3
    └── scratch4.mp3
```
</details>

## System Architecture

![Decision Path Selection Flow-2025-12-15-030217](https://hackmd.io/_uploads/H1MfoeazWx.png)

## Module Descriptions

### `gesture_dj.py`
> **Owner:** Eva Huang (lh764), Zoe Tseng (yzt2), Charlotte Lin (hl2575)

Main entry point that combines all input methods, display, and web interface.
- Initializes hardware display (PiTFT)
- Handles web server startup
- Main event loop polling all sensors

### `gesture_dj_core.py`
> **Owner:** Eva Huang (lh764), Zoe Tseng (yzt2), Charlotte Lin (hl2575)

Core business logic without UI code:
- Handles all gesture/touch/voice events
- Manages mood lighting state
- Coordinates audio engine

### `audio_engine.py`
> **Owner:** Eva Huang (lh764)

Handles audio playback using pygame:
- Track loading and switching (10 tracks)
- Play, pause, stop, resume controls
- Volume control with sound feedback
- DJ scratch effect (overlays random scratch sound on music)
- Theme change swoosh sound effect
- Playback speed adjustment via mixer frequency

### `apds_gesture.py`
> **Owner:** Charlotte Lin (hl2575), Zoe Tseng (yzt2)

Interface for APDS-9960 gesture sensor:
- Swipe detection (up, down, left, right)
- Proximity sensing
- Fallback simulation mode

### `mpr121_touch.py`
> **Owner:** Zoe Tseng (yzt2), Charlotte Lin (hl2575)

Interface for MPR121 capacitive touch sensor:
- 12 touch pads (0-11)
- Rising edge detection for reliable touch input
- Pads 0-9: track selection, Pad 10: play/pause, Pad 11: stop

### `voice_control.py`
> **Owner:** Zoe Tseng (yzt2), Charlotte Lin (hl2575)

Offline speech recognition using Vosk:
- Uses USB microphone input
- Recognizes "play" and "pause" commands
- Runs in background thread
- Alternative words supported

**Command Keywords:**
- **Play triggers**: "play", "start", "go", "resume"
- **Pause triggers**: "pause", "stop", "wait", "hold"

### `hand_tracker.py`
> **Owner:** Eva Huang (lh764)

MediaPipe hand tracking for gesture control:
- Palm detection (5 fingers) → Light theme
- Fist detection (0 fingers) → Dark theme
- Peace sign detection (2 fingers) → DJ scratch
- 2.5 second hold requirement for theme changes
- Headless mode support for web streaming
- Live camera feed with gesture overlays

### `mood_lighting.py`
> **Owner:** Eva Huang (lh764)

Theme/mood management system:
- Light theme: Baby blue gradient, blue primary accent
- Dark theme: Midnight black gradient, neon pink accent
- Gesture-to-mood mapping
- Color configurations for web and display

### `display.py`
> **Owner:** Eva Huang (lh764), Zoe Tseng (yzt2), Charlotte Lin (hl2575)

PiTFT display interface with retro vaporwave aesthetic:
- Shows track number and name
- Displays volume level with bars
- Shows playback status icons (play/pause/stop)
- Progress bar with slider handle
- Retro window frame design
- Framebuffer and SPI display support

### `web_server.py`
> **Owner:** Eva Huang (lh764)

Flask web server with Flask-SocketIO:
- Real-time audio state broadcasting
- Camera MJPEG streaming
- Visualization data generation
- REST API for playback control

## Troubleshooting

### APDS Sensor Not Working
1. Check I2C connection: `sudo i2cdetect -y 1` (should show `39`)
2. Ensure I2C is enabled in raspi-config
3. Check wiring (VCC, GND, SDA, SCL)

### Voice Control Not Working
1. Check microphone is connected: `arecord -l`
2. Test microphone: `arecord -d 3 test.wav && aplay test.wav`
3. Ensure Vosk model is downloaded (check `~/.cache/vosk/`)

### No Audio Output
1. Check speaker/headphone connection
2. Set audio output: `sudo raspi-config` -> System Options -> Audio
3. Test audio: `speaker-test -t wav`

### Display Not Showing
1. Ensure PiTFT is properly connected
2. Check SPI is enabled in raspi-config
3. Verify display driver is loaded
4. Try framebuffer mode: check `/dev/fb1` exists

### MPR121 Not Detected
1. Check I2C connection: `sudo i2cdetect -y 1` (should show `5a`)
2. Check wiring (VCC, GND, SDA, SCL)
3. Ensure I2C is enabled in raspi-config

### Camera/Hand Tracking Not Working
1. Check USB camera is connected: `ls /dev/video*`
2. Test camera: `libcamera-hello` or `ffplay /dev/video0`
3. Ensure good lighting for hand detection
4. Hand tracking requires MediaPipe (included in requirements)

### Web Interface Not Loading
1. Check Flask is installed: `pip show flask`
2. Verify port 5000 is not in use: `sudo lsof -i :5000`
3. Check firewall allows port 5000

## Dependencies

See `requirements.txt` for full list. Key dependencies:
- `pygame` - Audio playback
- `adafruit-circuitpython-apds9960` - APDS gesture sensor
- `adafruit-circuitpython-mpr121` - MPR121 touch sensor
- `adafruit-circuitpython-rgb-display` - PiTFT display
- `vosk` - Offline speech recognition
- `sounddevice` - Microphone input
- `mediapipe` - Hand tracking
- `opencv-python` - Camera capture
- `pillow` - Image processing for display
- `flask` - Web server
- `flask-socketio` - WebSocket support
- `lgpio` - GPIO for Raspberry Pi 5

## Design Documentation

### Design Process

<details>
<summary>Click to expand Initial idea </summary>
<img src="https://hackmd.io/_uploads/SkhPiR6Mbe.jpg" alt="Gesture DJ Device" width="300">
    
Early concept for the Gesture DJ
    
</details>

#### Prototype Iterations

| Version | Changes Made |
|---------|--------------|
| **v1** | MediaPipe hand tracking for play/pause control + APDS gesture sensor + USB camera |
| **v2** | Removed MediaPipe (conflicted with APDS) + Added voice control for play/pause + APDS + Removed camera + Added web interface |
| **v3 (Current)** | Re-added MediaPipe for UI theme switching & scratch effects + Voice control + APDS + MPR121 touch pads + Web interface + PiTFT display + Camera (for hand tracking) |

#### Physical Device Enclosure Design
| Stage | Photo |
|-------|-------|
| Design sketch | <img src="https://hackmd.io/_uploads/HktUWkCfbl.png" width="600"> |
| CAD/Design | <img src="https://hackmd.io/_uploads/rJglpA6fWl.png" width="600"> |
| Laser Cutting | <img src="https://hackmd.io/_uploads/BkuyXkRfZg.png" width="600"> |
| Finished |  <img src="https://hackmd.io/_uploads/B1o4Vy0z-l.png" width="600"> |

## Reflection
- **user voice input** : We didn't originally plan to include voice input in our device. During the functional check, Professor Ju suggested adding voice control for music playback, such as play and pause commands. We ran some trials with voice input and speech recognition, and initially it seemed to work pretty well. However, we hadn't really thought about background noise and other people talking nearby. As a result, at the final presentation, sometimes the microphone struggled to pick up voice commands accurately and respond quickly because of all the ambient sound in the room.

- **user gesture controls (adps)**: We used the APDS gesture sensor for two functions: switching tracks (next or previous) and volume control. The track switching worked well because it's a simple and discrete action as one swipe clearly moves to the next song. Volume control, however, was less successful. Each upward swipe increased the volume by 10%, but the change wasn't always noticeable to the user. Additionally, if someone wanted to raise the volume by 30%, they'd have to swipe up three separate times, which felt cumbersome. Looking back, a volume dial might have been a better choice for volume control since it would allow for smoother, more continuous adjustments.

- **user gesture recognition (media pipe)** : MediaPipe hand tracking was one of the most challenging parts of our project. Initially, we tried to use it for play/pause control, but it conflicted with the APDS gesture sensor. We ended up removing MediaPipe entirely to simplify the system. But later, we added it back but with a completely different purpose: UI theme switching (palm/fist gestures) and DJ scratch sound effects (peace sign). The most difficult technical challenge was making MediaPipe work simultaneously with all the other sensors (APDS, MPR121, voice) without conflicts. We had to carefully design the event handling system so that each input method had distinct responsibilities and wouldn't interfere with each other, which took us a lot of time working on multiple iterations of testing and debugging to ensure smooth multi-modal interaction.

- **web interface** : Initially, the web interface was just a backup plan. We designed it only as a visualization tool to give users clearer visual feedback. However, when testing with the PiTFT display, we realized it alone wasn't enough for users to easily see what was happening or interact with the device effectively. After a few design iterations, we settled on a neon theme for the interface to align with the DJ aesthetic of our project. We also added gesture control to let users switch between light and dark themes, giving them the flexibility to adjust the display based on their environment and personal preference without needing to navigate through menus.

- **physical device design** : For the physical design, our vision was to create a DJ board aesthetic using laser-cut wooden panels assembled into a box-like structure. We wanted the device to feel like an actual DJ controller, which would make the interaction more intuitive and engaging. The main challenge we faced was making it immediately clear to users where and how to interact with the device. Since gesture sensors and other components aren't as visually obvious as physical buttons or knobs, we had to carefully consider the placement of components and add visual cues like labels, icons, or designated interaction zones to guide users toward the right areas and help them understand which gestures to use. Looking ahead, there are many things we'd like to improve. For instance, the decorative elements on the DJ panel could actually be functional instead of just decorations, they could serve as interactive controls.