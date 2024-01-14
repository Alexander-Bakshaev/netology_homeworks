from pprint import pprint


def creating_dict():
    with open('cook_book.txt', 'r') as file:
        cook_book = {}
        for line in file:
            dish = line.rstrip()
            ingredients_count = int(file.readline().strip())
            cook_book[dish] = [0] * ingredients_count
            for item in range(ingredients_count):
                string_ingredient = file.readline().strip().split(' | ')
                cook_book[dish][item] = {'ingredient_name': string_ingredient[0],
                                       'quantity': int(string_ingredient[1]),
                                       'measure': string_ingredient[2]}
            file.readline()

    return cook_book


pprint(creating_dict(), width=100)


def get_shop_list_by_dishes(dishes: list, person_count: int):
    result_dict = {}
    cook_book = creating_dict()
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
