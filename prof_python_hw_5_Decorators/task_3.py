from task_1 import logger


class FlatIterator:
    """Итератор для плоского перебора элементов вложенных списков."""

    def __init__(self, list_of_list):
        # Сохраняем исходный список списков
        self.main_list = list_of_list

    def __iter__(self):
        """Инициализация курсоров для итерации по спискам."""
        self.main_list_cursor = 0  # Указатель на текущий список
        self.nested_list_cursor = -1  # Указатель на элемент внутри списка
        return self

    def __next__(self):
        """Получение следующего элемента в последовательности."""
        self.nested_list_cursor += 1

        # Переход к следующему вложенному списку, если текущий закончился
        if self.nested_list_cursor == len(self.main_list[self.main_list_cursor]):
            self.main_list_cursor += 1
            self.nested_list_cursor = 0

        # Остановка итерации, если закончились все списки
        if self.main_list_cursor == len(self.main_list):
            raise StopIteration

        # Возвращаем текущий элемент
        return self.main_list[self.main_list_cursor][self.nested_list_cursor]


@logger
def test_3():
    """Тестирование FlatIterator с различными вложенными списками."""

    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    # Проверка итератора с ожиданием результатов
    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    # Проверка, что итератор возвращает полный список при использовании list()
    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]


if __name__ == '__main__':
    test_3()
