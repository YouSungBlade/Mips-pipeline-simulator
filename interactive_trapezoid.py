import pygame
from const import *


class InteractiveTrapezoid():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.points = [(x, y)]
        self.gap = height / 4
        self.points.append((x, y + height))
        self.points.append((x + width, y + height - self.gap))
        self.points.append((x + width, y + self.gap))
    
    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.polygon(screen, color, self.points)

    def mouse_on(self, x, y):
        center_rect = (self.x <= x <= self.x + self.width and self.y + self.gap <= y <= self.y + self.height - self.gap)
        upper_triangle = self.inside_triangle((x, y), self.points[0], (self.x, self.y + self.gap), self.points[3])
        lower_triangle = self.inside_triangle((x, y), (self.x, self.y + self.height - self.gap), self.points[1], (self.x + self.width, self.y + self.height - self.gap))
        return center_rect or upper_triangle or lower_triangle
    
    def sign(self, p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    def inside_triangle(self, p, p1, p2, p3):
        d1 = self.sign(p, p1, p2)
        d2 = self.sign(p, p2, p3)
        d3 = self.sign(p, p3, p1)
        neg = d1 < 0 or d2 < 0 or d3 < 0
        pos = d1 > 0 or d2 > 0 or d3 > 0
        return not (neg and pos)


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
        self.output['value'] = (self.inputs[0]['value'] + self.inputs[1]['value']) & 0xFFFFFFFF
    
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


class ALU(SimpleAdder):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        super().set_inputs([(16, 8), (16, 8)])
        self.name = 'ALU'
        self.control = {
            'form': '#06b',
            'pos': (self.x + self.width / 2, self.y + self.height * 3 / 4),
            'value': 0
        }
    
    def set_control_value(self, value):
        self.control['value'] = value
    
    def get_control_pos(self):
        pos = self.control['pos']
        return (pos[0], pos[1] + 11)
    
    def calculate(self):
        if self.control['value'] == 0b0000:
            result = self.inputs[0]['value'] & self.inputs[1]['value']
        elif self.control['value'] == 0b0001:
            result = self.inputs[0]['value'] | self.inputs[1]['value']
        elif self.control['value'] == 0b0010:
            result = self.inputs[0]['value'] + self.inputs[1]['value']
            result &= 0xFFFFFFFF
        elif self.control['value'] == 0b0110:
            result = self.inputs[0]['value'] + self.complement(self.inputs[1]['value'])
            result &= 0xFFFFFFFF
        elif self.control['value'] == 0b0111:
            result = self.inputs[0]['value'] + self.complement(self.inputs[1]['value'])
            result = (result >> 31) & 1
        self.output['value'] = result
    
    def complement(self, number):
        return 0xffffffff - number + 1
    
    def draw(self, screen, mouse):
        super().draw(screen, mouse)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        if self.mouse_on(*mouse):
            control = font.render(format(self.control['value'], self.control['form']), True, COLOR_RED, COLOR_WHITE)
            control_rect = control.get_rect(midtop=(self.control['pos'][0], self.control['pos'][1] + 5))
            screen.blit(control, control_rect)