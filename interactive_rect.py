import pygame
from const import *


class InteractiveRect():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.height])

    def mouse_on(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
