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
            return '[{0} {1}]'.format(self.tag[0], self.txt)
        else:
            return '[{0}: {1}]'.format(self.tag[0], self.tag[1])
    def __repr__(self):
        return self.__str__()    
    def __eq__(self,that):
        return (self.tag == that.tag) and (self.txt == that.txt)

class Lexer:
    def __init__(self, input=''):
        self.reserved = {}
        self.pos = 0
        self.input = input
        self.line = 0
    def __repr__(self):
        return '[{0}]'.format(self.pos)

def peek(lexer):
    return lexer.input[lexer.pos]

def forward(lexer):
    lexer.pos += 1

def back(lexer):
    lexer.pos -= 1

def white_space(lexer):
    while True:
        if peek(lexer) ==  ' ' or peek(lexer) == '\t':
            forward(lexer)
        elif peek(lexer) == '\n':
            forward(lexer)
            lexer.line += 1
        else:
            break

def number(lexer):
    ptr = lexer.pos
    if not lexer.input[ptr].isdigit():
        return None 
    ptr += 1 

    while True: 
        if lexer.input[ptr].isdigit():
            ptr += 1
        else:
            token = Token(tag = NUMBER, txt = lexer.input[lexer.pos:lexer.pos+ptr])
            lexer.pos = ptr
            break
    return token 

def match(string, lexer):
    if lexer.input[lexer.pos:lexer.pos+len(string)] == string:
        lexer.pos += len(string)
        if string in RESERVED.keys():
            return Token(tag = RESERVED[string])
        else:
            return Token(tag = WORD, txt = string)
    else:
        return None
       

if __name__ == '__main__':
    lexer = Lexer('iconst0haltfoo')
    tok1 = match('iconst0', lexer)
    tok2 = match('halt',lexer)
    tok3 = match('foo', lexer)
    print([tok1, tok2, tok3])
        
        


