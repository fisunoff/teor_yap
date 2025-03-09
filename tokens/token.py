__all__ = [
    'Token',
    'OPEN_BRACKET_TOKEN',
    'CLOSE_BRACKET_TOKEN',
    'ASSIGNMENT_TOKEN',
    'COLON_TOKEN',
    'COMMA_TOKEN',
    'UNDERSCORE_TOKEN',
    'POINT_TOKEN',
    'SEMICOLON_TOKEN',
    'START_TOKEN',
    'END_TOKEN',
]


class Token:
    """Токен"""

    def __init__(self, name: str, code: int, value):
        # Имя токена
        self.name = name
        # Код токена
        self.code = code
        # Значение атрибута
        self.value = value

    def __str__(self):
        return f'<{self.name}, {self.value}>'


class RangeToken(Token):
    def __init__(self, attr_name):
        super().__init__(name='range', code=30, value=0)
        self.attr_name = attr_name

    def __str__(self):
        return f'<{self.name}, {self.value}> ({self.attr_name})'


OPEN_BRACKET_TOKEN = Token(name='(', code=15, value=0)
CLOSE_BRACKET_TOKEN = Token(name=')', code=16, value=0)
ASSIGNMENT_TOKEN = Token(name='ass', code=17, value=0)
COLON_TOKEN = Token(name=':', code=18, value=0)
COMMA_TOKEN = Token(name=',', code=19, value=0)
UNDERSCORE_TOKEN = Token(name='_', code=20, value=0)
POINT_TOKEN = Token(name='pt', code=24, value=0)
SEMICOLON_TOKEN = Token(name=';', code=27, value=0)
START_TOKEN = Token(name='{', code=28, value=0)
END_TOKEN = Token(name='}', code=29, value=0)

