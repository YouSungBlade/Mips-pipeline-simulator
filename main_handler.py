import pygame
from simple_adder import SimpleAdder
from pipeline_register import PipelineRegister
from multiplexer import Multiplexer
from alu import ALU
from hazard_detection import HazardDetection
from and_gate import AndGate
from or_gate import OrGate
from sign_extension import SignExtension
from shift_left import ShiftLeft
from ex_forwarding import ExForwarding
from id_forwarding import IdForwarding
from equal_unit import EqualUnit
from control_unit import ControlUnit
from alu_control_unit import ALUControlUnit
from const import *
from register_memory import RegisterMemory
from instruction_memory import InstructionMemory
from data_memory import DataMemory
from lines import *
from concat import Concat
from program_counter import ProgramCounter

from interactive_roundrect import InteractiveRoundrect

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()

adder_pc = SimpleAdder(400, 300, 30, 60)
adder_pc.set_inputs([(16, 8), (2, 4)])
adder_branch = SimpleAdder(800, 360, 30, 60)
adder_branch.set_inputs([(16, 8),(2, 4)])

concat = Concat(630, 300, 50, 50)
pc= ProgramCounter(240, 465, 50, 50)
IFID_pr = PipelineRegister(550, 230, 50, 700, 'IF/ID')
IDEX_pr = PipelineRegister(1050, 230, 50, 700, 'ID/EX')
EXMEM_pr = PipelineRegister(1400, 230, 50, 700, 'EX/MEM')
MEMWB_pr = PipelineRegister(1700, 230, 50, 700, 'MEM/WB')

labels = [
    ('NextPC', 1, 16, 8),
    ('Instruction', 3, 16, 8)
]
IFID_pr.set_inputs(labels)
IFID_pr.set_value('Instruction', 0b00000010001011100000000000000000)

labels = [
    ('ReStall', 1, 2, 1),
    ('RegWrite', 1, 2, 1), 
    ('MemtoReg', 1, 2, 1), 
    ('MemWrite', 1, 2, 1),
    ('MemRead', 1, 2, 1),
    ('RegDst', 1, 2, 1), 
    ('ALUOp', 1, 2, 2),
    ('ALUSrc', 1, 2, 1),
    ('Register1', 8, 16, 8), 
    ('Register2', 8, 16, 8), 
    ('Extended', 3, 16, 8), 
    ('Rs', 3, 2, 5), 
    ('Rt', 3, 2, 5), 
    ('Rd', 3, 2, 5)
]
IDEX_pr.set_inputs(labels)

labels = [
    ('RegWrite', 1, 2, 1),
    ('MemtoReg', 1, 2, 1),
    ('MemWrite', 1, 2, 1),
    ('MemRead', 1, 2, 1),   
    ('ALUResult', 4, 16, 8),
    ('Operand2', 4, 16, 8),
    ('RegisterRd', 3.5, 2, 5)
]
EXMEM_pr.set_inputs(labels)
EXMEM_pr.set_value('RegWrite', 1)
EXMEM_pr.set_value('MemtoReg', 1)
EXMEM_pr.set_value('MemWrite', 1)
EXMEM_pr.set_value('MemRead', 1)
EXMEM_pr.set_value('ALUResult', 0x89ABCDEF)
EXMEM_pr.set_value('Operand2', 0x12345678)
EXMEM_pr.set_value('RegisterRd', 0b10101)


labels = [
    ('RegWrite', 1, 2, 1),
    ('MemtoReg', 1, 2, 1),
    ('MemData', 3, 16, 8),
    ('ALUResult', 3, 16, 8),
    ('RegisterRd', 2, 2, 5)
]
MEMWB_pr.set_inputs(labels)
# MEMWB_pr.set_value('RegWrite', 1)
# MEMWB_pr.set_value('MemtoReg', 1)
# MEMWB_pr.set_value('MemData', 0x87654321)
# MEMWB_pr.set_value('ALUResult', 0x12345678)
# MEMWB_pr.set_value('RegisterRd', 0b10110)

instruction_memory = InstructionMemory(310, 430, 150, 150)
register_memory = RegisterMemory(750, 500, 120, 150)
data_memory = DataMemory(1500, 430, 150, 150)


