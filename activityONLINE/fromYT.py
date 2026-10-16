class Book:

    discount_rate = 0.10
    total_books = 0

    def  __init__(self, title, author, price):
        self.title = str(title)
        self.author = str(author)
        self.price = float(price)

        Book.total_books += 1

    def get_summary(self):
        # summary = self.title + ' by ' + self.author + ' - ${}'.format(self.price)
        summary = "'{}' by {} - {}".format(self.title, self.author, self.price)
        return summary


    def apply_discount(self):
        self.price = self.price - (self.price * self.discount_rate)
        return self.price

    @classmethod
    def get_books(cls, discount_rate):
        pass


book1 = Book("How deep is your love?", "Dave", 800)
book2 = Book("The anatomy of my dreams", "Deby", 1999)

book3 = "Alexa - Not so loud - 1000"

author, title, price = book3.split('-')
newBook3 = Book(title, author, price)
print(newBook3.author)
print(newBook3.get_summary())

import datetime
my_date = datetime.date(2026, 7, 8)

print(Employee.is_workday(my_date))


class Employee:

    raise_amount = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = '{}.{}@gmail.com'.format(self.first, self.last)


    def fullname(self):
        return "{} {}".format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)
        return self.pay

    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split("-")
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        sum = "working day"
        return sum

class Developer(Employee):
    raise_amount = 1.10
    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        Employee.__init__(self, first, last, pay)

        self.prog_lang = prog_lang

class Manager(Employee):
    def __init__(self, first, last, pay, employees = None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_employee(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_employee(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_employees(self):
        for emp in self.employees:
            print('--->', emp.fullname())


dev1 = Developer('Allen Dave', 'Ylagan', 5000, 'Phyton')
dev2 = Developer('Russel', 'Daquipil', 5000, 'C++')
dev3 = Developer('Justin Lloyd', 'Borja', 5000, 'Java')

manager1 = Manager ('James William', 'Tabios', 9000, [dev1, dev2, dev3])

manager1.print_employees()

print(isinstance(manager1, Manager))
print(isinstance(manager1, Employee))
print(isinstance(manager1, Developer))

print(issubclass(Developer, Employee))