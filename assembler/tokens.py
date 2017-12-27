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

    def __repr__(self):
        return '[{0}]'.format(self.pos)


def next_char(lexer):
    if assm.pos >= len(assm.input):
        raise EOFError('There are no more characters')
    else:
        c = assm.input[assm.pos]
        assm.pos += 1
        assm.start = assm.pos
        return c

def rewind(assm):
    assm.pos -= 1 
    assm.start = assm.pos

def ignore(assm):
    assm.start = assm.pos 

def peek(assm):
    c = next_char(assm)
    rewind(assm)
    return c

def at_front(to_match, assm):
    if to_match == assm.input[assm.start:assm.start+len(to_match)]:
        return True 
    else:
        return False

def iconst0(assm): 
    to_match = 'iconst0'
    if at_front(to_match, assm):
        assm.start += len(to_match)
        assm.pos = assm.start
        assm.op_codes += [ICONST0]
        return True 
    return False

def iconst1(assm): 
    to_match = 'iconst1'
    if at_front(to_match, assm):
        assm.start += len(to_match)
        assm.pos = assm.start
        assm.op_codes += [ICONST1]
        return True 
    return False

def iconst2(assm): 
    to_match = 'iconst2'
    if at_front(to_match, assm):
        assm.start += len(to_match)
        assm.pos = assm.start
        assm.op_codes += [ICONST2]
        return True 
    return False

def iadd(assm): 
    to_match = 'iadd'
    if at_front(to_match, assm):
        assm.start += len(to_match)
        assm.pos = assm.start
        assm.op_codes += [IADD]
        return True 
    return False

def isub(assm): 
    to_match = 'isub'
    if at_front(to_match, assm):
        assm.start += len(to_match)
        assm.pos = assm.start
        assm.op_codes += [ISUB]     
        return True 
    return False

def ipush(assm):
    to_match = 'ipush'
    if at_front(to_match, assm):
        assm.start += len(to_match)
        assm.pos = assm.start
        assm.op_codes += [IPUSH] 
        return True 
    return False

def halt(assm): 
    white_space(assm)
    to_match = 'halt'
    if at_front(to_match, assm):
        assm.start += len(to_match)
        assm.pos = assm.start
        assm.op_codes += [HALT]
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

def number(assm):
    white_space(assm)
    if not peek(assm).isdigit():
        return None 
    assm.pos += 1 

    while assm.pos < len(assm.input): 
        if assm.input[assm.pos].isdigit() or (assm.input[assm.pos] == '.'):
            assm.pos += 1
        else:
            n = assm.input[assm.start:assm.pos]
            assm.op_codes += [int(n)]
            assm.start = assm.pos
            break 


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
    assm = Assembler('ipush 43 halt\n')


    ipush(assm)  
    number(assm)
    halt(assm)
    print(assm.op_codes)
    print(assm.start)
    print(assm.pos)

        


