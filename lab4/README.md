# Coin Collector Lab

This project is a single-topic top-down Coin Collector game using
**Pygame**. It introduces students to per-frame collision bookkeeping,
entity variety, an obstacle/lives system, and round timing, using a
small, readable object-oriented codebase.

---

## What's Provided

A working Coin Collector game with:

- A player that moves around a play area with the arrow keys
- Coins scattered around the play area that award points on contact
- A running score display

It has **one deliberate bug** and **three features** left for you to
build. You are expected to **analyze**, **interact with an AI
assistant**, and **complete/fix** the game to make it fully functional
and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Arrow keys to move.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix the coin-collection bug

> A coin is supposed to be collected exactly once, the moment the
> player touches it. In the current build, `update()` (in
> `game/game_engine.py`) calls `check_collection` every frame and adds
> a coin's value to the score for as long as the player's rectangle
> keeps overlapping it - but the coin is never actually removed after
> being collected. Just walking through a single coin at normal speed
> (without stopping) scores it more than a dozen times in one pass.
> Fix it so each coin is collected exactly once, no matter how long
> the player stands on or walks through it.

### Task 2: Implement multiple coin types

> Introduce at least three coin types with different values - for
> example bronze (1 point), silver (3 points), and gold (5 points).
> Give each type its own color so they're visually distinguishable,
> and make sure the correct value is awarded when each type is
> collected.

### Task 3: Implement obstacles

> Add obstacles to the play area that the player must avoid while
> collecting coins. Colliding with an obstacle should have a clearly
> defined consequence (for example, losing a life). Obstacles should
> stay within the play area and interact correctly with the player.

### Task 4: Implement a timed round

> Add a 30-second countdown for the round. Display the remaining time
> on screen. Once it reaches zero (or lives run out, once Task 3 is
> done), stop the round, show the final score clearly, and provide a
> way to start a new round with the score, lives, and timer all reset.

---

## Expected Behavior

- Walking through or standing on a coin should collect it exactly
  once - the score should not keep climbing the whole time the player
  happens to be touching it.
- Coin types are visually distinguishable and award the correct value.
- Touching an obstacle has a real, clearly defined consequence, but a
  single touch shouldn't repeatedly punish the player every frame
  they're still overlapping it.
- The round ends when time runs out or lives reach zero, whichever
  comes first, with the final score shown clearly and a way to start
  again.

---

## Folder Structure

```
coin-collector/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── player.py
│   ├── coin.py
│   ├── collection.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
