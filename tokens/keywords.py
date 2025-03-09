from tokens.token import Token
from lexical_analysis import const

__all__ = [
    'AND_TOKEN',
    'BLOCK_LET_TOKEN',
    'CASE_TOKEN',
    'STRUCT_TOKEN',
    'END_PROG_TOKEN',
    'ENDBLOCK_LET_TOKEN',
    'FALSE_TOKEN',
    'MATCH_TOKEN',
    'NL_TOKEN',
    'NOT_TOKEN',
    'OR_TOKEN',
    'START_PROG_TOKEN',
    'TAB_TOKEN',
    'TRUE_TOKEN',
    'WORDS_TOKENS_MAPPING'
]

AND_TOKEN = Token(name='and', code=1, value=0)
BLOCK_LET_TOKEN = Token(name='block', code=2, value=0)
CASE_TOKEN = Token(name='case', code=3, value=0)
STRUCT_TOKEN = Token(name='struct', code=4, value=0)
END_PROG_TOKEN = Token(name='end', code=5, value=0)
ENDBLOCK_LET_TOKEN = Token(name='endblock', code=6, value=0)
FALSE_TOKEN = Token(name='False', code=7, value=0)
MATCH_TOKEN = Token(name='match', code=8, value=0)
NL_TOKEN = Token(name='nl', code=9, value=0)
NOT_TOKEN = Token(name='not', code=10, value=0)
OR_TOKEN = Token(name='or', code=11, value=0)
START_PROG_TOKEN = Token(name='start_prog', code=12, value=0)
TAB_TOKEN = Token(name='tab', code=13, value=0)
TRUE_TOKEN = Token(name='True', code=14, value=0)
FOR_TOKEN = Token(name='for', code=50, value=0)
IN_TOKEN = Token(name='in', code=51, value=0)

WORDS_TOKENS_MAPPING = {
    const.KW_AND: AND_TOKEN,
    const.KW_BLOCK_LET: BLOCK_LET_TOKEN,
    const.KW_CASE: CASE_TOKEN,
    const.KW_STRUCT: STRUCT_TOKEN,
    const.KW_END_PROG: END_PROG_TOKEN,
    const.KW_ENDBLOCK_LET: ENDBLOCK_LET_TOKEN,
    const.KW_FALSE: FALSE_TOKEN,
    const.KW_MATCH: MATCH_TOKEN,
    const.KW_NL: NL_TOKEN,
    const.KW_NOT: NOT_TOKEN,
    const.KW_OR: OR_TOKEN,
    const.KW_START_PROG: START_PROG_TOKEN,
    const.KW_TAB: TAB_TOKEN,
    const.KW_TRUE: TRUE_TOKEN,
    const.KW_FOR: FOR_TOKEN,
    const.KW_IN: IN_TOKEN,
}
