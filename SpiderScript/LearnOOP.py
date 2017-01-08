# -*- coding: utf-8 -*-
"""
Created on Sat Dec 31 03:06:55 2016

@author: ADEKUNLE
"""

#Background
#class Employeee:
#    pass #Pass allows us to bypass a class if we are not using filling it yet

#Now for an employee he has firstname, lastname, email, pay
#emp_1 = Employeee()
#emp_2 = Employeee()

#emp_1.first = "Babatunde"
#emp_1.last = "Adekunle"
#emp_1.email = "Adekunle.Babatunde@company.com"
#emp_1.pay = 50000

#emp_2.first = "Test"
#emp_2.last = "User"
#emp_2.email = "Test.User@company.com"
#emp_2.pay = 60000

#This idea is what is used to instantiat the init of a class
class Employee:
    
    number_of_emps = 0
    raise_amount = 1.04
    
    def __init__(self, first, last, pay):
        self.first = first
        #Note that this can also be written as self.fname = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@company.com'
        
        #Increment number of employee as each one runs self in the init i.e...
        #... each employee is created
        Employee.number_of_emps += 1
#You will still need to instantiate the Employee class as done in liines 13/14

#On another note, taking it back from line 49, to do same stuff with a function
    def fullname(self):
        #takes in only self to access the attributes of __init__
        return '{} {}'.format(self.first, self.last)
        #The reason for 'self' is so that the fullname will work for all...
        #...instances of the class like it should be able to work for both..
        #...emp_1 and emp_2 as instantiated.
    
    def payvalue(self):
        return '{} {} {}'.format('Amount for', self.fullname(), self.pay)
    
    #def apply_raise(self): #raise for all employee
        #self.pay = int(self.pay * 1.04)
        
    def apply_raise_mod(self): #using class variable 'raise_amount'
        self.pay = int(self.pay * self.raise_amount) #Or Employee.raise_amount
        #self.raise_amount has added advantage of modifying only for the ...
        #...instance of a class
    
    #define a set_raise_amount class method
    @classmethod #simply use this decorator to create a class method
    def set_raise_amount(cls, amount):
        cls.raise_amount = amount
        
    @classmethod
    def from_string(cls, emp_str):
        first, last, pay = emp_str.split('-')
        return cls(first, last, pay)
        
    @staticmethod #simple decorator to create a static method
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True
    
    def __repr__(self):
        return "Employee('{}', '{}', '{}')".format(self.first, self.last, self.pay)
        
    def __str__(self):
        return '{} - {}'.format(self.fullname(), self.email)
        #Now the print(emp) gives a more readable line for users

    def __add__(self, other):
        return self.pay + other.pay
    
    def __len__(self):
        return len(self.fullname())

#To inherit from a class
class Developer(Employee): #basic way to inherit from a class
    #We can change the raise_amount variable in our class
    raise_amount = 1.10
    
    #Assuming we need to add prog_lang attribute to our Developer class, to...
    #...do more than the parent class
    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay) #to singly inherit the classattri
        #Employee.__init__(self, first, last, pay) works as well
        self.prog_lang = prog_lang
        
class Manager(Employee):
    
     def __init__(self, first, last, pay, employees = None): 
         #Set default employee to None
         #NB: You dont want to pass mutable objects as attributes in the init
         #...method
         super().__init__(first, last, pay) #to singly inherit the classattr
         #Employee.__init__(self, first, last, pay) works as well
         if employees is None:
             self.employees = []
         else:
             self.employees = employees
             
     def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
            
     def rem_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)
            
     def print_emp(self):
        for emp in self.employees:
            print('-->', emp.fullname())

#Developer hass all attribute and methods of the Employee Class
    
        
print('{} {}'.format('Number of employer is', Employee.number_of_emps))
emp_1 = Employee("Babatunde", "Adekunle", 50000)
emp_2 = Employee("Test", "User", 60000)


##print(emp_1.email)

##print(emp_2.email)


#All the elements of the __init__ function are attributes of the class
#To perform some kind of actions we add methods to the class
#Example is to print out the employee full name 
#    This example is done outside of the class.

###print('{} {}'.format(emp_1.first, emp_1.last))

#ToDo:
#Print result using class method
#print(emp_1.fullname(), '\n', emp_2.fullname())


#ToDo:
#On another note, the class can be called directly on the method, but in this...
#... you will need to specify the instance on which the method is being called.
#print(Employee.fullname(emp_1)) #so it does similar thing as emp_1.fullname()
#..this is usually important when inheriting from other classes.

#ToDo:
#  Define a method in the Employee class that returns the pay for a particular
#...employee, save it in 'payvalue'
#print(emp_1.payvalue())

#Class Variables: Variables that are shared by all instanses of a class
#Instance Variables: Are the variables set in the init method

#The method apply_raise when added, then we can do something like this
#print(emp_1.pay)
#emp_1.apply_raise()
#print(emp_1.pay) #remember the new pay was saved into the self.pay variable

#ToDo:
#Apply raise modified to include a class variable(raise amount), which is ...
#... both accessible by the instance of the class or the Class itself
#To test the accessibility
#print(Employee.raise_amount)
#print(emp_1.raise_amount)
#print(emp_2.raise_amount)

