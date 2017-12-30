from assembler.tokens import *

def test_isub():
    assm = Assembler('isub\n')
    match('isub', assm)
    assert assm.pos == 4
    assert assm.ip == 1 
    assert assm.op_codes[0] == ISUB
