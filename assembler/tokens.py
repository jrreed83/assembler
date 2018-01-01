import io

NOP = 0
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

RESERVED = {
    'nop': NOP,
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
    'jump': JUMP
}


class Assembler:
    def __init__(self, input=''):
        self.reserved = {}
        self.pos = 0
        self.start = 0
        self.input = input
        self.markers = []
        self.line = 0
        self.code = []
        self.constants = []
        self.labels = {}
        self.ip = 0 # instruction pointer
        self.cp = 0 # constant pointer

    def __repr__(self):
        return '[{0}]'.format(self.pos)


def next_char(assm):
    if assm.pos >= len(assm.input):
        return '\0'
    else:
        c = assm.input[assm.pos]
        assm.pos += 1
        return c

def rewind(assm):
    assm.pos -= 1 

def rollback(assm):
    assm.pos = assm.markers[0]['pos']
    assm.start = assm.markers[0]['start']
    assm.markers = []

def commit(assm):
    string = assm.input[assm.start:assm.pos]
    assm.code += [RESERVED[string]]
    assm.ip += 1
    assm.start = assm.pos
    assm.markers = [] 

def mark(assm, start=0, pos=0, data=[]):
    marker = {'start': start, 'pos': pos, 'data': data}
    assm.markers += [marker]


def ignore(assm):
    assm.start = assm.pos 

def peek(assm):
    c = next_char(assm)
    rewind(assm)
    return c

def tail(assm):
    return assm.input[assm.start:]

def reserved(keyword, string, start=0): 
    start = space(string, start)    
    stop = start + len(keyword)    
    if keyword == string[start:stop]:
        if keyword in RESERVED.keys():
            token = RESERVED[keyword]
            return [stop, token]
    stop = start 
    return [stop, None]


def instruction_halt(assm):
    [stop, token] = reserved('halt', assm.input, assm.start)
    if token is None:
        return False
    
    assm.start = stop
    assm.pos = stop
    assm.code += [token]
    assm.ip += 1
    return True 

def instruction_iadd(assm):
    [stop, token] = reserved('iadd', assm.input, assm.start)
    if token is None:
        return False
    
    assm.start = stop
    assm.pos = stop
    assm.code += [token]
    assm.ip += 1
    return True 

def instruction_imul(assm):
    [stop, token] = reserved('imul', assm.input, assm.start)
    if token is None:
        return False
    
    assm.start = stop
    assm.pos = stop
    assm.code += [token]
    assm.ip += 1
    return True 

def instruction_isub(assm):
    [stop, token] = reserved('isub', assm.input, assm.start)
    if token is None:
        return False
    
    assm.start = stop
    assm.pos = stop
    assm.code += [token]
    assm.ip += 1
    return True 

def instruction_ipush(assm):
    start = assm.start
    [stop, token1] = reserved('ipush', assm.input, assm.start)
    if token1 is not None:
        [stop, token2] = integer(assm.input, stop)
        if token2 is not None:
            tokens = [token1] + token2
            assm.start = stop
            assm.pos = stop
            assm.code += tokens
            assm.ip += 5
            return True 
    return False

def instruction_spush(assm):
    start = assm.start
    [stop, token1] = reserved('spush', assm.input, assm.start)
    if token1 is not None:
        [stop, token2] = quoted_string(assm.input, stop)
        if token2 is not None:
            assm.code += [token1, assm.cp]
            assm.constants += [token2]
            assm.cp += 1
            assm.start = stop
            assm.pos = stop 
            assm.ip += 2
            return True 
    return False

def instruction_fpush(assm):
    start = assm.start
    [stop, token1] = reserved('fpush', assm.input, assm.start)
    if token1 is not None:
        [stop, token2] = decimal(assm.input, stop)
        if token2 is not None:
            assm.code += [token1, assm.cp]
            assm.constants += [token2]
            assm.cp += 1
            assm.start = stop
            assm.pos = stop 
            assm.ip += 2
            return True 
    return False

def instruction_iconst0(assm):
    [stop, token] = reserved('iconst0', assm.input, assm.start)
    if token is None:
        return False
    
    assm.start = stop
    assm.pos = stop
    assm.code += [token]
    assm.ip += 1
    return True 

