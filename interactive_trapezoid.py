import pygame
from const import *


class InteractiveTrapezoid():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.points = [(x, y)]
        self.gap = height / 4
        self.points.append((x, y + height))
        self.points.append((x + width, y + height - self.gap))
        self.points.append((x + width, y + self.gap))
    
    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.polygon(screen, color, self.points)

    def mouse_on(self, x, y):
        center_rect = (self.x <= x <= self.x + self.width and self.y + self.gap <= y <= self.y + self.height - self.gap)
        upper_triangle = self.inside_triangle((x, y), self.points[0], (self.x, self.y + self.gap), self.points[3])
        lower_triangle = self.inside_triangle((x, y), (self.x, self.y + self.height - self.gap), self.points[1], (self.x + self.width, self.y + self.height - self.gap))
        return center_rect or upper_triangle or lower_triangle
    
    def sign(self, p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    def inside_triangle(self, p, p1, p2, p3):
        d1 = self.sign(p, p1, p2)
        d2 = self.sign(p, p2, p3)
        d3 = self.sign(p, p3, p1)
        neg = d1 < 0 or d2 < 0 or d3 < 0
        pos = d1 > 0 or d2 > 0 or d3 > 0
        return not (neg and pos)
