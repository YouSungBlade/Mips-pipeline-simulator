import pygame
from interactive_trapezoid import InteractiveTrapezoid
from const import *


class SimpleAdder(InteractiveTrapezoid):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.name = '+'
        self.inputs = []
        self.output = {
            'pos': (self.x + self.width, self.y + self.height / 2),
            'value': 0
        }
    
    def set_inputs(self, inputs):
        block = self.height / len(inputs)
        for i, (notation, length) in enumerate(inputs):
            self.inputs.append({
                'form' : '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
                'pos' : (self.x, self.y + block * (i + 0.5)),
                'value' : 0
            })
    
    def get_value(self):
        return self.output['value']
    
    def set_value(self, index, value):
        self.inputs[index]['value'] = value
    
    def get_input_pos(self, index):
        return self.inputs[index]['pos']
    
    def get_output_pos(self):
        return self.output['pos']
    
    def calculate(self):
        self.output['value'] = sum(label['value'] for label in self.inputs)
    
    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render(self.name, True, COLOR_BLACK)
        title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        if self.mouse_on(*mouse):
            for label in self.inputs:
                value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
                value_rect = value.get_rect(midright=(self.x - 2, label['pos'][1]))
                screen.blit(value, value_rect)
            
            value = font.render(format(self.output['value'], '#010x'), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midleft=(self.x + self.width + 2, self.output['pos'][1]))
            screen.blit(value, value_rect)