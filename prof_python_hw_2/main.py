from pprint import pprint
import csv
import re


def change_full_name_and_phone(cont_list: list) -> None:
    """
    Функция изменяет формат номера телефона и разбивает полное имя на отдельные поля.
    """
    pattern = r"(\+7|8)[^\w]*(\d{3})[^\w]*(\d{3})[^\w]*(\d{2})[^\w]*(\d*)[ (]*(доб\.)*\s*(\d*)\)*"
    substitution = r"+7(\2)\3-\4-\5 \6\7"

    for contact in cont_list[1:]:
        phone = contact[-2]
        try:
            contact[-2] = re.sub(pattern, substitution, phone).strip()
        except Exception as e:
            print("Ошибка при обработке номера телефона:", e)

        full_name_list = ' '.join(contact[:3]).strip().split()
        if len(full_name_list) == 3:
            contact[0], contact[1], contact[2] = full_name_list
        else:
            contact[0], contact[1] = full_name_list


def join_duplicates(cont_list: list) -> None:
    """
    Функция объединяет дублирующиеся контакты в списке.
    """
    unique_contacts = {}

    for contact in cont_list[1:]:
        key = tuple(contact[:2])
        if key not in unique_contacts:
            unique_contacts[key] = contact
        else:
            for i in range(len(contact)):
                if not unique_contacts[key][i]:
                    unique_contacts[key][i] = contact[i]

    cont_list[1:] = list(unique_contacts.values())


if __name__ == "__main__":
    try:
        # читаем адресную книгу в формате CSV в список contacts_list
        with open("phonebook_raw.csv", encoding="utf-8") as f:
            rows = csv.reader(f, delimiter=",")
            contacts_list = list(rows)
    except FileNotFoundError as e:
        print("Файл не найден:", e)
    except Exception as e:
        print("Произошла ошибка при чтении файла:", e)

    change_full_name_and_phone(contacts_list)
    join_duplicates(contacts_list)

    try:
        # код для записи файла в формате CSV
        with open("phonebook.csv", "w", encoding="utf-8", newline="") as f:
            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerows(contacts_list)
    except Exception as e:
        print("Произошла ошибка при записи файла:", e)

    pprint(contacts_list, width=300)
