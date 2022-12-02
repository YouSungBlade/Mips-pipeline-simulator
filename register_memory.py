import pygame
from interactive_rect import InteractiveRect
from const import *

class RegisterMemory(InteractiveRect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.name = 'Registers'
        self.inputs = {}
        self.outputs = {}
        self.registers = []
        self.control = {}

        self.init_outputs()
        self.init_inputs()
        self.init_registers()
        self.init_control()

    def init_inputs(self):

        register_memory_labels = [
            ('ReadRegister1', 2, 5),
            ('ReadRegister2', 2, 5),
            ('WriteRegister', 2, 5),
            ('WriteData', 16, 8)
        ]

        block = self.height / len(register_memory_labels)

        for i, (name, notation, length) in enumerate(register_memory_labels):
            self.inputs[name] = {
                'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
                'pos': (self.x, self.y + block * (i + 0.5)),
                'value': 0
            }

    def init_outputs(self):
        outputs = [
            ('ReadData1', 16, 8),
            ('ReadData2', 16, 8),
        ]
        block = self.height / 2
        for i, (name, notation, length) in enumerate(outputs):
            self.outputs[name] = {
                'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
                'pos': (self.x + self.width, self.y + block * (i + 0.5)),
                'value': 0
            }

    def init_registers(self):
        register_memory = [0]*32
        # $sp 는 0x7ffffe40, $gp 는 0x10008000 초기화
        register_memory[29] = 0x7ffffe40
        register_memory[28] = 0x10008000
        self.registers = register_memory

    def init_control(self):
        self.control = {
            'form': '#0' + str(1 + 2) + 'b',
            'pos': (self.x + self.width / 2, self.y + self.height),
            'value': 0,
        }

    def get_registers(self):
        return self.registers

    def get_value(self, name):
        return self.output[name]['value']

    def set_value(self, name, value):
        self.inputs[name]['value'] = value

    def get_input_pos(self, name):
        return self.inputs[name]['pos']

    def get_output_pos(self, name):
        return self.output[name]['pos']

    def set_control_value(self, control):
        self.control['value'] = control

    def get_control_pos(self):
        return self.control['pos']

    def calculate(self, flag = 'Read'):
        if flag == 'Read':
            reg1_num = self.inputs['ReadRegister1']['value']
            reg2_num = self.inputs['ReadRegister2']['value']
            self.outputs['ReadData1']['value'] = self.registers[reg1_num]
            self.outputs['ReadData2']['value'] = self.registers[reg2_num]

        elif flag == 'Write':
            if self.control['value'] == 1:
                write_reg =  self.inputs['WriteRegister']['value']
                write_data = self.inputs['WriteData']['value']
                self.registers[write_reg] = write_data
        else:
            print("flag error")


    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render(self.name, True, COLOR_BLACK)
        title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        value = font.render("RegWrite", True, COLOR_BLUE)
        value_rect = value.get_rect(midbottom=(self.x + self.width / 2, self.control['pos'][1] - 2))
        screen.blit(value, value_rect)

        if self.mouse_on(*mouse):
            for label in self.inputs.values():
                value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
                value_rect = value.get_rect(midright=(self.x - 2, label['pos'][1]))
                screen.blit(value, value_rect)

            for label in self.outputs.values():
                value = font.render(format(label['value'], label['form']), True, COLOR_RED, COLOR_WHITE)
                value_rect = value.get_rect(midleft=(self.x+self.width+1, label['pos'][1]))
                screen.blit(value, value_rect)


            value = font.render(format(self.control['value'], self.control['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midtop=(self.x+self.width/2, self.control['pos'][1] + 2))
            screen.blit(value, value_rect)
