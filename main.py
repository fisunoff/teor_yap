from lexical_analysis.analyzer import LexicalAnalyzer
from syntactical_analysis.analyzer import SyntacticalAnalyzer
from semantic_analyzer.analyzer import SemanticAnalyzer
from semantic_analyzer.exceptions import SemanticError
from tokens import Token  # Импортируем базовый токен для проверки


def main():
    try:
        # 1. Создаем лексер
        lexer = LexicalAnalyzer()  # Убедитесь, что файл называется так

        # --- ДИАГНОСТИКА ---
        # 2. Получаем и ПЕЧАТАЕМ список токенов
        print("--- Результат работы лексического анализатора ---")
        lexer.analyze()  # Метод analyze теперь заполняет self.tokens

        if not lexer.tokens:
            print("Лексер не сгенерировал ни одного токена. Файл пустой или содержит только пробелы.")
            return

        for i, token in enumerate(lexer.tokens):
            print(f"Токен #{i}: {token}")
        print("-------------------------------------------------")
        # --- КОНЕЦ ДИАГНОСТИКИ ---

        # 3. Создаем анализаторы
        # Важно: передаем в парсер уже готовый экземпляр лексера,
        # чтобы он не анализировал файл заново.
        semantic_analyzer = SemanticAnalyzer()
        parser = SyntacticalAnalyzer(lexer, semantic_analyzer)  # Передаем лексер, а не его результат

        # 4. Запускаем синтаксический анализ
        print("\n--- Запуск синтаксического анализатора ---")
        generated_code = parser.parse()

        print("\n--- АНАЛИЗ УСПЕШНО ЗАВЕРШЕН ---")
        print("\n--- Сгенерированный промежуточный код ---")
        for command in generated_code:
            print(command)

    except (SyntaxError, SemanticError) as e:
        print(f"\nОШИБКА АНАЛИЗА: {e}")
    except Exception as e:
        print(f"\nНЕПРЕДВИДЕННАЯ ОШИБКА: {e}")


if __name__ == "__main__":
    main()