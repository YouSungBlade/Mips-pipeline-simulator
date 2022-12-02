import pygame
from const import *


class Multiplexer():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = width / 2
        self.upper_center = (x + self.radius, y + self.radius)
        self.lower_center = (x + self.radius, y + self.height - self.radius)

        self.inputs = []
        self.control = {}
        self.output = {
            'pos':(self.x + self.width, self.y + self.height / 2), 
            'value': 0
        }
    
    def set_form(self, notation, length):
        self.form = '#0' + str(length + 2) + ('x' if notation == 16 else 'b')
        
    def set_inputs(self, inputs):
        block = self.height / len(inputs)
        for i, control in enumerate(inputs):
            self.inputs.append({
                'control': control,
                'pos': (self.x, self.y + block * (i + 0.5)),
                'value': 0
            })
    
    def set_control(self, notation, length, top=True):
        self.control = {
            'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
            'pos': (self.x + self.width / 2, self.y - 2 if top else self.y + self.height + 2),
            'value': 0,
            'top': top
        }
    
    def get_value(self):
        return self.output['value']

    def set_control_value(self, control):
        self.control['value'] = control
    
    def set_value(self, index, value):
        self.inputs[index]['value'] = value
    
    def get_control_pos(self):
        return self.control['pos']
    
    def get_output_pos(self):
        return self.output['pos']

    def get_input_pos(self, index):
        return self.inputs[index]['pos']
    
    def calculate(self):
        for label in self.inputs:
            if self.control['value'] == label['control']:
                self.output['value'] = label['value']
                break

    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.rect(screen, color, [self.x, self.y + self.radius, self.width, self.height - self.radius * 2])
        pygame.draw.circle(screen, color, self.upper_center, self.radius)
        pygame.draw.circle(screen, color, self.lower_center, self.radius)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        for label in self.inputs:
            control = font.render(format(label['control'], self.control['form']), True, COLOR_BLACK)
            control_rect = control.get_rect(center=(self.x + self.width / 2, label['pos'][1]))
            screen.blit(control, control_rect)
        
        if self.mouse_on(*mouse):
            for label in self.inputs:
                value = font.render(format(label['value'], self.form), True, COLOR_RED, COLOR_WHITE)
                value_rect = value.get_rect(midright=(self.x - 2, label['pos'][1]))
                screen.blit(value, value_rect)

            control = font.render(format(self.control['value'], self.control['form']), True, COLOR_RED, COLOR_WHITE)
            if self.control['top']:
                control_rect = control.get_rect(midbottom=(self.control['pos'][0], self.control['pos'][1] + 2))
            else:
                control_rect = control.get_rect(midtop=(self.control['pos'][0], self.control['pos'][1] - 2))
            screen.blit(control, control_rect)
            
            output = font.render(format(self.output['value'], self.form), True, COLOR_RED, COLOR_WHITE)
            output_rect = output.get_rect(midleft=(self.x + self.width + 2, self.y + self.height / 2))
            screen.blit(output, output_rect)
    
    def mouse_on(self, x, y):
        center_rect = (self.x <= x <= self.x + self.width and self.y + self.radius <= y <= self.y + self.height - self.radius)
        upper_circle = self.inside_circle((x, y), self.upper_center)
        lower_circle = self.inside_circle((x, y), self.lower_center)
        return center_rect or upper_circle or lower_circle
    
    def inside_circle(self, p1, p2):
        return (p1[0] - p2[0])**2 + (p1[1] - p2[1])**2 <= self.radius**2