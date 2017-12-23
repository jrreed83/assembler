import io

RESERVED = [
    'nop',
    'halt',
    'iadd',
    'isub',
    'imul',
    'iconst0',
    'iconst1',  
    'iconst2',
    'ipush',
    'print'      
]



class Token:
    def __init__(self, tag='NOP', txt=None):
        self.tag = tag
        self.txt = txt
    def __str__(self):
        if self.txt is not None:
            return '[{0} {1}]'.format(self.tag, self.txt)
        else:
            return '[{0}]'.format(self.tag)
    def __repr__(self):
        return self.__str__()    

class Lexer:
    def __init__(self, stream = None, reserved = []):
        self.sid = stream
        self.reserved = reserved
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
            if buffer in self.reserved:
                return Token(buffer.upper())
            else: 
                return Token('WORD', buffer)
        elif peek.isdigit():
            buffer = peek
            peek = self.next_char()
            while peek.isdigit():
                buffer += peek 
                peek = self.next_char()
            return Token('NUMBER', buffer)           

if __name__ == '__main__':
    lexer = Lexer(io.StringIO('ipush 7 halt'), RESERVED)
    word = lexer.next_token()
    print(word)
    word = lexer.next_token()
    print(word)
    word = lexer.next_token()
    print(word)    
        
        


