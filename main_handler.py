import pygame
from interactive_rect import PipelineRegister, ProgramCounter, InstructionMemory, RegisterMemory, DataMemory
from interactive_ellipse import ConcatUnit, EqualUnit, ShiftLeft, SignExtension
from interactive_roundrect import ALUControlUnit, ControlUnit, ExForwarding, IdForwarding, HazardDetection
from interactive_trapezoid import SimpleAdder, ALU
from multiplexer import Multiplexer
from logic_gate import AndGate, OrGate
from show_data import ShowData
from show_progress import ShowProgress
from assembler import Assembler
from const import *
from lines import *
from PyQt5.QtWidgets import QApplication, QFileDialog

app = QApplication([])
filename, _ = QFileDialog.getOpenFileName(
    None,
    "Open File", "","Assembly Source Code (*.s)",
    )

assembler = Assembler(filename)
assembler.assemble()

pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()

show_progress = ShowProgress(190, 850) #생성
show_data = ShowData() #생성

adder_pc = SimpleAdder(400, 300, 30, 60)
adder_pc.set_inputs([(16, 8), (16, 1)])
adder_pc.set_value(1, 4)
adder_branch = SimpleAdder(800, 380, 30, 60)
adder_branch.set_inputs([(16, 8),(16, 8)])

concat = ConcatUnit(635, 318, 50, 50)
pc = ProgramCounter(220, 455, 50, 70)
pc.set_control_value(1)
pc.set_value(0x00400024)
pc.calculate()

IFID_pr = PipelineRegister(550, 260, 50, 670, 'IF/ID')
IDEX_pr = PipelineRegister(1050, 230, 50, 700, 'ID/EX')
EXMEM_pr = PipelineRegister(1400, 230, 50, 700, 'EX/MEM')
MEMWB_pr = PipelineRegister(1700, 230, 50, 700, 'MEM/WB')

labels = [
    ('NextPC', 1, 16, 8),
    ('Instruction', 3, 16, 8)
]
IFID_pr.set_inputs(labels)
IFID_pr.set_control('IF/IDWrite', 2, 1)

labels = [
    ('RegWrite', 1, 2, 1), 
    ('MemtoReg', 1, 2, 1), 
    ('MemWrite', 1, 2, 1),
    ('MemRead', 1, 2, 1),
    ('RegDst', 1, 2, 1), 
    ('ALUOp', 1, 2, 2),
    ('ALUSrc', 1, 2, 1),
    ('Register1', 9.5, 16, 8), 
    ('Register2', 6.5, 16, 8), 
    ('Extended', 3, 16, 8), 
    ('Rs', 3, 2, 5), 
    ('Rt', 3, 2, 5), 
    ('Rd', 3, 2, 5)
]
IDEX_pr.set_inputs(labels)

labels = [
    ('RegWrite', 0.5, 2, 1),
    ('MemtoReg', 0.5, 2, 1),
    ('MemWrite', 0.5, 2, 1),
    ('MemRead', 0.5, 2, 1),   
    ('ALUResult', 4, 16, 8),
    ('Operand2', 4, 16, 8),
    ('RegisterRd', 3.5, 2, 5)
]
EXMEM_pr.set_inputs(labels)

labels = [
    ('RegWrite', 1, 2, 1),
    ('MemtoReg', 1, 2, 1),
    ('MemData', 3, 16, 8),
    ('ALUResult', 3, 16, 8),
    ('RegisterRd', 2, 2, 5)
]
MEMWB_pr.set_inputs(labels)

instruction_memory = InstructionMemory(340, 400, 150, 150)
instruction_memory.init_memory(assembler.get_instructions())
register_memory = RegisterMemory(780, 600, 120, 150)
data_memory = DataMemory(1500, 430, 150, 150)
data_memory.init_memory(assembler.get_memory())


# mux

pc_mux = Multiplexer(160, 450, 30, 80)
pc_mux.set_inputs([1, 0])
pc_mux.set_control(2, 1, top=True)
pc_mux.set_form(16, 8)

