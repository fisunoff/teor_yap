from .symbols import Symbol, SymbolCategory, SymbolTable
from .types import TYPE_INT, TYPE_FLOAT, TYPE_BOOL, TypeDesc, TypeForm
from .exceptions import *  # Все наши семантические исключения
from tokens import *  # Все токены
from syntactical_analysis.commands import AssignmentCommand, commands, GotoCommand, ConditionCommand  # Наш IR
from syntactical_analysis.temp_var import TempVar


class SemanticAnalyzer:
    def __init__(self):
        self.global_scope = SymbolTable()
        self.current_scope = self.global_scope
        self.current_offset = 0

        self.type_to_name_map = {}
        self._initialize_builtins()

        self.type_stack = []
        self.operand_stack = []
        self.code = commands  # Используем ваш глобальный список команд

    def _initialize_builtins(self):
        """Добавляет предопределенные типы в глобальную область видимости."""
        # Создаем символы для имен типов
        int_sym = Symbol("integer", SymbolCategory.TYPE, TYPE_INT)
        float_sym = Symbol("float", SymbolCategory.TYPE, TYPE_FLOAT)
        bool_sym = Symbol("bool", SymbolCategory.TYPE, TYPE_BOOL)

        # Добавляем их в таблицу
        self.global_scope.add(int_sym)
        self.global_scope.add(float_sym)
        self.global_scope.add(bool_sym)

        # --- ДОБАВЛЯЕМ ЗАПОЛНЕНИЕ СЛОВАРЯ ---
        self.type_to_name_map[TYPE_INT] = "integer"
        self.type_to_name_map[TYPE_FLOAT] = "float"
        self.type_to_name_map[TYPE_BOOL] = "bool"

    # --- Методы, вызываемые парсером ---

    def declare_variable(self, name_token, type_token):
        # Действие {A1}
        var_name = name_token.value
        type_name = type_token.value

        type_symbol = self.current_scope.lookup(type_name)
        if not type_symbol or type_symbol.category != SymbolCategory.TYPE:
            raise WrongCategoryError(type_name, "именем типа")

        var_symbol = Symbol(var_name, SymbolCategory.VAR, type_symbol.type_ref)

        try:
            self.current_scope.add(var_symbol)
        except NameError:
            raise IdentifierRedeclarationError(var_name)

    def process_identifier_lvalue(self, id_token):
        # Действие {A3} / {A9}
        sym = self.current_scope.lookup(id_token.value)
        if not sym: raise UndeclaredIdentifierError(id_token.value)
        if sym.category != SymbolCategory.VAR: raise WrongCategoryError(id_token.value, "переменной")

        self.type_stack.append(sym.type_ref)
        self.operand_stack.append(sym)

    def process_number(self, num_token):
        # Действие {A10}
        token_type = TYPE_FLOAT if num_token.is_float else TYPE_INT
        self.type_stack.append(token_type)
        # Для простоты операндом будет сама лексема
        self.operand_stack.append(num_token.value)

    def process_boolean(self, bool_token):
        # Действие {A11}
        self.type_stack.append(TYPE_BOOL)
        # ИСПРАВЛЕНИЕ: Используем .value, которое хранит лексему 'true'/'false'
        # Но для этого надо исправить лексер. Давайте пока просто сделаем так:
        bool_value_str = 'true' if bool_token.name == 'True' else 'false'
        self.operand_stack.append(bool_value_str)

    def process_field_access(self, struct_token, field_token):
        """
        Обрабатывает доступ к полю структуры (s.field1).
        Действие {A4}.
        """
        struct_name = struct_token.value
        field_name = field_token.value

        # --- ЦЕЛЕВОЙ ОТЛАДОЧНЫЙ PRINT ---
        print(f"\n--- ОТЛАДКА: process_field_access для '{struct_name}.{field_name}' ---")
        # ------------------------------------

        # 1. Ищем символ структуры в таблице
        struct_sym = self.current_scope.lookup(struct_name)
        if not struct_sym:
            raise UndeclaredIdentifierError(struct_name)
        if struct_sym.category != SymbolCategory.VAR:
            raise WrongCategoryError(struct_name, "переменной")

        # 2. Проверяем, что это действительно структура
        struct_type_desc = struct_sym.type_ref
        if struct_type_desc.form != TypeForm.STRUCT:
            raise NotAStructError(struct_name)

        # 3. Ищем поле во вложенной таблице символов структуры
        field_sym = struct_type_desc.fields.lookup(field_name)
        if not field_sym:
            raise UnknownFieldError(struct_name, field_name)

        # 4. Все проверки пройдены. Помещаем тип и символ поля на стеки.
        self.type_stack.append(field_sym.type_ref)

        # В качестве операнда можно поместить сам символ поля,
        # но для генерации кода нам понадобится и структура, и поле.
        # Давайте создадим временный объект или кортеж.
        field_accessor = (struct_sym, field_sym)
        self.operand_stack.append(field_accessor)

    def process_assignment(self):
        # Действие {A2}
        expr_op = self.operand_stack.pop()
        lvalue_op = self.operand_stack.pop()

        expr_type = self.type_stack.pop()
        lvalue_type = self.type_stack.pop()

        if lvalue_type != expr_type: raise TypeIncompatibilityError("Несовместимые типы операндов.")

        # В качестве имени операнда используем .name или .value
        source_name = getattr(expr_op, 'name', str(expr_op))

        # Проверяем, чем является lvalue_op
        if isinstance(lvalue_op, tuple):  # Это доступ к полю (struct_sym, field_sym)
            struct_sym, field_sym = lvalue_op
            # Ваш IR не имеет команды ASSIGN_IDX, поэтому эмулируем ее строкой
            target_name = f"{struct_sym.name}.{field_sym.name}"
        else:  # Это обычная переменная
            target_name = getattr(lvalue_op, 'name', str(lvalue_op))

        AssignmentCommand.create(target=target_name, source=source_name)

    def process_binary_operation(self, op_token):
        # Действия {A5}-{A8}
        type2 = self.type_stack.pop()
        type1 = self.type_stack.pop()
        op2 = self.operand_stack.pop()
        op1 = self.operand_stack.pop()

        # Определяем операцию, проверяем типы и получаем символ операции
        if op_token in [PLUS_TOKEN, MINUS_TOKEN, MULT_TOKEN, DIV_TOKEN]:
            if type1 not in [TYPE_INT, TYPE_FLOAT] or type1 != type2:
                raise TypeIncompatibilityError(
                    "Операнды для арифметической операции должны быть int или float одного типа.")
            result_type = type1
            op_map = {PLUS_TOKEN: '+', MINUS_TOKEN: '-', MULT_TOKEN: '*', DIV_TOKEN: '/'}
            op_symbol = op_map[op_token]

        elif op_token in [AND_TOKEN, OR_TOKEN]:
            if type1 != TYPE_BOOL or type2 != TYPE_BOOL:
                raise TypeIncompatibilityError(f"Операнды для операции '{op_token.value}' должны быть типа bool.")
            result_type = TYPE_BOOL
            op_symbol_map = {AND_TOKEN: 'and', OR_TOKEN: 'or'}
            op_symbol = op_symbol_map[op_token]

        else:
            # ВОЗВРАЩАЕМ ПРОВЕРКУ НА НЕИЗВЕСТНУЮ ОПЕРАЦИЮ
            raise NotImplementedError(f"Бинарная операция для токена {op_token.name} не реализована")

        # Генерация кода
        source_op1 = getattr(op1, 'name', str(op1))
        source_op2 = getattr(op2, 'name', str(op2))

        result_type_name = self.type_to_name_map.get(result_type, "unknown_type")
        temp_var = TempVar(type_=result_type_name)

        AssignmentCommand.create(target=temp_var.name, source=f"{source_op1} {op_symbol} {source_op2}")

        # Помещаем результат обратно на стеки
        self.type_stack.append(result_type)
        self.operand_stack.append(temp_var)

    def gen_halt(self):
        # Команда останова, если она вам нужна
        # self.code.append(("HALT", None, None, None))
        pass

    def declare_struct_variable(self, name_token, fields_list):
        """
        Объявляет переменную анонимного структурного типа.
        Создает новое описание типа в TypeTable и новую переменную в SymbolTable.
        `fields_list` - это список пар (имя_поля_токен, имя_типа_токен), полученный от парсера.
        """
        struct_var_name = name_token.value

        # Создаем новую, локальную таблицу символов для полей этой структуры
        fields_scope = SymbolTable()
        struct_size = 0

        for field_name_token, field_type_name_token in fields_list:
            field_name = field_name_token.value
            field_type_name = field_type_name_token.value

            # 1. Находим описание типа для поля в глобальной области видимости
            field_type_symbol = self.current_scope.lookup(field_type_name)
            if not field_type_symbol or field_type_symbol.category != SymbolCategory.TYPE:
                raise TypeIncompatibilityError(f"Неизвестный тип '{field_type_name}' для поля '{field_name}'.")

            # 2. Создаем символ для поля
            field_symbol = Symbol(field_name, SymbolCategory.VAR, field_type_symbol.type_ref)
            field_symbol.offset = struct_size  # Смещение поля внутри структуры

            # 3. Добавляем поле в локальную таблицу полей (с проверкой на дубликаты)
            try:
                fields_scope.add(field_symbol)
            except NameError:
                raise IdentifierRedeclarationError(
                    f"Поле '{field_name}' уже объявлено в структуре '{struct_var_name}'.")

            # 4. Увеличиваем общий размер структуры
            struct_size += field_symbol.type_ref.size

        # 5. Создаем новое анонимное описание типа для нашей структуры
        new_struct_type = TypeDesc(form=TypeForm.STRUCT, size=struct_size)
        new_struct_type.fields = fields_scope  # Привязываем таблицу полей к типу

        # 6. Создаем символ для самой переменной-структуры
        struct_var_symbol = Symbol(struct_var_name, SymbolCategory.VAR, new_struct_type)
        # struct_var_symbol.offset = self.current_offset # Если нужно глобальное смещение

        # 7. Добавляем переменную-структуру в текущую (глобальную) область видимости
        try:
            self.current_scope.add(struct_var_symbol)
        except NameError:
            raise IdentifierRedeclarationError(struct_var_name)

        # 8. Обновляем глобальное смещение
        # self.current_offset += struct_size

    def process_not_operation(self):
        """
        Обрабатывает унарную операцию NOT.
        Действие {A12} из нашей таблицы СУТ.
        """
        # 1. Извлекаем тип и операнд со стеков
        operand_type = self.type_stack.pop()
        operand = self.operand_stack.pop()

        # 2. Проверяем тип операнда
        if operand_type != TYPE_BOOL:
            raise InvalidOperandTypeError(operation='not', expected_type='bool')

        # 3. Генерируем код
        # В вашем старом коде была сложная генерация. Давайте пока сделаем просто.
        source_operand_name = getattr(operand, 'name', str(operand))

        # Создаем временную переменную для результата
        temp_var = TempVar(type_='bool')  # Результат 'not' всегда bool

        # Генерируем команду. Ваш IR не имеет унарной команды NOT,
        # поэтому мы эмулируем ее как в вашем старом `NotOperationHandler`.
        # Для этого нам понадобится доступ к командам и меткам.
        # Давайте пока сделаем более простую, "арифметическую" версию
        AssignmentCommand.create(target=temp_var.name, source=f"not {source_operand_name}")

        # 4. Помещаем результат обратно в стеки
        self.type_stack.append(TYPE_BOOL)  # Тип результата всегда bool
        self.operand_stack.append(temp_var)

    def process_for_loop_header(self, loop_variable_token):
        """
        Проверяет семантику заголовка цикла for и генерирует начальный код.
        Действие {A13} - часть 1.
        """
        # 1. Проверяем переменную цикла
        loop_var_symbol = self.current_scope.lookup(loop_variable_token.value)
        if not loop_var_symbol or loop_var_symbol.type_ref != TYPE_INT:
            raise InvalidOperandTypeError("Переменная цикла for", "integer")

        # 2. Проверяем границы диапазона
        range_end_type = self.type_stack.pop()
        range_start_type = self.type_stack.pop()

        if range_start_type != TYPE_INT or range_end_type != TYPE_INT:
            raise TypeIncompatibilityError("Границы диапазона в цикле for должны быть типа integer.")

        range_end_op = self.operand_stack.pop()
        range_start_op = self.operand_stack.pop()

        # 3. Генерация начального кода
        # a) Инициализируем переменную цикла
        start_op_name = getattr(range_start_op, 'name', str(range_start_op))
        AssignmentCommand.create(target=loop_var_symbol.name, source=start_op_name)

        # b) Создаем метки для начала и конца цикла
        # Мы будем использовать их для backpatching (метода обратных поправок)
        loop_start_label_pos = len(self.code)

        # c) Генерируем условие выхода (i < end)
        temp_cond_var = TempVar(type_='bool')
        end_op_name = getattr(range_end_op, 'name', str(range_end_op))
        source_expr = f"{loop_var_symbol.name} < {end_op_name}"  # Пример условия, возможно понадобится команда CMP
        AssignmentCommand.create(target=temp_cond_var.name, source=source_expr)  # Эмуляция

        # d) Генерируем условный переход на конец (адрес пока неизвестен)
        # Ваш IR использует ConditionCommand, который сложнее для backpatching,
        # давайте пока создадим его с заглушкой
        cond_goto = ConditionCommand.create(cond=f"not {temp_cond_var.name}", goto_command_ind=999)  # 999 - заглушка

        # Сохраняем важную информацию в стеке для использования в конце цикла
        self.operand_stack.append({
            "start_label_pos": loop_start_label_pos,
            "exit_goto": cond_goto,
            "loop_var": loop_var_symbol
        })

    def process_for_loop_end(self):
        """
        Генерирует код конца цикла (инкремент и переход).
        Действие {A13} - часть 2.
        """
        loop_info = self.operand_stack.pop()
        loop_var_symbol = loop_info["loop_var"]

        # 1. Инкрементируем переменную цикла
        temp_inc_var = TempVar(type_='integer')
        AssignmentCommand.create(target=temp_inc_var.name, source=f"{loop_var_symbol.name} + 1")
        AssignmentCommand.create(target=loop_var_symbol.name, source=temp_inc_var.name)

        # 2. Безусловный переход на начало цикла
        GotoCommand.create(next_command_ind=loop_info["start_label_pos"])

        # 3. "Backpatching": теперь мы знаем, куда ведет условный переход
        # Адрес выхода из цикла - это текущая позиция в коде
        exit_pos = len(self.code)
        loop_info["exit_goto"].goto_command_ind = exit_pos
