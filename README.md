# Mips-pipeline-simulator


<팀원>
20191588 마준영 
20191582 김혜성 
20191591 박근우 

<설계 조건>
MIPS 파이프라인 시뮬레이터 만들기  
MIPS and/or/add/sub/slt/lw/sw/beq/j 명령어를 수행하는 5단계 파이프라인 프로세서 (레지스터 화일과 메모리 포함) 를 cycle 단위로 simulation 하여 시각화하여 보여주는 프로그램을 완성
프로그램 입력 : 위의 9개 명령어와 MIPS assmbler directives, comment 로 구성된 any assembly source file  
필수 기능  
    - MIPS assembler/disassembler 포함 (open source 사용 가능)  
    - pipeline visualization : 프로그램을 cycle 단위로 수행하고 정지된 상태에서 회로 상의 모든 component 입출력 값을 시각화  
    - data/branch hazard 해결 ( j 명령의 hazard 도 해결해야 함)  
    - assemble 된 프로그램은 0x00400024 번지에 load 되고 PC 의 값은 이 값으로 초기화되어 수행이 시작됨.  
    - $sp 는 0x7ffffe40, $gp 는 0x10008000 로 초기화  
    - data memory 는 0으로 초기화하고 .data directive 의 내용에 따라 초기화  
    - memory 에는 OS code 가 없어도 됨  
    - memory 의 내용은 전체를 한꺼번에 보여줄 수 없으므로 적절한 방법으로 보여줄 것  
    - 프로그램의 종료 시점은 따로 정해지지 않음.  
    - exception handling 과 memory hierarchy 는 구현하지 않아도 됨  
    - visulaization 화면에는 클락 사이클을 0부터 카운트하여 몇번째 사이클인지 보여주는 화면이 포함되어야 함.  
    - 프로그램 소스는 github 에서 download 받아 compile 하여 수행할 수 있는 형태로 공개되어야 함  
    - web service 형태로 구현하는 것도 가능, 이 경우에도 소스가 공개되어야 함  
    - github repository 에는 본 프로젝트에 대한 설명 (보고서를 대신함, 소스 코드 설명, 설치, 사용법 설명) 이 포함되어야 함      
