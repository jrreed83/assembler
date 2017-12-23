class Stack():
    def __init__(self, size=256):
        self.array = [0] * size
        self.head = 0

def push(stack, x):
    stack.head = stack.head+1
    stack.array[stack.head] = x
    return stack.head

def pop(stack):
    x = stack.array[stack.head]
    stack.head = stack.head-1
    return x 

def peek(stack):
    return stack.array[stack.head]

class OpCode:
    NOP = 0
    HALT = 1
    IADD = 2
    ISUB = 3
    IMUL = 4
    ICONST0 = 5
    ICONST1 = 6
    ICONST2 = 7
    PRINT = 8


class CPU():
    def __init__(self):
        self.op_stack = Stack()
        self.ip = 0

def execute(cpu, instructions=[]):
    ip = cpu.ip
    op_stack = cpu.op_stack
    op = instructions[ip]
    while op != OpCode.HALT:
        ip = ip + 1
        if op == OpCode.NOP:
            pass
        elif op == OpCode.IADD:
            x = pop(op_stack)
            y = pop(op_stack)
            push(op_stack, x+y)
        elif op == OpCode.ICONST0:
            push(op_stack, 0)  
        elif op == OpCode.ICONST1:
            push(op_stack, 1)    
        elif op == OpCode.ICONST2:
            push(op_stack, 2)                                             
        elif op == OpCode.ISUB:
            x = pop(op_stack)
            y = pop(op_stack)
            push(op_stack, x-y)              
        elif op == OpCode.PRINT:
            print(op_stack.pop())

        op = instructions[ip]
    