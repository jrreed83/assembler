
class Stack():
    def __init__(self, size=256):
        self.array = [0] * size
        self.head  = 0
    def push(self, x):
        self.head = self.head+1
        self.array[self.head] = x
        return self.head
    def pop(self):
        x = self.array[self.head]
        self.head = self.head-1
        return x 
    def peek(self):
        return self.array[self.head]

class OpCode:
    NOP     = 0
    HALT    = 1
    IADD    = 2
    ISUB    = 3
    IMUL    = 4
    ICONST0 = 5
    ICONST1 = 6
    ICONST2 = 7
    PRINT   = 8

class CPU():
    def __init__(self):
        self.opStack = Stack()
        self.ip = 0
    def execute(self, instructions=[]):
        op = instructions[self.ip]
        while(op != OpCode.HALT):
            self.ip = self.ip + 1
            if op == OpCode.NOP:
                pass
            elif op == OpCode.IADD:
                x = self.opStack.pop()
                y = self.opStack.pop()
                self.opStack.push(x+y)
            elif op == OpCode.ICONST0:
                self.opStack.push(0)   
            elif op == OpCode.ICONST1:
                self.opStack.push(1)    
            elif op == OpCode.ICONST2:
                self.opStack.push(2)                                             
            elif op == OpCode.ISUB:
                x = self.opStack.pop()
                y = self.opStack.pop()
                self.opStack.push(x-y)                
            elif op == OpCode.PRINT:
                print(self.opStack.pop())

            op = instructions[self.ip]
    