#To check namespace of a class or instance of a class.__dict__ attribute
#print(Employee.__dict__)
#print(emp_1.__dict__)

#Now to run  a change in raise_amount you can do something like this
#Employee.raise_amount = 1.05

#Also i can do raise_amount for only an instance of a class
#emp_1.raise_amount = 1.05 #With this emp_1 now has raise_amount in its namespace

#print(Employee.raise_amount)
#print(emp_1.raise_amount)
#print(emp_2.raise_amount)

#Another awesome concept is to increment as each self is instantiated i.e. ...
#... as new employee is created

print('{} {}'.format('Number of employer now is', Employee.number_of_emps))

#3. There is a difference between Regular Methods, Class Methods and Static...
#...methods
#...Regular Methods automatically takes the instance(self) as the 1st argument
#...Class methods different from regular methods in that it takes the class...
#....as its 1st argument
#Employee.set_raise_amount(1.05) #no need to specify class again, since it...
#...automatically pass the class to the method
#It's just similar to saying Employee.raise_amount = 1.05, just that we now...
#...introduce it easily with a method
#print(Employee.raise_amount)
#print(emp_1.raise_amount)
#print(emp_2.raise_amount)

#To Do: Given employee string seperated by hyphen, create a new employee with..
#...the Employee class
#Now assume the above is a common use case, we can create a new construct...
#...class method, a term called 'Alternative Constructor' but before then, ...
#...to do this without the construct is given below
emp_str_1 = 'John-Doe-7000'
emp_str_2 = 'Steve-Smith-3000'
emp_str_3 = 'Jane-Doe-4000'
#
#first, last, pay = emp_str_1.split('-')
#
#new_emp_1 = Employee(first, last, pay)
#
#TO do same thing After creating class method employee string, then we can... 
#... use to create new_emp1
new_emp_1 = Employee.from_string(emp_str_1)
print('{} {}'.format('Number of employer now is', Employee.number_of_emps))
print(new_emp_1.email)

#Static Method, simply don't access the instance or the class within the...
#...function, usually created cos it has logical connection to the class
#ToDo: Test Static method
import datetime

my_date = datetime.date(2016, 12, 3)

print(Employee.is_workday(my_date))

#Question: the weekday() method used in the class where was it gotten from
#and if its the method on the day attribute, how was it able to check the '=='
#sign to be true or false.
#
#
#Inheritace allows us to inherit attributes and methods from a parent class, ...
#... thus we can create subclasses - that gets all the functionality of...
#... the parent class, we can override or add new functionality without ...
#... affecting the parent class in anyway
#TODO Having created class Developer create two new employee
dev_1 = Developer('Mike', 'Shaw', 70000, 'Python')
dev_2 = Developer('David', 'Fresh', 80000, 'Java')

print(dev_1.email, dev_1.prog_lang)
print(dev_2.prog_lang)

#Method Resolution Order are the classes that python search attributes and...
#... functions for an inherited class
#To try out apply_raise()
#print(dev_1.pay)
#dev_1.apply_raise_mod()
#print(dev_1.pay)

#Note that if you use class Employee to instantiate, the subclass variable...
#...usually not affect the class variable
#dev_1 = Employee('Mike', 'Shaw', 70000)
#
#print(dev_1.pay)
#dev_1.apply_raise_mod()
#print(dev_1.pay)
#
#Question: Do you need to bring in the the init method to expand a subclass

#Question2: Will you be able to inherit all attributes of a parentclass and
#...subclass if you inherit a subclass directly for a new subclass, has seen..
#...in the HTTPException where Badrequest was also inherited by a
#...clientDisconnect subclass

#After creating the Manager subclass
#TODO: do some stunt with the Manager subclass
#mgr_1 = Manager('Mor', 'Grath', 90000, [dev_1])
#
#print(mgr_1.email)
#mgr_1.print_emp()
#
#mgr_1.add_emp(dev_2)
#mgr_1.print_emp()
#
#mgr_1.rem_emp(dev_1)
#mgr_1.print_emp()
##
##One quick thing is to check if an instance is an instance of a class
#print(isinstance(mgr_1, Manager))
#print(isinstance(mgr_1, Employee))
#print(isinstance(mgr_1, Developer))
#
##Another one is to check if a class is a subclass of another class
#print(issubclass(Manager, Employee))
#print(issubclass(Developer, Employee))
#print(issubclass(Manager, Developer))
#print(issubclass(Employee, Manager))

#4. The special Method __repr__ and __str__, the double underscore == dunder.
#print(dev_1)
#
##You can print out __repr__ and __str__ specifically
#print(repr(emp_1))
#print(str(emp_1))
#
##What is literarilly happening is that we have:
#print(emp_1.__repr__())
#print(emp_1.__str__())

#Taking us a little into the inner workings of pyton
print(1 + 2)
print('a' + 'b')

#Under the hood this is
print(int.__add__(1, 2))
print(str.__add__('a', 'b'))

#After initiating __add__ in Employee class we can calcuate sum of salary for..
#..two employee
print(emp_1 + emp_2) #The '+' sign calls on __add__()

#More examples __len__()
print(len('test'))
print('test'.__len__())

print(len(emp_1))