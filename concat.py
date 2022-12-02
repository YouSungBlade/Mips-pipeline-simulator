import pygame
from interactive_ellipse import InteractiveEllipse
from const import *


class Concat(InteractiveEllipse):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.inputs = [
            {'pos': (self.x, self.y + self.height / 2), 'value': 0, 'form': '#03x'},
            {'pos': (self.x + self.width / 2, self.y + self.height), 'value': 0, 'form': '#010x'}
        ]
        self.output = {'pos': (self.x + self.width / 2, self.y), 'value': 0, 'form': '#010x'}

    def get_value(self):
        return self.output['value']
    
    def set_value(self, index, value):
        self.inputs[index]['value'] = value
    
    def get_input_pos(self, index):
        return self.inputs[index]['pos']
    
    def get_output_pos(self):
        return self.output['pos']
    
    def calculate(self):
        self.output['value'] = self.inputs[0]['value'] << 28 | self.inputs[1]['value']
    
    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render('Concat', True, COLOR_BLACK)
        title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        if self.mouse_on(*mouse):
            font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
            value = font.render(format(self.inputs[0]['value'], self.inputs[0]['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midright=(self.inputs[0]['pos'][0] - 2, self.inputs[0]['pos'][1]))
            screen.blit(value, value_rect)

            font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
            value = font.render(format(self.inputs[1]['value'], self.inputs[1]['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midtop=(self.inputs[1]['pos'][0], self.inputs[1]['pos'][1] + 2))
            screen.blit(value, value_rect)

            value = font.render(format(self.output['value'], self.output['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midbottom=(self.output['pos'][0], self.output['pos'][1] - 2))
            screen.blit(value, value_rect)
    


        