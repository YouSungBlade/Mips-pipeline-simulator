import pygame
from interactive_rect import InteractiveRect
from const import *


class PipelineRegister():
    def __init__(self, x, y, width, height, name):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.left_rect = InteractiveRect(x, y, width / 2, height)
        self.right_rect = InteractiveRect(x + width / 2, y, width / 2, height)
        self.inputs = {}
        self.outputs = {}
    
    def set_inputs(self, inputs):
        total = sum(label[1] for label in inputs)
        unit = self.height / total
        count_unit = 0
        for name, portion, notation, length in inputs:
            self.inputs[name] = {
                'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
                'pos': (self.x, (count_unit + portion / 2) * unit + self.y),
                'value': 0
            }
            self.outputs[name] = {
                'form': self.inputs[name]['form'],
                'pos': (self.x + self.width, self.inputs[name]['pos'][1]),
                'value': 0
            }
            count_unit += portion
    
    def get_value(self, name):
        return self.outputs[name]['value']
    
    def set_value(self, name, value):
        self.inputs[name]['value'] = value

    def get_input_pos(self, name):
        return self.inputs[name]['pos']

    def get_output_pos(self, name):
        return self.outputs[name]['pos']
    
    def calculate(self):
        for name in self.inputs.keys():
            self.outputs[name]['value'] = self.inputs[name]['value']
        
    def draw(self, screen, mouse):
        self.left_rect.draw(screen, mouse)
        self.right_rect.draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render(self.name, True, COLOR_BLACK)
        title_rect = title.get_rect(midbottom=(self.x + self.width / 2, self.y))
        screen.blit(title, title_rect)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        for name, label in self.inputs.items():
            label_name = font.render(name, True, COLOR_BLUE)
            label_name_rect = label_name.get_rect(center=(self.x + self.width / 2, label['pos'][1]))
            screen.blit(label_name, label_name_rect)
        
        if self.left_rect.mouse_on(*mouse):
            for label in self.inputs.values():
                value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
                value = pygame.transform.rotate(value, 90)
                value_rect = value.get_rect(midright=(self.x - 2, label['pos'][1]))
                screen.blit(value, value_rect)
        
        if self.right_rect.mouse_on(*mouse):
            for label in self.outputs.values():
                value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
                value = pygame.transform.rotate(value, 270)
                value_rect = value.get_rect(midleft=(self.x + self.width + 2, label['pos'][1]))
                screen.blit(value, value_rect)
        
    def mouse_on(self, x, y):
        return self.left_rect.mouse_on(x, y) or self.right_rect.mouse_on(x, y)
    