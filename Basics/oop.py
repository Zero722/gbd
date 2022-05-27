from datetime import date

class Dog:
    attr1 = "mammal"

    def __init__(self, name):
        self.name = name

    def do_tricks(self):
        print("Roll over")


class StrayDog(Dog):
    def __init__(self, name, breed, location):
        self.breed = breed
        self.location = location

        Dog.__init__(self, name)

    def details(self):
        print("My name is", self.name)
        print("I am a", self.breed)
        print("You can find me in", self.location)

    def do_tricks(self):
        print("Do nothing")


tommy = Dog("Tommy")
print("Hello, My name is", tommy.name)
print("I am", tommy.attr1)
tommy.do_tricks()
print("\n")

dalle = StrayDog("Dalle", "Pog", "Sanepa")
dalle.details()
dalle.do_tricks()


class Class1:
 
    __hiddenVar = 0
   
    def add(self, increment):
        self.__hiddenVar += increment
        print (self.__hiddenVar)

obj1 = Class1()    
obj1.add(2)
obj1.add(5)
 
# This line causes error
# print (obj1.__hiddenVar)

# This doesn't give error
print (obj1._Class1__hiddenVar)


  
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
      
    
    @classmethod
    def fromBirthYear(cls, name, year):
        return cls(name, date.today().year - year)
      
    @staticmethod
    def isAdult(age):
        return age > 18
  
person1 = Person('mayank', 21)
person2 = Person.fromBirthYear('mayank', 1996)
  
print(person1.age)
print(person2.age)
  
print(Person.isAdult(22))



from abc import ABC, abstractmethod
class Animal(ABC):
    
    @abstractmethod
    def move(self):
        pass
 
class Human(Animal):
    def move(self):
        print("I can walk and run")
 
class Snake(Animal):
    def move(self):
        print("I can crawl")
 
class Bird(Animal):
    def move(self):
        print("I can fly")

ram = Human()
ram.move()
 
hebi = Snake()
hebi.move()

peeka = Bird()
peeka.move()
 
# Cannot be instantiated
# lion = Animal()