from assembler.parser import *

def test_string():
    assert quoted_string(""" "hello" """) == (8, (Type.STRING, 'hello'))

def test_comment():
    assert comment('; this is a comment\n', 0) == (19, True)

def test_label():
    assert label('test:\n', 0) == (5, (Type.LABEL, 'test'))

def test_iadd(): 
    assert operation('iadd\n', 0) == (4, Op.IADD)

def test_integer():
    assert integer('235\n') == (3, (Type.INTEGER, '235'))

def test_decimal():
    assert decimal('2.35\n') == (4, (Type.DECIMAL, '2.35'))

def test_ipush():
    assert operation('ipush 5635\n', 0) == (5, Op.IPUSH)

def test_print():
    assert operation('print\n', 0) == (5, Op.PRINT) 

def test_failed_op():
    assert operation('foo\n', 0) == (0, None)

def test_failed_statement():
    assert statement('foo\n     ', 0) == (0, None)    