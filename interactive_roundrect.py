import pygame
from const import *


class InteractiveRoundrect():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = int(0.05 * (width + height))
    
    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.height], 0, self.radius)

    def mouse_on(self, x, y):
        hor_rect = (self.x <= x <= self.x + self.width and self.y + self.radius <= y <= self.y + self.height - self.radius)
        ver_rect = (self.x + self.radius <= x <= self.x + self.width - self.radius and self.y <= y <= self.y + self.height)
        if hor_rect or ver_rect:
            return True

        x_poses = (self.x + self.radius, self.x + self.width - self.radius)
        y_poses = (self.y + self.radius, self.y + self.height - self.radius)
        for center_x, center_y in [(cx, cy) for cx in x_poses for cy in y_poses]:
            if (x - center_x)**2 + (y - center_y)**2 <= self.radius**2:
                return True
        return False