# mux

pc_mux = Multiplexer(180, 450, 30, 80)
pc_mux.set_inputs([1, 0])
pc_mux.set_control(2, 1, top=True)
pc_mux.set_form(16, 8)

branch_mux = Multiplexer(130, 450, 30, 80)
branch_mux.set_inputs([0, 1])
branch_mux.set_control(2, 1, top=True)
branch_mux.set_form(16, 8)

RegDst_mux = Multiplexer(1140, 830, 30, 80)
RegDst_mux.set_inputs([0, 1])
RegDst_mux.set_control(2, 1, top=True)
RegDst_mux.set_form(2, 5)

control_mux = Multiplexer(960, 230, 30, 80)
control_mux.set_inputs([0, 1])
control_mux.set_control(2, 1, top=True)
control_mux.set_form(16, 8)

ID_a_mux = Multiplexer(920, 480, 30, 80)
ID_a_mux.set_inputs([0, 1])
ID_a_mux.set_control(2, 1, top=False)
ID_a_mux.set_form(16, 8)

ID_b_mux = Multiplexer(920, 580, 30, 80)
ID_b_mux.set_inputs([0, 1])
ID_b_mux.set_control(2, 1, top=False)
ID_b_mux.set_form(16, 8)

EX_a_mux = Multiplexer(1170, 420, 30, 80)
EX_a_mux.set_inputs([0, 1 ,2])
EX_a_mux.set_control(2, 1, top=False)
EX_a_mux.set_form(16, 8)

EX_b_mux = Multiplexer(1170, 530, 30, 80)
EX_b_mux.set_inputs([0, 1, 2])
EX_b_mux.set_control(2, 1, top=False)
EX_b_mux.set_form(16, 8)

ALUSrc_mux = Multiplexer(1220, 560, 30, 80)
ALUSrc_mux.set_inputs([0, 1])
ALUSrc_mux.set_control(2, 1, top=True)
ALUSrc_mux.set_form(16, 8)

MemtoReg_mux = Multiplexer(1800, 500, 30, 80)
MemtoReg_mux.set_inputs([0, 1])
MemtoReg_mux.set_control(2, 1, top=True)
MemtoReg_mux.set_form(16, 8)

alu = ALU(1300, 450, 50, 100)
alu.set_value(0, 0x01234567)
alu.set_value(1, 0x12345678)
alu.set_control_value(0b0010)
alu.calculate()

hazard_detection = HazardDetection(630, 30, 300, 150)
hazard_detection.set_value('ID/EX.MemRead', 1)
hazard_detection.set_value('ID/EX.rt', 4)
hazard_detection.set_value('IF/ID.rs', 4)
hazard_detection.set_value('IF/ID.rt', 8)
hazard_detection.calculate()

and_gate = AndGate(1000, 100, 40, 50)
and_gate.set_value(0, 1)
and_gate.calculate()

or_gate_test = OrGate(0, 900, 40, 50)
or_gate_test.set_value(1, 1)
or_gate_test.calculate()

sign_extension = SignExtension(650, 720, 50, 50)
sign_extension.set_value(0x8000)
sign_extension.calculate()

shift_left_jump = ShiftLeft(660, 430, 50, 50)
shift_left_branch = ShiftLeft(720, 430, 50, 50)
shift_left_jump.set_value(0x0003ab2f)
shift_left_jump.calculate()

ex_forwarding = ExForwarding(1210, 880, 150, 100)

id_forwarding = IdForwarding(850, 880, 150, 100)

equal = EqualUnit(960, 540, 40, 40)

control = ControlUnit(700, 220, 120, 130)
control.calculate()

alu_control = ALUControlUnit(1230, 700, 150, 100)
alu_control.calculate()


cycle_button = InteractiveRoundrect(100, 50, 100, 70)

