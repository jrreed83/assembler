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
        [stop, token2] = string(assm.input, stop)
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

def string_with_quotes(assm):
    white_space(assm)
    if next_char(assm) == '\"':
        ignore(assm)
        c = next_char(assm)
        while (c.isalpha() or c.isdigit()):
            c = next_char(assm)
        rewind(assm)
        if c =='\"':
            assm.constants += [assm.input[assm.start:assm.pos]]
            index = len(assm.constants)
            assm.code += [index]   
            assm.start = assm.pos   
            next_char(assm)
            next_char(assm)
            ignore(assm)
            assm.ip += 1
            return True
    return False

def string(string, start=0):
    ptr0 = space(string, start)

    if string[ptr0] == '\"':
        ptr0 += 1
        ptr1 = ptr0
        c = string[ptr1]
        while (c.isalpha() or c.isdigit()):
            ptr1 += 1
            c = string[ptr1] 
        if string[ptr1] == '\"':
            ptr1 += 1
            return [ptr1, string[ptr0: ptr1-1]]
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
    ptr = space(string, start)

    if not string[ptr].isdigit():
        return [ptr, None]

    while string[ptr].isdigit():
        ptr += 1 

    value = float(string[start:ptr])

    return [ptr, value]

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
    #elif label(assm):
    #    return True    
    #elif comment(assm):
    #    return True
    else:
        return False

def label(assm):
    white_space(assm)
    while next_char(assm).isalpha():
        pass
    rewind(assm)
    if peek(assm) == ':':        
        assm.labels[assm.input[assm.start:assm.pos]] = assm.ip
        next_char(assm)
        ignore(assm)
        return True
    assm.pos = assm.start
    return False

def main():
    src = """ipush 540
             ipush 4335
             ipush 45
          """

    a = assemble(src)
    print(a.code)
    print(a.constants)
    print(a.labels)

    assm = Assembler("hello ;\n")

if __name__ == '__main__':
    main()
        


