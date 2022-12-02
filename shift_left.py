import pygame
from interactive_ellipse import InteractiveEllipse
from const import *


class ShiftLeft(InteractiveEllipse):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.input = {'pos': (self.x + self.width / 2, self.y + self.height), 'value': 0}
        self.output = {'pos': (self.x + self.width / 2, self.y), 'value': 0}
        self.form = '#010x'
    
    def get_value(self):
        return self.output['value']
    
    def set_value(self, value):
        self.input['value'] = value
    
    def get_input_pos(self):
        return self.input['pos']
    
    def get_output_pos(self):
        return self.output['pos']
    
    def calculate(self):
        self.output['value'] = self.input['value'] * 4
    
    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render('Shift', True, COLOR_BLACK)
        title_rect = title.get_rect(midbottom=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)
        title = font.render('Left', True, COLOR_BLACK)
        title_rect = title.get_rect(midtop=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        if self.mouse_on(*mouse):
            font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
            value = font.render(format(self.input['value'], self.form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midtop=(self.input['pos'][0], self.input['pos'][1] + 2))
            screen.blit(value, value_rect)

            value = font.render(format(self.output['value'], self.form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midbottom=(self.output['pos'][0], self.output['pos'][1] - 2))
            screen.blit(value, value_rect)