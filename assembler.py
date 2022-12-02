class Assembler:
    def __init__(self, file_path):
        self.base_inst_loc = 0x00400024
        self.base_mem_loc = 0x00000000

        self.label_table = {}
        self.instructions = {}
        self.memory = {}

        f = open(file_path, 'r')
        self.lines = f.readlines()
        f.close()
    
    def first_pass(self):
        mode = 'text'
        inst_loc = self.base_inst_loc
        mem_loc = self.base_mem_loc

        for line in self.lines:
            if '#' in line:
                line = line[:line.find('#')]
            line = line.strip()
            
            if ':' in line:
                label = line[:line.find(':')]
                self.label_table[label] = inst_loc if mode == 'text' else mem_loc
                line = line[line.find(':') + 1:].strip()
            
            if not line:
                continue
            
            if '.' in line:
                if '.data' in line:
                    mode = 'data'
                    addr = line[5:].strip()
                    if addr:
                        mem_loc = int(addr, 0)
                elif '.text' in line:
                    mode = 'text'
                    addr = line[5:].strip()
                    if addr:
                        inst_loc = int(addr, 0)
                elif '.asciiz' in line:
                    string = line[7:].strip()[1:-1]
                    mem_loc += len(string) + 1
                elif '.ascii' in line:
                    string = line[7:].strip()[1:-1]
                    mem_loc += len(string)
                elif '.space' in line:
                    amount = int(line[6:].strip(), 0)
                    mem_loc += amount
                elif '.byte' in line:
                    data = [int(x.strip(), 0) for x in line[5:].strip().split(',')]
                    mem_loc += len(data)
                elif '.half' in line:
                    data = [int(x.strip(), 0) for x in line[5:].strip().split(',')]
                    mem_loc += len(data) * 2
                elif '.word' in line:
                    mem_loc = (mem_loc + 3) // 4 * 4
                    data = [int(x.strip(), 0) for x in line[5:].strip().split(',')]
                    mem_loc += len(data) * 4
            else:
                inst_loc += 4
            
    def second_pass(self):
        inst_loc = self.base_inst_loc
        mem_loc = self.base_mem_loc
        
        for line in self.lines:
            if '#' in line:
                line = line[:line.find('#')]
            line = line.strip()
            
            if ':' in line:
                line = line[line.find(':') + 1:].strip()
            
            if not line:
                continue
            
            if '.' in line:
                if '.data' in line:
                    addr = line[5:].strip()
                    if addr:
                        mem_loc = int(addr, 0)
                elif '.text' in line:
                    addr = line[5:].strip()
                    if addr:
                        inst_loc = int(addr, 0)
                elif '.asciiz' in line:
                    string = line[7:].strip()[1:-1]
                    for character in string:
                        self.memory[mem_loc] = ord(character)
                        mem_loc += 1
                    mem_loc += 1
                elif '.ascii' in line:
                    string = line[7:].strip()[1:-1]
                    for character in string:
                        self.memory[mem_loc] = ord(character)
                        mem_loc += 1
                elif '.space' in line:
                    amount = int(line[6:].strip(), 0)
                    mem_loc += amount
                elif '.byte' in line:
                    data = [int(x.strip(), 0) for x in line[5:].strip().split(',')]
                    for value in data:
                        self.memory[mem_loc] = value
                        mem_loc += 1
                elif '.half' in line:
                    data = [int(x.strip(), 0) for x in line[5:].strip().split(',')]
                    for value in data:
                        upper = (0xFF00 & value) >> 8
                        for i in range(1, -1, -1):
                            to_store = ((0xFF << (i * 8)) & value) >> (i * 8)
                            self.memory[mem_loc] = to_store
                            mem_loc += 1
                elif '.word' in line:
                    mem_loc = (mem_loc + 3) // 4 * 4
                    data = [int(x.strip(), 0) for x in line[5:].strip().split(',')]
                    for value in data:
                        for i in range(4):
                            to_store = ((0xFF << (i * 8)) & value) >> (i * 8)
                            self.memory[mem_loc] = to_store
                            mem_loc += 1
            else:
                if 'beq' in line:
                    rs, rt, label = [x.strip() for x in line.replace(',', ' ').replace('(', ' ').replace(')', ' ')[3:].split()]
                    rt = register_table[rt] if rt in register_table else int(rt[1:])
                    rs = register_table[rs] if rs in register_table else int(rs[1:])
                    immediate = self.label_table[label] - (inst_loc + 4)
                    immediate >>= 2
                    immediate = (0b1111111111111111 - abs(immediate) + 1) if immediate < 0 else immediate
                    opcode = opcode_table['beq']
                    instruction = (opcode << 26) | (rs << 21) | (rt << 16) | immediate
                elif 'j' in line:
                    opcode = opcode_table['j']
                    label = line[1:].strip()
                    address = self.label_table[label] >> 2
                    instruction = (opcode << 26) | address
                elif '(' in line:
                    name, rt, immediate, rs = [x.strip() for x in line.replace(',', ' ').replace('(', ' ').replace(')', ' ').split()]
                    opcode = opcode_table[name]
                    rt = register_table[rt] if rt in register_table else int(rt[1:])
                    rs = register_table[rs] if rs in register_table else int(rs[1:])
                    immediate = int(immediate)
                    instruction = (opcode << 26) | (rs << 21) | (rt << 16) | immediate
                else:
                    name = line[:line.find(' ')]
                    opcode = 0b000000
                    funct = funct_table[name]
                    arguments = [x.strip() for x in line[len(name):].split(',')]
                    for i in range(3):
                        if arguments[i] in register_table:
                            arguments[i] = register_table[arguments[i]]
                        else:
                            arguments[i] = int(arguments[i][1:])
                    rd, rs, rt = arguments
                    instruction = (opcode << 26) | (rs << 21) | (rt << 16) | (rd << 11) | (0b00000 << 6) | funct
                self.instructions[inst_loc] = (instruction, line)
                inst_loc += 4
    
    def get_instructions(self):
        return self.instructions
    
    def get_memory(self):
        return self.memory

register_table = {
    '$zero': 0,
	'$at': 1,
	'$v0': 2,
	'$v1': 3,
	'$a0': 4,
	'$a1': 5,
	'$a2': 6,
	'$a3': 7,
	'$t0': 8,
	'$t1': 9,
	'$t2': 10,
	'$t3': 11,
	'$t4': 12,
	'$t5': 13,
	'$t6': 14,
	'$t7': 15,
	'$s0': 16,
	'$s1': 17,
	'$s2': 18,
	'$s3': 19,
	'$s4': 20,
    '$s5': 21,
	'$s6': 22,
	'$s7': 23,
	'$t8': 24,
	'$t9': 25,
	'$k0': 26,
	'$k1': 27,
    '$gp': 28,
	'$sp': 29,
	'$fp': 30,
    '$ra': 31
}

funct_table = {
    'add': 0b100000,
    'sub': 0b100010,
    'and': 0b100100,
    'or': 0b100101,
    'slt': 0b101010
}

opcode_table = {
    'lw': 0b100011,
    'sw': 0b101011,
    'beq': 0b000100,
    'j': 0b000010
}