branch_mux = Multiplexer(105, 470, 30, 80)
branch_mux.set_inputs([0, 1])
branch_mux.set_control(2, 1, top=True)
branch_mux.set_form(16, 8)

RegDst_mux = Multiplexer(1140, 820, 30, 80)
RegDst_mux.set_inputs([0, 1])
RegDst_mux.set_control(2, 1, top=True)
RegDst_mux.set_form(2, 5)

control_mux = Multiplexer(950, 270, 30, 80)
control_mux.set_inputs([1, 0])
control_mux.set_control(2, 1, top=True)
control_mux.set_form(2, 9)

ID_a_mux = Multiplexer(930, 585, 30, 80)
ID_a_mux.set_inputs([0, 1])
ID_a_mux.set_control(2, 1, top=False)
ID_a_mux.set_form(16, 8)

ID_b_mux = Multiplexer(930, 685, 30, 80)
ID_b_mux.set_inputs([0, 1])
ID_b_mux.set_control(2, 1, top=False)
ID_b_mux.set_form(16, 8)

EX_a_mux = Multiplexer(1170, 420, 30, 80)
EX_a_mux.set_inputs([0, 1 ,2])
EX_a_mux.set_control(2, 2, top=False)
EX_a_mux.set_form(16, 8)

EX_b_mux = Multiplexer(1170, 530, 30, 80)
EX_b_mux.set_inputs([0, 1, 2])
EX_b_mux.set_control(2, 2, top=False)
EX_b_mux.set_form(16, 8)

ALUSrc_mux = Multiplexer(1220, 560, 30, 80)
ALUSrc_mux.set_inputs([0, 1])
ALUSrc_mux.set_control(2, 1, top=True)
ALUSrc_mux.set_form(16, 8)

MemtoReg_mux = Multiplexer(1800, 500, 30, 80)
MemtoReg_mux.set_inputs([1, 0])
MemtoReg_mux.set_control(2, 1, top=True)
MemtoReg_mux.set_form(16, 8)

instruction_mux = Multiplexer(450, 600, 30, 80)
instruction_mux.set_inputs([0, 1])
instruction_mux.set_control(2, 1, top=False)
instruction_mux.set_form(16, 8)

alu = ALU(1300, 450, 50, 100)

hazard_detection = HazardDetection(630, 60, 250, 100)
hazard_detection.calculate()

and_gate = AndGate(1010, 120, 30, 40)
or_gate = OrGate(400, 120, 40, 30)

sign_extension = SignExtension(655, 695, 50, 50)
shift_left_jump = ShiftLeft(650, 450, 50, 50)
shift_left_branch = ShiftLeft(730, 450, 50, 50)
equal = EqualUnit(960, 655, 40, 40)

ex_forwarding = ExForwarding(1210, 880, 150, 100)
id_forwarding = IdForwarding(850, 880, 150, 100)

control = ControlUnit(705, 230, 140, 130)
alu_control = ALUControlUnit(1230, 700, 150, 100)
alu_control.calculate()

objs = []
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
objs.append(or_gate)
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
objs.append(instruction_mux)

