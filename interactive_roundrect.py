import pygame
from const import *


class InteractiveRoundrect():
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.radius = int(0.05 * (width + height))
    
    def draw(self, screen, mouse):
        color = COLOR_ON if self.mouse_on(*mouse) else COLOR_OFF
        pygame.draw.rect(screen, color, [self.x, self.y, self.width, self.height], 0, self.radius)

    def mouse_on(self, x, y):
        hor_rect = (self.x <= x <= self.x + self.width and self.y + self.radius <= y <= self.y + self.height - self.radius)
        ver_rect = (self.x + self.radius <= x <= self.x + self.width - self.radius and self.y <= y <= self.y + self.height)
        if hor_rect or ver_rect:
            return True

        x_poses = (self.x + self.radius, self.x + self.width - self.radius)
        y_poses = (self.y + self.radius, self.y + self.height - self.radius)
        for center_x, center_y in [(cx, cy) for cx in x_poses for cy in y_poses]:
            if (x - center_x)**2 + (y - center_y)**2 <= self.radius**2:
                return True
        return False


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

        if not self.mouse_on(*mouse):
            title = font.render(self.name, True, COLOR_BLACK)
            title_rect = title.get_rect(center=(self.x + self.width / 2, self.y + self.height / 2))
            screen.blit(title, title_rect)
        else:
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


class ALUControlUnit(SignalUnit):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, [1, 0, 1, 1], 'ALU Control')
        labels = [
            ('ALUOp', 2, 0, 2, 2),
            ('Funct', 3, 0, 2, 6)
        ]
        self.set_inputs(labels)
        labels = [
            ('Operation', 0, 0, 2, 4)
        ]
        self.set_outputs(labels)
    
    def calculate(self):
        aluop = self.inputs['ALUOp']['value']
        funct = self.inputs['Funct']['value']

        if aluop == 0b00:
            operation = 0b0010
        elif aluop == 0b01:
            operation = 0b0110
        elif funct == 0b100000:
            operation = 0b0010
        elif funct == 0b100010:
            operation = 0b0110
        elif funct == 0b100100:
            operation = 0b0000
        elif funct == 0b100101:
            operation = 0b0001
        elif funct == 0b101010:
            operation = 0b0111
        self.outputs['Operation']['value'] = operation


class ControlUnit(SignalUnit):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, [0, 9, 0, 1], 'Control')
        labels = [
            ('Instruction', 3, 0, 16, 8)
        ]
        self.set_inputs(labels)
        labels = [
            ('Jump', 1, 0, 2, 1),
            ('Branch', 1, 1, 2, 1),
            ('RegWrite', 1, 2, 2, 1),
            ('MemtoReg', 1, 3, 2, 1),
            ('MemWrite', 1, 4, 2, 1),
            ('MemRead', 1, 5, 2, 1),
            ('RegDst', 1, 6, 2, 1),
            ('ALUOp', 1, 7, 2, 2),
            ('ALUSrc', 1, 8, 2, 1)
        ]
        self.set_outputs(labels)
    
    def calculate(self):
        opcode = (self.inputs['Instruction']['value'] >> 26) & 0b111111
        if self.inputs['Instruction']['value'] == 0x00000000:
            setting = [0, 0, 0, 0, 0, 0, 0, 0b00, 0]
        elif opcode == 0b000000:
            setting = [0, 0, 1, 0, 0, 0, 1, 0b10, 0]
        elif opcode == 0b100011:
            setting = [0, 0, 1, 1, 0, 1, 0, 0b00, 1]
        elif opcode == 0b101011:
            setting = [0, 0, 0, 0, 1, 0, 0, 0b00, 1]
        elif opcode == 0b000100:
            setting = [0, 1, 0, 0, 0, 0, 0, 0b00, 0]
        else:
            setting = [1, 0, 0, 0, 0, 0, 0, 0b00, 0]
        
        for i, name in enumerate(self.outputs.keys()):
            self.outputs[name]['value'] = setting[i]


