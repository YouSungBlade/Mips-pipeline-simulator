from signal_unit import SignalUnit


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
        opcode = self.inputs['Instruction']['value'] & 0b111111
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
        
        