objs = []
objs.append(cycle_button)
objs.append(adder_pc)
objs.append(adder_branch)
objs.append(pc)
objs.append(IFID_pr)
objs.append(IDEX_pr)
objs.append(EXMEM_pr)
objs.append(MEMWB_pr)
objs.append(pc_mux)
objs.append(branch_mux)
objs.append(RegDst_mux)
objs.append(control_mux)
objs.append(ID_a_mux)
objs.append(ID_b_mux)
objs.append(EX_a_mux)
objs.append(EX_b_mux)
objs.append(ALUSrc_mux)
objs.append(MemtoReg_mux)
objs.append(alu)
objs.append(hazard_detection)
objs.append(and_gate)
# objs.append(or_gate_test)
objs.append(sign_extension)
objs.append(shift_left_jump)
objs.append(shift_left_branch)
objs.append(ex_forwarding)
objs.append(id_forwarding)
objs.append(concat)
objs.append(equal)
objs.append(control)
objs.append(alu_control)
objs.append(data_memory)
objs.append(instruction_memory)
objs.append(register_memory)

lines = []
lines.append(OneCornerLine(MEMWB_pr.get_output_pos('MemtoReg'), MemtoReg_mux.get_control_pos(), True))
lines.append(TwoCornerLine(MEMWB_pr.get_output_pos('MemData'), MemtoReg_mux.get_input_pos(0), 1770, True))
lines.append(TwoCornerLine(MEMWB_pr.get_output_pos('ALUResult'), MemtoReg_mux.get_input_pos(1), 1770, True))
lines.append(FourCornerLine(MemtoReg_mux.get_output_pos(), register_memory.get_input_pos('WriteData'), (735, 1030), 1850, True, False))
lines.append(FourCornerLine(MEMWB_pr.get_output_pos('RegisterRd'), register_memory.get_input_pos('WriteRegister'), (720, 1050), 1770, True, False))
lines.append(ThreeCornerLine(MEMWB_pr.get_output_pos('RegWrite'), register_memory.get_control_pos(), (1785, 1010), True, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('RegWrite'), MEMWB_pr.get_input_pos('RegWrite'), 1665, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('MemtoReg'), MEMWB_pr.get_input_pos('MemtoReg'), 1650, True))
lines.append(OneCornerLine(EXMEM_pr.get_output_pos('MemWrite'), data_memory.get_contol_pos('MemWrite'), True))
lines.append(ThreeCornerLine(EXMEM_pr.get_output_pos('MemRead'), data_memory.get_contol_pos('MemRead'), (1485, 620), True, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('ALUResult'), data_memory.get_input_pos('Address'), 1465, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('Operand2'), data_memory.get_input_pos('WriteData'), 1457, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('RegisterRd'), MEMWB_pr.get_input_pos('RegisterRd'), 1600, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('ALUResult'), MEMWB_pr.get_input_pos('ALUResult'), 1465, True))
lines.append(TwoCornerLine(data_memory.get_output_pos(), MEMWB_pr.get_input_pos('MemData'), 1685, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('RegWrite'), EXMEM_pr.get_input_pos('RegWrite'), 1350, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('MemtoReg'), EXMEM_pr.get_input_pos('MemtoReg'), 1350, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('MemWrite'), EXMEM_pr.get_input_pos('MemWrite'), 1300, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('MemRead'), EXMEM_pr.get_input_pos('MemRead'), 1250, True))
lines.append(OneCornerLine(IDEX_pr.get_output_pos('ALUSrc'), ALUSrc_mux.get_control_pos(), True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Extended'), ALUSrc_mux.get_input_pos(1), 1210, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Extended'), alu_control.get_input_pos('Funct'), 1210, True))
lines.append(ThreeCornerLine(IDEX_pr.get_output_pos('ALUOp'), alu_control.get_input_pos('ALUOp'), (1390, 830), True, True))
lines.append(TwoCornerLine(alu_control.get_output_pos('Operation'), alu.get_control_pos(), 625, False))
lines.append(OneCornerLine(IDEX_pr.get_output_pos('RegDst'), RegDst_mux.get_control_pos(), True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Rt'), RegDst_mux.get_input_pos(0), 1115, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Rd'), RegDst_mux.get_input_pos(1), 1107, True))
lines.append(TwoCornerLine(RegDst_mux.get_output_pos(), EXMEM_pr.get_input_pos('RegisterRd'), 1375, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Rs'), ex_forwarding.get_input_pos('ID/EX.rs'), 1176, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Rt'), ex_forwarding.get_input_pos('ID/EX.rt'), 1115, True))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('RegWrite'), ex_forwarding.get_input_pos('EX/MEM.RegWrite'), (1370, 975), 1665, True, False))
lines.append(TwoCornerLine(MEMWB_pr.get_output_pos('RegWrite'), ex_forwarding.get_input_pos('MEM/WB.RegWrite'), 1785, True))
lines.append(TwoCornerLine(MEMWB_pr.get_output_pos('RegisterRd'), ex_forwarding.get_input_pos('MEM/WB.rd'), 1770, True))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('RegisterRd'), ex_forwarding.get_input_pos('EX/MEM.rd'), (1385, 950), 1500, True, False))
lines.append(FourCornerLine(ex_forwarding.get_output_pos('ForwardA'), EX_a_mux.get_control_pos(), (1162, 520), 815, False, True))
lines.append(TwoCornerLine(ex_forwarding.get_output_pos('ForwardB'), EX_b_mux.get_control_pos(), 855, False))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Register1'), EX_a_mux.get_input_pos(0), 1115, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Register2'), EX_b_mux.get_input_pos(0), 1115, True))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('ALUResult'), EX_a_mux.get_input_pos(1), (1125, 990), 1465, True, False))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('ALUResult'), EX_b_mux.get_input_pos(1), (1125, 990), 1465, True, False))
lines.append(FourCornerLine(MemtoReg_mux.get_output_pos(), EX_a_mux.get_input_pos(2), (1133, 1030), 1850, True, False))
lines.append(FourCornerLine(MemtoReg_mux.get_output_pos(), EX_b_mux.get_input_pos(2), (1133, 1030), 1850, True, False))
lines.append(TwoCornerLine(EX_a_mux.get_output_pos(), alu.get_input_pos(0), 1270, True))
lines.append(TwoCornerLine(EX_b_mux.get_output_pos(), ALUSrc_mux.get_input_pos(0), 1210, True))
lines.append(TwoCornerLine(ALUSrc_mux.get_output_pos(), alu.get_input_pos(1), 1280, True))
lines.append(TwoCornerLine(alu.get_output_pos(), EXMEM_pr.get_input_pos('ALUResult'), 1370, True))
lines.append(FourCornerLine(EX_b_mux.get_output_pos(), EXMEM_pr.get_input_pos('Operand2'), (1265, 540), 1210, True, False))

