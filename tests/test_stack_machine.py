from assembler.parser import *

def test_string():
    assert quoted_string(""" "hello" """) == (8, (Type.STRING, 'hello'))

def test_comment():
    assert comment('; this is a comment\n', 0) == (19, True)

def test_label():
    assert label('test:\n', 0) == (5, (Type.LABEL, 'test'))

def test_iadd_op(): 
    assert iadd_op('iadd\n', 0) == (4, Op.IADD)

def test_integer():
    assert integer('235\n') == (3, (Type.INTEGER, '235'))

def test_ipush_op():
    assert ipush_op('ipush 5635\n', 0) == (5, Op.IPUSH)

def test_print_op():
    assert print_op('print\n', 0) == (5, Op.PRINT) 