lines = []
lines.append(OneCornerLine(MEMWB_pr.get_output_pos('MemtoReg'), MemtoReg_mux.get_control_pos(), True))
lines.append(TwoCornerLine(MEMWB_pr.get_output_pos('MemData'), MemtoReg_mux.get_input_pos(0), 1770, True))
lines.append(TwoCornerLine(MEMWB_pr.get_output_pos('ALUResult'), MemtoReg_mux.get_input_pos(1), 1770, True))
lines.append(FourCornerLine(MemtoReg_mux.get_output_pos(), register_memory.get_input_pos('WriteData'), (755, 1050), 1850, True, False))
lines.append(FourCornerLine(MEMWB_pr.get_output_pos('RegisterRd'), register_memory.get_input_pos('WriteRegister'), (740, 1065), 1770, True, False))
lines.append(ThreeCornerLine(MEMWB_pr.get_output_pos('RegWrite'), register_memory.get_control_pos(), (1785, 1035), True, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('RegWrite'), MEMWB_pr.get_input_pos('RegWrite'), 1665, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('MemtoReg'), MEMWB_pr.get_input_pos('MemtoReg'), 1650, True))
lines.append(OneCornerLine(EXMEM_pr.get_output_pos('MemWrite'), data_memory.get_contol_pos('MemWrite'), True))
lines.append(ThreeCornerLine(EXMEM_pr.get_output_pos('MemRead'), data_memory.get_contol_pos('MemRead'), (1491, 620), True, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('ALUResult'), data_memory.get_input_pos('Address'), 1467, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('Operand2'), data_memory.get_input_pos('WriteData'), 1456, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('RegisterRd'), MEMWB_pr.get_input_pos('RegisterRd'), 1600, True))
lines.append(TwoCornerLine(EXMEM_pr.get_output_pos('ALUResult'), MEMWB_pr.get_input_pos('ALUResult'), 1467, True))
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
lines.append(TwoCornerLine(ex_forwarding.get_output_pos('ForwardB'), EX_b_mux.get_control_pos(), 848, False))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Register1'), EX_a_mux.get_input_pos(0), 1145, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('Register2'), EX_b_mux.get_input_pos(0), 1145, True))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('ALUResult'), EX_a_mux.get_input_pos(2), (1133, 990), 1467, True, False))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('ALUResult'), EX_b_mux.get_input_pos(2), (1133, 990), 1467, True, False))
lines.append(FourCornerLine(MemtoReg_mux.get_output_pos(), EX_a_mux.get_input_pos(1), (1125, 1050), 1850, True, False))
lines.append(FourCornerLine(MemtoReg_mux.get_output_pos(), EX_b_mux.get_input_pos(1), (1125, 1050), 1850, True, False))
lines.append(TwoCornerLine(EX_a_mux.get_output_pos(), alu.get_input_pos(0), 1270, True))
lines.append(TwoCornerLine(EX_b_mux.get_output_pos(), ALUSrc_mux.get_input_pos(0), 1210, True))
lines.append(TwoCornerLine(ALUSrc_mux.get_output_pos(), alu.get_input_pos(1), 1280, True))
lines.append(TwoCornerLine(alu.get_output_pos(), EXMEM_pr.get_input_pos('ALUResult'), 1370, True))
lines.append(FourCornerLine(EX_b_mux.get_output_pos(), EXMEM_pr.get_input_pos('Operand2'), (1265, 540), 1210, True, False))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), control.get_input_pos('Instruction'), 620, True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), register_memory.get_input_pos('ReadRegister1'), 620, True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), register_memory.get_input_pos('ReadRegister2'), 620, True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), IDEX_pr.get_input_pos('Rs'), 620, True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), IDEX_pr.get_input_pos('Rt'), 620, True))
lines.append(FourCornerLine(IFID_pr.get_output_pos('Instruction'), IDEX_pr.get_input_pos('Rd'), (1035, 860), 620, True, False))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('RegWrite'), id_forwarding.get_input_pos('EX/MEM.RegWrite'), (1015, 1020), 1665, True, False))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('RegisterRd'), id_forwarding.get_input_pos('EX/MEM.rd'), (1025, 1005), 1500, True, False))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), id_forwarding.get_input_pos('IF/ID.rs'), 620, True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), id_forwarding.get_input_pos('IF/ID.rt'), 620, True))
lines.append(FourCornerLine(control.get_output_pos('Branch'), id_forwarding.get_input_pos('Branch'), (770, 565), 870, True, False))
lines.append(TwoCornerLine(register_memory.get_output_pos('ReadData1'), ID_a_mux.get_input_pos(0), 905, True))
lines.append(TwoCornerLine(register_memory.get_output_pos('ReadData2'), ID_b_mux.get_input_pos(0), 905, True))
lines.append(FourCornerLine(id_forwarding.get_output_pos('ForwardA'), ID_a_mux.get_control_pos(), (922, 680), 825, False, True))
lines.append(TwoCornerLine(id_forwarding.get_output_pos('ForwardB'), ID_b_mux.get_control_pos(), 825, False))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('ALUResult'), ID_a_mux.get_input_pos(1), (913, 205), 1467, True, False))
lines.append(FourCornerLine(EXMEM_pr.get_output_pos('ALUResult'), ID_b_mux.get_input_pos(1), (913, 205), 1467, True, False))
lines.append(TwoCornerLine(ID_a_mux.get_output_pos(), IDEX_pr.get_input_pos('Register1'), 995, True))
lines.append(TwoCornerLine(ID_b_mux.get_output_pos(), IDEX_pr.get_input_pos('Register2'), 1015, True))
lines.append(OneCornerLine(ID_a_mux.get_output_pos(), equal.get_input_pos(0), True))
lines.append(OneCornerLine(ID_b_mux.get_output_pos(), equal.get_input_pos(1), True))
lines.append(OneCornerLine(equal.get_output_pos(), and_gate.get_input_pos(1), True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), id_forwarding.get_input_pos('IF/ID.rs'), 620, True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), sign_extension.get_input_pos(), 620, True))
lines.append(FourCornerLine(sign_extension.get_output_pos(), IDEX_pr.get_input_pos('Extended'), (1030, 805), 720, True, False))
lines.append(ThreeCornerLine(sign_extension.get_output_pos(), shift_left_branch.get_input_pos(), (720, 540), True, True))
lines.append(OneCornerLine(shift_left_branch.get_output_pos(), adder_branch.get_input_pos(1), False))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('NextPC'), adder_branch.get_input_pos(0), 610, True))
lines.append(ThreeCornerLine(IFID_pr.get_output_pos('Instruction'), shift_left_jump.get_input_pos(), (620, 545), True, True))
lines.append(TwoCornerLine(shift_left_jump.get_output_pos(), concat.get_input_pos(1), 425, False))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('NextPC'), concat.get_input_pos(0), 610, True))
for name in ['Branch', 'RegWrite', 'MemtoReg', 'MemWrite', 'MemRead', 'RegDst', 'ALUOp', 'ALUSrc']:
    lines.append(TwoCornerLine(control.get_output_pos(name), control_mux.get_input_pos(0), 890, True))
