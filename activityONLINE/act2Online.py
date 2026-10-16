class Employee:
    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = int(pay)

    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

class Developer(Employee):
    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
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

    def get_employees(self):
        for emp in self.employees:
            print(emp.first)

dev_1 = Employee.from_string("Alex-Rivera-95000")
Newdev_1 = Developer(dev_1.first, dev_1.last, dev_1.pay, "Python")

manager1 = Manager("allen", "dave", 1000, )
manager1.add_employee(Newdev_1)

manager1.get_employees()

print(isinstance(Newdev_1, Employee))
print(issubclass(Manager, Employee))