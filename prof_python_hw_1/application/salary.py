import numpy as np

def calculate_salary():
    print("Вычисление оклада сотрудников...")
    data = [2000, 2000, 3000, 4000, 5000]
    mean_salary = np.mean(data)
    print("Средний оклад:", mean_salary)
