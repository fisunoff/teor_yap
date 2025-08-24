import re

from tokens import (
    IdentifierToken, DigitalConstToken, RangeToken,
    WORDS_TOKENS_MAPPING,
    OPEN_BRACKET_TOKEN, CLOSE_BRACKET_TOKEN, ASSIGNMENT_TOKEN, COLON_TOKEN, COMMA_TOKEN,
    POINT_TOKEN, SEMICOLON_TOKEN, START_TOKEN, END_TOKEN,
    PLUS_TOKEN, MINUS_TOKEN, MULT_TOKEN, DIV_TOKEN
)

__all__ = [
    'LexicalAnalyzer'
]

# Определяем спецификацию токенов с помощью регулярных выражений
TOKEN_SPECIFICATION = [
    ('SKIP', r'[ \t]+'),
    ('NEWLINE', r'\n'),
    ('COMMENT', r'/\*.*?\*/'),
    ('MOD', r'mod\b'),
    ('END_MOD', r'end_mod\b'),
    ('LET', r'let\b'),
    ('END_LET', r'end_let\b'),
    ('STRUCT', r'struct\b'),
    ('FOR', r'for\b'),
    ('IN', r'in\b'),
    ('AND', r'and\b'),
    ('OR', r'or\b'),
    ('NOT', r'not\b'),
    ('TRUE', r'true\b'),
    ('FALSE', r'false\b'),
    ('FLOAT_NUM', r'\d+\.\d+'),
    ('INT_NUM', r'\d+'),
    ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),
    ('RANGE', r'\.\.'),
    ('ASSIGN', r'='),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LBRACE', r'\{'),
    ('RBRACE', r'\}'),
    ('COLON', r':'),
    ('COMMA', r','),
    ('SEMI', r';'),
    ('DOT', r'\.'),
    ('MISMATCH', r'.'),
]

tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_SPECIFICATION)

TOKEN_MAPPING = {
    'MOD': WORDS_TOKENS_MAPPING['mod'],
    'END_MOD': WORDS_TOKENS_MAPPING['end_mod'],
    'LET': WORDS_TOKENS_MAPPING['let'],
    'END_LET': WORDS_TOKENS_MAPPING['end_let'],
    'STRUCT': WORDS_TOKENS_MAPPING['struct'],
    'FOR': WORDS_TOKENS_MAPPING['for'],
    'IN': WORDS_TOKENS_MAPPING['in'],
    'AND': WORDS_TOKENS_MAPPING['and'],
    'OR': WORDS_TOKENS_MAPPING['or'],
    'NOT': WORDS_TOKENS_MAPPING['not'],
    'TRUE': WORDS_TOKENS_MAPPING['True'],
    'FALSE': WORDS_TOKENS_MAPPING['False'],
    'ASSIGN': ASSIGNMENT_TOKEN,
    'PLUS': PLUS_TOKEN,
    'MINUS': MINUS_TOKEN,
    'MUL': MULT_TOKEN,
    'DIV': DIV_TOKEN,
    'LPAREN': OPEN_BRACKET_TOKEN,
    'RPAREN': CLOSE_BRACKET_TOKEN,
    'LBRACE': START_TOKEN,
    'RBRACE': END_TOKEN,
    'COLON': COLON_TOKEN,
    'COMMA': COMMA_TOKEN,
    'SEMI': SEMICOLON_TOKEN,
    'DOT': POINT_TOKEN,
}


class LexicalAnalyzer:
    def __init__(self, source_file='tests/editable.txt'):
        self.source_file = source_file
        self.code = ""
        self.tokens = []
        self._read_file()

    def _read_file(self):
        with open(self.source_file) as f:
            self.code = f.read()
            # --- ОТЛАДОЧНЫЙ PRINT #2 ---
            print("--- ИСХОДНЫЙ КОД ---")
            print(repr(self.code))  # repr покажет все невидимые символы
            print("----------------------")

    def analyze(self):
        self.tokens = []
        for mo in re.finditer(tok_regex, self.code, re.DOTALL):
            kind = mo.lastgroup
            value = mo.group()

            if kind in ['SKIP', 'COMMENT', 'NEWLINE']:
                continue
            elif kind == 'FLOAT_NUM':
                self.tokens.append(DigitalConstToken(lexeme=value, is_float=True))
            elif kind == 'INT_NUM':
                self.tokens.append(DigitalConstToken(lexeme=value, is_float=False))
            elif kind == 'ID':
                self.tokens.append(IdentifierToken(lexeme=value))
            elif kind == 'RANGE':
                self.tokens.append(RangeToken('..'))
            elif kind in TOKEN_MAPPING:
                self.tokens.append(TOKEN_MAPPING[kind])
            elif kind == 'MISMATCH':
                raise RuntimeError(f'Неожиданный символ: {value}')

        return self.tokens

    def write(self, filename='lexical_analysis_result.txt'):
        """
        Сейчас вместо этого вывод в консоль.
        """
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write('\n'.join(map(str, self.tokens)))