def next_cycle():
    pc.calculate()
    IFID_pr.calculate()
    IDEX_pr.calculate()
    EXMEM_pr.calculate()
    MEMWB_pr.calculate()

    MemtoReg_mux.set_control_value(MEMWB_pr.get_value('MemtoReg'))
    MemtoReg_mux.set_value(0, MEMWB_pr.get_value('MemData'))
    MemtoReg_mux.set_value(1, MEMWB_pr.get_value('ALUResult'))
    MemtoReg_mux.calculate()

    register_memory.set_value('WriteData', MemtoReg_mux.get_value())
    register_memory.set_value('WriteRegister', MEMWB_pr.get_value('RegisterRd'))
    register_memory.set_control_value(MEMWB_pr.get_value('RegWrite'))
    register_memory.calculate('Write')

    MEMWB_pr.set_value('RegWrite', EXMEM_pr.get_value('RegWrite'))
    MEMWB_pr.set_value('MemtoReg', EXMEM_pr.get_value('MemtoReg'))
    data_memory.set_control_value('MemWrite', EXMEM_pr.get_value('MemWrite'))
    data_memory.set_control_value('MemRead', EXMEM_pr.get_value('MemRead'))
    data_memory.set_value('Address', EXMEM_pr.get_value('ALUResult'))
    data_memory.set_value('WriteData', EXMEM_pr.get_value('Operand2'))
    MEMWB_pr.set_value('RegisterRd', EXMEM_pr.get_value('RegisterRd'))
    MEMWB_pr.set_value('ALUResult', EXMEM_pr.get_value('ALUResult'))
    data_memory.calculate()
    MEMWB_pr.set_value('MemData', data_memory.get_value())

    EXMEM_pr.set_value('RegWrite', IDEX_pr.get_value('RegWrite'))
    EXMEM_pr.set_value('MemtoReg', IDEX_pr.get_value('MemtoReg'))
    EXMEM_pr.set_value('MemWrite', IDEX_pr.get_value('MemWrite'))
    EXMEM_pr.set_value('MemRead', IDEX_pr.get_value('MemRead'))

    ALUSrc_mux.set_control_value(IDEX_pr.get_value('ALUSrc'))
    extended = IDEX_pr.get_value('Extended')
    funct = extended & 0b111111
    ALUSrc_mux.set_value(1, IDEX_pr.get_value('Extended'))
    alu_control.set_value('Funct', funct)
    alu_control.set_value('ALUOp', IDEX_pr.get_value('ALUOp'))
    alu_control.calculate()
    alu.set_control_value(alu_control.get_value('Operation'))

    RegDst_mux.set_control_value(IDEX_pr.get_value('RegDst'))
    RegDst_mux.set_value(0, IDEX_pr.get_value('Rt'))
    RegDst_mux.set_value(1, IDEX_pr.get_value('Rd'))
    RegDst_mux.calculate()
    EXMEM_pr.set_value('RegisterRd', RegDst_mux.get_value())

    ex_forwarding.set_value('ID/EX.rs', IDEX_pr.get_value('Rs'))
    ex_forwarding.set_value('ID/EX.rt', IDEX_pr.get_value('Rt'))
    ex_forwarding.set_value('EX/MEM.RegWrite', EXMEM_pr.get_value('RegWrite'))
    ex_forwarding.set_value('MEM/WB.RegWrite', MEMWB_pr.get_value('RegWrite'))
    ex_forwarding.set_value('MEM/WB.rd', MEMWB_pr.get_value('RegisterRd'))
    ex_forwarding.set_value('EX/MEM.rd', EXMEM_pr.get_value('RegisterRd'))
    ex_forwarding.calculate()

    EX_a_mux.set_control_value(ex_forwarding.get_value('ForwardA'))
    EX_b_mux.set_control_value(ex_forwarding.get_value('ForwardB'))

    EX_a_mux.set_value(0, IDEX_pr.get_value('Register1'))
    EX_b_mux.set_value(0, IDEX_pr.get_value('Register2'))
    EX_a_mux.set_value(1, EXMEM_pr.get_value('ALUResult'))
    EX_b_mux.set_value(1, EXMEM_pr.get_value('ALUResult'))
    EX_a_mux.set_value(2, MemtoReg_mux.get_value())
    EX_b_mux.set_value(2, MemtoReg_mux.get_value())
    EX_a_mux.calculate()
    EX_b_mux.calculate()

    alu.set_value(0, EX_a_mux.get_value())
    ALUSrc_mux.set_value(0, EX_b_mux.get_value())
    ALUSrc_mux.calculate()
    alu.set_value(1, ALUSrc_mux.get_value())
    alu.calculate()
    EXMEM_pr.set_value('ALUResult', alu.get_value())
    EXMEM_pr.set_value('Operand2', EX_b_mux.get_value())

    instruction = IFID_pr.get_value('Instruction')
    rs = (0b00000011111000000000000000000000 & instruction) >> 21
    rt = (0b00000000000111110000000000000000 & instruction) >> 16

run = True
while run:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == pygame.KEYDOWN:
            if ev.key == pygame.K_ESCAPE:
                run = False
            elif ev.key == pygame.K_RIGHT:
                next_cycle()
        elif ev.type == pygame.MOUSEBUTTONUP:
            mouse = pygame.mouse.get_pos()
            print(mouse)
            if cycle_button.mouse_on(*mouse):
                next_cycle()
    screen.fill(COLOR_BACK)
    mouse = pygame.mouse.get_pos()

    for line in lines:
        line.draw(screen)
    for obj in sorted(objs, key=lambda x: x.mouse_on(*mouse)):
        obj.draw(screen, mouse)
    pygame.display.update()