lines.append(ThreeCornerLine(control.get_output_pos('Branch'), hazard_detection.get_input_pos('Branch'), (870, 190), True, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('MemRead'), hazard_detection.get_input_pos('ID/EX.MemRead'), 1200, True))
lines.append(TwoCornerLine(IDEX_pr.get_output_pos('RegWrite'), hazard_detection.get_input_pos('ID/EX.RegWrite'), 1175, True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), hazard_detection.get_input_pos('IF/ID.rs'), 620, True))
lines.append(TwoCornerLine(IFID_pr.get_output_pos('Instruction'), hazard_detection.get_input_pos('IF/ID.rt'), 620, True))
lines.append(ThreeCornerLine(IDEX_pr.get_output_pos('Rt'), hazard_detection.get_input_pos('ID/EX.rt'), (1115, 170), True, True))
lines.append(ThreeCornerLine(IDEX_pr.get_output_pos('Rd'), hazard_detection.get_input_pos('ID/EX.rd'), (1107, 180), True, True))
lines.append(OneCornerLine(hazard_detection.get_output_pos('ControlMUX'), control_mux.get_control_pos(), True))
lines.append(OneCornerLine(control_mux.get_output_pos(), and_gate.get_input_pos(0), True))
for name in ['RegWrite', 'MemtoReg', 'MemWrite', 'MemRead', 'RegDst', 'ALUOp', 'ALUSrc']:
    lines.append(TwoCornerLine(control_mux.get_output_pos(), IDEX_pr.get_input_pos(name), 1013, True))
