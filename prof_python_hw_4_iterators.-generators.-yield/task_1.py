class FlatIterator:
    def __init__(self, nested_list):
        self.nested_list = nested_list
        self.current_list_index = 0
        self.current_item_index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_list_index >= len(self.nested_list):
            raise StopIteration

        current_item = self.nested_list[self.current_list_index][self.current_item_index]
        self.current_item_index += 1

        if self.current_item_index >= len(self.nested_list[self.current_list_index]):
            self.current_list_index += 1
            self.current_item_index = 0

        return current_item

def test():
    nested_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None],
    ]
    flat_iterator = FlatIterator(nested_list)
    check_items = ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]

    for check_item in check_items:
        assert next(flat_iterator) == check_item

    flat_iterator = FlatIterator(nested_list)
    assert list(flat_iterator) == check_items

if __name__ == '__main__':
    test()
    print("Тест пройден.")