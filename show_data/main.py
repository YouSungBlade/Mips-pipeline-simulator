import pygame
from const import *
from assembler import Assembler
from show_data import show_format

def init_registers():
    register_memory = [0] * 32
    # $sp 는 0x7ffffe40, $gp 는 0x10008000 초기화
    register_memory[29] = 0x7ffffe40
    register_memory[28] = 0x10008000
    return register_memory


assembler = Assembler('./test.s')
memory = assembler.get_memory()
reg = init_registers()

show_data = show_format.ShowData(1000, 1000)
show_data.set_memory(memory)
show_data.set_reg(reg)
print(len(show_data.reg))

for i in show_data.memory_order:
    print(show_data.read_four_words(i))


pygame.init()
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
clock = pygame.time.Clock()



objs = []
objs.append(show_data)

run = True
while run:
    clock.tick(30)
    for ev in pygame.event.get():
        if ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE:
            run = False

    screen.fill(COLOR_BACK)
    mouse = pygame.mouse.get_pos()

    for obj in objs:
        obj.draw(screen, mouse)
    pygame.display.update()