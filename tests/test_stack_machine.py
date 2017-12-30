from assembler.tokens import *

def test_isub():
    assm = Assembler('isub\n')
    match('isub', assm)
    assert assm.pos == 4
    assert assm.ip == 1 
    assert assm.op_codes[0] == ISUB

def test_comment():
    string = '; this is a comment\n'
    assm = Assembler('{0} next'.format(string))
    comment(assm)
    assert assm.ip == 0
    assert assm.pos == len(string)
