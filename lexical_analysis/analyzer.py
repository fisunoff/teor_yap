from typing import List

from tokens.token import RangeToken
from . import const
from . import utils
from .custom_exceptions import WrongSymbolException
from .state_machine import STATE_TRANSITION_TABLE, STATE_TOKEN_MAPPING
from tokens import *

__all__ = [
    'LexicalAnalyzer'
]


class LexicalAnalyzer:
    """Лексический анализатор"""

    def __init__(self, source_file='tests/editable.txt', *args, **kwargs):
        self.source_file = source_file  # type: str
        self.data = []  # type: List[str]
        self.read()
        self.tokens = []
        # Текущее состояние автомата
        self.current_state = 0

    def read(self):
        """Считывает код из файла"""
        with open(self.source_file) as f:
            self.data = [
                utils.change_prefix_to_tabs(line)
                for line in f.readlines()
            ]

    def write(self, filename='lexical_analysis_result.txt'):
        with open(filename, 'w', encoding='UTF-8') as f:
            f.write('\n'.join(map(str, self.tokens)))

    def analyze(self):
        """Анализ файла"""
        for line in self.data:
            if line and line != '\n':
                line_to_explore = line.lstrip(' ').replace('\t', ' ')  # плевать на пробелы в начале
                self._analyze_line(line_to_explore)

    def _analyze_line(self, line):
        """Анализ строки файла """
        if line == 'end_prog':
            self.tokens.append(END_PROG_TOKEN)
        left, right = 0, 0
        while right <= len(line) - 1:

            symbol_ = line[right]
            if symbol_ in const.DIGITS_STR:
                table_key = 'digits'
            elif symbol_ in const.LETTERS and not self.current_state == 10:
                table_key = 'letters'
            else:
                table_key = symbol_

            if table_key not in STATE_TRANSITION_TABLE:
                table_key = 'another'

            if self.current_state == 3 and table_key == '*':
                right += 1
                self.current_state = 4  # пытаемся закончить комментарий
                continue
            if self.current_state == 4:
                if table_key == '/':  # закончили комментарий
                    right += 1
                    self.current_state = 0
                    left = right
                    continue
                else:  # а нет, продолжаем комментарий
                    self.current_state = 3
            if self.current_state == 3:
                right += 1
                continue
            new_state = STATE_TRANSITION_TABLE[table_key][self.current_state]
            if new_state == const.INF:
                raise WrongSymbolException(symbol_)
            if new_state < 0:
                # Пришли в конечное состояние
                lexeme = line[left:right + (left == right)]
                # print(new_state, self.current_state, lexeme)
                # Проверим, является ли лексема ключевым словом
                if lexeme in const.KEYWORDS:
                    # Является, добавим соответствующий токен
                    self.tokens.append(WORDS_TOKENS_MAPPING[lexeme])
                else:
                    # Не является
                    # Проверим, является ли заранее определенный токеном
                    if new_state in STATE_TOKEN_MAPPING:
                        # Является
                        self.tokens.append(STATE_TOKEN_MAPPING[new_state])
                    else:
                        # Не является, а значит это или числовая константа, или идентификатор
                        # Числовую константу можно получить из конечных состояний -21 и -30
                        if new_state in [-21, -30]:
                            if new_state == -21:
                                # Числовая константа целового типа
                                token_type = const.INT
                            else:
                                # Числовая константа вещественного типа
                                token_type = const.FLOAT
                            self.tokens.append(DigitalConstToken.get_or_create(lexeme=lexeme, type=token_type))
                        elif new_state in [-28]:  # range ..
                            token_ = RangeToken(lexeme)
                            self.tokens.append(token_)
                        else:
                            token_ = IdentifierToken.get_or_create(lexeme)
                            if token_:
                                self.tokens.append(token_)

                if new_state in [-9, -11, -13, -16, -18, -20, -21, -28, -30]:
                    # Состояния с возвратом 1.
                    left = right
                else:
                    # Состояния с возвратом 0
                    right += 1
                    left = right
                self.current_state = 0
            else:
                right += 1
                self.current_state = new_state
