import pygame
from const import *


class OrGate:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.form = '#03b'
        self.inputs = self.inputs = [
            {'pos': (self.x + self.width * 0.1, self.y + self.height), 'value': 0},
            {'pos': (self.x + self.width * 0.9, self.y + self.height), 'value': 0}
        ]
        self.output = {
            'pos': (self.x + self.width / 2, self.y),
            'value': 0
        }
    
    def get_value(self):
        return self.output['value']
    
    def set_value(self, index, value):
        self.inputs[index]['value'] = value
    
    def get_output_pos(self):
        return self.output['pos']
    
    def get_input_pos(self, index):
        return self.inputs[index]['pos']
    
    def calculate(self):
        self.output['value'] = self.inputs[0]['value'] or self.inputs[1]['value']
    
    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.ellipse(screen, color, [self.x, self.y, self.width, self.height * 2])
        pygame.draw.rect(screen, COLOR_BACK, [self.x, self.y + self.height, self.width, self.height])
        pygame.draw.ellipse(screen, COLOR_BACK, [self.x, self.y + self.height * 0.9, self.width, self.height * 0.2])

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        if self.mouse_on(*mouse):
            for label in self.inputs:
                value = font.render(format(label['value'], self.form), True, COLOR_RED, COLOR_WHITE)
                value_rect = value.get_rect(midtop=(label['pos'][0], label['pos'][1] + 2))
                screen.blit(value, value_rect)
            
            value = font.render(format(self.output['value'], self.form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midbottom=(self.output['pos'][0], self.output['pos'][1] - 2))
            screen.blit(value, value_rect)

    def mouse_on(self, x, y):
        a, b = self.width / 2, self.height
        scale_y = a / b
        center_x, center_y = self.x + a, self.y + b
        dx, dy = x - center_x, (y - center_y) * scale_y
        bigger_ellipse = dx**2 + dy**2 <= a**2

        a, b = self.width / 2, self.height * 0.1
        scale_y = a / b
        center_x, center_y = self.x + a, self.y + self.height * 0.9 + b
        dx, dy = x - center_x, (y - center_y) * scale_y
        smaller_ellipse = dx**2 + dy**2 <= a**2
        return bigger_ellipse and not smaller_ellipse and y <= self.y + self.height