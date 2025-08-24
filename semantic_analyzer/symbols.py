from enum import Enum, auto
from semantic_analyzer.types import TypeDesc

class SymbolCategory(Enum):
    """Категория символа: переменная или тип."""
    VAR = auto()
    TYPE = auto()

class Symbol:
    """
    Символ (запись в таблице символов).
    Представляет любой именованный объект в программе.
    """
    def __init__(self, name: str, category: SymbolCategory, type_ref: TypeDesc):
        self.name = name
        self.category = category
        self.type_ref = type_ref  # Ссылка на объект TypeDesc
        self.offset = None # Смещение в памяти для переменных

    def __repr__(self):
        return f"<Symbol name='{self.name}' cat={self.category.name}>"

class SymbolTable:
    """
    Таблица символов. Управляет областями видимости.
    """
    def __init__(self, outer_scope=None):
        self._symbols = {}
        self.outer_scope = outer_scope

    def add(self, symbol: Symbol):
        """Добавляет символ в текущую область видимости."""
        if symbol.name in self._symbols:
            # Ошибка повторного объявления в этой же области видимости
            raise NameError(f"Идентификатор '{symbol.name}' уже объявлен.")
        self._symbols[symbol.name] = symbol

    def lookup(self, name: str) -> Symbol | None:
        """Ищет символ по имени в текущей и всех внешних областях видимости."""
        symbol = self._symbols.get(name)
        if symbol:
            return symbol
        if self.outer_scope:
            return self.outer_scope.lookup(name)
        return None
