CODESIZE = 1024
PACKETSIZE = 1518
TABLES = 256

Labels = dict()

pc = 0
codeptr = 0
packetptr = 0
packetsize = 0
flag = 1

code = [0]*CODESIZE
packet = [0]*PACKETSIZE

matchtable = [[0 for i in range(256)] for j in range(TABLES)]
table = 0


def settable(start, end):
    global table
    global matchtable
    print('Setting: ', start, '..', end, '[', chr(start), chr(end), '] for subset ', table)
    for i in range (start, end):
        matchtable[i][table] = 1


def ismatch(sym, tabindex):
    global matchtable
    if matchtable[sym][tabindex] != 0:
        return True
    else:
        return False


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


# constant NOP : std_logic_vector(3 downto 0) := "0000";
# constant EQ : std_logic_vector(3 downto 0) := "0001";
# constant TOINDEX : std_logic_vector(3 downto 0) := "0010";
# constant TOINDEXEND : std_logic_vector(3 downto 0) := "0011";
# constant EQSET : std_logic_vector(3 downto 0) := "0100";
# constant EQSETSYM : std_logic_vector(3 downto 0) := "0101";


def assemble(line):
    token = line.split()
    match token[0]:
        case 'label':
            Labels[token[1]] = codeptr
        case 'nop':
            addcmd(0)
        case 'eq':
            addcmdlit(1, int(token[1]))
        case 'toindex':
            addcmdlitlit(2, int(token[1]), int(token[2]))
        case 'toindexend':
            addcmdlitlit(3, int(token[1]), int(token[2]))
        case 'eqset':
            addcmdlit(4, int(token[1]))
        case 'eqsetsym':
            addcmdlitlit(5, int(token[1]), int(token[2]))
        case _:
            print('Error: ', token[0])


print('Assembling')
assemble('eq 1')
assemble('eq 2')
assemble('eq 42')
assemble('eqset 1')
assemble('eqset 2')
assemble('eq 0')




print('Code size =', codeptr)
print('Program:')
for i in range (0, codeptr):
    print(i, ' => conv_std_logic_vector(', code[i], ', 24),')


# pc <= 0 when reset_reg = '1' else
#       pc_reg when (cmd(23 downto 20) = TOINDEX and conv_integer(index) < conv_integer(cmd(19 downto 8)))
#              or (cmd(23 downto 20) = TOINDEXEND and (conv_integer(size) - conv_integer(index)) > conv_integer(cmd(19 downto 8)))
#              or (cmd(23 downto 20) = EQSETSYM and match_bus(conv_integer(cmd(7 downto 0))) = '1' and symbol = cmd(15 downto 8))
#       else
#       pc_reg + 1;
#
# new_flag <= match_bus(conv_integer(cmd(7 downto 0))) when ((cmd(23 downto 20) = TOINDEXEND) and (conv_integer(size) - conv_integer(index)) >= conv_integer(cmd(19 downto 8))) else
#            '1' when cmd(23 downto 20) = NOP else
#            '1' when cmd(23 downto 20) = EQ and cmd(7 downto 0) = symbol else
#            '1' when cmd(23 downto 20) = TOINDEX and match_bus(conv_integer(cmd(7 downto 0))) = '1' else
#            '1' when cmd(23 downto 20) = EQSETSYM and match_bus(conv_integer(cmd(7 downto 0))) = '1' and symbol = cmd(15 downto 8) else
#            '0';

def step():
    global pc
    global packetptr
    global packetsize
    global flag
    cmd = code[pc]
    sym = packet[packetptr]
    opcode = (cmd >> 20) & 15
    match opcode:
        case 0:
            pc += 1
        case 1:
            if (sym != cmd & 255):
               flag = 0
            pc += 1
        case 2: # toindex
            if (packetptr == ((cmd >> 8) & 4095)):
                pc += 1
            if not(ismatch(sym, cmd & 255)):
                flag = 0
        case 3: # toindexend
            if (packetsize - packetptr) == ((cmd >> 8) & 4095):
                pc += 1
            if not(ismatch(sym, cmd & 255)):
                flag = 0
        case 4: # eqset
            pc += 1
            if not(ismatch(sym, cmd & 255)):
                flag = 0
        case 5: # eqsetsym
            if sym == ((cmd >> 8) & 255):
                pc += 1
            else:
                if not (ismatch(sym, cmd & 255)):
                    flag = 0
        case _:
            print('Error while executing unknown opcode ', opcode, ' at addr ', pc)
    packetptr += 1

def run():
    global pc, packetptr, packetsize, flag
    pc = 0
    flag = 1
    packetptr = 0
    lastflag = 1

    print('Run emulation with packet size', packetsize)
    while packetptr < packetsize:
        step()
        if flag != lastflag:
            print('Not match at ', packetptr)
        lastflag = flag
    print('Done, flag = ', flag)


table = 0
settable(0, 255)

table = 1
settable(48, 57)

table = 2
settable(65, 90)

packetsize = 10
packet = [1, 2, 42, 48, 69, 50, 51, 52, 53, 54]

run()

