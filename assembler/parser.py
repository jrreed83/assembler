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

Result = namedtuple('Result', ['ptr', 'token'])
Token = namedtuple('Token', ['type', 'value'])

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

def halt_op(string, ptr):
    return reserved('halt', string, ptr)

def iadd_op(string, ptr):
    return reserved('iadd', string, ptr)

def isub_op(string, ptr):
    return reserved('isub', string, ptr)

def imul_op(string, ptr):
    return reserved('imul', string, ptr)

def print_op(string, ptr):
    return reserved('print', string, ptr)

def pop_op(string, ptr):
    return reserved('pop', string, ptr)

def fadd_op(string, ptr):
    return reserved('fadd', string, ptr)

def fsub_op(string, ptr):
    return reserved('fsub', string, ptr)

def fmul_op(string, ptr):
    return reserved('fmul', string, ptr)

def iconst0_op(string, ptr):
    return reserved('iconst0', string, ptr)

def iconst1_op(string, ptr):
    return reserved('iconst1', string, ptr)

def iconst2_op(string, ptr):
    return reserved('iconst2', string, ptr)

def ipush_op(string, ptr):
    return reserved('ipush', string, ptr)

def spush_op(string, ptr):
    return reserved('spush', string, ptr)

def fpush_op(string, ptr):
    return reserved('fpush', string, ptr)

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
    if string[ptr] == char:
        return (ptr+1, char)
    return (start, None) 


def quoted_string(input_string, start=0):
    ptr = space(input_string, start)
    result1 = match('\"', input_string, ptr)
    if failed (result1):
        return (start, None)

    ptr1, _ = result1
    result2 = string(input_string, ptr1)
    if failed(result2):
        return (start, None)

    ptr2, (tag, val) = result2
    result3 = match('\"',input_string, ptr2)
    if failed(result3):
        return (start, None)

    ptr3,_ = result3
    return (ptr3, (tag, val))
    

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
    d = string[ptr]
    if not d.isdigit():
        return (start, None)

    result1 = integer(string, ptr)
    if failed(result1):
        return (start, None)

    ptr1, _ = result1
    result2 = match('.', string, ptr1)
    if failed(result2):    
        return (start, None)

    ptr2, _ = result2
    result3 = integer(string, ptr2)
    if failed(result3):
        return (start, None)    

    ptr3, _ = result3
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
    result1 = string(input_string, ptr)
    if is_successful(result1):
        ptr1, (_, val) = result1
        result2 = match(':', input_string, ptr1)
        if is_successful(result2):
            ptr2, _ = result2
            return Result(ptr2, (Type.LABEL, val))
    return Result(ptr, None)


def comment(string, ptr):
    result = semicolon(string, ptr)
    if is_successful(result):
        ptr = result.ptr
        while string[ptr] != '\n':
            ptr += 1
        return Result(ptr, True)
    return Result(ptr, None)


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
        


