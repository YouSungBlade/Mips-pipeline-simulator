import pygame
from const import *


class InteractiveEllipse():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.ellipse(screen, color, [self.x, self.y, self.width, self.height])

    def mouse_on(self, x, y):
        a, b = self.width / 2, self.height / 2
        scale_y = a / b
        center_x, center_y = self.x + a, self.y + b
        dx, dy = x - center_x, (y - center_y) * scale_y
        return dx**2 + dy**2 <= a**2