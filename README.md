### README for the Game

# Desert Hero: Quest for the Artifact

**Desert Hero** is a survival adventure game set in the vast, unforgiving Karakum Desert. The player controls a Turkmen warrior, exploring the desert, avoiding scorpions, collecting water jugs to survive, and ultimately searching for the ancient artifact hidden in the sand. Will you survive the desert’s dangers and claim the artifact, or will the scorching sun and dangerous creatures claim you first?

## Features:

- **WASD Movement:** Move your character through the desert using the `WASD` keys.
- **Survival Mechanics:** Keep an eye on your spirit level. It decreases over time due to dehydration, but collecting water jugs will replenish it.
- **Scorpions:** Beware of scorpions! These deadly creatures chase you down, and if they touch you, they reduce your spirit.
- **Artifact:** Once you have collected all the water jugs, the artifact becomes active. Find it and win the game!
- **High Score Tracking:** Your highest score is saved to a file, allowing you to track your best survival efforts.
- **Victory & Game Over Screens:** The game shows a **game over screen** if you run out of spirit and a **victory screen** if you manage to find the artifact.

## Game Controls:

- **W** - Move up
- **A** - Move left
- **S** - Move down
- **D** - Move right
- **ESC** - Exit the game (after losing or winning)

## Requirements:

- Python 3.x
- Pygame library (use `pip install pygame` to install)

## How to Play:

1. **Start the game:** Press any key to begin at the intro screen.
2. **Survive:** Navigate the desert, collect water jugs, and avoid scorpions. Keep an eye on your spirit.
3. **Find the Artifact:** Once you collect all the water jugs, the artifact becomes active. Find it to win the game.
4. **Game Over / Victory:** If your spirit runs out, the game ends with a **game over screen**. If you find the artifact, you win and see a **victory screen**.

## High Score:

- The game keeps track of your highest score (based on the number of jugs collected and how long you survive) in a file called `turkmen_hero_score.txt`.
- The highest score is updated when you achieve a higher score than the current one.

## How to Quit:

- Press `ESC` on the game over or victory screen to exit the game.

---

## Setup and Installation:

1. Ensure that you have **Python 3.x** installed on your system.
2. Install **Pygame** by running:

   ```bash
   pip install pygame
   ```

3. Download or clone this repository to your computer.
4. Run the game using the following command:

   ```bash
   python game.py
   ```

---

## Credits:

- Created by: [basimkaka]
