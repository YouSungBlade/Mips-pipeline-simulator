import pygame
from const import *


class InteractiveRect():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.height])

    def mouse_on(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height


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
        self.control = None
    
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
    
    def set_control(self, name, notation, length):
        self.control = {
            'name': name,
            'form': '#0' + str(length + 2) + ('x' if notation == 16 else 'b'),
            'pos': (self.x + self.width / 2, self.y - 30),
            'value': 0,
        }

    def get_value(self, name):
        return self.outputs[name]['value']
    
    def set_value(self, name, value):
        self.inputs[name]['value'] = value
    
    def set_control_value(self, value):
        if self.control:
            self.control['value'] = value

    def get_input_pos(self, name):
        return self.inputs[name]['pos']

    def get_output_pos(self, name):
        return self.outputs[name]['pos']
    
    def get_control_pos(self):
        return self.control['pos'] if self.control else None
    
    def calculate(self):
        if not self.control or self.control['value']:
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
        
        if self.control:
            font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
            control = font.render(self.control['name'], True, COLOR_BLUE)
            control_rect = control.get_rect(midtop=(self.control['pos'][0], self.control['pos'][1] + 2))
            screen.blit(control, control_rect)
        
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
        
        if self.left_rect.mouse_on(*mouse) or self.right_rect.mouse_on(*mouse):
            if self.control:
                value = font.render(format(self.control['value'], self.control['form']), True, COLOR_RED, COLOR_WHITE)
                value_rect = value.get_rect(midbottom=(self.control['pos'][0], self.control['pos'][1] - 2))
                screen.blit(value, value_rect)
        
    def mouse_on(self, x, y):
        return self.left_rect.mouse_on(x, y) or self.right_rect.mouse_on(x, y)


class ProgramCounter(InteractiveRect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.input = {'pos': (self.x, self.y + self.height / 2), 'value': 0}
        self.output = {'pos': (self.x + self.width, self.y + self.height / 2), 'value': 0}
        self.control = {'pos': (self.x + self.width / 2, self.y), 'value': 0, 'form': '#03b'}
        self.form = '#010x'
    
    def get_value(self):
        return self.output['value']
    
    def set_value(self, value):
        self.input['value'] = value
    
    def set_control_value(self, value):
        self.control['value'] = value
    
    def get_input_pos(self):
        return self.input['pos']
    
    def get_output_pos(self):
        return self.output['pos']
    
    def get_control_pos(self):
        return self.control['pos']
    
    def calculate(self):
        if self.control['value']:
            self.output['value'] = self.input['value']
    
    def draw(self, screen, mouse):
        super().draw(screen, mouse)
        font = pygame.font.SysFont(FONT, FONT_SIZE_L, True)
        title = font.render('PC', True, COLOR_BLACK)
        title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
        screen.blit(title, title_rect)

        font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
        control = font.render("PCWrite", True, COLOR_BLUE)
        control_rect = control.get_rect(midtop=(self.control['pos'][0], self.control['pos'][1] + 2))
        screen.blit(control, control_rect)

        if self.mouse_on(*mouse):
            font = pygame.font.SysFont(FONT, FONT_SIZE_S, True)
            value = font.render(format(self.input['value'], self.form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midright=(self.input['pos'][0] - 2, self.input['pos'][1]))
            screen.blit(value, value_rect)

            value = font.render(format(self.output['value'], self.form), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midleft=(self.output['pos'][0] + 2, self.output['pos'][1]))
            screen.blit(value, value_rect)

            value = font.render(format(self.control['value'], self.control['form']), True, COLOR_RED, COLOR_WHITE)
            value_rect = value.get_rect(midbottom=(self.control['pos'][0], self.control['pos'][1] - 2))
            screen.blit(value, value_rect)


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
        self.inputs = {
            'form': '#0' + str(10) + 'x',
            'pos': (self.x, self.y + self.height / 2),
            'value': 0
        }

    def init_outputs(self):

        self.outputs['Fetched'] = {
            'pos': (self.x + self.width//2 , self.y + self.height),
            'value': 'nop'
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
        if self.inputs['value'] in self.instruction_memory:
            decoded, fetched = self.instruction_memory[self.inputs['value']]
        else:
            decoded, fetched = 0x00000000, 'nop'
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
        return self.outputs[name]['value']

    def set_value(self, name, value):
        self.inputs[name]['value'] = value

    def get_input_pos(self, name):
        return self.inputs[name]['pos']

    def get_output_pos(self, name):
        return self.outputs[name]['pos']

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