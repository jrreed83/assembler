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
SPUSH = 10

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
}


class Assembler:
    def __init__(self, input=''):
        self.reserved = {}
        self.pos = 0
        self.start = 0
        self.input = input
        self.line = 0
        self.op_codes = []
        self.constant_pool = []
        self.ip = 0

    def __repr__(self):
        return '[{0}]'.format(self.pos)


def next_char(lexer):
    if assm.pos >= len(assm.input):
        raise EOFError('There are no more characters')
    else:
        c = assm.input[assm.pos]
        assm.pos += 1
        return c

def rewind(assm):
    assm.pos -= 1 

def rollback(assm):
    assm.pos = assm.start 

def commit(assm):
    assm.start = assm.pos 

def ignore(assm):
    assm.start = assm.pos 

def peek(assm):
    c = next_char(assm)
    rewind(assm)
    return c

def at_front(to_match, assm):
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        commit(assm)
        return True
    else:
        rollback(assm)
        return False

def iconst0(assm): 
    to_match = 'iconst0'
    if at_front(to_match, assm):
        assm.op_codes += [ICONST0]
        assm.ip += 1
        return True
    else:
        return False

def iconst1(assm): 
    to_match = 'iconst1'
    if at_front(to_match, assm):
        assm.op_codes += [ICONST1]
        assm.ip += 1        
        return True 
    else:
        return False

def iconst2(assm): 
    to_match = 'iconst2'
    if at_front(to_match, assm):
        assm.op_codes += [ICONST2]
        assm.ip += 1        
        return True 
    return False

def iadd(assm): 
    to_match = 'iadd'
    if at_front(to_match, assm):
        assm.op_codes += [IADD]
        assm.ip += 1        
        return True 
    return False

def isub(assm): 
    to_match = 'isub'
    if at_front(to_match, assm):
        assm.op_codes += [ISUB]    
        assm.ip += 1         
        return True 
    return False

def ipush(assm):
    to_match = 'ipush'
    if at_front(to_match, assm):
        assm.op_codes += [IPUSH] 
        assm.ip += 1        
        return True 
    return False

def spush(assm):
    to_match = 'spush'
    if at_front(to_match, assm):
        assm.op_codes += [SPUSH] 
        assm.ip += 1        
        return True 
    return False

def halt(assm): 
    white_space(assm)
    to_match = 'halt'
    if at_front(to_match, assm):
        assm.op_codes += [HALT]
        assm.ip += 1        
        return True 
    return False

def white_space(assm):
    c = next_char(assm)    
    while c.isspace():
        c = next_char(assm) 
        if c == '\n':
            assm.line += 1
    rewind(assm)
    assm.start = assm.pos

def char_buffer(assm, term = lambda x: x.isspace()):
    buffer = ''
    c = next_char(assm)
    while not term(c):
        buffer += c
        c = next_char(assm)
    rewind(assm)
    return buffer 

def iconst(assm):
    white_space(assm)
    buffer = char_buffer(assm)
    assm.op_codes += [int(buffer)]
    assm.ip += 1    
    return True

def sconst(assm):
    white_space(assm)
    buffer = char_buffer(assm)
    string = buffer[1:len(buffer)-1]
    assm.constant_pool += [string]
    index = len(assm.constant_pool)
    assm.op_codes += [index]    
    return True

def fconst(assm):
    white_space(assm)
    buffer = char_buffer(assm)
    assm.constant_pool += [float(buffer)]
    index = len(assm.constant_pool)
    assm.op_codes += [index]    
    return True



# def label(assm):
#     while True:
#         if assm.input[assm.pos] != ':':
#             assm.pos += 1
#         else:
#             token = Token(tag = LABEL, txt = assm.input[assm.start:assm.pos])
#             assm.start = assm.pos+1            
#             assm.op_codes += [token]
#             break 
      

if __name__ == '__main__':
    assm = Assembler('spush \'hello\'\n')

    if spush(assm):
        if sconst(assm):
            pass
    print(assm.op_codes)
    print(assm.constant_pool)
    print(assm.start)
    print(assm.pos)

        