class ExForwarding(SignalUnit):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, [2, 4, 0, 2], 'Ex Forwarding')
        labels = [
            ('EX/MEM.rd', 1, 0, 2, 5),
            ('EX/MEM.RegWrite', 1, 1, 2, 1),
            ('MEM/WB.rd', 1, 2, 2, 5),
            ('MEM/WB.RegWrite', 1, 3, 2, 1),
            ('ID/EX.rs', 3, 0, 2, 5),
            ('ID/EX.rt', 3, 1, 2, 5)
        ]
        self.set_inputs(labels)
        labels = [
            ('ForwardA', 0, 0, 2, 2),
            ('ForwardB', 0, 1, 2, 2)
        ]
        self.set_outputs(labels)
    
    def calculate(self):
        if self.inputs['EX/MEM.RegWrite']['value'] and self.inputs['EX/MEM.rd']['value'] != 0 and \
            self.inputs['EX/MEM.rd']['value'] == self.inputs['ID/EX.rs']['value']:
            forward_a = 0b10
        elif self.inputs['MEM/WB.RegWrite']['value'] and self.inputs['MEM/WB.rd']['value'] != 0 and \
            self.inputs['MEM/WB.rd']['value'] == self.inputs['ID/EX.rs']['value']:
            forward_a = 0b01
        else:
            forward_a = 0b00
        
        if self.inputs['EX/MEM.RegWrite']['value'] and self.inputs['EX/MEM.rd']['value'] != 0 and \
            self.inputs['EX/MEM.rd']['value'] == self.inputs['ID/EX.rt']['value']:
            forward_b = 0b10
        elif self.inputs['MEM/WB.RegWrite']['value'] and self.inputs['MEM/WB.rd']['value'] != 0 and \
            self.inputs['MEM/WB.rd']['value'] == self.inputs['ID/EX.rt']['value']:
            forward_b = 0b01
        else:
            forward_b = 0b00
        
        self.outputs['ForwardA']['value'] = forward_a
        self.outputs['ForwardB']['value'] = forward_b


class IdForwarding(SignalUnit):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, [2, 2, 0, 3], 'Id Forwarding')
        labels = [
            ('EX/MEM.rd', 1, 0, 2, 5),
            ('EX/MEM.RegWrite', 1, 1, 2, 1),
            ('Branch', 3, 0, 2, 2),
            ('IF/ID.rs', 3, 1, 2, 5),
            ('IF/ID.rt', 3, 2, 2, 5)
        ]
        self.set_inputs(labels)
        labels = [
            ('ForwardA', 0, 0, 2, 1),
            ('ForwardB', 0, 1, 2, 1)
        ]
        self.set_outputs(labels)
    
    def calculate(self):
        forward_a = 0b0
        forward_b = 0b0
        if self.inputs['EX/MEM.RegWrite']['value'] and self.inputs['Branch']['value'] and \
            self.inputs['EX/MEM.rd']['value'] != 0:
            if self.inputs['EX/MEM.rd']['value'] == self.inputs['IF/ID.rs']['value']:
                forward_a = 0b1
            if self.inputs['EX/MEM.rd']['value'] == self.inputs['IF/ID.rt']['value']:
                forward_b = 0b1
        self.outputs['ForwardA']['value'] = forward_a
        self.outputs['ForwardB']['value'] = forward_b


class HazardDetection(SignalUnit):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, [3, 3, 3, 4], 'Hazard Detection')
        labels = [
            ('EX/MEM.MemRead', 0, 0, 2, 1),
            ('EX/MEM.RegisterRd', 0, 2, 2, 5),
            ('ID/EX.MemRead', 1, 0, 2, 1),
            ('ID/EX.RegWrite', 1, 1, 2, 1),
            ('Branch', 2, 0, 2, 1),
            ('ID/EX.rd', 2, 1, 2, 5),
            ('ID/EX.rt', 2, 2, 2, 5),
            ('IF/ID.rs', 3, 2, 2, 5),
            ('IF/ID.rt', 3, 3, 2, 5)
        ]
        self.set_inputs(labels)
        labels = [
            ('ControlMUX', 1, 2, 2, 1),
            ('PCWrite', 3, 0, 2, 1),
            ('IF/IDWrite', 3, 1, 2, 1)
        ]
        self.set_outputs(labels)
    
    def calculate(self):
        value = 1
        if self.inputs['ID/EX.MemRead']['value'] and self.inputs['ID/EX.RegWrite']['value'] and \
            (self.inputs['ID/EX.rt']['value'] == self.inputs['IF/ID.rs']['value'] or \
                self.inputs['ID/EX.rt']['value'] == self.inputs['IF/ID.rt']['value']):
            value = 0
        elif self.inputs['Branch']['value'] and self.inputs['ID/EX.RegWrite']['value'] and \
            (self.inputs['ID/EX.rd']['value'] == self.inputs['IF/ID.rs']['value'] or \
                self.inputs['ID/EX.rd']['value'] == self.inputs['IF/ID.rt']['value']):
            value = 0
        elif self.inputs['Branch']['value'] and self.inputs['EX/MEM.MemRead']['value'] and \
            (self.inputs['EX/MEM.RegisterRd']['value'] == self.inputs['IF/ID.rs']['value'] or \
                self.inputs['EX/MEM.RegisterRd']['value'] == self.inputs['IF/ID.rt']['value']):
            value = 0
        self.outputs['PCWrite']['value'] = value
        self.outputs['IF/IDWrite']['value'] = value
        self.outputs['ControlMUX']['value'] = value