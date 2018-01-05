import io
from collections import namedtuple
from enum import Enum 

class Type(Enum):
    OPCODE = 0
    STRING  = 1
    INTEGER = 2 
    DECIMAL = 3
    LABEL = 4

class Op(Enum):
    HALT = 1
    IADD = 2
    ISUB = 3
    IMUL = 4
    ICONST0 = 5
    ICONST1 = 6
    ICONST2 = 7
    IPUSH = 8
    PRINT = 9
    FPUSH = 10
    SPUSH = 11
    JUMP = 12 
    FADD = 13
    FMUL = 14
    FSUB = 15
    POP = 16

RESERVED = {
    'halt': Op.HALT,
    'iadd': Op.IADD,
    'isub': Op.ISUB,
    'imul': Op.IMUL,
    'iconst0': Op.ICONST0,
    'iconst1': Op.ICONST1, 
    'iconst2': Op.ICONST2,
    'ipush': Op.IPUSH,
    'print': Op.PRINT,    
    'spush': Op.SPUSH,
    'fpush': Op.FPUSH,  
    'jump': Op.JUMP,
    'fadd': Op.FADD,
    'fmul': Op.FMUL,
    'fsub': Op.FSUB,
    'pop': Op.POP,
}


class Assembler:
    def __init__(self, input=''):
        self.reserved = {}
        self.pos = 0
        self.start = 0
        self.input = input
        self.line = 0
        self.code = [0] * 1000
        self.constants = [0] * 1000
        self.labels = {}
        self.ip = 0 # instruction pointer
        self.cp = 0 # constant pointer

    def __repr__(self):
        return '[{0}]'.format(self.pos)


def is_successful(result):
    ptr, rest = result
    return (rest is not None)

def failed(result):
    _, rest = result
    return (rest is None)

def reserved(keyword, string, start=0): 
    start = space(string, start)    
    stop = start + len(keyword)    
    if keyword == string[start:stop]:
        if keyword in RESERVED.keys():
            value = RESERVED[keyword]
            return (stop, value)
    return (start, None)

def operation(string, ptr):
    for key in RESERVED.keys():
        ptr, token = reserved(key, string, ptr)
        if token is not None:
            result = (ptr, token)
            break
    else:
        result = (ptr, None)
    return result

def statement(string, ptr):
    ptr1, token1 = operation(string, ptr)
    if token1 is not None:
        return (ptr1, token1)

    ptr1, token1 = comment(string, ptr)
    if token1 is not None:
        return (ptr1, token1)

#    ptr1, token1 = label(string, ptr)
#    if token1 is not None:
#        return (ptr1, token1)

    return (ptr, None)    

def space(string, start = 0):
    ptr = start
    while string[ptr].isspace():
        ptr += 1
    return ptr

def integer(string, start=0):
    start = space(string, start)
    ptr = start
    if not string[ptr].isdigit():
        return (ptr, None)

    while string[ptr].isdigit():
        ptr += 1 
    val = string[start:ptr]
    return (ptr, (Type.INTEGER, val))


def match(char, string, start):
    ptr = space(string, start)

    if ptr == len(string):
        return (ptr, None)  

    if string[ptr] == char:
        return (ptr+1, char)
    return (start, None) 


def quoted_string(input_string, start=0):
    ptr = space(input_string, start)
    ptr1, token1 = match('\"', input_string, ptr)
    if token1 is None:
        return (start, None)

    ptr2, token2 = string(input_string, ptr1)
    if token2 is None:
        return (start, None)
    tag2, val2 = token2

    ptr3, token3 = match('\"',input_string, ptr2)
    if token3 is None:
        return (start, None)

 
    return (ptr3, (tag2, val2))
    

def string(input_string, start=0):
    start = space(input_string, start)
    ptr = start
    c = input_string[ptr]
    if not c.isalpha():
        return (start, None)
    ptr += 1
    c = input_string[ptr]
    while c.isalpha() or c.isdigit():
        ptr += 1
        c = input_string[ptr]
    return (ptr, (Type.STRING, input_string[start:ptr]))


def decimal(string, start = 0):
    start = space(string, start)
    ptr = start 

    ptr1, token1 = integer(string, ptr)
    if token1 is None:
        return (start, None)

    ptr2, token2 = match('.', string, ptr1)
    if token2 is None:    
        return (start, None)

    ptr3, token3 = integer(string, ptr2)
    if token3 is None:
        return (start, None)    

    number = string[start:ptr3]
    return (ptr3, (Type.DECIMAL, number))



class CPU():
    def __init__(self):
        self.code = []
    def commit(self, result):
        ptr, (tag, val) = result

        if tag == Type.DECIMAL:
            return (ptr, 'statement')
        elif tag == Type.INTEGER:
            val = int(val)
            b0 = (val >> 0 ) & 0xff
            b1 = (val >> 8 ) & 0xff 
            b2 = (val >> 16) & 0xff
            b3 = (val >> 24) & 0xff
            self.code += [b0, b1, b2, b3] 
            return (ptr, 'statement')
        elif tag == Type.LABEL:
            return (ptr, 'statement')
        elif tag == Type.STRING:
            return (ptr, 'statement') 
        elif tag == Type.OPCODE:
            self.code += [val.value]
            if val in [Op.FADD, Op.IADD, Op.PRINT, Op.HALT]:
                return (ptr, 'statement')
            elif val == Op.IPUSH:
                return (ptr, 'integer')
            elif val == Op.SPUSH:
                return (ptr, 'quoted_string')
            elif val == Op.FPUSH:
                return (ptr, 'decimal')
    
    def execute(self, string):
        state = 'statement'
        ptr = 0
        while 1:
            if state == 'statement':
                result = statement(string, ptr)
            elif state == 'integer':
                result = integer(string, ptr)

            ptr, state = self.commit(result)

def label(input_string, ptr):
    ptr1, token1 = string(input_string, ptr)
    if token1 is None:
        return (ptr, None)
    _, label = token1 

    ptr2, token2 = match(':', input_string, ptr1)
    if token2 is None: 
        return (ptr, None)
            
    return (ptr2, (Type.LABEL, label))


def comment(string, ptr):
    ptr1, token1 = match(';', string, ptr)
    if token1 is None: 
        return (ptr, None)

    while string[ptr1] != '\n':
        ptr1 += 1
    return (ptr1, True)


def main():
    src = """iconst1
             iconst1
             fpush 5.65
             fpush 4.23
             spush "hello"
             iadd
             print
             halt
          """  

    a = assemble(src)
    print(a.code[0:a.ip])
    print(a.constants[0:a.cp])
if __name__ == '__main__':
    main()
        


