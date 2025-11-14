from collections import UserDict
from datetime import datetime
import re


from storage import Storage


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
    def __init__(self, name, phone=None, email=None, birthday=None, address=""):
        self.name = Name(name)
        self.phones = []
        if phone:
            self.add_phone(phone)
        self.email = Email(email) if email else None
        self.birthday = Birthday(birthday) if birthday else None
        self.address = address

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def change_phone(self, old_phone, new_phone):
        for i, p in enumerate(self.phones):
            if p.value == old_phone:
                self.phones[i] = Phone(new_phone)
                return
        raise ValueError("Старий телефон не знайдено.")

    def __str__(self):
        phones = ", ".join(p.value for p in self.phones) if self.phones else "—"
        email = self.email.value if self.email else "—"
        birthday = self.birthday.value.strftime("%d.%m.%Y") if self.birthday else "—"
        return f"Name: {self.name.value}| Phones: {phones} | Email: {email} | Birthday: {birthday} | Address: {self.address}"


class ContactBook(UserDict):
    def __init__(self, filename="contacts.pkl"):
        super().__init__()
        self.filename = filename
        self.load_data()

    def add_contact(self, record: Record):
        self.data[record.name.value] = record
        self.save_data()

    def edit_contact(self, edited_record: Record):
        record = self.data.get(edited_record.name.value)
        if not record:
            raise KeyError("Контакт не знайдено.")

        record = edited_record
        self.data[record.name.value] = record
        self.save_data()

    def delete_contact(self, name):
        if name in self.data:
            del self.data[name]
            self.save_data()
        else:
            raise KeyError("Контакт не знайдено.")

    def save_data(self):
        Storage.save(self.filename, self.data)

    def load_data(self):
        self.data = Storage.load(self.filename)

    def list_contacts(self):
        if not self.data:
            print("Список контактів порожній.")
            return
        for record in self.data.values():
            print(record)
