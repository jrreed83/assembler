from assembler.parser import *

def test_string():
    n, token = quoted_string(""""hello"\n""")
    assert (n, token) == (7, (Type.STRING, 'hello'))

def test_comment():
    n, token = comment('; this is a comment\n')
    assert (n, token) == (19, True)

def test_label():
    n, token = label('test:\n')    
    assert (n, token) == (5, (Type.LABEL, 'test'))

def test_iadd(): 
    n, token = operation('iadd\n')    
    assert (n, token) == (4, Op.IADD)

def test_integer():
    n, token = integer('235\n')    
    assert (n, token) == (3, (Type.INTEGER, '235'))

def test_decimal():
    n, token = decimal('2.35\n')    
    assert (n, token) == (4, (Type.DECIMAL, '2.35'))

def test_ipush():
    n, token = operation('ipush\n')    
    assert (n, token) == (5, Op.IPUSH)

def test_print():
    n, token = operation('print\n')    
    assert (n, token) == (5, Op.PRINT)
  