from signal_unit import SignalUnit


class HazardDetection(SignalUnit):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, [2, 2, 3, 4], 'Hazard Detection')
        labels = [
            ('Stall', 0, 1, 2, 1),
            ('ID/EX.MemRead', 1, 0, 2, 1),
            ('Branch', 2, 0, 2, 1),
            ('ID/EX.rd', 2, 1, 2, 5),
            ('ID/EX.rt', 2, 2, 2, 5),
            ('IF/ID.rs', 3, 2, 2, 5),
            ('IF/ID.rt', 3, 3, 2, 5)
        ]
        self.set_inputs(labels)
        labels = [
            ('ReStall', 0, 0, 2, 1),
            ('ControlMUX', 1, 1, 2, 1),
            ('PCWrite', 3, 0, 2, 1),
            ('IF/IDWrite', 3, 1, 2, 1)
        ]
        self.set_outputs(labels)
    
    def calculate(self):
        value = 1
        if self.inputs['ID/EX.MemRead']['value'] and \
            (self.inputs['ID/EX.rt']['value'] == self.inputs['IF/ID.rs']['value'] or \
                self.inputs['ID/EX.rt']['value'] == self.inputs['IF/ID.rt']['value']):
            value = 0
            if self.inputs['Branch']['value']:
                self.outputs['ReStall']['value'] = 1
        elif self.inputs['Branch']['value'] and \
            (self.inputs['ID/EX.rd']['value'] == self.inputs['IF/ID.rs']['value'] or \
                self.inputs['ID/EX.rd']['value'] == self.inputs['IF/ID.rt']['value']):
            value = 0
        self.outputs['PCWrite']['value'] = value
        self.outputs['IF/IDWrite']['value'] = value
        self.outputs['ControlMUX']['value'] = value
