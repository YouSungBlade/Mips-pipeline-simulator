from signal_unit import SignalUnit


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