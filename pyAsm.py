CODESIZE = 16384

Labels = dict()

codeptr = 0

code = [0]*CODESIZE


def addcmd(x):
    global codeptr
    code[codeptr] = x
    codeptr += 1


def addcmdlit(cmd, lit):
    global codeptr
    code[codeptr] = (cmd << 19) + lit
    codeptr += 1


def addcmdreg(cmd, reg):
    global codeptr
    code[codeptr] = (cmd << 19) + (reg << 16)
    codeptr += 1


def addcmdreglit(cmd, reg, lit):
    global codeptr
    code[codeptr] = (cmd << 19) + (reg << 16) + lit
    codeptr += 1

def addcmdregreg(cmd, regdest, regsrc):
    global codeptr
    code[codeptr] = (cmd << 19) + (regdest << 16) + (regsrc << 14)
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
        case 'ret':
            addcmd(1 << 19)
        case 'jmp':
            addcmdlit(2, Labels[token[1]])
        case 'call':
            addcmdlit(3, Labels[token[1]])
        case 'jmpnz':
            addcmdlit(4, Labels[token[1]])
        case 'jmpz':
            addcmdlit(5, Labels[token[1]])
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


print('Assembling')
assemble('nop')
assemble('add r2 r1')
assemble('label main')
assemble('jmp main')
assemble('store r1 r2')
assemble('load r3 r2')
assemble('label start')
assemble('movl r3 1234')
assemble('jmpnz start')

print('Code size =', codeptr)
print('Program:')
for i in range (0, codeptr):
    print(hex(code[i]))


