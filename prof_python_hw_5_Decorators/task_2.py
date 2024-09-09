import os
from datetime import datetime
from functools import wraps


def logger(path='main.log'):
    """Декоратор для логирования вызовов функций в указанный файл."""

    def __logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            # Запись данных в файл лога
            with open(path, 'a', encoding='utf-8') as f:
                f.write(f'Date/time: {datetime.now()}\n')
                f.write(f'Function name: {old_function.__name__}\n')
                f.write(f'Arguments: {args, kwargs}\n')
                f.write(f'Return value: {result}\n\n')
            return result

        return new_function

    return __logger


def test_2():
    """Тестирование функций с логированием для разных файлов."""

    # Определяем три различных файла для лога
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    # Цикл для тестирования логирования в каждом файле
    for path in paths:
        # Удаляем лог, если он уже существует
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        # Проверяем результат выполнения функций
        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    # Проверка наличия файлов логов и их содержимого
    for path in paths:

        # Убедимся, что файл лога был создан
        assert os.path.exists(path), f'Файл {path} должен существовать'

        # Чтение содержимого логов для проверки корректности записи
        with open(path) as log_file:
            log_file_content = log_file.read()

        # Проверка, что функция 'summator' была записана в лог
        assert 'summator' in log_file_content, 'Должно записаться имя функции'

        # Проверка, что переданные значения аргументов и результаты были записаны в лог
        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()
