from tokens.token import Token
# Удаляем импорт const, он здесь больше не нужен

__all__ = [
    'DigitalConstToken',
]

class DigitalConstToken(Token):
    """
    Упрощенный токен для числовых констант.
    Хранит лексему и информацию о том, есть ли в ней точка.
    """
    def __init__(self, lexeme: str, is_float: bool):
        # Поле value теперь хранит саму лексему
        super().__init__(name='num', code=26, value=lexeme)
        self.is_float = is_float # Этот флаг поможет семантическому анализатору определить тип

    def __str__(self):
        return f'<{self.name}, {self.value}>'

# Таблица digital_consts_table и метод get_or_create УДАЛЕНЫ.