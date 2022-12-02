from assembler import Assembler


assembler = Assembler('test.s')
assembler.first_pass()
assembler.second_pass()
memory = assembler.memory
for key, value in sorted(memory.items()):
    print(f'key: {key}, value: {hex(value)}')

instructions = assembler.instructions
for key, (value, string) in sorted(instructions.items()):
    value = '{0:032b}'.format(value)
    print(f'key: {key}, value: {value}, instruction: {string}')

