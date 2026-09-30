"""
Coin Collector

Controls:
    Arrow keys - Move
    R          - Restart after game over
"""

import pygame

from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE


def main():
    pygame.init()

    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption(
        "Coin Collector"
    )

    clock = pygame.time.Clock()

    font = pygame.font.SysFont(
        "consolas",
        22
    )

    engine = GameEngine()

    running = True

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Restart only when the round has ended.
            elif (
                event.type == pygame.KEYDOWN
                and event.key == pygame.K_r
                and engine.game_over
            ):
                engine.reset()

        keys = pygame.key.get_pressed()

        engine.handle_input(keys)
        engine.update()
        engine.draw(screen, font)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()