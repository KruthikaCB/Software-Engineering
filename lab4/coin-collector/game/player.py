"""
Player: a simple square the player moves around with the arrow keys.
"""

import pygame


class Player:
    def __init__(self, x, y, size=28, speed=4):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed

    def move(self, dx, dy, bounds_width, bounds_height):
        self.x = max(self.size / 2, min(bounds_width - self.size / 2, self.x + dx))
        self.y = max(self.size / 2, min(bounds_height - self.size / 2, self.y + dy))

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.size / 2), int(self.y - self.size / 2),
            self.size, self.size,
        )
