import string
import sys
import tkinter as tk

pc = 0
depth = 0
rdepth = 0
ldepth = 0

stack = [0] * 16
rstack = [0] * 16
lstacki = [0] * 16
lstackimax = [0] * 16
lstackiaddr = [0] * 16

program = [0] * 16384
data = [0] * 2048

litflag = 0

vmem = [0]*65536*3
screen = bytearray([0] * (256 * 256 * 3))


def make_image(w, h, pixels):
    header = f'P6 {w} {h} 255 '.encode()
    data = header + pixels
    return tk.PhotoImage(width=w, height=h, data=data, format='PPM')


def update():
    for y in range(256):
        for x in range(256):
            r = vmem[(256 * y + x) * 3]
            g = vmem[(256 * y + x) * 3 + 1]
            b = vmem[(256 * y + x) * 3 + 2]
            screen[3 * (256 * y + x)] = r * 16
            screen[3 * (256 * y + x) + 1] = g * 16
            screen[3 * (256 * y + x) + 2] = b * 16
    label.image = make_image(256, 256, screen).zoom(2, 2)
    label.config(image=label.image)
    root.after(16, update)
def step():
    global pc
    global depth
    global rdepth
    global ldepth
    global litflag
    cmd = program[pc]
    pc = pc + 1

    top = depth - 1
    next = depth - 2
    match cmd:
        case 0:
            pass
        case 1:  # not
            if stack[top] != 0:
                stack[top] = 0
            else:
                stack[top] = -1
        case 2:  # @
            stack[top] = data[stack[top]]
        case 3:  # shl
            stack[top] = stack[top] << 1
        case 4:  # shr
            stack[top] = stack[top] >> 1
        case 5:  # shra
            stack[top] = stack[top] >> 1
        case 6:  # inport
            pass
        case 7:  # swap
            temp = stack[next]
            stack[next] = stack[top]
            stack[top] = temp
        case 8:  # dup
            stack[top + 1] = stack[top]
            depth += 1
        case 9:
            stack[top + 1] = stack[next]
            depth += 1
        case 11: # loop
            lstacki[ldepth - 1] += 1
            if lstacki[ldepth - 1] == lstackimax[ldepth - 1]:
                pc = pc + 1
                ldepth -= 1
            else: pc = lstackiaddr[ldepth - 1]
        case 12: # sysreg, 2 = I
            if stack[top] == 2:
                stack[top] = lstacki[ldepth - 1]
            else:
                pass
        case 13: # +
            stack[next] = stack[next] + stack[top]
            depth -= 1
        case 24: # call
            rstack[rdepth] = pc
            rdepth += 1
            pc = stack[top]
            depth -= 1
        case 27: # !
            if stack[top] <= 2047:
                data[stack[top]] = stack[next]
            if stack[top] >= 100000:  # 00011 00001 10101 00000  = 3  1  21 0 = 35 33 53 32
                vmem[stack[top] - 100000] = stack[next]
            depth -= 2
        case 28: # do
            lstacki[ldepth] = stack[top]
            lstackimax[ldepth] = stack[next]
            lstackiaddr[ldepth] = pc
            ldepth += 1
            depth -= 2
        case 31: # ret
            rdepth -= 1
            pc = rstack[rdepth]
        case _:
            pass

    if cmd in range(32, 64):
            if litflag == 0:
                depth = depth + 1
                stack[depth - 1] = cmd & 31
                litflag = 1
            else:
                stack[depth - 1] = (stack[depth - 1] << 5) | (cmd & 31)

    if cmd in range(0, 31):
        litflag = 0


def report():
    global depth
    global pc

    print("depth=", depth)
    if depth > 0:
        for i in range(depth):
            print(stack[i])


def reset():
    global pc
    global litflag
    global depth
    global rdepth

    pc = 0
    litflag = 0
    depth = 0
    rdepth = 0


here = 0


def compile(cmd):
    global here
    program[here] = cmd
    here += 1


def compile_lit(x):
    if here > 0:
        if program[here - 1] > 31:
            compile(0)
    if x > 67108863:
        compile(32 + (x >> 30))
    if x > 3354431:
        compile(32 + ((x >> 25) & 31))
    if x > 1048575:
        compile(32 + ((x >> 20) & 31))
    if x > 32767:
        compile(32 + ((x >> 15) & 31))
    if x > 1023:
        compile(32 + ((x >> 10) & 31))
    if x > 31:
        compile(32 + ((x >> 5) & 31))
    compile(32 + (x & 31))


def interpret(str):
    tokens = str.split()
    print(tokens)
    for token in tokens:
        match token:
            case 'nop':
                compile(0)
            case '+':
                compile(13)
            case '!':
                compile(27)
            case 'do':
                compile(28)
            case 'loop':
                compile(11)
            case 'i':
                compile_lit(2)
                compile(12)
            case _:
                number = int(token)
                print("Literal ", number)
                compile_lit(number)


reset()

interpret("15 0 + 100000 ! 15 100004 ! 5 0 do i loop nop")

while pc < here:
    step()
    report()

root = tk.Tk()
label = tk.Label()
label.pack()
root.after(0, update)
tk.mainloop()


print(program[0:here])