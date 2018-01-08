from assembler.parser import *

def test_string():
    s = stream(""" "hello" """)
    s, token = quoted_string(s)
    assert token == (Type.STRING, 'hello')
    assert s['ptr'] ==  8 

def test_comment():
    s = stream('; this is a comment\n')
    s, token = comment(s)
    assert token == True
    assert s['ptr'] ==  19

def test_label():
    s = stream('test:\n')
    s, token = label(s)    
    assert token == (Type.LABEL, 'test')
    assert s['ptr'] == 5

def test_iadd(): 
    s = stream('iadd\n')
    s, token = operation(s)    
    assert token == Op.IADD
    assert s['ptr'] == 4

def test_integer():
    s = stream('235\n')
    s, token = integer(s)    
    assert token == (Type.INTEGER, '235')
    assert s['ptr'] == 3

def test_decimal():
    s = stream('2.35\n')
    s, token = decimal(s)    
    assert token == (Type.DECIMAL, '2.35')    
    assert s['ptr'] == 4

def test_ipush():
    s = stream('ipush\n')
    s, token = operation(s)    
    assert token == Op.IPUSH
    assert s['ptr'] == 5

def test_print():
    s = stream('print\n')
    s, token = operation(s)    
    assert token == Op.PRINT
    assert s['ptr'] == 5

def test_failed_op():
    assert operation('foo\n', 0) == (0, None)

def test_failed_statement():
    assert statement('foo:\n     ', 0) == (0, None)    