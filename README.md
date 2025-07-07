# Garronch

Garronch is an innovative 2D platformer game built with Python and Pygame, featuring vision-based gesture controls using OpenCV and MediaPipe. Play using traditional keyboard controls or leverage your webcam for hands-free gameplay powered by real-time facial movement and gesture recognition.

## Features

- **Vision-Based Gesture Controls:** Play using head movements detected via webcam, enabled by OpenCV and MediaPipe.
- **Traditional Controls:** Full keyboard support for classic platformer gameplay.
- **Custom Level Editor:** Design and build your own levels for endless replayability.
- **Dynamic Gameplay:** Includes enemy AI, projectile physics, dashing, jumping, and custom particle effects.
- **Smooth Performance:** Optimized for 60+ FPS, low input latency, and efficient memory usage.
- **Polished Experience:** Animated backgrounds, sound effects, and visual feedback for immersive play.

## How It Works

- **Gesture Input:** Uses your webcam to detect head movements and facial gestures, translating them into in-game actions like jumping or dashing.
- **Game Engine:** Built on Pygame for rendering, events, and audio. Multiprocessing ensures real-time gesture recognition without impacting gameplay performance.
- **Level Editor:** Create, save, and load custom levels in JSON format for easy expansion and sharing.

## Getting Started

### Prerequisites

- Python 3.8+
- [Pygame](https://www.pygame.org/news)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://google.github.io/mediapipe/)
- [pynput](https://pynput.readthedocs.io/en/latest/) (for keyboard control)
- (Optional) Webcam for gesture-based input

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/utkarshgupta14/Garronch.git
   cd Garronch
   ```

2. **Install dependencies:**

3. **Run the game:**
   ```bash
   python Game.py
   ```

   For the gesture-based demos:
   ```bash
   python scripts/head_movement_demo.py
   python scripts/hand_gesture_demo.py
   ```

### Controls

- **Keyboard:**
  - Left/Right: Move character
  - Up: Jump
  - X: Dash

- **Gesture Controls (with webcam):**
  - Move your head left/right to move
  - Upward head jerk to jump
  - Open right hand (visible palm) for dash

## Project Structure

```
Garronch/
├── Game.py                  # Main game script
├── game_state_1.py          # Game states
├── game_state_2.py
├── scripts/
│   ├── head_movement.py     # references scripts
│   ├── head_movement_demo.py
│   |── spark.py
|   |-- utils.py
|   |-- ........
├── data/
   ├── images/
   ├── maps/
   ├── sfx/
   └── music.wav

```

## Custom Level Editor

Create and edit levels easily using the built-in JSON editor. Levels are stored in `data/maps/`. Refer to the code and sample files for the level structure.

## Acknowledgments

- [Pygame](https://www.pygame.org/)
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://google.github.io/mediapipe/)
- Sound effects and visual assets used under open licenses or created by the author.

**Enjoy playing Garronch — the platformer where you can play with your moves!**
