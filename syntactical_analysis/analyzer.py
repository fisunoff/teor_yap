from lexical_analysis.analyzer import LexicalAnalyzer
from semantic_analyzer.analyzer import SemanticAnalyzer
from tokens import *


class SyntacticalAnalyzer:
    """
    Синтаксический анализатор, реализованный методом рекурсивного спуска.
    Он проверяет синтаксис и делегирует семантические действия и генерацию кода
    объекту SemanticAnalyzer.
    """

    def __init__(self, lexer: LexicalAnalyzer, semantic_analyzer: SemanticAnalyzer):
        self.tokens = lexer.analyze()
        self.semantic_analyzer = semantic_analyzer
        self.current_token_index = 0

    # --- Вспомогательные методы для работы с потоком токенов ---
    def _current_token(self):
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None  # EOF

    def _advance(self):
        self.current_token_index += 1

    def _expect(self, expected_token):
        """Проверяет, что текущий токен - ожидаемый, и сдвигает указатель."""
        token = self._current_token()
        if token == expected_token:
            self._advance()
        else:
            raise SyntaxError(f"Ожидался токен {expected_token.name}, но получен {token.name if token else 'EOF'}")

    # --- Методы разбора, соответствующие правилам грамматики ---

    def parse(self):
        """Главный метод, запускающий анализ программы."""
        self.parse_program()
        # После успешного разбора можно получить код
        return self.semantic_analyzer.code

    def parse_program(self):
        # R1: Program -> mod Block end_mod
        self._expect(START_PROG_TOKEN)  # 'mod'
        self.parse_block()
        self._expect(END_PROG_TOKEN)  # 'end_mod'
        self.semantic_analyzer.gen_halt()  # Генерируем команду останова

    def parse_block(self):
        # R2, R3: Block -> let [VarDecls] end_let { StmtSeq }
        self._expect(BLOCK_LET_TOKEN)  # 'let'
        if self._current_token() != ENDBLOCK_LET_TOKEN:
            self.parse_var_decls()
        self._expect(ENDBLOCK_LET_TOKEN)  # 'end_let'

        self._expect(START_TOKEN)  # '{'
        if self._current_token() != END_TOKEN:
            self.parse_stmt_seq()
        self._expect(END_TOKEN)  # '}'

        self.semantic_analyzer.print_memory_layout()

    def parse_var_decls(self):
        # R4, R5: VarDecls -> VarDecl ; { VarDecl ; }
        self.parse_var_decl()
        self._expect(SEMICOLON_TOKEN)
        while self._current_token() != ENDBLOCK_LET_TOKEN:
            self.parse_var_decl()
            self._expect(SEMICOLON_TOKEN)

    def parse_var_decl(self):
        """
        Разбирает объявление переменной.
        R6: VarDecl -> NameList : id
        R7: VarDecl -> id : struct { FieldDecls }
        """
        # Сначала мы видим либо список имен, либо одно имя.
        # Для простоты, сначала проверим на структуру.
        id_token = self._current_token()
        next_token = self.tokens[self.current_token_index + 1]  # Смотрим вперед

        if next_token == COLON_TOKEN and self.tokens[self.current_token_index + 2] == STRUCT_TOKEN:
            # Это объявление структуры: id : struct ...
            self._advance()  # Пропускаем id
            self._expect(COLON_TOKEN)
            self._expect(STRUCT_TOKEN)
            self._expect(START_TOKEN)  # '{'

            fields_list = []
            if self._current_token() != END_TOKEN:
                fields_list = self.parse_field_decls()

            self._expect(END_TOKEN)  # '}'

            # Вызываем семантическое действие для объявления структуры
            self.semantic_analyzer.declare_struct_variable(id_token, fields_list)

        else:
            # Это объявление простой переменной: NameList : id
            name_list_tokens = self.parse_name_list()
            self._expect(COLON_TOKEN)
            type_token = self._current_token()
            self._expect(type_token)  # Сдвигаем указатель

            # Действие {A1}
            for name_token in name_list_tokens:
                self.semantic_analyzer.declare_variable(name_token, type_token)

    def parse_field_decls(self):
        """
        Разбирает список полей внутри структуры.
        R8, R9: FieldDecls -> FieldDecl { , FieldDecl }
        """
        fields = []
        # R11: FieldDecl -> NameList : id

        name_list_tokens = self.parse_name_list()
        self._expect(COLON_TOKEN)
        type_token = self._current_token()
        self._expect(type_token)
        # Добавляем все поля из списка
        for name_token in name_list_tokens:
            fields.append((name_token, type_token))

        # Проверяем, есть ли еще поля через запятую
        while self._current_token() == COMMA_TOKEN:
            self._advance()
            # Если после запятой идет '}', это висячая запятая, игнорируем.
            if self._current_token() == END_TOKEN:
                break

            name_list_tokens = self.parse_name_list()
            self._expect(COLON_TOKEN)
            type_token = self._current_token()
            self._expect(type_token)
            for name_token in name_list_tokens:
                fields.append((name_token, type_token))

        return fields

    def parse_name_list(self):
        # R12, R13: NameList -> id { , id }
        names = [self._current_token()]
        self._expect(names[0])  # Сдвигаем
        while self._current_token() == COMMA_TOKEN:
            self._advance()
            next_name = self._current_token()
            self._expect(next_name)
            names.append(next_name)
        return names

    def parse_stmt_seq(self):
        """Разбирает последовательность операторов."""
        self.parse_statement()
        while self._current_token() != END_TOKEN:
            self.parse_statement()

    def parse_statement(self):
        """Разбирает один оператор."""
        current_token = self._current_token()

        if current_token == WORDS_TOKENS_MAPPING.get('for'):
            self.parse_loop()  # Цикл сам по себе является полным оператором
        elif isinstance(current_token, IdentifierToken):
            # Это присваивание, которое должно заканчиваться ';'
            self.parse_lvalue()
            self._expect(ASSIGNMENT_TOKEN)
            self.parse_expression()
            self.semantic_analyzer.process_assignment()
            self._expect(SEMICOLON_TOKEN)  # ; обязательна здесь
        else:
            raise SyntaxError(f"Ожидался оператор, но получен {current_token.name if current_token else 'EOF'}")

    def parse_loop(self):
        """
        Разбирает цикл for.
        R21: Loop -> for id in Range { StmtSeq }
        """
        self._expect(WORDS_TOKENS_MAPPING['for'])

        loop_variable_token = self._current_token()
        self._expect(loop_variable_token)  # Сдвигаем

        self._expect(WORDS_TOKENS_MAPPING['in'])

        self.parse_range()

        # Семантическое действие для проверки переменной цикла и диапазона
        self.semantic_analyzer.process_for_loop_header(loop_variable_token)

        self._expect(START_TOKEN)  # '{'
        if self._current_token() != END_TOKEN:
            self.parse_stmt_seq()
        self._expect(END_TOKEN)  # '}'

        # Семантическое действие в конце цикла
        self.semantic_analyzer.process_for_loop_end()

    def parse_range(self):
        """
        Разбирает диапазон (range).
        R22: Range -> Factor .. Factor
        """
        self.parse_factor()  # Разбираем начало диапазона

        current_token = self._current_token()
        if isinstance(current_token, RangeToken) and current_token.value == '..':
            self._advance()
        else:
            raise SyntaxError(f"Ожидался '..', но получен {current_token.value if current_token else 'EOF'}")

        self.parse_factor()  # Разбираем конец диапазона

    def parse_lvalue(self):
        id1_token = self._current_token()

        self._expect(id1_token)

        if self._current_token() == POINT_TOKEN:
            self._advance()
            id2_token = self._current_token()
            self._expect(id2_token)
            # Действие {A4}
            self.semantic_analyzer.process_field_access(id1_token, id2_token)
        else:
            # Действие {A3}
            self.semantic_analyzer.process_identifier_lvalue(id1_token)

    # --- Методы для разбора выражений ---

    def parse_expression(self):
        # R23, R24: Expression -> Term { AddOp Term }
        self.parse_term()
        while self._current_token() in [PLUS_TOKEN, MINUS_TOKEN, OR_TOKEN]:
            op = self._current_token()
            self._advance()
            self.parse_term()
            # Действия {A5}, {A6}
            self.semantic_analyzer.process_binary_operation(op)

    def parse_term(self):
        # R25, R26: Term -> Factor { MulOp Factor }
        self.parse_factor()
        while self._current_token() in [MULT_TOKEN, DIV_TOKEN, AND_TOKEN]:
            op = self._current_token()
            self._advance()
            self.parse_factor()
            # Действия {A7}, {A8}
            self.semantic_analyzer.process_binary_operation(op)

    def parse_factor(self):
        # R27-R32
        token = self._current_token()
        if isinstance(token, IdentifierToken):
            self.parse_lvalue()  # LValue является подмножеством Factor
        elif isinstance(token, DigitalConstToken):
            self._advance()
            # Действие {A10}
            self.semantic_analyzer.process_number(token)
        elif token in [TRUE_TOKEN, FALSE_TOKEN]:
            self._advance()
            # Действие {A11}
            self.semantic_analyzer.process_boolean(token)
        elif token == NOT_TOKEN:
            self._advance()
            self.parse_factor()
            # Действие {A12}
            self.semantic_analyzer.process_not_operation()
        elif token == OPEN_BRACKET_TOKEN:
            self._advance()
            self.parse_expression()
            self._expect(CLOSE_BRACKET_TOKEN)
        else:
            raise SyntaxError(f"Неожиданный токен в выражении: {token.name}")

