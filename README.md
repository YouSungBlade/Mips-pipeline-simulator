# < MIPS PIPELINE SIMULATOR > 
![mainScreen](https://user-images.githubusercontent.com/103012667/207578677-d2555598-2fe3-4405-8a2e-bb9999aedbf4.png)

# **팀원**

20191582 김혜성, 20191588 마준영, 20191591 박근우

# **실행환경, 실행방법**

실행환경 : Python (Version : 3.10), Visual Studio Code, Python Modul pygame,
PyQt5  
실행방법 :   
1. github 주소에서 zipfile을 자신이 지정한 local에 저장  

2. file 폴더의 gitbash 혹은 명령 프로그램 실행

3. 아래의 명령어로 다운로드
```console
pip install PyQt5
```
```console
pip install pygame
```

4. ~.s 파일에 실행시킬 코드 작성

5. main_handler.py 실행

6. 실행 시킬 코드 선택


# **필수 기능**

- MIPS assembler 포함 (open source 사용 가능)

- pipeline visualization : 프로그램을 cycle 단위로 수행하고 정지된 상태에서  회로 상의 모든 component 입출력 값을 시각화 

- data/branch hazard 해결 ( j 명령의 hazard 도 해결해야 함)

- assemble 된 프로그램은 0x00400024 번지에 load 되고 PC 의 값은 이 값으로 초기화되어 수행이 시작됨.

- sp 는 0x7ffffe40, gp 는 0x10008000 로 초기화

- data memory 는 0으로 초기화하고 .data directive 의 내용에 따라 초기화

- memory 에는 OS code 가 없어도 됨

- memory 의 내용은 전체를 한꺼번에 보여줄 수 없으므로 적절한 방법으로 보여줄 것

- 프로그램의 종료 시점은 따로 정해지지 않음.                   

- exception handling 과 memory hierarchy 는 구현하지 않아도 됨

- visulaization 화면에는 클락 사이클을 0부터 카운트하여 몇번째 사이클인지 보여주는 화면이 포함되어야 함. 

- 프로그램 소스는 github 에서 download 받아 compile 하여 수행할 수 있는 형태로 공개되어야 함

- web service 형태로 구현하는 것도 가능, 이 경우에도 소스가 공개되어야 함

- github repository 에는 본 프로젝트에 대한 설명 (보고서를 대신함, 소스 코드 설명, 설치, 사용법 설명) 이 포함

# **기능** 
- .s파일을 assemble하여 simulator에 적용
- 사이클 단위 각 Component의 입력 값과 출력값 확인
- data hazard, load use hazard, branch hazard 지원
- forwarding
- 지원하는 명령어 : add, sub, and, or, lw, sw, beq, j

# **실행 종료 방법**
"esc" key 를 누른다

# **다음 Cycle 진행 방법**
오른쪽 방향키를 누르면 1 cycle 진행


# **Testcase**

(1)
```
.data 701
.word 0x12345678, 0x87654321
.byte 0x12, 0x34, 0x56, 0x78
.space 20
.half 0x09AB, 0xCDEF
.asciiz "star"
.byte 0x11
.word 0x32323232
.text
lw $s1, 0($gp)
beq $s1, $s2, L
add $s1, $s2, $s3
sub $s1, $s2, $s3
and $t1, $t3, $t8
L: or $s1, $s2, $s3
slt $s1, $s2, $s3  
```
(2)
```
.data  
.text  
main:  
lw $2, 4($3)  
beq $5, $6, L  
slt $6, $0, $1  
or $7, $8, $9  
add $8, $0, $9  

L: and $2, $8, $9
```
(3)
```
.data
.text
main:
lw $2, 4($3)  
sub $5, $3, $2
slt  $6, $2, $5
or   $7, $2, $6
and $2, $8, $
```

(4)
```
.data
.text
main:
add $2, $2, $4 
sub $5, $3, $2
slt  $6, $2, $5
or   $7, $2, $6
and $2, $8, $
```
(5) 
```
.data
.text
main:
L: lw $s1, 0($gp)  
beq $s1, $s2, L
add $s1, $s2, $s1
```
(6) 
```
.data 701
.word 0x12345678, 0x87654321
.byte 0x12, 0x34, 0x56, 0x78
.space 20
.half 0x09AB, 0xCDEF
.asciiz "star"
.byte 0x11
.word 0x32323232
.text
lw $s1, 0($gp)
beq $s2, $s3, L
L: add $t1, $t2, $t3
sub $t4, $t5, $t6
and $t5, $t7, $t8
```
(7) No Forwarding
```
.data 0x10008000
.word 0x00000001, 0x00000009
.text
main:
lw $1, 0($gp)
lw $2, 0($gp)
add $14, $1, $2
sw $14, 100($2)
```
(8) Double hazard
```
.data 0x10008000
.word 0x00000005, 0xffffffff
.text
main:
lw $2, 0($gp)
lw $3, 4($gp)
add $2, $3, $3
or $2, $3, $5
add $3, $2, $3
```
(9) Load-Use Data Hazard
```
.data 0x10008000
.word 0x0000000a, 0x00000003
.text
main:
lw $1, 0($gp)
lw $2, 4($gp)

slt $10, $1, $2
```
(10) MEM hazard
```
.data 0x10008000
.word 0x00000002, 0x00000001, 0x0000000d

.data
.text
main:
lw $2, 0($gp)
lw $3, 4($gp)
lw $12, 8($gp)
sub $2, $1, $3
and $12, $2, $3
or $1, $1, $2
sw $2, 100($gp)
```
(11) Stall for Branch Taken
```
.data 0x10008000
.word 0x00000002, 0x00000001

.text
main:
lw $2, 0($gp)
lw $1, 4($gp)
sub $2, $2, $1
beq $1, $2, m
add $2, $2, $1
m:
sub $2, $2, $1
```
(12) Stall for J

```
.data 0x10008000
.word 0x00000002, 0x00000001

.text
main:
lw $2, 0($gp)
lw $1, 4($gp)
j m
add $2, $2, $1
m:
sub $2, $2, $1
```

![image](https://user-images.githubusercontent.com/103012667/207578686-094d6042-a4fe-4984-910f-d7700d2bb7c8.png)
# Main_Handler
- pygame screen (1920*1080) 생성
- test.s 소스코드에서 data memory 초기화 및 instrution assemble
- components 생성 및 초기화 (datamemory, pipeline, hazard detection unit ...)
- line 객체 생성
- 모든 객체 draw
- components들의 input output 값을 연결
- 오른쪽 방향키로 next_cycle() 수행
- 1 cycle 진행함
- 각 스테이지별로 연산 수행 후 다음 파이프라인 레지스터에 값 저장 or 종료
- 좌측 하단에 클락 사이클과 스테이지별로 실행중인 instruction 출력
- 레지스터 메모리 mouse_on() = True 일 때 레지스터 값 출력
- 데이터 메모리 mouse_on() = True 일 때 메모리 값 출력

# Components
### Interactive_Rect
사각형 부모 클래스
- ### Pipeline Register
각 파이프라인 별로 해당하는 레지스터를 저장하고 calculate 실행시 input에 있는 값을 output으로 옮긴다.
- ### Instruction Memory
init_memory(instruction_memory)
인스트럭션 메모리 생성후 실행되며 다음과 같은 형식의 딕셔너리를 인자로 받아 멤버 변수에 저장한다. instruction memory = {{pc1 : instruction1}, {pc2: instruction2}...}
calculate() 함수 실행시에 해당하는 pc값 키값으로 instruction 메모리에서 찾고 키값이 존재하면 두 가지 output을 계산하는데, Decoded에 instruction을 16진수로 해석한 것을 저장하고 Fetched에는 instruction의 원본을 저장한다.
- ### Register Memory
init_registers() 함수가 Register Memory 생성시 실행되어 레지스터 값을 조건에 맞게 초기화한다.  레지스터는 모두 16진수 ((ex) 0x12345678) 형식을 갖추고 있다.
- calculate(flag) flag : {'Read', 'Write'}
- flag == 'Read'일 때,
각 레지스터 number인 Reg1와 Reg2에 해당하는 register 데이터 값을 읽어 output인 ReadData1 ReadData2에 저장한다.
- flag == 'Write'일 때,
control signal인 RegWrite 1이면,
write_reg에 해당하는 레지스터에 write_data 값을 저장한다. Write는 WB 스테이지보다 늦게 수행되도록 구현하여 Dependancy가 존재하더라도 포워딩이 필요하지 않다.
RegWrite값이 0이면 아무 일도 일어나지 않는다.
- ### Data Memory
- init_memory(memory
Data Memory 생성후 메모리를 초기화하는 함수이며 키값으로 주소값과 value로 데이터 값이 담긴 딕셔너리를 인자로 받는다. memory = {{'10008000' : 0x12345678}, {'100080004':0x87654321}}
- calculate()
control signal은 MemWrite와 MemRead 두 가지가 있다.
MemWrite == 1 일 때,
memory에 멤버변수 Address에 해당하는 주소의 값에 멤버변수 WriteData 값을 little_endian 형식으로 저장한다.
MemRead == 1 일 때,
멤버변수 Address에 해당하는 값을 메모리에서 찾아 little_endian 형식으로 데이터를 읽어서 output으로 저장한다.
컨트롤 시그널이 모두 0일 때는 아무 일도 일어나지 않는다.
- ### Program Counter
calculate() 함수 실행시,
control signal PCWrite 값이 1일 경우
멤버변수 input에 저장된 pc값을 멤버변수 output에 저장한다.
PCWrite 값이 0일 경우 아무 일도 일어나지 않는다.
### Interactive_ellipse
타원 부모 클래스
- ### Concat unit
PC의 상위 4비트와 left shift된 28 비트를 이어붙인다. jump instruction을 위해 사용됨.
- ### EqualUnit
- calculate()
멤버변수인 첫 번째 인풋 값과 두 번째 인풋 값이 같은지 비교하여 output 값에 부울변수로
저장한다.
- ### ShiftLeft
- calculate()
멤버변수인 인풋 값에 '2' 만큼 shift 연산한 뒤 0xFFFFFFFF와 and 연산을 하여 1 word 단위로 확장시킨다.
- ### SignExtension
- calculate()
- 인풋의 16번째 비트가 1일 때
    MSB 앞에 16비트를 모두 1을 이어붙여 1 word 단위로 SignExtension
- 인풋의 16번째 비트가 0일 때
    MSB 앞에 16비트를 모두 0으로 이어붙여 1 word 단위로 SignExtension
### InteractiveRoundRect
원 부모 클래스
- ### SignalUnit
- ### ALUControlUnit
멤버변수인 op와 funct field의 값을 받아 위 ALU Control 진리표에 해당하는 Operation값을 Output에 저장한다.
- ### ControlUnit
operation Field 6개의 비트를 받아 위 진리표 값에 알맞게 ControlSignal을 설정하여 output에 저장한다.
- ### ExForwarding
alu의 input의 두 레지스터를 연산하는 과정에서 Dependancy가 발생하면 forwarding을 결정
forwanrdA와 forwardB가 있음
- ### IdForwarding
beq instruction을 위해 두 레지스터의 값이 같은지 비교하는 과정에서 Dependancy가 발생하면 forwarding을 결정
forwardA와 forwardB가 있음
- ### HazardDetection
##### Data Hazard for Branch
beq가 ID stage에서 계산되면서 생기는 특수한 Hazard
1. R-type 다음 beq
    ```python
    (hazard_detection의 소스코드 중)
    elif self.inputs['Branch']['value'] and self.inputs['ID/EX.RegWrite']['value'] and \
            (self.inputs['ID/EX.rd']['value'] == self.inputs['IF/ID.rs']['value'] or \
                self.inputs['ID/EX.rd']['value'] == self.inputs['IF/ID.rt']['value']):
            value = 0
    ```
2. lw 다음 beq
    기존의 load use hazard와 동일하게 처리할 수 있다.
3. lw 다다음 beq
    ```python
    (hazard_detection의 소스코드 중)
    elif self.inputs['Branch']['value'] and self.inputs['EX/MEM.MemRead']['value'] and \
            (self.inputs['EX/MEM.RegisterRd']['value'] == self.inputs['IF/ID.rs']['value'] or \
                self.inputs['EX/MEM.RegisterRd']['value'] == self.inputs['IF/ID.rt']['value']):
            value = 0
    ```
### InteractiveTrapezoid
다각형 부모 클래스
- ### SimpleAdder
alu의 부모 클래스
- ### ALU
alu op에 해당하는 산술 연산을 수행한다.
### ShowData
- Register Memory위에 마우스가 올라가면 32개의 Register의 값들을 화면에 출력한다.
- Data Memory위에 마우스가 올라가면 User Data segment를 spim 형식에 맞게 출력한다.
- 메모리를 16 단위 즉, 4 word 단위로 읽어 little endian으로 출력하고, 오른쪽에는 text로 변환하여 출력한다.
### ShowProgress
- 현재 클락 사이클과 각 스테이지에서 실행되고 있는 instruction을 출력한다.
- 실행중 instruction이 필요시에 Nop로 바뀐다.
### LogicGate
- ### AND Gate
- and 연산 수행
- ### OR Gate
- or 연산 수행
### Multiplexer
- control signal에 해당하는 순서에 맞게 output을 결정한다.
- input이 두 개일 때 control signal은 1bit 세 개일 때 2bit

##### Assembler
지원하는 명령어 : .data, .text, .asciiz, .ascii, .space, .byte, .half, .word
.s file을 assemble하여 그 결과인 Instruction들과 Data들을 Instruction Memory와 Data Memory에 전달한다.
word의 경우 4byte 단위로 align되고, Little Endian 방식으로 저장된다.
First pass에서 Label의 주소를 결정하고, Second pass에서 데이터를 저장하고 기계어로 번역한다.

##### File Select
PyQt5 라이브러리의 QFileDialog를 사용했다.
사용자가 선택한 어셈블리 소스 코드로 Assembler가 작업을 시작한다.
```python
app = QApplication([])
filename, _ = QFileDialog.getOpenFileName(
    None,
    "Open File", "","Assembly Source Code (*.s)",
    )
```
