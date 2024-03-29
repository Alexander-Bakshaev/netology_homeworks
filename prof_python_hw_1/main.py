from application.salary import calculate_salary
from application.db.people import get_employees
from datetime import datetime

def main():
    date = datetime.today().date().strftime("%d.%m.%Y")
    print("Текущая дата:", date)
    calculate_salary()
    get_employees()

if __name__ == '__main__':
    main()
