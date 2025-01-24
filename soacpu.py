CODESIZE = 1024

PACKETSIZE = 1518

Labels = dict()

pc = 0
codeptr = 0
packetptr = 0

code = [0]*CODESIZE
packet = [0]*PACKETSIZE

def addcmd(x):
    global codeptr
    code[codeptr] = x
    codeptr += 1


def addcmdlit(cmd, lit):
    global codeptr
    code[codeptr] = (cmd << 20) + lit
    codeptr += 1

def addcmdlitlit(cmd, lit1, lit2):
    global codeptr
    code[codeptr] = (cmd << 20) + (lit1 << 8) + lit2
    codeptr += 1



def regindex(regname):
    temp = -1
    match regname:
        case 'r0':
            temp = 0
        case 'r1':
            temp = 1
        case 'r2':
            temp = 2
        case 'r3':
            temp = 3
        case _:
            print('Error: register name is wrong: ', regname)
    return temp


def assemble(line):
    token = line.split()
    match token[0]:
        case 'label':
            Labels[token[1]] = codeptr
        case 'nop':
            addcmd(0)
        case 'jmp':
            addcmdlit(5, Labels[token[1]])
        case 'eq':
            addcmdlit(1, int(token[1]))
        case 'set':
            addcmdlit(2, int(token[1]))
        case 'setsym':
            addcmdlitlit(3, int(token[1]), int(token[2]))
        case 'setset':
            addcmdlitlit(4, int(token[1]), int(token[2]))
        case _:
            print('Error: ', token[0])


print('Assembling')
assemble('nop')
assemble('eq 42')
assemble('set 1')
assemble('setsym 1 42')


print('Code size =', codeptr)
print('Program:')
for i in range (0, codeptr):
    print(i, ' => conv_std_logic_vector(', code[i], ', 24),')

def step():
    global pc
    global packetptr
    cmd = code[pc]
    data = packet[packetptr]


