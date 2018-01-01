from assembler.parser import *


def test_string():
    assert quoted_string(""" "hello" """) == [8, 'hello']

def test_comment():
    x = '; this is a comment\n'
    assm = Assembler('{0} next'.format(x))
    comment(assm)
    assert assm.ip == 0
    assert assm.pos == len(x)

def test_label():
    x = 'test:\n'
    assm = Assembler(x)
    label(assm)
    assert assm.labels == {'test':0}

def test_instruction_iadd():
    assm = Assembler('iadd\n')
    instruction_iadd(assm)
    assert assm.pos == 4
    assert assm.ip == 1 
    assert assm.code[0:1] == [IADD]

def test_integer():
    assert integer('235\n') == [3, [235, 0, 0, 0]]

def test_instruction_ipush():
    assm = Assembler('ipush 56\n')
    instruction_ipush(assm)
    assert assm.pos == 8
    assert assm.ip == 5 
    assert assm.code[0:5] == [IPUSH, 56, 0, 0, 0]

def test_instruction_spush():
    assm = Assembler("""spush "hello"\n""")
    instruction_spush(assm)
    assert assm.pos == 13
    assert assm.ip == 2 
    assert assm.code[0:2] == [SPUSH, 0]
    assert assm.constants == ['hello']
    assert assm.cp == 1 

def test_instruction_print():
    assm = Assembler('print\n')
    instruction_print(assm)
    assert assm.pos == 5
    assert assm.ip == 1 
    assert assm.code[0:1] == [PRINT]    