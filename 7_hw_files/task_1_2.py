from pprint import pprint


def creating_dict():
    with open('cook_book.txt', 'r') as file:
        cook_book = {}
        dish = None
        for line in file:
            line = line.strip()
            if not line:
                continue
            if dish is None:
                dish = line
                cook_book[dish] = []
            else:
                ingredients_count = int(line)
                for _ in range(ingredients_count):
                    string_ingredient = file.readline().strip().split(' | ')
                    ingredient = {
                        'ingredient_name': string_ingredient[0],
                        'quantity': int(string_ingredient[1]),
                        'measure': string_ingredient[2]
                    }
                    cook_book[dish].append(ingredient)
                dish = None
    return cook_book


pprint(creating_dict(), width=100)


def get_shop_list_by_dishes(dishes: list, person_count: int):
    cook_book = creating_dict()
    result_dict = {}
    for dish in dishes:
        for value in cook_book[dish]:
            ingredient = value['ingredient_name']
            measure = value['measure']
            quantity = value['quantity']
            if ingredient in result_dict:
                result_dict[ingredient]['quantity'] += quantity * person_count
            else:
                result_dict[ingredient] = {'measure': measure, 'quantity': quantity * person_count}

    return result_dict


print('\n\n')
pprint(get_shop_list_by_dishes(['Запеченный картофель', 'Утка по-пекински'], 3), width=100)
