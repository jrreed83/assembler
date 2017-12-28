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
SHOW = 9
FPUSH = 10
SPUSH = 11

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
    'show': SHOW,      
}

class Assembler:
    def __init__(self, input=''):
        self.reserved = {}
        self.pos = 0
        self.start = 0
        self.input = input
        self.line = 0
        self.op_codes = []
        self.constants = []
        self.labels = {}
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
    assm.op_codes += [assm.input[assm.start:assm.pos]]
    assm.ip += 1
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
    white_space(assm)     
    to_match = 'iconst0'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [ICONST0]
        assm.ip += 1
        assm.start = assm.pos
        return True
    assm.pos = assm.start
    return False

def show(assm): 
    white_space(assm)    
    to_match = 'show'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [SHOW]
        assm.ip += 1
        assm.start = assm.pos
        return True
    assm.pos = assm.start
    return False

def iconst1(assm): 
    white_space(assm)     
    to_match = 'iconst1'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [ICONST1]
        assm.ip += 1   
        assm.start = assm.pos          
        return True 
    assm.pos = assm.start
    return False

def iconst2(assm): 
    white_space(assm)     
    to_match = 'iconst2'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [ICONST2]
        assm.ip += 1      
        assm.start = assm.pos            
        return True 
    assm.pos = assm.start
    return False

def iadd(assm): 
    white_space(assm)     
    to_match = 'iadd'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [IADD]
        assm.ip += 1        
        assm.start = assm.pos
        return True 
    assm.pos = assm.start
    return False

def isub(assm): 
    white_space(assm)     
    to_match = 'isub'
    assm.pos = assm.start + len(to_match)   
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [ISUB]    
        assm.ip += 1  
        assm.start = assm.pos               
        return True 
    assm.pos = assm.start
    return False

def ipush(assm):
    white_space(assm)     
    to_match = 'ipush'
    assm.pos = assm.start + len(to_match)    
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [IPUSH] 
        assm.ip += 1       
        assm.start = assm.pos           
        return True 
    assm.pos = assm.start
    return False

def spush(assm):
    white_space(assm)     
    to_match = 'spush'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [SPUSH] 
        assm.ip += 1   
        assm.start = assm.pos               
        return True 
    assm.pos = assm.start
    return False

def fpush(assm):
    white_space(assm)    
    to_match = 'fpush'
    assm.pos = assm.start + len(to_match)
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [FPUSH] 
        assm.ip += 1   
        assm.start = assm.pos               
        return True 
    assm.pos = assm.start
    return False

def halt(assm): 
    white_space(assm)
    to_match = 'halt'
    assm.pos = assm.start + len(to_match)
    print(assm.input[assm.start:assm.pos])         
    if to_match == assm.input[assm.start:assm.pos]:
        assm.op_codes += [HALT]
        assm.ip += 1     
        assm.start = assm.pos             
        return True 
    assm.pos = assm.start
    return False

def white_space(assm):
    c = next_char(assm)    
    if c == '\n':
        assm.line += 1
    while c.isspace():
        c = next_char(assm) 
        if c == '\n':
            assm.line += 1
    rewind(assm)
    assm.start = assm.pos

def integer(assm):
    white_space(assm)

    if not peek(assm).isdigit():
        return False

    while next_char(assm).isdigit():
        pass
    rewind(assm)
    assm.op_codes += [int(assm.input[assm.start:assm.pos])]
    assm.start = assm.pos
    return True

def string(assm):
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
            assm.op_codes += [index]   
            assm.start = assm.pos   
            next_char(assm)
            next_char(assm)
            ignore(assm)
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
        assm.constants += [float(buffer)]
        index = len(assm.constants)
        assm.op_codes += [index] 
        assm.start = assm.pos
        return True
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
        assm.constants += [float(buffer)]
        index = len(assm.constants)
        assm.op_codes += [index] 
        assm.start = assm.pos
        return True
    return False

def instruction(assm):
    if ipush(assm):
        integer(assm)
        return 0
    elif iadd(assm):
        return 0
    elif isub(assm):
        return 0
    elif spush(assm):
        string(assm)
        return 0
    elif halt(assm):
        return 0
    elif label(assm):
        return 0
    elif show(assm):
        return 0

def label(assm):
    white_space(assm)
    while next_char(assm).isalpha():
        pass
    rewind(assm)
    if peek(assm) == ':':        
        assm.labels[assm.input[assm.start:assm.pos]] = assm.line
        next_char(assm)
        ignore(assm)
        return True
    return False

if __name__ == '__main__':
    assm = Assembler("""spush "hello" 
                        ipush 56
                        foo: 
                        iadd 
                        isub
                        halt
                        show
                        spush "world"
                    """)

    instruction(assm)
    instruction(assm)
    instruction(assm)
    instruction(assm)
    instruction(assm)
    instruction(assm)
    instruction(assm)
    instruction(assm)
    print(assm.op_codes)
    print(assm.constants)
    print(assm.start)
    print(assm.pos)
    print(assm.labels)
    print(tail(assm))
        


