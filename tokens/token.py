__all__ = [
    'Token',
    'RangeToken',
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

    def __eq__(self, other):
        """
        Переопределяем оператор сравнения (==).
        Два токена считаются равными, если у них совпадают имя, код и значение.
        """
        if not isinstance(other, Token):
            return NotImplemented  # Не сравниваем с другими типами

        return (self.name == other.name and
                self.code == other.code and
                self.value == other.value)

    def __hash__(self):
        """
        Реализуем хэширование.
        Объект становится хэшируемым и может быть использован как ключ в словаре.
        """
        # Хэш вычисляется от кортежа полей, которые участвуют в сравнении
        return hash((self.name, self.code, self.value))


class RangeToken(Token):
    def __init__(self, lexeme: str):
        super().__init__(name='range', code=30, value=lexeme)

    def __str__(self):
        return f'<{self.name}, {self.value}>'


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

