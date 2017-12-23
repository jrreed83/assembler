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
    def __init__(self, reserved = None, what_to_lex = {}):
        self.reserved = reserved        
        if type(what_to_lex) is str:
            self.sid = io.StringIO(what_to_lex)
        elif type(what_to_lex) is io.StringIO:
            self.sid = what_to_lex 
        else:
            raise Exception('Bad input')
    def next_char(self):
        return self.sid.read(1) 
    def next_token(self):
        peek = self.next_char() 
        while peek.isspace():
            peek = self.next_char()
        if peek.isalpha():
            buffer = peek
            peek = self.next_char()
            while peek.isalpha():
                buffer += peek 
                peek = self.next_char()
            if buffer in self.reserved.keys():
                return Token(self.reserved[buffer])
            else: 
                return Token(WORD, buffer)
        elif peek.isdigit():
            buffer = peek
            peek = self.next_char()
            while peek.isdigit():
                buffer += peek 
                peek = self.next_char()
            return Token(NUMBER, buffer)           

if __name__ == '__main__':
    lexer = Lexer(RESERVED, 'ipush 7 halt')
    word = lexer.next_token()
    print(word)
    word = lexer.next_token()
    print(word)
    word = lexer.next_token()
    print(word)    
        
        


