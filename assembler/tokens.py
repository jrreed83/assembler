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
        self.ip = 0

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

def mark(assm, data=[]):
    marker = {'start': assm.start, 'pos': assm.pos, 'data': data}
    assm.markers += [marker]


def ignore(assm):
    assm.start = assm.pos 

def peek(assm):
    c = next_char(assm)
    rewind(assm)
    return c

def tail(assm):
    return assm.input[assm.start:]

def reserved(keyword, assm):
    white_space(assm)     
    assm.pos = assm.start + len(keyword)    
    if keyword == assm.input[assm.start:assm.pos]:
        if keyword in RESERVED.keys():
            data = RESERVED[keyword]
            mark(assm, data)
        return True
    return False

def match(string, assm):
    white_space(assm)     
    assm.pos = assm.start + len(string)    
    if string == assm.input[assm.start:assm.pos]:
        assm.code += [RESERVED[string]] 
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

def instruction_halt(assm):
    if reserved('halt', assm):
        commit(assm)
        return True
    rollback(assm)
    return False 

def instruction_iadd(assm):
    if reserved('iadd', assm):
        commit(assm)
        return True
    rollback(assm)
    return False 

def instruction_isub(assm):
    if reserved('iadd', assm):
        commit(assm)
        return True
    rollback(assm)
    return False 

def instruction_ipush(assm):
    if reserved('ipush', assm):
        commit(assm)
        if integer(assm):
            return True
    rollback(assm)
    return False 

def instruction_iconst0(assm):
    if reserved('iconst0', assm):
        commit(assm)
        return True
    rollback(assm)
    return False  

def instruction_iconst1(assm):
    if reserved('iconst1', assm):
        commit(assm)
        return True
    rollback(assm)
    return False  

def instruction_iconst2(assm):
    if reserved('iconst2', assm):
        commit(assm)
        return True
    rollback(assm)
    return False  

def instruction_spush(assm):
    if reserved('spush', assm):
        commit(assm)
        if string_with_quotes(assm):
            return True
    rollback(assm)
    return False 

def instruction_fpush(assm):
    if reserved('fpush', assm):
        commit(assm)
        if decimal(assm):
            return True
    rollback(assm)
    return False 

def instruction_print(assm):
    if reserved('print', assm):
        commit(assm)
        return True
    rollback(assm)
    return False 

def integer(assm):
    white_space(assm)
    if not peek(assm).isdigit():
        return False

    while next_char(assm).isdigit():
        pass
    rewind(assm)
    value = int(assm.input[assm.start:assm.pos])
    b0 = (value >> 0 ) & 0xff
    b1 = (value >> 8 ) & 0xff 
    b2 = (value >> 16) & 0xff
    b3 = (value >> 24) & 0xff 

    assm.code += [b0,b1,b2,b3]
    assm.start = assm.pos
    assm.ip += 4
    return True

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
        assm.code += [index] 
        assm.start = assm.pos
        assm.ip += 1
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
        assm.code += [index] 
        assm.start = assm.pos
        assm.ip += 1
        return True
    return False

def assemble(source_code=''):
    assm = Assembler(source_code)
    while assm.pos < len(assm.input):
        expression(assm)
        if tail(assm).isspace():
            break
    return assm

def instruction(assm):
    if match('ipush', assm):               
        if integer(assm):
            return True         
    elif match('iadd', assm):
        return True
    elif match('isub', assm):
        return True
    elif match('imul', assm):
        return True
    elif match('fpush', assm):
        if decimal(assm):
            return True
    elif match('spush', assm):
        if string_with_quotes(assm):
            return True
    elif match('halt', assm):
        return True
    elif match('print', assm):
        return True
    elif match('iconst0', assm):
        return True 
    elif match('iconst1', assm):
        return True 
    elif match('iconst2', assm):
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
             bar:
                iadd 
                imul
                spush "hello"
             foo: 
                fpush 6.56
                iconst2
                print ; this is a test comment
            halt
          """

    a = assemble(src)
    print(a.code)
    print(a.constants)
    print(a.labels)

    assm = Assembler("hello ;\n")
    print(label_ref(assm))
if __name__ == '__main__':
    main()
        


