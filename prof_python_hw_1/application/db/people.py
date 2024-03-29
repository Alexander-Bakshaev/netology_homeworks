import numpy as np

def get_employees():
    print("Выборка сотрудников...")
    random_numbers = np.random.randint(1, 100, size=5)
    print("Случайные ID сотрудников:", random_numbers)
