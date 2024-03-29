from application.salary import *
from application.db.people import *
from datetime import *

def main():
    date = datetime.today().date().strftime("%d.%m.%Y")
    print("Текущая дата:", date)
    calculate_salary()
    get_employees()

if __name__ == '__main__':
    main()
