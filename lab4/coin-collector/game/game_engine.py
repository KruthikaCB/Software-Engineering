"""
GameEngine: owns the player, coins, and moving obstacles.

Coin types:
- Bronze: 1 point
- Silver: 3 points
- Gold: 5 points

There are always 6 coins on screen.
When a coin is collected, a new random coin is spawned
at a position that does not overlap an obstacle.

Each coin is scored exactly once.

The player starts with 3 lives and has 30 seconds per round.
The round ends when the timer reaches zero or lives reach zero.
Press R to restart the round.

During the invulnerability period after being hit,
the player blinks to indicate temporary immunity.
"""

import random
import time
import pygame

from game.player import Player
from game.coin import Coin
from game.obstacle import Obstacle
from game.collection import check_collection
from game.renderer import WIDTH, HEIGHT


NUM_COINS = 6
NUM_OBSTACLES = 3

STARTING_LIVES = 3
ROUND_TIME = 30.0
INVULNERABILITY_TIME = 1.0

COIN_RADIUS = 12

COIN_TYPES = [
    (1, (205, 127, 50)),    # Bronze
    (3, (192, 192, 192)),   # Silver
    (5, (255, 215, 0)),     # Gold
]


class GameEngine:
    def __init__(self):
        self.reset()

    def reset(self):
        """Reset the entire round."""

        self.player = Player(
            x=WIDTH / 2,
            y=HEIGHT / 2
        )

        self.score = 0
        self.lives = STARTING_LIVES

        self.invulnerable_until = 0.0

        self.start_time = time.monotonic()
        self.remaining_time = ROUND_TIME

        self.game_over = False
        self.game_over_reason = ""

        # Create obstacles first so that coins
        # can avoid them when spawning.
        self.obstacles = [
            self._random_obstacle()
            for _ in range(NUM_OBSTACLES)
        ]

        # Always start with exactly 6 coins.
        self.coins = [
            self._random_coin()
            for _ in range(NUM_COINS)
        ]

    def _random_coin(self):
        """
        Create a random coin that does not overlap
        any obstacle.
        """

        for _ in range(100):
            x = random.randint(
                COIN_RADIUS,
                WIDTH - COIN_RADIUS
            )

            y = random.randint(
                70 + COIN_RADIUS,
                HEIGHT - COIN_RADIUS
            )

            value, color = random.choice(
                COIN_TYPES
            )

            candidate = Coin(
                x=x,
                y=y,
                radius=COIN_RADIUS,
                value=value,
                color=color
            )

            if not self._coin_overlaps_obstacle(
                candidate
            ):
                return candidate

        # Fallback position.
        value, color = random.choice(
            COIN_TYPES
        )

        return Coin(
            x=COIN_RADIUS + 5,
            y=75,
            radius=COIN_RADIUS,
            value=value,
            color=color
        )

    def _coin_overlaps_obstacle(self, coin):
        """Check whether a coin overlaps any obstacle."""

        for obstacle in self.obstacles:
            dx = coin.x - obstacle.x
            dy = coin.y - obstacle.y

            distance_squared = (
                dx * dx +
                dy * dy
            )

            minimum_distance = (
                coin.radius +
                obstacle.radius
            )

            if distance_squared < (
                minimum_distance ** 2
            ):
                return True

        return False

    def _random_obstacle(self):
        """
        Create an obstacle at least 120 pixels away
        from the player's starting position.
        """

        player_x = self.player.x
        player_y = self.player.y

        minimum_distance = 120

        for _ in range(100):
            x = random.randint(
                30,
                WIDTH - 30
            )

            y = random.randint(
                70,
                HEIGHT - 30
            )

            dx = x - player_x
            dy = y - player_y

            distance = (
                dx * dx +
                dy * dy
            ) ** 0.5

            if distance >= minimum_distance:
                return Obstacle(
                    x=x,
                    y=y,
                    radius=16,
                    dx=random.choice(
                        [-3, -2, 2, 3]
                    ),
                    dy=random.choice(
                        [-3, -2, 2, 3]
                    ),
                    color=(220, 60, 60)
                )

        # Fallback position.
        return Obstacle(
            x=30,
            y=70,
            radius=16,
            dx=random.choice(
                [-3, -2, 2, 3]
            ),
            dy=random.choice(
                [-3, -2, 2, 3]
            ),
            color=(220, 60, 60)
        )

    def handle_input(self, keys_pressed):
        """Handle player movement using arrow keys."""

        if self.game_over:
            return

        dx = 0
        dy = 0

        if keys_pressed[pygame.K_UP]:
            dy -= self.player.speed

        if keys_pressed[pygame.K_DOWN]:
            dy += self.player.speed

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.player.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.player.speed

        self.player.move(
            dx,
            dy,
            WIDTH,
            HEIGHT
        )

    def update(self):
        """Update the game state."""

        if self.game_over:
            return

        current_time = time.monotonic()

        # -------------------------
        # Countdown timer
        # -------------------------

        elapsed_time = (
            current_time -
            self.start_time
        )

        self.remaining_time = max(
            0.0,
            ROUND_TIME - elapsed_time
        )

        if self.remaining_time <= 0:
            self.remaining_time = 0.0
            self.game_over = True
            self.game_over_reason = "Time's up!"
            return

        # -------------------------
        # Update obstacles
        # -------------------------

        for obstacle in self.obstacles:
            obstacle.update(
                WIDTH,
                HEIGHT
            )

        # -------------------------
        # Collect coins
        # -------------------------

        collected = check_collection(
            self.player,
            self.coins
        )

        for coin in collected:
            self.score += coin.value

        if collected:
            # Remove collected coins.
            self.coins = [
                coin
                for coin in self.coins
                if coin not in collected
            ]

            # Spawn one replacement for every
            # coin collected.
            for _ in collected:
                self.coins.append(
                    self._random_coin()
                )

        # -------------------------
        # Obstacle collision
        # -------------------------

        if current_time >= self.invulnerable_until:

            # The player is drawn as a rectangle.
            # Use the rectangle's center and derive
            # a collision radius from its size.
            player_rect = self.player.get_rect()

            player_x = player_rect.centerx
            player_y = player_rect.centery

            player_radius = min(
                player_rect.width,
                player_rect.height
            ) / 2

            for obstacle in self.obstacles:

                dx = (
                    player_x -
                    obstacle.x
                )

                dy = (
                    player_y -
                    obstacle.y
                )

                distance_squared = (
                    dx * dx +
                    dy * dy
                )

                collision_distance = (
                    player_radius +
                    obstacle.radius
                )

                # Circle-to-circle collision.
                if distance_squared <= (
                    collision_distance ** 2
                ):
                    self.lives -= 1

                    # Start the invulnerability period.
                    self.invulnerable_until = (
                        current_time +
                        INVULNERABILITY_TIME
                    )

                    break

        # -------------------------
        # Lives game over
        # -------------------------

        if self.lives <= 0:
            self.lives = 0

            # Freeze the timer at the moment
            # the final life is lost.
            self.remaining_time = max(
                0.0,
                ROUND_TIME - (
                    current_time -
                    self.start_time
                )
            )

            self.game_over = True
            self.game_over_reason = "Out of lives!"

    def get_remaining_time(self):
        """
        Return remaining time.

        Once the round ends, return the stored value
        so the timer stays frozen.
        """

        if self.game_over:
            return self.remaining_time

        current_time = time.monotonic()

        elapsed_time = (
            current_time -
            self.start_time
        )

        self.remaining_time = max(
            0.0,
            ROUND_TIME - elapsed_time
        )

        return self.remaining_time

    def _is_player_invulnerable(self):
        """Return True while the player is invulnerable."""

        if self.game_over:
            return False

        return (
            time.monotonic() <
            self.invulnerable_until
        )

    def draw(self, surface, font):
        """Draw the complete game scene."""

        from game import renderer

        # Blink the player during invulnerability.
        player_visible = True

        if self._is_player_invulnerable():
            blink_phase = int(
                time.monotonic() * 10
            )

            player_visible = (
                blink_phase % 2 == 0
            )

        renderer.draw_scene(
            surface,
            self.player,
            self.coins,
            self.obstacles,
            player_visible=player_visible
        )

        remaining_time = (
            self.get_remaining_time()
        )

        # -------------------------
        # Score
        # -------------------------

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 10)
        )

        # -------------------------
        # Lives
        # -------------------------

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 40)
        )

        # -------------------------
        # Timer
        # -------------------------

        renderer.draw_text(
            surface,
            font,
            f"Time: {int(remaining_time + 0.999)}",
            (10, 70)
        )

        # -------------------------
        # Game-over screen
        # -------------------------

        if self.game_over:
            renderer.draw_game_over(
                surface,
                font,
                self.score,
                self.game_over_reason
            )