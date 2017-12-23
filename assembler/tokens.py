class Tag:
    NOP = 'NOP'
    HALT = 'HALT'
    IADD = 'IADD'
    ISUB = 'ISUB'
    IMUL = 'IMUL'
    ICONST0 = 'ICONST0'
    ICONST1 = 'ICONST1'
    ICONST2 = 'ICONST2'
    PRINT = 'PRINT'
    NUMBER = 'NUMBER'

class Token:
    def __init__(self, tag=Tag.NOP, txt=None):
        self.tag = tag
        self.txt = txt
    def __str__(self):
        if self.txt is not None:
            return '<{0}, {1}>'.format(self.tag, self.txt)
        else:
            return '<{0}>'.format(self.tag)
    def __repr__(self):
        return self.__str__()    
