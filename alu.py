import pygame
from simple_adder import SimpleAdder
from const import *


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
            if result & (1 << 32): result -= (1 << 32)
        elif self.control['value'] == 0b0110:
            result = self.inputs[0]['value'] + self.complement(self.inputs[1]['value'])
            if result & (1 << 32): result -= (1 << 32)
        elif self.control['value'] == 0b0111:
            result = self.inputs[0]['value'] + self.complement(self.inputs[1]['value'])
            result >>= 31
        self.output['value'] = result
    
    def complement(self, number):
        return 0xffffffff - number + 1 if number & (1 << 31) else number
    
    def draw(self, screen, mouse):
        super().draw(screen, mouse)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        if self.mouse_on(*mouse):
            control = font.render(format(self.control['value'], self.control['form']), True, COLOR_RED, COLOR_WHITE)
            control_rect = control.get_rect(midtop=(self.control['pos'][0], self.control['pos'][1] + 5))
            screen.blit(control, control_rect)

