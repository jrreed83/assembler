from assembler.parser import * 

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

class CPU():
    def __init__(self, code=[], constants=[]):
        self.op_stack = Stack()
        self.memory = {}
        self.code = code 
        self.constants = constants

def execute(cpu):
    ip = 0
    op_stack = cpu.op_stack
    constants = cpu.constants
    code = cpu.code

    op = code[ip]
    while op != HALT:
        ip = ip + 1
        if op == IADD:
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
            print(pop(op_stack))
        elif op == POP:
            pop(op_stack)
        elif op == IPUSH:
            b0 = code[ip  ]
            b1 = code[ip+1]
            b2 = code[ip+2]
            b3 = code[ip+3]

            x = (b0 << 0) | (b1 << 8) | (b2 << 16) | (b3 << 24) 
            push(op_stack, x)
            ip += 4
        elif op == FPUSH:
            index = code[ip]
            value = constants[index]
            push(op_stack, value)
            ip += 1
        elif op == FADD:
            x_1 = pop(op_stack)
            x_2 = pop(op_stack)
            push(op_stack, x_1+x_2)            
            
        op = code[ip]

if __name__ == '__main__':
    src = """ipush 5
             ipush 5
             iadd
             print
             halt
          """  
    a = assemble(src)
    cpu = CPU(code=a.code, constants=a.constants)
    execute(cpu)

         
    