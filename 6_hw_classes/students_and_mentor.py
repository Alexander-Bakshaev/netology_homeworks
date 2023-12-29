class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def rate_hw(self, lecturer, course, grade):
        if isinstance(lecturer,
                      Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    def __average_grade(self):
        total = 0
        count = 0
        for course in self.grades:
            total += sum(self.grades[course])
            count += len(self.grades[course])
        return round(total / count, 2)

    def __str__(self):
        return (f"Имя: {self.name}\n"
                f"Фамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {self.__average_grade()}\n"
                f"Курсы в процессе изучения: {', '.join(self.courses_in_progress)}\n"
                f"Завершенные курсы: {', '.join(self.finished_courses)}")

    def __ed__(self, student):
        if isinstance(student, Student):
            return self.__average_grade() == student.__average_grade()
        else:
            return 'Ошибка'

    def __lt__(self, student):
        if isinstance(student, Student):
            return self.__average_grade() < student.__average_grade()
        else:
            return 'Ошибка'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname}'


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []
        self.grades = {}

    def __average_grade(self):
        total = 0
        count = 0
        for course in self.grades:
            total += sum(self.grades[course])
            count += len(self.grades[course])
        return round(total / count, 2)

    def __str__(self):
        return f'Имя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {self.__average_grade()}'

    def __eq__(self, lector):
        if not isinstance(lector, Lecturer):
            return NotImplemented
        return self.__average_grade() == lector.__average_grade()

    def __lt__(self, lector):
        if not isinstance(lector, Lecturer):
            return NotImplemented
        return self.__average_grade() < lector.__average_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


def average_grade_students(students, course):
    total = 0
    count = 0
    for student in students:
        if isinstance(student, Student) and course in student.grades:
            total += sum(student.grades[course])
            count += len(student.grades[course])
    if count == 0:
        return 0
    else:
        return round(total / count, 2)


def average_grade_lecturers(lecturers, course):
    total = 0
    count = 0
    for lector in lecturers:
        if course in lector.grades:
            total += sum(lector.grades[course])
            count += len(lector.grades[course])
    if count == 0:
        return 0
    else:
        return round(total / count, 2)


student_1 = Student('Сергей', 'Сергеев', 'man')
student_1.finished_courses += ['Введение в программирование']
student_1.courses_in_progress += ['Python', 'JS', 'Git']
student_2 = Student('Пётр', 'Петров', 'man')
student_2.finished_courses += ['Введение в программирование']
student_2.courses_in_progress += ['Python', 'JS', 'CSS', 'HTML']

lecturer_1 = Lecturer('Леонид', 'Якубович')
lecturer_1.courses_attached += ['Python', 'Git', 'CSS', 'HTML']
lecturer_2 = Lecturer('Валдис', 'Пельш')
lecturer_2.courses_attached += ['Java', 'JS', 'CSS', 'HTML']

reviewer_1 = Reviewer('Андрей', 'Малахов')
reviewer_1.courses_attached += ['JS', 'Git', 'CSS']
reviewer_2 = Reviewer('Иван', 'Ургант')
reviewer_2.courses_attached += ['Python', 'JS', 'HTML']

student_1.rate_hw(lecturer_1, 'Python', 9)
student_1.rate_hw(lecturer_2, 'JS', 7)
student_2.rate_hw(lecturer_1, 'CSS', 8)
student_2.rate_hw(lecturer_2, 'HTML', 6)

reviewer_1.rate_hw(student_1, 'JS', 10)
reviewer_1.rate_hw(student_1, 'Git', 9)
reviewer_1.rate_hw(student_2, 'CSS', 8)
reviewer_2.rate_hw(student_1, 'HTML', 9)
reviewer_2.rate_hw(student_2, 'Python', 6)
reviewer_2.rate_hw(student_2, 'JS', 7)

print(student_1)
print()
print(student_2)
print()
print(lecturer_1)
print()
print(lecturer_2)
print()
print(reviewer_1)
print()
print(reviewer_2)
print()
print(student_1 > student_2)
print(student_1 < student_2)
print(student_1 == student_2)
print()
print(lecturer_1 > lecturer_2)
print(lecturer_1 < lecturer_2)
print(lecturer_1 == lecturer_2)
print()
print(average_grade_students([student_1, student_2], 'JS'))
print(average_grade_lecturers([lecturer_1, lecturer_2], 'Git'))
