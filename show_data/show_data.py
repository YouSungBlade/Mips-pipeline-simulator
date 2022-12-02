import pygame
from const import *

class ShowData:
    def __init__(self):
        self.reg_alias = ['r0', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 's0', 's1',
             's2', 's3', 's4', 's5', 's6', 's7', 't8', 't9', 'k0', 'k1', 'gp', 'sp', 's8', 'ra']

        self.reg = []

        self.memory = {}
        self.memory_order = []

        self.color = (255, 255, 255)

    def set_reg(self, reg):
        self.reg = reg

    def set_memory(self, memory):
        self.memory = memory

        key_set = set()
        for idx in memory.keys():
            key_set.add(idx - (idx % 16))

        self.memory_order = sorted(list(key_set))

    def read_endian(self, address):
        res = 0

        for i in range(0, 4):
            if address in self.memory.keys():
                num = self.memory[address]
            else:
                num = 0
            res += (0xFF & num) << 8 * i
            address += 1
        return res

    def convert_int_to_hex(self, integer):
        return format(integer, '#0' + str(10) + 'x')

    def convert_word_to_ascii(self, hex_num):
        hex_num = hex_num[2:]
        res = ''
        for i in range(0, 8, 2):
            str = int("0x"+hex_num[i:i+2], 16)
            res += chr(str) if 32 < str < 127 else '.'

        return res

    def read_four_words(self, address):
        res = '[' + self.convert_int_to_hex(address)[2:] +'] '
        str_list = []
        for i in range(0, 4):
            data = self.read_endian(address + 4*i)
            hex_data = self.convert_int_to_hex(data)
            res += ' '+ hex_data[2:]
            str_list.append(self.convert_word_to_ascii(hex_data)[::-1])

        res += '     '+ ' '.join(str_list)
        return res

    def draw_reg(self, screen, x, y):
        color = (190, 255, 170)
        pygame.draw.rect(screen, color, [x, y-10, 230, 980])

        font = pygame.font.SysFont('consolas', FONT_SIZE_L, True)
        for idx, alias in enumerate(self.reg_alias):
            str_idx = str(idx)+' ' if len(str(idx)) == 1 else str(idx)
            value = font.render('R'+str_idx+'['+alias+ ']'+'='+self.convert_int_to_hex(self.reg[idx]), True, COLOR_BLACK)
            value_rect = value.get_rect(midleft=(x, y + idx*(FONT_SIZE_L+10)+10))
            screen.blit(value, value_rect)

    def draw_memory(self, screen, x, y):
        color = (190, 255, 170)

        pygame.draw.rect(screen, color, [x+600, y+180, 860, (len(self.memory_order)*(FONT_SIZE_L+10))+10])

        font = pygame.font.SysFont('consolas', FONT_SIZE_L, True)
        for idx, value in enumerate(self.memory_order):
            value = font.render(self.read_four_words(value), True,
                                COLOR_BLACK)
            value_rect = value.get_rect(midleft=(x+600, y + idx * (FONT_SIZE_L + 10) + 200))
            screen.blit(value, value_rect)