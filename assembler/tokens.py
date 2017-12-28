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

def tail(assm):
    return assm.input[assm.start:]

def iconst0(assm): 
    to_match = 'iconst0'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [ICONST0]
        assm.ip += 1
        assm.start = assm.pos
        return True
    else:
        return False

def iconst1(assm): 
    to_match = 'iconst1'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [ICONST1]
        assm.ip += 1   
        assm.start = assm.pos          
        return True 
    else:
        return False

def iconst2(assm): 
    to_match = 'iconst2'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [ICONST2]
        assm.ip += 1      
        assm.start = assm.pos            
        return True 
    return False

def iadd(assm): 
    to_match = 'iadd'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [IADD]
        assm.ip += 1        
        assm.start = assm.pos
        return True 
    return False

def isub(assm): 
    to_match = 'isub'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [ISUB]    
        assm.ip += 1  
        assm.start = assm.pos               
        return True 
    return False

def ipush(assm):
    to_match = 'ipush'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [IPUSH] 
        assm.ip += 1       
        assm.start = assm.pos           
        return True 
    return False

def spush(assm):
    to_match = 'spush'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [SPUSH] 
        assm.ip += 1   
        assm.start = assm.pos               
        return True 
    return False

def fpush(assm):
    to_match = 'fpush'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [FPUSH] 
        assm.ip += 1   
        assm.start = assm.pos               
        return True 
    return False

def halt(assm): 
    white_space(assm)
    to_match = 'halt'
    assm.pos = assm.start + len(to_match)    
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [HALT]
        assm.ip += 1     
        assm.start = assm.pos             
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

def char_buffer(string, accept = lambda x: x.isalpha() or x.isdigit()):
    for i,c in enumerate(string):
        if not accept(c):
            break
    return string[:i]

def integer(assm):
    white_space(assm)

    if not peek(assm).isdigit():
        return False

    buffer = ''
    c = next_char(assm)
    buffer += c
    while c.isdigit():
        buffer += c 
        c = next_char(assm)
    rewind(assm)
    assm.op_codes += [int(buffer)]
    commit(assm)
    return True



def string(assm):
    white_space(assm)
    if next_char(assm) == '\'':
        buffer = ''
        c = next_char(assm)
        while (c.isalpha() or c.isdigit()):
            buffer += c 
            c = next_char(assm)
        if c =='\'':
            assm.constant_pool += [buffer]
            index = len(assm.constant_pool)
            assm.op_codes += [index]   
            commit(assm)     
            return True
    return False

def decimal(assm):
    white_space(assm)

    if peek(assm) == '.':
        buffer = '0.'
        next_char(assm)
        c = next_char(assm)
        while c.isdigit():
            buffer += c 
            c = next_char(assm)
        rewind(assm)
        assm.constant_pool += [float(buffer)]
        index = len(assm.constant_pool)
        assm.op_codes += [index] 
        commit(assm)
    elif peek(assm).isdigit():
        buffer = ''
        c = next_char(assm)
        while c.isdigit():
            buffer += c 
            c = next_char(assm)
        if c == '.':
            buffer += '.'
            c = next_char(assm)
            while c.isdigit():
                buffer += c 
                c = next_char(assm)            
        rewind(assm)
        assm.constant_pool += [float(buffer)]
        index = len(assm.constant_pool)
        assm.op_codes += [index] 
        commit(assm)

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
    assm = Assembler("fpush 7.123 \n")

    if fpush(assm):
        if decimal(assm):
            pass
    print(assm.op_codes)
    print(assm.constant_pool)
    print(assm.start)
    print(assm.pos)

        


