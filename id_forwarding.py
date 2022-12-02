from signal_unit import SignalUnit


class IdForwarding(SignalUnit):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, [2, 2, 0, 3], 'Id Forwarding')
        labels = [
            ('EX/MEM.rd', 1, 0, 2, 5),
            ('EX/MEM.RegWrite', 1, 1, 2, 1),
            ('Branch', 3, 0, 2, 2),
            ('IF/ID.rt', 3, 1, 2, 5),
            ('IF/ID.rs', 3, 2, 2, 5)
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
        if self.inputs['EX/MEM.RegWrite']['value'] and self.inputs['Branch'] and \
            self.inputs['EX/MEM.rd']['value'] != 0:
            if self.inputs['EX/MEM.rd']['value'] == self.inputs['IF/ID.rs']['value']:
                forward_a = 0b1
            if self.inputs['EX/MEM.rd']['value'] == self.inputs['IF/ID.rt']['value']:
                forward_b = 0b1
        self.outputs['ForwardA']['value'] = forward_a
        self.outputs['ForwardB']['value'] = forward_b