import io
from collections import namedtuple

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


Result = namedtuple('Result', ['ptr', 'tokens'])
Token = namedtuple('Token', ['kind', 'value'])

RESERVED = {
    'halt': HALT,
    'iadd': IADD,
    'isub': ISUB,
    'imul': IMUL,
    'iconst0': ICONST0,
    'iconst1': ICONST1, 
    'iconst2': ICONST2,
    'ipush': IPUSH,
    'print': PRINT,    
    'spush': SPUSH,
    'fpush': FPUSH,  
    'jump': JUMP,
    'fadd': FADD,
    'fmul': FMUL,
    'fsub': FSUB,
    'pop': POP,
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
    return len(result.tokens) != 0


def reserved(keyword, string, start=0): 
    start = space(string, start)    
    stop = start + len(keyword)    
    if keyword == string[start:stop]:
        if keyword in RESERVED.keys():
            data = RESERVED[keyword]
            return Result(stop, [Token('reserved', data)])
    stop = start 
    return Result(stop, [])

def instruction_halt(string, ptr):
    return reserved('halt', string, ptr)

def instruction_iadd(string, ptr):
    return reserved('iadd', string, ptr)

def instruction_isub(string, ptr):
    return reserved('isub', string, ptr)

def instruction_imul(string, ptr):
    return reserved('imul', string, ptr)

def instruction_print(string, ptr):
    return reserved('print', string, ptr)

def instruction_pop(string, ptr):
    return reserved('pop', string, ptr)

def instruction_fadd(string, ptr):
    return reserved('fadd', string, ptr)

def instruction_fsub(string, ptr):
    return reserved('fsub', string, ptr)

def instruction_fmul(string, ptr):
    return reserved('fmul', string, ptr)

def instruction_iconst0(string, ptr):
    return reserved('iconst0', string, ptr)

def instruction_iconst1(string, ptr):
    return reserved('iconst1', string, ptr)

def instruction_iconst2(string, ptr):
    return reserved('iconst2', string, ptr)

def instruction(string, ptr):

    result = instruction_ipush(string, ptr)
    if is_successful(result):
        return result

    result = instruction_iadd(string, ptr)
    if is_successful(result):
        return result

    result = instruction_fadd(string, ptr)
    if is_successful(result):
        return result

    result = instruction_isub(string, ptr)
    if is_successful(result):
        return result

    result = instruction_imul(string, ptr)
    if is_successful(result):
        return result

    result = instruction_fpush(string, ptr)
    if is_successful(result):
        return result

    result = instruction_spush(string, ptr)
    if is_successful(result):
        return result

    result = instruction_halt(string, ptr)
    if is_successful(result):
        return result

    result = instruction_print(string, ptr)
    if is_successful(result):
        return result

    result = instruction_iconst0(string, ptr)
    if is_successful(result):
        return result

    result = instruction_iconst1(string, ptr)
    if is_successful(result):
        return result

    result = instruction_iconst2(string, ptr)
    if is_successful(result):
        return result

    return Result(ptr, None)

def instruction_ipush(string, ptr):
    result1 = reserved('ipush', string, ptr)
    print(result1)    
    if is_successful(result1):
        result2 = integer(string, result1.ptr)
        if is_successful(result2):
            _, [tok1] = result1 
            _, [tok2] = result2
            return Result(result2.ptr, [tok1, tok2])
    return Result(ptr, [])


def instruction_spush(string, ptr):
    result1 = reserved('spush', string, ptr)
    if is_successful(result1):
        result2 = quoted_string(string, result1.ptr)
        if is_successful(result2):
            _, [tok1] = result1 
            _, [tok2] = result2
            return Result(result2.ptr, [tok1, tok2])
    return Result(ptr, [])


def instruction_fpush(string, ptr):
    result1 = reserved('fpush', string, ptr)
    if is_successful(result1):
        result2 = decimal(string, result1.ptr)
        if is_successful(result2):
            _, [tok1] = result1 
            _, [tok2] = result2
            return Result(result2.ptr, [tok1, tok2])
    return Result(ptr, [])

def space(string, start = 0):
    ptr = start
    while string[ptr].isspace():
        ptr += 1
    return ptr

def integer(string, start=0):
    ptr = space(string, start)
    if not string[ptr].isdigit():
        return Result(ptr, [])

    while string[ptr].isdigit():
        ptr += 1 

    value = int(string[start:ptr])
    #b0 = (value >> 0 ) & 0xff
    #b1 = (value >> 8 ) & 0xff 
    #b2 = (value >> 16) & 0xff
    #b3 = (value >> 24) & 0xff 
    return Result(ptr, [Token('int', value)])


def quote(string, start = 0):
    ptr = space(string, start)
    if string[ptr] == '\"':
        return Result(ptr+1, '\"')
    return Result(start, None)  

def colon(string, start = 0):
    ptr = space(string, start)
    if string[ptr] == ':':
        return Result(ptr+1, ':')
    return Result(start, None)  

def semicolon(string, start = 0):
    start = space(string, start)
    ptr = start
    if string[ptr] == ';':
        return Result(ptr+1, ';')
    return Result(start, None) 

def period(string, start = 0):
    ptr = space(string, start)
    if string[ptr] == '.':
        return Result(ptr+1, '.')
    return Result(start, None) 

def quoted_string(input_string, start=0):
    ptr = space(input_string, start)
    result1 = quote(input_string, ptr)
    if is_successful(result1):
        result2 = string(input_string, result1.ptr)
        if is_successful(result2):
            result3 = quote(input_string, result2.ptr)
            if is_successful(result3):
                return Result(result3.ptr, [result2.token])
    return Result(start, [])

def string(input_string, start=0):
    start = space(input_string, start)
    ptr = start
    c = input_string[ptr]
    if c.isalpha():
        ptr += 1
        c = input_string[ptr]
        while c.isalpha() or c.isdigit():
            ptr += 1
            c = input_string[ptr]
        return Result(ptr, [Token('str', input_string[start:ptr])])
    return Result(start, None)

def label_ref(assm):
    white_space(assm)
    c = peek(assm)
    if c.isalpha():
        c = next_char(assm)
        while (c.isalpha() or c.isdigit()):
            c = next_char(assm)
        rewind(assm) 
        assm.ip += 1
        return True
    return False

def decimal(string, start = 0):
    start = space(string, start)
    ptr = start 
    d = string[ptr]
    if d.isdigit():
        result1 = integer(string, ptr)
        if is_successful(result1):
            result2 = period(string, result1.ptr)
            if is_successful(result2):    
                result3 = integer(string, result2.ptr)
                if is_successful(result3):
                    return Result(result3.ptr, [Token('flt',float(string[start:result3.ptr])])
    return Result(start, [])

def assemble(source_code=''):
    assm = Assembler(source_code)
    while assm.pos < len(assm.input):
        expression(assm)
        if assm.input[assm.start:].isspace():
            break
    return assm

def commit(cpu, instruction):
    ptr, token = instruction
    if len(token) == 1:
        cpu.code[cpu.ip] = token 
        cpu.ip += 1    
        return cpu

def instruction(assm):
    if instruction_ipush(assm):
        return True 
    elif instruction_iadd(assm):
        return True
    elif instruction_fadd(assm):
        return True    
    elif instruction_isub(assm):
        return True
    elif instruction_imul(assm):
        return True
    elif instruction_fpush(assm):
        return True
    elif instruction_spush(assm):
        return True
    elif instruction_halt(assm):
        return True
    elif instruction_print(assm):
        return True
    elif instruction_iconst0(assm):
        return True
    elif instruction_iconst1(assm):
        return True
    elif instruction_iconst2(assm):
        return True
    else:
        return False

def expression(assm):
    if instruction(assm):
        return True
    elif label(assm):
        return True    
    elif comment(assm):
        return True
    else:
        return False

def label(input_string, ptr):
    result1 = string(input_string, ptr)
    if is_successful(result1):
        result2 = colon(input_string, result1.ptr)
        if is_successful(result2):
            return Result(result2.ptr, result1.token)
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
        


