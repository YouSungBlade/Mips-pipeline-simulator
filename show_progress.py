import pygame
from const import *

class ShowProgress:
    def __init__(self, x, y):
        self.stage_list = ['IF', 'ID', 'EX', 'MEM', 'WB']
        self.display_list = ['nop'] * 5
        self.x = x
        self.y = y
        self.offset = 45
        self.center_pos = (0, 0)
        self.color_list = [(255, 51, 51), (204, 0, 0), (254,102,102),
                           (204, 102, 102), (153, 102, 52)]
        self.clock = 0

    def next_cycle(self, instruction, data_hazard, control_hazard):
        self.clock += 1
        if self.display_list.count('nop') != 5 and data_hazard:
            self.display_list.insert(2, 'nop')
        else:
            self.display_list.insert(0, instruction)
            if control_hazard:
                self.display_list[1] = 'nop'
        if len(self.display_list) > 5:
            self.display_list.pop()

    #스테이지에 위치한 instruction을 NOP로 바꾼다
    def change_instruction_to_nop(self, stage):
        idx = self.stage_list.index(stage)
        self.display_list[idx] = 'nop'
    
    def data_hazard(self):
        self.display_list.insert(2, 'nop')

    def control_hazard(self):
        self.display_list.insert(1, 'nop')

    def draw_stage(self, screen):
        pygame.draw.rect(screen, COLOR_BLACK, [self.x-self.offset, self.y, self.offset*6, 100], 3)
        self.center_pos = (self.x + self.offset*3, 50)

    def draw_inst(self, screen):
        font = pygame.font.SysFont('consolas', FONT_SIZE_L, True)
        for idx, value in enumerate(self.display_list):
            value = font.render(value, True, (255, 0, 120))
            value_rect = value.get_rect(center=(self.x+idx*self.offset, self.y+70))
            screen.blit(value, value_rect)

        for idx, value in enumerate(self.stage_list):
            value = font.render(value, False, COLOR_BLACK)
            value_rect = value.get_rect(center=(self.x+idx*self.offset, self.y+(self.offset/2)))
            screen.blit(value, value_rect)

    def draw_clock(self, screen):
        font = pygame.font.SysFont('consolas', FONT_SIZE_L+self.offset//2, True)
        value = font.render('CC : ' + str(self.clock), True, COLOR_RED)
        value_rect = value.get_rect(center=(self.x+self.offset*2, self.y-self.offset))
        screen.blit(value, value_rect)

    def draw(self, screen):
        self.draw_clock(screen)
        self.draw_inst(screen)
        self.draw_stage(screen)

if __name__ == '__main__':
    show_progress = ShowProgress(3, 5)
    lst = ['add', 'sub', 'slt', 'and', 'beq', 'sub', 'slt']

    display_lst = []
    for inst in lst:
        if len(display_lst) > 5:
            display_lst.pop()
        display_lst.insert(0, inst)
        print(display_lst)