lines.append(TwoCornerLine(and_gate.get_output_pos(), branch_mux.get_control_pos(), 15, False))
lines.append(FourCornerLine(adder_branch.get_output_pos(), branch_mux.get_input_pos(1), (60, 215), 930, True, False))
lines.append(OneCornerLine(hazard_detection.get_output_pos('PCWrite'), pc.get_control_pos(), True))
lines.append(ThreeCornerLine(control.get_output_pos('Jump'), pc_mux.get_control_pos(), (860, 200), True, True))
lines.append(TwoCornerLine(pc.get_output_pos(), adder_pc.get_input_pos(0), 305, True))
lines.append(FourCornerLine(adder_pc.get_output_pos(), branch_mux.get_input_pos(0), (85, 250), 450, True, False))
lines.append(TwoCornerLine(adder_pc.get_output_pos(), IFID_pr.get_input_pos('NextPC'), 450, True))
lines.append(TwoCornerLine(branch_mux.get_output_pos(), pc_mux.get_input_pos(1), 150, True))
lines.append(ThreeCornerLine(concat.get_output_pos(), pc_mux.get_input_pos(0), (145, 180), False, False))
lines.append(TwoCornerLine(pc_mux.get_output_pos(), pc.get_input_pos(), 205, True))
lines.append(TwoCornerLine(pc.get_output_pos(), instruction_memory.get_input_pos(), 320, True))
lines.append(OneCornerLine(hazard_detection.get_output_pos('IF/IDWrite'), IFID_pr.get_control_pos(), True))
lines.append(ThreeCornerLine(and_gate.get_output_pos(), or_gate.get_input_pos(0), (505, 15), False, False))
lines.append(FourCornerLine(control.get_output_pos('Jump'), or_gate.get_input_pos(1), (505, 200), 860, True, False))
lines.append(FourCornerLine(instruction_memory.get_output_pos('Decoded'), instruction_mux.get_input_pos(0), (420, 580), 520, True, False))
lines.append(ThreeCornerLine(or_gate.get_output_pos(), instruction_mux.get_control_pos(), (290, 700), True, True))
lines.append(TwoCornerLine(instruction_mux.get_output_pos(), IFID_pr.get_input_pos('Instruction'), 515, True))
lines.append(ThreeCornerLine(EXMEM_pr.get_output_pos('MemRead'), hazard_detection.get_input_pos('EX/MEM.MemRead'), (1491, 32), True, True))
lines.append(ThreeCornerLine(EXMEM_pr.get_output_pos('RegisterRd'), hazard_detection.get_input_pos('EX/MEM.RegisterRd'), (1480, 46), True, True))


split_points = [
    (306, 491), (611, 344), (621, 679), (621, 657), (621, 619), (621, 546), (621, 296), (621, 141), (621, 721), (621, 781), (621, 841), (621, 861),
    (621, 931), (721, 721), (451, 331), (871, 257), (1014, 241), (1014, 301), (1014, 281), (1014, 261), (1014, 321), (1014, 341), (981, 626), (981, 726),
    (506, 16), (506, 201), (1201, 301), (1211, 721), (1116, 841), (1108, 881), (1211, 571), (1666, 266), (1666, 976), (1468, 438), (1468, 686), (1126, 571),
    (914, 646), (1501, 840), (1501, 951), (1786, 961), (1771, 941), (1134, 597), (1126, 1051), (1176, 241), (1492, 321), (1481, 840), (1468, 451)
]

texts = [
    ('4', FONT_SIZE_S, COLOR_BLACK, (390, 345)),
    ('0', FONT_SIZE_S, COLOR_BLACK, (942, 330)),
    ('nop', FONT_SIZE_S, COLOR_BLACK, (436, 660)),
    ('IF.Flush', FONT_SIZE_S, COLOR_BLUE, (345, 124))
]