def instruction_iconst1(assm):
    [stop, token] = reserved('iconst1', assm.input, assm.start)
    if token is None:
        return False
    
    assm.start = stop
    assm.pos = stop
    assm.code += [token]
    assm.ip += 1
    return True 

def instruction_iconst2(assm):
    [stop, token] = reserved('iconst2', assm.input, assm.start)
    if token is None:
        return False
    
    assm.start = stop
    assm.pos = stop
    assm.code += [token]
    assm.ip += 1
    return True  


def instruction_print(assm):
    [stop, token] = reserved('print', assm.input, assm.start)
    if token is None:
        return False
    
    assm.start = stop
    assm.pos = stop
    assm.code += [token]
    assm.ip += 1
    return True 

def space(string, start = 0):
    ptr = start
    while string[ptr].isspace():
        ptr += 1
    return ptr

def integer(string, start=0):

    ptr = space(string, start)

    if not string[ptr].isdigit():
        return [ptr, None]

    while string[ptr].isdigit():
        ptr += 1 

    value = int(string[start:ptr])
    b0 = (value >> 0 ) & 0xff
    b1 = (value >> 8 ) & 0xff 
    b2 = (value >> 16) & 0xff
    b3 = (value >> 24) & 0xff 
    return [ptr, [b0, b1, b2, b3]]

def comment(assm):
    white_space(assm)
    if peek(assm) == ';':
        while next_char(assm) != '\n':
            pass
        return True
    return False


def quote(string, start = 0):
    ptr = space(string, start)
    if string[ptr] == '\"':
        return [ptr+1, '\"']
    return [start, None]  

def colon(string, start = 0):
    ptr = space(string, start)
    if string[ptr] == ':':
        return [ptr+1, ':']
    return [start, None]  

def semicolon(string, start = 0):
    start = space(string, start)
    ptr = start
    if string[ptr] == ';':
        return [ptr+1, ';']
    return [start, None] 

def period(string, start = 0):
    ptr = space(string, start)
    if string[ptr] == '.':
        return [ptr+1, '.']
    return [start, None] 

def quoted_string(input_string, start=0):
    ptr = space(input_string, start)
    [ptr, token] = quote(input_string, ptr)
    if token is not None:
        [ptr, token_] = string(input_string, ptr)
        if token is not None:
            [ptr, token] = quote(input_string, ptr)
            return [ptr, token_]
    return [start, None]

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
        return [ptr, input_string[start:ptr]]
    return [start, None]

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
        [ptr, token] = integer(string, ptr)
        if token is not None:
            [ptr, token] = period(string,ptr)
            if token is not None:    
                [ptr, token] = integer(string, ptr)
                return [ptr, float(string[start:ptr])]
    return [start, None]

def assemble(source_code=''):
    assm = Assembler(source_code)
    while assm.pos < len(assm.input):
        expression(assm)
        if tail(assm).isspace():
            break
    return assm

def instruction(assm):
    if instruction_ipush(assm):
        return True 
    elif instruction_iadd(assm):
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

def label(assm):
    ptr = assm.start 
    [ptr, token_] = string(assm.input, ptr)
    if token_ is not None:
        [ptr, token] = colon(assm.input, ptr)
        if token is not None:
            assm.labels[token_] = assm.ip
            assm.start = ptr 
            assm.pos = ptr
            return True 
    return False

def comment(assm):
    [ptr, token] = semicolon(assm.input, assm.start)
    if token is not None:
        while assm.input[ptr] != '\n':
            ptr += 1
        assm.start = ptr+1 
        assm.pos = ptr+1
        return True 
    return False

def main():
    src = """ipush 540
             foo:
                ipush 4335
                ipush 45 ; this is a comment
             bar:
                spush "hello"
                fpush 5.0
          """

    a = assemble(src)
    print(a.code)
    print(a.constants)
    print(a.labels)

    assm = Assembler("; this is a test dude\n")
    comment(assm)
    print(assm.pos)
if __name__ == '__main__':
    main()
        


