from tokens.token import Token

__all__ = [
    'IdentifierToken',
]

class IdentifierToken(Token):
    """
    Упрощенный токен идентификатора.
    Хранит только лексему.
    """
    def __init__(self, lexeme: str):
        # Поле value теперь хранит саму лексему
        super().__init__(name='id', code=25, value=lexeme)

    def __str__(self):
        return f'<{self.name}, {self.value}>'