def next_cycle():
    pc.calculate()
    instruction_memory.set_value(pc.get_value())
    instruction_memory.calculate()
    show_progress.next_cycle(
        instruction=instruction_memory.get_value("Fetched").split()[0],
        data_hazard=not hazard_detection.get_value('ControlMUX'),
        control_hazard=or_gate.get_value()
    )
    
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
    EX_a_mux.set_value(1, MemtoReg_mux.get_value())
    EX_b_mux.set_value(1, MemtoReg_mux.get_value())
    EX_a_mux.set_value(2, EXMEM_pr.get_value('ALUResult'))
    EX_b_mux.set_value(2, EXMEM_pr.get_value('ALUResult'))
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
    rd = (0b00000000000000001111100000000000 & instruction) >> 11
    immediate = (0xFFFF & instruction)
    jump_address = (0b00000011111111111111111111111111 & instruction)

    control.set_value('Instruction', instruction)
    control.calculate()
    register_memory.set_value('ReadRegister1', rs)
    register_memory.set_value('ReadRegister2', rt)
    register_memory.calculate('Read')
    IDEX_pr.set_value('Rs', rs)
    IDEX_pr.set_value('Rt', rt)
    IDEX_pr.set_value('Rd', rd)

    id_forwarding.set_value('EX/MEM.rd', EXMEM_pr.get_value('RegisterRd'))
    id_forwarding.set_value('EX/MEM.RegWrite', EXMEM_pr.get_value('RegWrite'))
    id_forwarding.set_value('IF/ID.rs', rs)
    id_forwarding.set_value('IF/ID.rt', rt)
    id_forwarding.set_value('Branch', control.get_value('Branch'))
    id_forwarding.calculate()

    ID_a_mux.set_value(0, register_memory.get_value('ReadData1'))
    ID_b_mux.set_value(0, register_memory.get_value('ReadData2'))
    ID_a_mux.set_control_value(id_forwarding.get_value('ForwardA'))
    ID_b_mux.set_control_value(id_forwarding.get_value('ForwardB'))
    ID_a_mux.set_value(1, EXMEM_pr.get_value('ALUResult'))
    ID_b_mux.set_value(1, EXMEM_pr.get_value('ALUResult'))
    ID_a_mux.calculate()
    ID_b_mux.calculate()

    IDEX_pr.set_value('Register1', ID_a_mux.get_value())
    IDEX_pr.set_value('Register2', ID_b_mux.get_value())
    equal.set_value(0, ID_a_mux.get_value())
    equal.set_value(1, ID_b_mux.get_value())
    equal.calculate()
    and_gate.set_value(1, equal.get_value())

    sign_extension.set_value(immediate)
    sign_extension.calculate()
    IDEX_pr.set_value('Extended', sign_extension.get_value())

    shift_left_branch.set_value(sign_extension.get_value())
    shift_left_branch.calculate()
    adder_branch.set_value(1, shift_left_branch.get_value())
    adder_branch.set_value(0, IFID_pr.get_value('NextPC'))
    adder_branch.calculate()

    shift_left_jump.set_value(jump_address)
    shift_left_jump.calculate()
    
    concat.set_value(1, shift_left_jump.get_value())
    concat.set_value(0, IFID_pr.get_value('NextPC') >> 28)
    concat.calculate()

    branch = control.get_value('Branch') << 8
    reg_write = control.get_value('RegWrite') << 7
    mem_to_reg = control.get_value('MemtoReg') << 6
    mem_write = control.get_value('MemWrite') << 5
    mem_read = control.get_value('MemRead') << 4
    reg_dst = control.get_value('RegDst') << 3
    alu_op = control.get_value('ALUOp') << 1
    alu_src = control.get_value('ALUSrc')
    control_mux.set_value(0, branch | reg_write | mem_to_reg | mem_write | mem_read | reg_dst | alu_op | alu_src)

    hazard_detection.set_value('Branch', control.get_value('Branch'))
    hazard_detection.set_value('ID/EX.MemRead', IDEX_pr.get_value('MemRead'))
    hazard_detection.set_value('ID/EX.RegWrite', IDEX_pr.get_value('RegWrite'))
    hazard_detection.set_value('IF/ID.rs', rs)
    hazard_detection.set_value('IF/ID.rt', rt)
    hazard_detection.set_value('EX/MEM.MemRead', EXMEM_pr.get_value('MemRead'))
    hazard_detection.set_value('EX/MEM.RegisterRd', EXMEM_pr.get_value('RegisterRd'))
    hazard_detection.set_value('ID/EX.rt', IDEX_pr.get_value('Rt'))
    hazard_detection.set_value('ID/EX.rd', IDEX_pr.get_value('Rd'))
    hazard_detection.calculate()

    control_mux.set_control_value(hazard_detection.get_value('ControlMUX'))
    control_mux.calculate()
    control_bundle = control_mux.get_value()
    and_gate.set_value(0, control_bundle >> 8)
    IDEX_pr.set_value('RegWrite', (control_bundle & 0b010000000) >> 7)
    IDEX_pr.set_value('MemtoReg', (control_bundle & 0b001000000) >> 6)
    IDEX_pr.set_value('MemWrite', (control_bundle & 0b000100000) >> 5)
    IDEX_pr.set_value('MemRead', (control_bundle & 0b000010000) >> 4)
    IDEX_pr.set_value('RegDst', (control_bundle & 0b000001000) >> 3)
    IDEX_pr.set_value('ALUOp', (control_bundle & 0b000000110) >> 1)
    IDEX_pr.set_value('ALUSrc', control_bundle & 0b000000001)
    and_gate.calculate()
    
    pc.set_control_value(hazard_detection.get_value('PCWrite'))
    branch_mux.set_control_value(and_gate.get_value())
    branch_mux.set_value(1, adder_branch.get_value())
    pc_mux.set_value(0, control.get_value('Jump'))
    adder_pc.set_value(0, pc.get_value())
    adder_pc.calculate()

    branch_mux.set_value(0, adder_pc.get_value())
    branch_mux.calculate()
    IFID_pr.set_value('NextPC', adder_pc.get_value())
    pc_mux.set_value(1, branch_mux.get_value())
    pc_mux.set_value(0, concat.get_value())
    pc_mux.calculate()

    pc.set_value(pc_mux.get_value())
    IFID_pr.set_control_value(hazard_detection.get_value('IF/IDWrite'))

    or_gate.set_value(0, and_gate.get_value())
    or_gate.set_value(1, control.get_value('Jump'))
    or_gate.calculate()

    instruction_mux.set_value(0, instruction_memory.get_value('Decoded'))
    instruction_mux.set_control_value(or_gate.get_value())
    instruction_mux.calculate()
    IFID_pr.set_value('Instruction', instruction_mux.get_value())


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
    
    screen.fill(COLOR_BACK)
    mouse = pygame.mouse.get_pos()

    show_progress.draw(screen) #clock

    for line in lines:
        line.draw(screen)
    for text, size, color, pos in texts:
        font = pygame.font.SysFont(FONT, size, True)
        textbox = font.render(text, True, color)
        textbox_rect = textbox.get_rect(center=pos)
        screen.blit(textbox, textbox_rect)

    for point in split_points:
        pygame.draw.circle(screen, COLOR_BLACK, point, 4, 0)
    for obj in sorted(objs, key=lambda x: x.mouse_on(*mouse)):
        obj.draw(screen, mouse)

    

    if data_memory.mouse_on(*mouse):
        show_data.set_memory(data_memory.get_memory_data())
        show_data.draw_memory(screen, -55, 50)
    if register_memory.mouse_on(*mouse):
        show_data.set_reg(register_memory.get_registers())
        show_data.draw_reg(screen, 400, 50)

    pygame.display.update()

