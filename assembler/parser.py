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



def reserved(keyword, string):
    n = len(keyword)   
    if keyword == string[0:n]:
        token = RESERVED.get(keyword, None)
        if token is not None:
            return (n, token)
    return (0, None)

def operation(string):
    for key in RESERVED.keys():
        n, token = reserved(key, string)
        if token is not None:
            return (n, token)
    return (0, None)

def statement(string):

    n, token = operation(string)
    if token is not None:
        return (n, token)

    n, token = comment(string)
    if token is not None:
        return (n, token)

    n, token = label(string)
    if token is not None:
        return (n, token)

    return (0, None)    

def white_space(string):
    consumed = 0
    new_lines = 0
    for i, c in enumerate(string):
        if c == '\n':
            new_lines += 1
        if not c.isspace():
            break
    consumed = i
    return consumed, new_lines

def integer(string):
    buffer = []
    for i, c in enumerate(string):
        if c.isdigit():
            buffer += [c]
        else:
            break

    if len(buffer) == 0:
        return (0, None)
    else:
        return (i, (Type.INTEGER, ''.join(buffer)))        


def match(char, string):
    head, *tail = string
    return (1, char) if head == char else (0, None)


def quoted_string(string_):

    consumed = 0
    n, _ = match('\"', string_)
    if n == 0:
        return (0, None)
    consumed += n 

    n, token = string(string_[consumed:])
    if token is None:
        return (0, None)
    consumed += n 

    n, _ = match('\"', string_[consumed:])
    if n == 0:
        return (0, None)
    consumed += n

    return (consumed, token)
    

def string(string_):
    
    consumed = 0
    c = string_[0]
    if not c.isalpha():
        return (0, None)
    consumed += 1
    c = string_[consumed]
    while c.isalpha() or c.isdigit():
        consumed += 1
        c = string_[consumed]
    val = string_[0:consumed]
    return (consumed, (Type.STRING, val))

def decimal(string):
    consumed = 0

    n, _ = integer(string)
    if n == 0:
        return (n, None)
    consumed += n

    n, _ = match('.', string[consumed:])
    if n == 0:    
        return (n, None)
    consumed += n 

    n, _ = integer(string[consumed:])
    if n == 0:
        return (n, None)  
    consumed += n  
    
    number = string[0:consumed]
    return (consumed, (Type.DECIMAL, number))

def label(string_):
    for c in string_:
        if c == ':':
            break
    else:
        return (0, None)

    consumed = 0

    n, token = string(string_)
    if token is None:
        return (0, None)
    
    _, label = token 
    consumed += n 

    n, token = match(':', string_[consumed:])
    if token is None: 
        return (0, None)
    consumed += n 

    return (consumed, (Type.LABEL, label))


def comment(string):
    n, token = match(';', string)
    if token is None: 
        return (0, None)
    for i, c in enumerate(string):
        if c == '\n':
            break 
    return (i, True)

def tokenize(string):
    action = statement
    tokens = []
    line_num = 1
    while not string.isspace():
        ptr, new_lines = white_space(string)
        line_num += new_lines
        string = string[ptr:]
        ptr, tok = action(string)
        if tok is None:
            raise ValueError('Lexing error on Line {}'.format(line_num))
        tokens += [tok]
        string = string[ptr:]

        if tok == Op.IPUSH:
            action = integer 
        elif tok == Op.FPUSH:
            action = decimal 
        elif tok == Op.SPUSH:
            action = quoted_string
        elif tok == Op.JUMP:
            action = string
        else:
            action = statement
    return tokens


