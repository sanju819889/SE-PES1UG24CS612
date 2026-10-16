# Lab 4 – Vibe Coding: Coin Collector

## Student Details

- **Name:** SANJEEV MURTHY
- **SRN:** PES1UG24CS612
- **Lab:** Software Engineering Lab 4 – Vibe Coding

## Project

**Coin Collector Game**

This project uses Python and Pygame. The objective of the lab is to use Vibe Coding/AI assistance to identify and fix existing problems and add new features to the game.

## Tasks Implemented

### Task 1 – Fix Repeated Coin Collection

Fixed the original issue where a coin could be collected repeatedly while the player remained on top of it.

- Each coin is collected only once.
- The collected coin is removed from the active coin list.
- The score is increased only once for that coin.

### Task 2 – Multiple Coin Types

Added three different types of coins:

| Coin Type | Score |
|-----------|-------|
| Bronze | 1 |
| Silver | 3 |
| Gold | 5 |

Each coin type has a different color and contributes its corresponding score when collected.

### Task 3 – Obstacles and Lives

Added obstacles to the game.

- Obstacles are displayed separately from coins.
- Collision between the player and an obstacle is detected.
- The player loses one life after a collision.
- A single collision does not continuously reduce lives every frame.
- Remaining lives are displayed during gameplay.

### Task 4 – Timed Round and Restart

Added a 30-second game round.

- The remaining time is displayed.
- The game ends when the timer reaches 0.
- The game also ends when the player loses all lives.
- The final score is displayed after the round ends.
- Pressing **R** restarts the game.
- Restart resets the score, lives, timer, coins, player position, and game state.

## Technologies Used

- Python
- Pygame
- Git
- GitHub
- VS Code
- AI/Vibe Coding assistance

## Project Structure

```text
06_coin_collector_/
├── main.py
├── requirements.txt
└── game/
    ├── __init__.py
    ├── coin.py
    ├── collection.py
    ├── game_engine.py
    ├── player.py
    └── renderer.py
