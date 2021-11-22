from datetime import datetime
from collections import UserDict
import pickle


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name] = record

    def iterator(self, n):
        data_list = list(self.data.values())
        while data_list:
            for i in data_list[:n]:
                yield i
            data_list = data_list[n:]

    def search_contacts(self, search_item):
        result_list = []
        for i in self.data.values():
            if search_item.lower() in str(i).lower():
                result_list.append(i)
        if result_list:
            return result_list
        else:
            return 'No such contact!'

    def serializer(self, file_name='dump.txt'):
        with open(file_name, 'wb') as file:
            pickle.dump(self, file)

    def deserializer(self, file_name='dump.txt'):
        try:
            with open(file_name, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError as e:
            print(e)


class Record:
    def __init__(self, name, birthday=None):
        self.name = name
        self.phones = []
        self.birthday = birthday

    def add_field(self, phone):
        self.phones.append(phone)

    def change_field(self, phone, new_phone):
        try:
            self.phones[self.phones.index(phone)] = new_phone
        except ValueError as e:
            return e

    def delete_field(self, phone):
        try:
            self.phones.remove(phone)
        except ValueError:
            return f'{phone} is not in list'

    def days_to_birthday(self):
        now = datetime.today()
        try:
            if datetime(self.birthday.value.year, self.birthday.value.month, self.birthday.value.day) < now:
                birthday_date = datetime(now.year, self.birthday.value.month, self.birthday.value.day)
                if birthday_date > now:
                    return (birthday_date - now).days + 1
                else:
                    birthday_date = datetime(now.year + 1, self.birthday.value.month, self.birthday.value.day)
                    return (birthday_date - now).days + 1
            else:
                return 'The date cannot be in the future!'
        except AttributeError:
            return 'Wrong date format!'

    def __repr__(self):
        return f"{self.name} {self.birthday} {self.phones}"


class Field:
    def __init__(self, value):
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value

    def __repr__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        if value.isdigit():
            if len(value) == 10:
                self.__value = value
            else:
                print('There should be 10 numbers!')
        else:
            print('There should be only numbers!')


class Birthday(Field):
    def __init__(self, value):
        super().__init__(value)
        self.__value = value
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value = value
        try:
            s = datetime.strptime(value, '%Y-%m-%d').date()
            self.__value = s
        except ValueError as e:
            print(e)

if __name__ == '__main__':
    pass

name = Name('Sasha')
phone = Phone('0236537890')
birthday = Birthday('2020-11-30')
name1 = Name('Masha')
phone1 = Phone('0948763456')
phone2 = Phone('0000000000')
birthday1 = Birthday('2020-10-30')
r = Record(name, birthday)
r.change_field(phone, phone2)
r.add_field(phone1)
r1 = Record(name1)
r.add_field(phone)
r1.add_field(phone1)
print(r.days_to_birthday())
print(r1.days_to_birthday())
ab = AddressBook()
ab.add_record(r)
ab.add_record(r1)
it = ab.iterator(3)
for i in it:
    print(i)
print(ab.search_contacts('sha'))
print(ab.search_contacts('023'))
ab.serializer()
ab = AddressBook()
ab.deserializer()
it = ab.iterator(3)
for i in it:
    print(i)