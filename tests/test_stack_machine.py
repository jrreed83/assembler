from assembler.parser import *

def test_string():
    s = stream(""" "hello" """)
    _, token = quoted_string(s)
    assert token == (Type.STRING, 'hello')

def test_comment():
    s = stream('; this is a comment\n')
    _, token = comment(s)
    assert token == True

def test_label():
    s = stream('test:\n')
    _, token = label(s)    
    assert token == (Type.LABEL, 'test')

def test_iadd(): 
    s = stream('iadd\n')
    _, token = operation(s)    
    assert token == Op.IADD

def test_integer():
    s = stream('235\n')
    _, token = integer(s)    
    assert token == (Type.INTEGER, '235')

def test_decimal():
    s = stream('2.35\n')
    _, token = decimal(s)    
    assert token == (Type.DECIMAL, '2.35')    

def test_ipush():
    assert operation('ipush 5635\n', 0) == (5, Op.IPUSH)

def test_print():
    assert operation('print\n', 0) == (5, Op.PRINT) 

def test_failed_op():
    assert operation('foo\n', 0) == (0, None)

def test_failed_statement():
    assert statement('foo:\n     ', 0) == (0, None)    