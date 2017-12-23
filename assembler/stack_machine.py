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
        self.memory = {}

def execute(cpu, instructions=[]):
    ip = cpu.ip
    op_stack = cpu.op_stack
    op = instructions[ip]
    while op != HALT:
        ip = ip + 1
        if op == NOP:
            pass
        elif op == IADD:
            x_1 = pop(op_stack)
            x_2 = pop(op_stack)
            push(op_stack, x_1+x_2)
        elif op == ICONST0:
            push(op_stack, 0)  
        elif op == ICONST1:
            push(op_stack, 1)    
        elif op == ICONST2:
            push(op_stack, 2)                                             
        elif op == ISUB:
            x_1 = pop(op_stack)
            x_2 = pop(op_stack)
            push(op_stack, x_1-x_2)              
        elif op == PRINT:
            print(op_stack.pop())

        op = instructions[ip]
    