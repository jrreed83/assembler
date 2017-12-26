import io

NOP = ('NOP', 0)
HALT = ('HALT', 1)
IADD = ('IADD', 2)
ISUB = ('ISUB', 3)
IMUL = ('IMUL', 4)
ICONST0 = ('ICONST0', 5)
ICONST1 = ('ICONST1', 6)
ICONST2 = ('ICONST2', 7)
IPUSH = ('IPUSH', 8)
PRINT = ('PRINT', 9)
NUMBER = ('NUMBER',)
WORD = ('WORD',)
LABEL = ('LABEL',)

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



class Token:
    def __init__(self, tag=NOP, txt=None):
        self.tag = tag
        self.txt = txt
    def __str__(self):
        if self.txt is not None:
            return '{0} {1}'.format(self.tag[0], self.txt)
        else:
            return '{0}'.format(self.tag[0])
    def __repr__(self):
        return self.__str__()    
    def __eq__(self,that):
        return (self.tag == that.tag) and (self.txt == that.txt)

class Lexer:
    def __init__(self, input=''):
        self.reserved = {}
        self.pos = 0
        self.start = 0
        self.input = input
        self.line = 0
        self.tokens = []
    def __repr__(self):
        return '[{0}]'.format(self.pos)


def next_char(lexer):
    if lexer.pos >= len(lexer.input):
        return {'error': 'end of file'} 
    else:
        c = lexer.input[lexer.pos]
        lexer.pos += 1
        lexer.start = lexer.pos
        return c

def rewind(lexer):
    lexer.pos -= 1 
    lexer.start = lexer.pos

def ignore(lexer):
    lexer.start = lexer.pos 

def peek(lexer):
    c = next_char(lexer)
    rewind(lexer)
    return c

def at_front(to_match, lexer):
    if to_match == lexer.input[lexer.start:lexer.start+len(to_match)]:
        return True 
    else:
        return False

def iconst0(lexer): 
    to_match = 'iconst0'
    if at_front(to_match, lexer):
        lexer.start += len(to_match)
        lexer.pos = lexer.start
        lexer.tokens += [ICONST0[1]]

def iconst1(lexer): 
    to_match = 'iconst1'
    if at_front(to_match, lexer):
        lexer.start += len(to_match)
        lexer.pos = lexer.start
        lexer.tokens += [ICONST1[1]]

def iconst2(lexer): 
    to_match = 'iconst2'
    if at_front(to_match, lexer):
        lexer.start += len(to_match)
        lexer.pos = lexer.start
        lexer.tokens += [ICONST2[1]]

def iadd(lexer): 
    to_match = 'iadd'
    if at_front(to_match, lexer):
        lexer.start += len(to_match)
        lexer.pos = lexer.start
        lexer.tokens += [IADD[1]]

def isub(lexer): 
    to_match = 'isub'
    if at_front(to_match, lexer):
        lexer.start += len(to_match)
        lexer.pos = lexer.start
        lexer.tokens += [ISUB[1]]     

def ipush(lexer):
    to_match = 'ipush'
    if at_front(to_match, lexer):
        lexer.start += len(to_match)
        lexer.pos = lexer.start
        lexer.tokens += [IPUSH[1]] 

        number(lexer)


def halt(lexer): 
    white_space(lexer)
    to_match = 'halt'
    if at_front(to_match, lexer):
        lexer.start += len(to_match)
        lexer.pos = lexer.start
        lexer.tokens += [HALT[1]]

def white_space(lexer):
    c = next_char(lexer)    
    while c.isspace():
        c = next_char(lexer) 
    rewind(lexer)
    lexer.start = lexer.pos

def number(lexer):
    white_space(lexer)
    if not lexer.input[lexer.pos].isdigit():
        return None 
    lexer.pos += 1 

    while lexer.pos < len(lexer.input): 
        if lexer.input[lexer.pos].isdigit() or (lexer.input[lexer.pos] == '.'):
            lexer.pos += 1
        else:
            number = lexer.input[lexer.start:lexer.pos]
            lexer.tokens += [number]
            lexer.start = lexer.pos
            break 


def label(lexer):
    while True:
        if lexer.input[lexer.pos] != ':':
            lexer.pos += 1
        else:
            token = Token(tag = LABEL, txt = lexer.input[lexer.start:lexer.pos])
            lexer.start = lexer.pos+1            
            lexer.tokens += [token]
            break 

def match(lexer, string):
    if lexer.input[lexer.start:lexer.start+len(string)] == string:
        lexer.start += len(string)

        if string in RESERVED.keys():
            token = Token(tag = RESERVED[string])
            lexer.tokens += [token]
        else:
            token = Token(tag = WORD, txt = string)
            lexer.tokens += [token]

STATES = {
    'number': number,
    'label': label
}       

if __name__ == '__main__':
    lexer = Lexer('ipush 43 halt\n')


    ipush(lexer)
    halt(lexer)
    print(lexer.tokens)
    print(lexer.start)
    print(lexer.pos)

        


