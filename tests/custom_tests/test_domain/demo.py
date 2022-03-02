import os


class UmlDecorator:

    def __init__(self, relations=[]):
        self.relations = relations

    def __call__(self, cls):
        class_attributes = [attribute + ': ' + str(type(getattr(cls, attribute)))
                            for attribute in cls.__dict__.keys()
                            if attribute.startswith('__') is False
                            and not callable(getattr(cls, attribute))]
        obj = cls()
        methods = [method for method in dir(obj)
                   if method.startswith('__') is False
                   and callable(getattr(obj, method))]

        instance_attributes = [attribute + ': ' + str(type(getattr(obj, attribute)))
                               for attribute in obj.__dict__.keys()
                               if attribute.startswith('__') is False
                               and not callable(getattr(obj, attribute))]


        self._create_classes_file(cls.__name__, class_attributes, methods, instance_attributes)
        self._create_relations_file()

        return cls

    @staticmethod
    def _create_classes_file(class_name, class_attributes, methods, instance_attributes):
        payload = f"class {class_name}" + "{\n"
        string_methods = ''
        string_class_attributes = ''
        string_instance_attributes = ''
        for method in methods:
            string_methods += method + '()\n'

        for class_attribute in class_attributes:
            string_class_attributes += class_attribute + '\n'

        for instance_attribute in instance_attributes:
            string_instance_attributes += instance_attribute + '\n'

        payload += string_methods + string_instance_attributes + string_class_attributes
        payload += "}\n"
        with open("classes.txt", "a") as file:
            file.write(payload)

    def _create_relations_file(self):
        with open("relations.txt", "a") as file:
            for relation in self.relations:
                file.write(relation + '\n')

    @staticmethod
    def create_uml_file():
        with open("classes.txt", "r+") as classes_file:
            classes = classes_file.readlines()
        os.remove("classes.txt")
        with open("relations.txt", "r+") as relations_file:
            relations = relations_file.readlines()
        os.remove("relations.txt")
        with open("../uml.txt", "w") as uml_file:
            uml_file.write("@startuml\n")
            for line in classes:
                uml_file.write(line)
            for line in relations:
                uml_file.write(line)
            uml_file.write("@enduml")


# @UmlDecorator()
class Wheel:
    pass


# @UmlDecorator(['Car *- Wheel : has 4 >'])
class Car:
    price = 100

    def __init__(self, fuel=0.0):
        self.fuel = fuel
        self.speed = 0.0
        self.wheel_list = [Wheel(), Wheel(), Wheel(), Wheel()]

    def start(self):
        pass

    def stop(self):
        pass

class SpecialCar(Car):

    def super_speed(self):
        pass

    def super_breaks(self):
        pass


class PrototypeCar(SpecialCar):

    def self_drive(self):
        pass

    def image_recognition(self):
        pass

    def _private_method(self):
        pass

# @UmlDecorator()
class License:
    pass


# @UmlDecorator(
#     [
#         'Driver - Car : drives >',
#         'Driver -left-o License : has a >'
#     ])
class Driver:
    pass


# @UmlDecorator(['Person -- Car : owns >'])
class Person:
    pass


class Bike:
    price = 5

    def __init__(self):
        self.speed = 0.0
        self._production_id = 1234
        self.owner = None
        self.style = None

    def brake(self):
        pass

    def cycle(self):
        pass

    def light_on(self):
        pass

Bike()