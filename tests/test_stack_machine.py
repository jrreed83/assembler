from assembler.tokens import *

def test_token_equality():
    assert(Token(IADD) == Token(IADD))