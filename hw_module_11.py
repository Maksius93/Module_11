from itertools import islice
from collections import UserDict
from datetime import datetime

dict_of_contacts = {}


class Field:
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return str(self.__value)

    @value.setter
    def value(self, value):
        self.__value = value

    def __str__(self) -> str:
        return str(self.value)


class Name(Field):
    def __str__(self) -> str:
        return str(self.value)


class Phone(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return str(self.__value)

    @value.setter
    def value(self, value):

        if len(value) != 10:
            raise ValueError("Number of phone is not full")
        self.__value = "+38" + value

    def __repr__(self) -> str:
        return str(self)


class Birthday(Field):
    def __init__(self, value):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return str(self.__value)

    @value.setter
    def value(self, value):
        correct_list = value.split(".")
        if len(correct_list) > 1:
            self.__value = value
        else:
            raise ValueError("Not correct format for date")

    def __repr__(self) -> str:
        return str(self)


class Record:
    def __init__(self, name: Name, phone=None, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.phones.append(phone)

    def add_phone(self, phone: Phone):
        self.phones.append(phone)
        return self.phones

    def change_phone(self, new_phone: Phone):
        self.phones.clear
        self.phones.append(new_phone)
        return self.phones

    def days_to_birthday(self):
        self.value = datetime.strptime(str(self.birthday), "%d.%m.%Y")
        self.value = self.value.replace(year=datetime.now().year)
        self.waiting_days = self.value.date() - datetime.now().date()
        return self.waiting_days


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = [record.phones, record.birthday]

    def __getitem__(self, key):
        return self.data.get(key, "Not contact with this name. Try again")

    def __setitem__(self, key, item):
        self.data[key] = item

    def iterator(self, number_of_iteration):
        result = islice(self.data.items(), number_of_iteration)
        return result

    def __str__(self) -> str:
        return str(self)


dict = AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError:
            return print("Enter user name or correct integer number")
    return inner


def hello(*args):
    return print("How can I help You?")


def add(*args):
    list_of_param = args[0].split()
    name = Name(list_of_param.pop(0))
    record = Record(name)
    for el in list_of_param:
        if not el.isdigit():
            birthday = Birthday(el)
            record.birthday = birthday
        else:
            phone = Phone(el)
            record.add_phone(phone)
    dict.add_record(record)
    return dict


def change(*args):
    list_of_param = args[0].split()
    name = (list_of_param.pop(0))
    contact_details = dict[name]
    record = Record(Name(name))
    for el in list_of_param:
        phone = Phone(el)
        record.add_phone(phone)
    new_phone = record.phones
    record.change_phone(new_phone)
    contact_details[0] = record.phones
    dict.update({name: contact_details})
    return dict


def birthday(*args):
    name = str(args[0])
    contact_details = dict[name]
    if len(contact_details) > 1:
        record = Record(name, contact_details[0], contact_details[1])
    wait_days = record.days_to_birthday()
    return print(wait_days)


def phone(*args):
    name = str(args[0])
    contact_details = dict[name]
    print(contact_details)


@ input_error
def show_all(*args):
    if isinstance(int(args[0]), int):
        result = dict.iterator(int(args[0]))
        for el in result:
            print(el)
    else:
        raise ValueError()


def exit(*args):
    return print("Good bye!")


def no_command(*args):
    return print("Unknown command, try again")


COMMANDS = {hello: "hello", add: "add", change: "change", birthday: "birthday", phone: "phone",
            show_all: "show all", exit: ["good bye", "close", "exit"]}


def handler(text):
    for command, kword in COMMANDS.items():
        if type(kword) is str:
            if text.startswith(kword):
                return command, text.replace(kword, "").strip()
        else:
            if text in kword:
                return command, None
    return no_command, None


def main():
    while True:
        user_input = input(">>>")
        command, data = handler(user_input.lower())
        command(data)
        if command == exit:
            break


if __name__ == "__main__":
    main()
