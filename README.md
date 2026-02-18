# In-Between Card Game Simulator 🃏

A Python simulation of **In-Between**, a card game where players bet on whether a third card's value will fall between two drawn cards. Includes both an interactive player mode and an automated computer bot.

---

## How the Game Works

Each round, two cards are drawn and revealed. The player then bets on the outcome of a third card:

- **If the two cards have different values** — the player bets on whether the third card lands *in between* them.
- **If the two cards have the same value** — the player chooses whether the third card will be *higher* or *lower*.
- **TIANG** — if the third card matches either of the first two, the player loses **double** their bet.

The game ends when the player runs out of money or all cards have been played.

---

## Features

- 🎮 **Player Mode** — interactive CLI gameplay with manual betting
- 🤖 **Computer Mode** — automated bot that makes decisions based on calculated odds
- 📊 **Odds Calculator** — computes win probability from the remaining deck in real time
- 🃏 **No duplicate cards** — cards are tracked per suit to prevent repeats
- 📈 **Stats tracking** — wins, losses, passes, and net value gained/lost

---

## Project Structure

```
.
├── main.ipynb        # Jupyter notebook for running simulations and experiments
├── Simulation.py     # Core game logic, betting engine, and computer/player modes
├── Card.py           # Card class with random card generation
└── config.py         # Game constants (suits, card value range)
```

---

## Getting Started

### Prerequisites

- Python 3.x
- Jupyter Notebook (optional, for `main.ipynb`)

### Running the Game

**Player mode (interactive CLI):**
```python
from Simulation import Simulation

s = Simulation(base=100, pot=100)
s.startPlayer()
```

**Computer/bot mode:**
```python
from Simulation import Simulation

s = Simulation(base=100, pot=100)
s.startComputer(skip_threshold=0.4)
```

**Running multiple simulations:**

Open `main.ipynb` in Jupyter and run the cells to batch-simulate games and review aggregate stats.

---

## Configuration

Edit `config.py` to adjust the deck parameters:

```python
VAL_START = 1   # Lowest card value (Ace)
VAL_END = 13    # Highest card value (King)
SUITS = ["HEARTS", "SPADES", "CLUBS", "DIAMONDS"]
```

---

## Computer Bot Logic

The bot uses real-time probability calculations to make decisions:

- **Skips** rounds where the win probability is below `skip_threshold` (default: 40%)
- **Scales bet size** proportionally to the calculated win probability
- **Automatically chooses** Higher/Lower when the two cards match, based on which outcome has better odds

---

## Game Parameters

| Parameter | Description | Default |
|---|---|---|
| `base` | Starting balance | `10` |
| `pot` | Maximum pot size (caps bets) | `100` |
| `skip_threshold` | Minimum probability for the bot to place a bet | `0.4` |

Bets are capped at the lower of `base // 2` or `pot`.
