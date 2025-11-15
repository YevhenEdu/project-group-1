from collections import UserDict
from datetime import datetime
import pickle
import re


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"[+\-\d\s]+", value):
            raise ValueError("Телефон може містити лише цифри, '+', '-' та пробіли.")
        super().__init__(value)


class Email(Field):
    def __init__(self, value):
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w{2,4}$", value):
            raise ValueError("Невірний формат email. Використовуйте name@domain.com")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Невірний формат дати. Використовуйте DD.MM.YYYY")


class Record:
    def __init__(self, name, address="", phone=None, email=None, birthday=None):
        self.name = Name(name)
        self.address = address
        self.phones = []
        if phone:
            self.add_phone(phone)
        self.email = Email(email) if email else None
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Старий телефон не знайдено.")
    

    def days_to_birthday(self):
        if self.birthday is None:
            return -1
        today = datetime.now().date()
        birthday_date = self.birthday.value 
        next_birthday = birthday_date.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        
        delta = next_birthday - today
        return delta.days
    
    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "—"
        email = self.email.value if self.email else "—"
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "—"
        return f"{self.name.value}: {phones} | Email: {email} | Birthday: {birthday} | Address: {self.address}"


class ContactBook(UserDict):
    def __init__(self, filename="contacts.pkl"):
        super().__init__()
        self.filename = filename
        self.load_data()

    def add_contact(self, record: Record):
        self.data[record.name.value] = record
        self.save_data()

    def edit_contact(self, name, **kwargs):
        record = self.data.get(name)
        if not record:
            raise KeyError("Контакт не знайдено.")

        if "name" in kwargs and kwargs["name"]:
            record.name = Name(kwargs["name"])
        if "address" in kwargs and kwargs["address"]:
            record.address = kwargs["address"]
        if "phone" in kwargs and kwargs["phone"]:
            record.add_phone(kwargs["phone"])
        if "email" in kwargs and kwargs["email"]:
            record.email = Email(kwargs["email"])
        if "birthday" in kwargs and kwargs["birthday"]:
            record.birthday = Birthday(kwargs["birthday"])

        self.save_data()

    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
            self.save_data()
        else:
            raise KeyError("Контакт не знайдено.")

    def save_data(self):
        with open(self.filename, "wb") as f:
            pickle.dump(self, f)

    def load_data(self):
        try:
            with open(self.filename, "rb") as f:
                loaded = pickle.load(f)
                self.data = loaded.data
        except FileNotFoundError:
            self.data = {}

    def list_contacts(self):
        if not self.data:
            print("Список контактів порожній.")
            return
        for record in self.data.values():
            print(record)

    def birthdays_in_days(self, days: int):
        if not isinstance(days, int) or days < 0:
            raise ValueError("Кількість днів повинна бути невід'ємним цілим числом.")
        upcoming_birthdays = []

        for record in self.data.values():
            if record.birthdays:
                days_left = record.days_to_birthdays()
                if days_left == days:
                    upcoming_birthdays.append(record)

        return upcoming_birthdays  
