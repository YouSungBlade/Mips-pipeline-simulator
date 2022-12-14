import pygame
from const import *


class InteractiveEllipse():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.ellipse(screen, color, [self.x, self.y, self.width, self.height])

    def mouse_on(self, x, y):
        a, b = self.width / 2, self.height / 2
        scale_y = a / b
        center_x, center_y = self.x + a, self.y + b
        dx, dy = x - center_x, (y - center_y) * scale_y
        return dx**2 + dy**2 <= a**2


class ConcatUnit(InteractiveEllipse):
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


class EqualUnit(InteractiveEllipse):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.inputs = [
            {'pos': (self.x + self.width / 2, self.y), 'value': 0},
            {'pos': (self.x + self.width / 2, self.y + self.height), 'value': 0}
        ]
        self.output = {'pos': (self.x + self.width, self.y + self.height / 2), 'value': 0}
        self.input_form = '#010x'
        self.output_form = '#03b'
    
    def get_value(self):
        return self.output['value']
    
    def set_value(self, index, value):
        self.inputs[index]['value'] = value
    
    def get_input_pos(self, index):
        return self.inputs[index]['pos']
    
    def get_output_pos(self):
        return self.output['pos']
    
    def calculate(self):
        self.output['value'] = self.inputs[0]['value'] == self.inputs[1]['value']
    
    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render('=', True, COLOR_BLACK)
        title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        if self.mouse_on(*mouse):
            font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
            value = font.render(format(self.inputs[0]['value'], self.input_form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midbottom=(self.inputs[0]['pos'][0], self.inputs[0]['pos'][1] - 2))
            screen.blit(value, value_rect)

            value = font.render(format(self.inputs[1]['value'], self.input_form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midtop=(self.inputs[1]['pos'][0], self.inputs[1]['pos'][1] + 2))
            screen.blit(value, value_rect)

            value = font.render(format(self.output['value'], self.output_form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midleft=(self.output['pos'][0] + 2, self.output['pos'][1]))
            screen.blit(value, value_rect)


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
        self.output['value'] = self.input['value'] << 2 & 0xFFFFFFFF
    
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


class SignExtension(InteractiveEllipse):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.input = {'pos': (self.x, self.y + self.height / 2), 'value': 0}
        self.output = {'pos': (self.x + self.width, self.y + self.height / 2), 'value': 0}
        self.input_form = '#06x'
        self.output_form = '#010x'
    
    def get_value(self):
        return self.output['value']
    
    def set_value(self, value):
        self.input['value'] = value
    
    def get_input_pos(self):
        return self.input['pos']

    def get_output_pos(self):
        return self.output['pos']
    
    def calculate(self):
        if (self.input['value'] >> 15) & 1:
            self.output['value'] = self.input['value'] + 0xFFFF0000
        else:
            self.output['value'] = self.input['value']

    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render('Sign', True, COLOR_BLACK)
        title_rect = title.get_rect(midbottom=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)
        title = font.render('Extension', True, COLOR_BLACK)
        title_rect = title.get_rect(midtop=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        if self.mouse_on(*mouse):
            font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
            value = font.render(format(self.input['value'], self.input_form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midright=(self.input['pos'][0] - 2, self.input['pos'][1]))
            screen.blit(value, value_rect)

            value = font.render(format(self.output['value'], self.output_form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midleft=(self.output['pos'][0] + 2, self.output['pos'][1]))
            screen.blit(value, value_rect)