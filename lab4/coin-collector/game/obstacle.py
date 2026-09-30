"""
Moving obstacle that bounces inside the play area.
"""

import pygame


class Obstacle:
    def __init__(
        self,
        x,
        y,
        radius=16,
        dx=3,
        dy=2,
        color=(220, 60, 60),
    ):
        self.x = x
        self.y = y
        self.radius = radius
        self.dx = dx
        self.dy = dy
        self.color = color

    def update(self, width, height):
        self.x += self.dx
        self.y += self.dy

        # Bounce off the left and right edges.
        if self.x - self.radius <= 0:
            self.x = self.radius
            self.dx = abs(self.dx)

        elif self.x + self.radius >= width:
            self.x = width - self.radius
            self.dx = -abs(self.dx)

        # Bounce off the top and bottom edges.
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.dy = abs(self.dy)

        elif self.y + self.radius >= height:
            self.y = height - self.radius
            self.dy = -abs(self.dy)

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.radius),
            int(self.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )