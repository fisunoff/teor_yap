from lexical_analysis.const import INF
from tokens import *

__all__ = [
    'STATE_TRANSITION_TABLE',
    'STATE_TOKEN_MAPPING',
]

STATE_TRANSITION_TABLE = {
    '(': [-1, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    ')': [-2, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    ':': [-3, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    ',': [-4, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '_': [-5, -11, -9, 3, 3, -13, INF, -16, -18, 9, -21, INF, INF, -30, INF, -30, INF, -28],
    '+': [-6, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, 14, -30, INF, -30, INF, -28],
    '-': [-7, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, 14, -30, INF, -30, INF, -28],
    '*': [-8, -11, 3, 4, 4, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '/': [2, -11, -9, 3, -12, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '.': [-22, -11, -9, 3, 3, -13, INF, -16, -18, -20, 11, 16, INF, -30, INF, -30, INF, -28],
    ' ': [1, 1, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '{': [-25, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '}': [-26, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    ';': [-27, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    'digits': [10, -11, -9, 3, 3, -13, INF, -16, -18, 9, 10, 13, 15, 13, 15, 11, 17, 17],
    'e': [INF, -11, -9, 3, 3, -13, INF, -16, -18, -20, 12, INF, INF, -30, INF, -30, INF, -28],
    '=': [5, -11, -9, 3, 3, -14, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '!': [6, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '>': [7, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '<': [8, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    'letters': [9, -11, -9, 3, 3, -13, INF, -16, -18, 9, -21, INF, INF, -30, INF, -30, INF, -28],
    '\n': [-23, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    '\t': [-24, -11, -9, 3, 3, -13, INF, -16, -18, -20, -21, INF, INF, -30, INF, -30, INF, -28],
    'another': [INF, INF, INF, 3, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF, INF],
}

STATE_TOKEN_MAPPING = {
    -1: OPEN_BRACKET_TOKEN,
    -2: CLOSE_BRACKET_TOKEN,
    -3: COLON_TOKEN,
    -4: COMMA_TOKEN,
    -5: UNDERSCORE_TOKEN,
    -6: PLUS_TOKEN,
    -7: MINUS_TOKEN,
    -8: MULT_TOKEN,
    -9: DIV_TOKEN,
    -13: ASSIGNMENT_TOKEN,
    -14: EQUAL_TOKEN,
    -15: NOT_EQUAL_TOKEN,
    -16: MORE_TOKEN,
    -17: MORE_EQUAL_TOKEN,
    -18: LESS_TOKEN,
    -19: LESS_EQUAL_TOKEN,
    -22: POINT_TOKEN,
    -25: START_TOKEN,
    -26: END_TOKEN,
    -27: SEMICOLON_TOKEN,
}
