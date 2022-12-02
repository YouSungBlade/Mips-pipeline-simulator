from signal_unit import SignalUnit


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