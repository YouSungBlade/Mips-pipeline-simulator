import pygame
from interactive_rect import InteractiveRect
from const import *

class InstructionMemory(InteractiveRect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.name = 'Instruction Memory'
        self.instruction_memory = {}
        self.inputs = '0x00000000'
        self.outputs = {}
        self.init_outputs()
        self.set_inputs()

    def init_memory(self, instruction_memory):
        self.instruction_memory = instruction_memory

    def set_inputs(self):
        pc = 0x00000004
        self.inputs = {
            'form': '#0' + str(10) + 'x',
            'pos': (self.x, self.y),
            'value': pc
        }

    def init_outputs(self):

        self.outputs['Fetched'] = {
            'pos': (self.x + self.width//2 , self.y + self.height),
            'value': 'add $0, $0, $0'
        }

        self.outputs['Decoded'] = {
            'form': '#0' + str(10) + 'x',
            'pos': (self.x + self.width, self.y + self.height//2),
            'value': 0
        }

    def get_value(self, name):
        return self.outputs[name]['value']

    def set_value(self, pc):
        self.inputs['value'] = pc

    def get_input_pos(self):
        return self.inputs['pos']

    def get_output_pos(self, name):
        return self.outputs[name]['pos']

    #fetch와 decode 계산
    def calculate(self):
        decoded, fetched = self.instruction_memory[self.inputs['value']]
        self.outputs['Decoded']['value'], self.outputs['Fetched']['value'] = decoded, fetched

    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)

        names = self.name.split()
        title1 = font.render(names[0], True, COLOR_BLACK)
        title_rect1 = title1.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2-20))
        title2 = font.render(names[1], True, COLOR_BLACK)
        title_rect2 = title2.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))

        screen.blit(title1, title_rect1)
        screen.blit(title2, title_rect2)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        if self.mouse_on(*mouse):
            value = font.render(format(self.inputs['value'], self.inputs['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midright=(self.x - 2, self.inputs['pos'][1]+5))
            screen.blit(value, value_rect)

            value = font.render(format(self.outputs['Decoded']['value'], self.outputs['Decoded']['form']), True,
                                COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midleft=(self.x+self.width+1, self.outputs['Decoded']['pos'][1]))
            screen.blit(value, value_rect)

            value = font.render(self.outputs['Fetched']['value'], True,
                                COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(center=(self.x + self.width // 2, self.outputs['Fetched']['pos'][1]-20))
            screen.blit(value, value_rect)

