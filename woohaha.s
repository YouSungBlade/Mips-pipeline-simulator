.data 0x10008000
.word 0x00000010, 0x00000004
.asciiz "test"
.asciiz "majunyoung"
.asciiz "parkgeonwoo"
.asciiz "hyesung"
.data 0x11541234
.word 0x01134678
.byte 0x12
.byte 0x37
.byte 0x10

.text 0x00400024
main:

lw $16, 0($gp)          # $16 = 0x00000010
lw $4, 4($gp)           # $4  = 0x00000004

slt $1, $16, $4         # $1 = $16 < $4

beq $1, $0, m           # branch when $16 is bigger

or $16, $16, $16        # no execute

m:                         
sub $16, $16, $4           # $16 = $16 - 4
slt $1, $16, $4            # $1 = $16 < 4
sw $4, 0($16)              # sw $4 to $16
beq $1, $0, m              # loop while $16 >= $4

j L                        # jump to L

add $16, $4, $0            # no execute

L:
and $16, $16, $0           # $16 = 0