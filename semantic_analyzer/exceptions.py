class SemanticError(Exception):
    """Базовый класс для всех семантических ошибок."""
    def __init__(self, message, line=None, col=None):
        # В будущем можно добавить номер строки и колонки для точных сообщений
        self.message = message
        super().__init__(self.message)

class IdentifierRedeclarationError(SemanticError):
    """Ошибка: Повторное объявление идентификатора."""
    def __init__(self, name):
        super().__init__(f"Идентификатор '{name}' уже объявлен в текущей области видимости.")

class UndeclaredIdentifierError(SemanticError):
    """Ошибка: Использование необъявленного идентификатора."""
    def __init__(self, name):
        super().__init__(f"Идентификатор '{name}' не был объявлен.")

class WrongCategoryError(SemanticError):
    """Ошибка: Использование идентификатора не той категории (например, тип вместо переменной)."""
    def __init__(self, name, expected_category):
        super().__init__(f"Идентификатор '{name}' не является {expected_category}.")

class TypeIncompatibilityError(SemanticError):
    """Ошибка: Несовместимость типов в операции или присваивании."""
    def __init__(self, message="Несовместимые типы операндов."):
        super().__init__(message)

class InvalidOperandTypeError(SemanticError):
    """Ошибка: Тип операнда не подходит для операции."""
    def __init__(self, operation, expected_type):
        super().__init__(f"Операция '{operation}' требует операнд типа '{expected_type}'.")

class NotAStructError(SemanticError):
    """Ошибка: Попытка доступа к полю у переменной, которая не является структурой."""
    def __init__(self, name):
        super().__init__(f"Переменная '{name}' не является структурой, доступ к полю невозможен.")

class UnknownFieldError(SemanticError):
    """Ошибка: Попытка доступа к несуществующему полю структуры."""
    def __init__(self, struct_name, field_name):
        super().__init__(f"Структура '{struct_name}' не имеет поля с именем '{field_name}'.")
