import pygame
from interactive_rect import InteractiveRect
from const import *

class DataMemory(InteractiveRect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.name = 'Data Memory'
        self.inputs = {}
        self.output = {}
        self.controls = {}
        self.memory = {}

        self.init_output()
        self.init_controls()
        self.set_inputs()

    def set_inputs(self):

        inputs = [
            ('Address', 16, 8),
            ('WriteData', 16, 8)
        ]

        block = self.height-35
        for i, (name, notation, length) in enumerate(inputs):
            self.inputs[name] = {
                'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
                'pos': (self.x, self.y + block*i+20),
                'value': 0
            }

    def init_output(self):
        name, notation, length = ('ReadData', 16, 8)
        self.output = {
            'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
            'pos': (self.x + self.width, self.y + self.height / 2),
            'value': 0
        }

    def init_controls(self):
        controls = [
            ('MemWrite', 2, 1),
            ('MemRead', 2, 1),
        ]
        
        for i, (name, notation, length) in enumerate(controls):
            self.controls[name] = {
                'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
                'pos': (self.x +self.width/2, self.y + self.height * i),
                'value': 0
            }

    def set_control_value(self, name, value):
        self.controls[name]['value'] = value

    def init_memory(self, memory):
        self.memory = memory

    def get_value(self):
        return self.output['value']

    def set_value(self, name, value):
        self.inputs[name]['value'] = value

    def get_input_pos(self, name):
        return self.inputs[name]['pos']

    def get_output_pos(self):
        return self.output['pos']
    
    def get_contol_pos(self, name):
        return self.controls[name]['pos']

    def get_memory_data(self):
        return self.memory

    #데이터에 쓰기
    def write_to_data(self):
        pass
    #데이터에서 읽기
    def read_endian(self, address):
        res = 0

        for i in range(0, 4):
            if address in self.memory.keys():
                num = self.memory[address]
            else:
                num = 0
            res += (0xFF & num) << 8 * i
            address += 1
        return res

    def calculate(self):
        if self.controls['MemWrite']['value'] == 1:
            address = self.inputs['Address']['value']
            data = self.inputs['WriteData']['value']
            for i in range(0, 4):
                self.memory[address + i] = (data & (0xFF << 8 * i)) >> (8 * i)
        elif self.controls['MemRead']['value'] == 1:
            address = self.inputs['Address']['value']
            self.output['value'] = self.read_endian(address)

    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render(self.name, True, COLOR_BLACK)
        title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)

        value = font.render("MemWrite", True, COLOR_BLUE)
        value_rect = value.get_rect(midtop=(self.x + self.width / 2, self.controls['MemWrite']['pos'][1] + 2))
        screen.blit(value, value_rect)

        value = font.render("MemRead", True, COLOR_BLUE)
        value_rect = value.get_rect(midbottom=(self.x + self.width / 2, self.controls['MemRead']['pos'][1] - 2))
        screen.blit(value, value_rect)

        if self.mouse_on(*mouse):
            for label in self.inputs.values():
                value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
                value_rect = value.get_rect(midright=(self.x - 2, label['pos'][1]))
                screen.blit(value, value_rect)

            value = font.render(format(self.output['value'], self.output['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midleft=(self.x+self.width+1, self.output['pos'][1]))
            screen.blit(value, value_rect)

            label = self.controls['MemWrite']
            value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midbottom=(label['pos'][0], label['pos'][1] - 2))
            screen.blit(value, value_rect)

            label = self.controls['MemRead']
            value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midtop=(label['pos'][0], label['pos'][1] + 2))
            screen.blit(value, value_rect)
