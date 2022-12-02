class InteractivePolygon:
    def __init__(self, name):
        self.name = name
        self.value = 0x00000000
    
    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return format(self.value, '#010x')