from enum import Enum, auto

class TypeForm(Enum):
    """Форма типа: базовый или структура."""
    BASE = auto()
    STRUCT = auto()

class TypeDesc:
    """
    Описание типа (запись в таблице типов).
    Хранит полную информацию о любом типе в языке.
    """
    def __init__(self, form: TypeForm, size: int):
        self.form = form
        self.size = size
        # Для структур здесь будет ссылка на их собственную таблицу символов полей.
        self.fields = None  # Инициализируется позже для STRUCT

    def __repr__(self):
        return f"<Type form={self.form.name} size={self.size}>"

    def __eq__(self, other):
        """
        Переопределяем оператор сравнения (==).
        Два описания типов равны, если у них одинаковая форма и размер.
        Для структур в будущем можно добавить сравнение полей.
        """
        if not isinstance(other, TypeDesc):
            return NotImplemented

        # Для базовых типов достаточно сравнить форму и размер
        if self.form == TypeForm.BASE and other.form == TypeForm.BASE:
            return self.size == other.size

        # Для структур они равны, только если это один и тот же объект
        # (т.к. у нас анонимные типы структур)
        if self.form == TypeForm.STRUCT and other.form == TypeForm.STRUCT:
            return self is other

        return False

    def __hash__(self):
        """
        Реализуем хэширование.
        """
        # Хэш для базовых типов зависит от их размера.
        # Для структур - от их id в памяти (т.к. они уникальны).
        if self.form == TypeForm.BASE:
            return hash((self.form, self.size))
        else: # STRUCT
            return hash(id(self))

# --- Предопределенные типы ---
# Это единственные экземпляры базовых типов. Мы будем на них ссылаться.
TYPE_INT = TypeDesc(form=TypeForm.BASE, size=4)
TYPE_FLOAT = TypeDesc(form=TypeForm.BASE, size=8)
TYPE_BOOL = TypeDesc(form=TypeForm.BASE, size=1)
TYPE_UNDEFINED = TypeDesc(form=TypeForm.BASE, size=0) # для ошибок
