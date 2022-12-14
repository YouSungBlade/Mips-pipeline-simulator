import pygame
from const import *


class StraightLine:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.direction = None
    
    def draw(self, screen):
        pygame.draw.lines(screen, COLOR_BLACK, False, [self.p1, self.p2], 2)
        if not self.direction:
            self.set_direction(self.p1, self.p2)
        self.triangle(screen, self.p2)
    
    def set_direction(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 and y1 < y2:
            self.direction = 2
        elif x1 == x2 and y1 > y2:
            self.direction = 0
        elif x1 > x2:
            self.direction = 3
        else:
            self.direction = 1
    
    def triangle(self, screen, p):
        x, y = p
        if self.direction == 0:
            pygame.draw.polygon(screen, COLOR_BLACK, [(x, y), (x + 3, y + 4), (x - 3, y + 4)])
        elif self.direction == 1:
            pygame.draw.polygon(screen, COLOR_BLACK, [(x, y), (x - 4, y + 3), (x - 4, y - 3)])
        elif self.direction == 2:
            pygame.draw.polygon(screen, COLOR_BLACK, [(x, y), (x + 3, y - 4), (x - 3, y - 4)])
        elif self.direction == 3:
            pygame.draw.polygon(screen, COLOR_BLACK, [(x, y), (x + 4, y + 3), (x + 4, y - 3)])
    
class OneCornerLine(StraightLine):
    def __init__(self, p1, p2, x_first=True):
        super().__init__(p1, p2)
        if x_first:
            self.p3 = (self.p2[0], self.p1[1])
        else:
            self.p3 = (self.p1[0], self.p2[1])
    
    def draw(self, screen):
        pygame.draw.lines(screen, COLOR_BLACK, False, [self.p1, self.p3, self.p2], 2)
        if not self.direction:
            self.set_direction(self.p3, self.p2)
        self.triangle(screen, self.p2)

class TwoCornerLine(StraightLine):
    def __init__(self, p1, p2, base, x_first=True):
        super().__init__(p1, p2)
        if x_first:
            self.p3 = (base, self.p1[1])
            self.p4 = (base, self.p2[1])
        else:
            self.p3 = (self.p1[0], base)
            self.p4 = (self.p2[0], base)
    
    def draw(self, screen):
        pygame.draw.lines(screen, COLOR_BLACK, False, [self.p1, self.p3, self.p4, self.p2], 2)
        if not self.direction:
            self.set_direction(self.p4, self.p2)
        self.triangle(screen, self.p2)

class ThreeCornerLine(StraightLine):
    def __init__(self, p1, p2, p3, x_first_1=True, x_first_2=True):
        super().__init__(p1, p2)
        self.p3 = p3
        if x_first_1:
            self.p4 = (p3[0], p1[1])
        else:
            self.p4 = (p1[0], p3[1])
        
        if x_first_2:
            self.p5 = (p2[0], p3[1])
        else:
            self.p5 = (p3[0], p2[1])

    def draw(self, screen):
        pygame.draw.lines(screen, COLOR_BLACK, False, [self.p1, self.p4, self.p3, self.p5, self.p2], 2)
        if not self.direction:
            self.set_direction(self.p5, self.p2)
        self.triangle(screen, self.p2)

class FourCornerLine(StraightLine):
    def __init__(self, p1, p2, p3, base, x_first_1=True, x_first_2=True):
        super().__init__(p1, p2)
        self.p3 = p3
        if x_first_1:
            self.p4 = (base, p1[1])
            self.p5 = (base, p3[1])
        else:
            self.p4 = (p1[0], base)
            self.p5 = (p3[0], base)
        
        if x_first_2:
            self.p6 = (p2[0], p3[1])
        else:
            self.p6 = (p3[0], p2[1])
        
    def draw(self, screen):
        pygame.draw.lines(screen, COLOR_BLACK, False, [self.p1, self.p4, self.p5, self.p3, self.p6, self.p2], 2)
        if not self.direction:
            self.set_direction(self.p6, self.p2)
        self.triangle(screen, self.p2)
