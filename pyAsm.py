CODESIZE = 16384

Labels = dict()
Forwards = dict()

codeptr = 0

code = [0]*CODESIZE


def addcmd(x):
    global codeptr
    code[codeptr] = x
    codeptr += 1


def addcmdlit(cmd, lit):
    addcmd((cmd << 19) + lit)


def addcmdreg(cmd, reg):
    addcmd((cmd << 19) + (reg << 16))


def addcmdreglit(cmd, reg, lit):
    addcmd((cmd << 19) + (reg << 16) + lit)


def addcmdregreg(cmd, regdest, regsrc):
    addcmd((cmd << 19) + (regdest << 16) + (regsrc << 14))


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


def resolve(label):
    global Forwards
    global code
    global codeptr
    for lab in Forwards:
        if Forwards[lab] == label:
            code[lab] |= codeptr




def asm(line):
    global codeptr

    def trylabel(opcode):
        global codeptr
        global Labels
        global Forwards
        nonlocal token
        if token[1] in Labels:
            addcmdlit(opcode, Labels[token[1]])
        else:
            Forwards[codeptr] = token[1]
            addcmdlit(opcode, 0)

    token = line.split()
    match token[0]:
        case 'label':
            Labels[token[1]] = codeptr
            resolve(token[1])
        case 'nop':
            addcmd(0)
        case 'ret':
            addcmd(1 << 19)
        case 'jmp':
            trylabel(2)
        case 'call':
            trylabel(3)
        case 'jmpnz':
            trylabel(4)
        case 'jmpz':
            trylabel(5)
        case 'store':
            addcmdregreg(6, regindex(token[1]), regindex(token[2]))
        case 'load':
            addcmdreg(7, regindex(token[2]))
            addcmdreg(8, regindex(token[1]))
        case 'add':
            addcmdregreg(9, regindex(token[1]), regindex(token[2]))
        case 'sub':
            addcmdregreg(10, regindex(token[1]), regindex(token[2]))
        case 'cmp':
            addcmdregreg(11, regindex(token[1]), regindex(token[2]))
        case 'in':
            addcmdregreg(12, regindex(token[1]), regindex(token[2]))
        case 'out':
            addcmdregreg(13, regindex(token[1]), regindex(token[2]))
        case 'mult':
            addcmdregreg(14, regindex(token[1]), regindex(token[2]))
        case 'shl':
            addcmdreg(15, regindex(token[1]))
        case 'shr':
            addcmdreg(16, regindex(token[1]))
        case 'inc':
            addcmdreg(17, regindex(token[1]))
        case 'dec':
            addcmdreg(18, regindex(token[1]))
        case 'mov':
            addcmdregreg(19, regindex(token[1]), regindex(token[2]))
        case 'movl':
            addcmdreglit(20, regindex(token[1]), int(token[2]) & 65535)
            addcmdreglit(21, regindex(token[1]), (int(token[2]) >> 16) & 65535)
        case _:
            print('Error: ', token[0])


def asm_lines(text):
    for line in text.split('\n'):
        line = line.strip()
        if line:
            asm(line)


print('Assembling')
asm_lines('''movl r0 0
movl r1 1000000
store r1 r0
movl r0 1
movl r1 2000000
store r1 r0
jmp main
label delay
dec r0
cmp r0 r1
jmpnz delay
ret
label main
movl r1 1
label loop
movl r3 10000
out r2 r3
movl r3 20000
in r0 r3
movl r2 0
load r1 r2
mult r0 r1
movl r2 1
load r1 r2
add r0 r1
movl r1 0
call delay
shl r2
movl r1 16
cmp r2 r1
jmpnz loop
movl r2 1
jmp loop''')


print('Code size =', codeptr)
print('Program:')
for i in range (0, codeptr):
    print(i, ' => conv_std_logic_vector(', code[i], ', 24),')

print(Labels)

