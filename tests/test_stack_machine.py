from assembler.tokens import *

def test_isub():
    assm = Assembler('isub\n')
    match('isub', assm)
    assert assm.pos == 4
    assert assm.ip == 1 
    assert assm.code == [ISUB]

def test_comment():
    string = '; this is a comment\n'
    assm = Assembler('{0} next'.format(string))
    comment(assm)
    assert assm.ip == 0
    assert assm.pos == len(string)

def test_instruction_iadd():
    assm = Assembler('iadd\n')
    instruction_iadd(assm)
    assert assm.pos == 4
    assert assm.ip == 1 
    assert assm.code == [IADD]

def test_instruction_ipush():
    assm = Assembler('ipush 56\n')
    instruction_ipush(assm)
    assert assm.pos == 8
    assert assm.ip == 5 
    assert assm.code == [IPUSH, 56, 0, 0, 0]

def test_instruction_print():
    assm = Assembler('print\n')
    instruction_print(assm)
    assert assm.pos == 5
    assert assm.ip == 1 
    assert assm.code == [PRINT]    