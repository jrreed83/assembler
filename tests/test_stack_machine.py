from assembler.parser import *

def test_string():
    assert quoted_string(""" "hello" """) == Result(8, 'hello')

def test_comment():
    assert comment('; this is a comment\n', 0) == Result(19, True)

def test_label():
    assert label('test:\n', 0) == Result(5, 'test')

def test_instruction_iadd(): 
    assert instruction_iadd('iadd\n', 0) == Result(4, IADD)

def test_integer():
    assert integer('235\n') == Result(3, 235)

def test_instruction_ipush():
    assert instruction_ipush('ipush 5635\n', 0) == Result(10, [IPUSH, 5635])

def test_instruction_print():
    assert instruction_print('print\n', 0) == Result(5, PRINT) 