import os
from datetime import datetime
from functools import wraps

def logger(old_function):
    """Декоратор для логирования вызовов функций и их результатов."""

    @wraps(old_function)
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as f:
            f.write(f'Date/time: {datetime.now()}\n')
            f.write(f'Function name: {old_function.__name__}\n')
            f.write(f'Arguments: {args, kwargs}\n')
            f.write(f'Return value: {result}\n\n')
        return result

    return new_function

def test_1():
    """Тестирование работы функций с логированием."""

    log_file_path = os.path.join(os.getcwd(), 'main.log')

    # Удаление существующего файла лога перед тестированием
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    # Проверки результатов работы функций
    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    # Проверка наличия файла лога после вызовов функций
    assert os.path.exists(log_file_path), 'Файл main.log должен существовать'

    # Дополнительные вызовы функций для записи в лог
    summator(4.3, b=2.2)
    summator(a=0, b=0)

    # Проверка записей в файле лога
    with open(log_file_path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'Должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'

if __name__ == '__main__':
    test_1()
