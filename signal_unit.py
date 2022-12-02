import pygame
from interactive_roundrect import InteractiveRoundrect
from math import sin, cos, pi
from const import *


class SignalUnit(InteractiveRoundrect):
    def __init__(self, x, y, width, height, entries, name):
        super().__init__(x, y, width, height)
        self.entries = entries
        self.name = name
        self.inputs = {}
        self.outputs = {}
        self.scale = height / width
        
    def set_inputs(self, inputs):
        for name, side, index, notation, length in inputs:
            if side == 0:
                x = self.width / (self.entries[side] + 1) * (index + 1) + self.x
                y = self.y
            elif side == 1:
                x = self.x + self.width
                y = self.height / (self.entries[side] + 1) * (index + 1) + self.y
            elif side == 2:
                x = self.width / (self.entries[side] + 1) * (index + 1) + self.x
                y = self.y + self.height
            else:
                x = self.x
                y = self.height / (self.entries[side] + 1) * (index + 1) + self.y

            self.inputs[name] = {
                'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
                'pos': (x, y),
                'value': 0,
                'side': side
            }
    
    def set_outputs(self, outputs):
        for name, side, index, notation, length in outputs:
            if side == 0:
                x = self.width / (self.entries[side] + 1) * (index + 1) + self.x
                y = self.y
            elif side == 1:
                x = self.x + self.width
                y = self.height / (self.entries[side] + 1) * (index + 1) + self.y
            elif side == 2:
                x = self.width / (self.entries[side] + 1) * (index + 1) + self.x
                y = self.y + self.height
            else:
                x = self.x
                y = self.height / (self.entries[side] + 1) * (index + 1) + self.y
            self.outputs[name] = {
                'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
                'pos': (x, y),
                'value': 0,
                'side': side
            }
    
    def get_value(self, name):
        return self.outputs[name]['value']
    
    def set_value(self, name, value):
        self.inputs[name]['value'] = value

    def get_input_pos(self, name):
        return self.inputs[name]['pos']
    
    def get_output_pos(self, name):
        return self.outputs[name]['pos']

    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render(self.name, True, COLOR_BLACK)
        title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        for name, label in {**self.inputs, **self.outputs}.items():
            label_name = font.render(name, True, COLOR_BLUE)
            if label['side'] == 0:
                label_name_rect = label_name.get_rect(midtop=(label['pos'][0], label['pos'][1] + 2))
            elif label['side'] == 1:
                label_name_rect = label_name.get_rect(midright=(label['pos'][0] - 2, label['pos'][1]))
            elif label['side'] == 2:
                label_name_rect = label_name.get_rect(midbottom=(label['pos'][0], label['pos'][1] - 2))
            else:
                label_name_rect = label_name.get_rect(midleft=(label['pos'][0] + 2, label['pos'][1]))
            screen.blit(label_name, label_name_rect)

        if self.mouse_on(*mouse):
            for name, label in {**self.inputs, **self.outputs}.items():
                value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
                if label['side'] == 0:
                    value_rect = value.get_rect(midbottom=(label['pos'][0], label['pos'][1] - 2))
                elif label['side'] == 1:
                    value_rect = value.get_rect(midleft=(label['pos'][0] + 2, label['pos'][1]))
                elif label['side'] == 2:
                    value_rect = value.get_rect(midtop=(label['pos'][0], label['pos'][1] + 2))
                else:
                    value_rect = value.get_rect(midright=(label['pos'][0] - 2, label['pos'][1]))
                screen.blit(value, value_rect)
