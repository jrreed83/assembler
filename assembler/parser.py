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

def stream(string):
    return {'string': string, 'ptr': 0}

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

def reserved(keyword, stream): 
    stream = space(stream)
    start = stream.get('ptr', 0)   
    string = stream.get('string') 
    stop = start + len(keyword)    
    if keyword == string[start:stop]:
        token = RESERVED.get(keyword, None)
        if token is not None:
            return ({**stream, 'ptr': stop}, token)
    return (stream, None)

def operation(stream):
    for key in RESERVED.keys():
        stream, token = reserved(key, stream)
        if token is not None:
            return (stream, token)
    return (stream, None)

def statement(stream):
    stream, token = operation(stream)
    if token is not None:
        return (stream, token)

    stream, token = comment(stream)
    if token is not None:
        return (stream, token)

    stream, token = label(stream)
    if token is not None:
        return (stream, token)

    return (stream, None)    

def space(stream):#string, start = 0):
    ptr = stream.get('ptr', 0)
    string = stream.get('string')
    while string[ptr].isspace():
        ptr += 1
    return {**stream, 'ptr': ptr}

def integer(stream):
    stream = space(stream)
    start = stream.get('ptr')
    stop = start
    string = stream.get('string')
    if not string[stop].isdigit():
        return (stream, None)

    while string[stop].isdigit():
        stop += 1 
    val = string[start:stop]
    return ({**stream, 'ptr': stop}, (Type.INTEGER, val))


def match(char, stream):
    stream = space(stream)
    string = stream.get('string')
    ptr = stream.get('ptr')
    if string[ptr] == char:
        return ({**stream, 'ptr':ptr+1}, char)
    return (stream, None) 


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


def decimal(stream):
    stream = space(stream)
    start = stream.get('ptr')

    stream, token = integer(stream)
    if token is None:
        return (stream, None)

    stream, token = match('.', stream)
    if token is None:    
        return (stream, None)

    stream, token = integer(stream)
    if token is None:
        return (stream, None)    
    
    stop = stream.get('ptr')
    string = stream.get('string')
    number = string[start:stop]
    return (stream, (Type.DECIMAL, number))



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

    for c in input_string[ptr:]:
        if c == ':':
            break
    else:
        return (ptr, None)

    
    ptr1, token1 = string(input_string, ptr)
    if token1 is None:
        return (ptr, None)
    _, label = token1 

    ptr2, token2 = match(':', input_string, ptr1)
    if token2 is None: 
        return (ptr, None)
            
    return (ptr2, (Type.LABEL, label))


def comment(stream):
    stream, token = match(';', stream)
    if token is None: 
        return (stream, None)

    string = stream.get('string')
    ptr = stream.get('ptr')
    while string[ptr] != '\n':
        ptr += 1
    return ({**stream, 'ptr': ptr}, True)


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
        


