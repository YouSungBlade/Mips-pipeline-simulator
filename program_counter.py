from interactive_rect import InteractiveRect
import pygame
from const import *


class ProgramCounter(InteractiveRect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.input = {'pos': (self.x, self.y + self.height / 2), 'value': 0}
        self.output = {'pos': (self.x + self.width, self.y + self.height / 2), 'value': 0}
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
        self.output['value'] = self.input['value']
    
    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render('PC', True, COLOR_BLACK)
        title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        if self.mouse_on(*mouse):
            font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
            value = font.render(format(self.input['value'], self.form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midright=(self.input['pos'][0] - 2, self.input['pos'][1]))
            screen.blit(value, value_rect)

            value = font.render(format(self.output['value'], self.form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midleft=(self.output['pos'][0] + 2, self.output['pos'][1]))
            screen.blit(value, value_rect)