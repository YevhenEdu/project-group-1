from contacts.contact_book import ContactBook, Record
from .colored import Colored

class Commands:
    @staticmethod
    def start_command():
        print(Colored.green("Привіт! Це бот-помічник!"))

    @staticmethod
    def help_command():
        commands = '\n'.join([f"/{cmd}" for cmd in Commands.COMMAND_HANDLERS.keys()])
        print(Colored.blue(f"Доступні команди:\n{commands}"))

    @staticmethod
    def invalid_command():
        print(Colored.red("Неправильна команда. Введіть 'help' для переліку команд."))

    @staticmethod
    def exit_command():
        print(Colored.green("На все добре!"))
        exit()

    @staticmethod
    def graceful_exit():
        print()
        Commands.exit_command()

    @staticmethod
    def list_contacts():
        contact_book = ContactBook()
        contact_book.list_contacts()

    @staticmethod
    def add_contact():
        try:
            name = input("Введіть ім'я нового контакта:")
            phone = input("Введить телефон (10 цифр):")
            email = input("Введить email:")
            birthday = input("Введить день народженя в форматі DD.MM.YYYY:")
            address = input("Введить адресу:")

            record = Record(name, phone, email, birthday, address)
            contact_book = ContactBook()
            contact_book.add_contact(record)
            print(Colored.green('Новий контакт створено: ' + str(record)))
        except ValueError as e:
            print(Colored.red('Проблема валідації:' + str(e)))

    @staticmethod
    def edit_contact():
        try:
            contact_book = ContactBook()

            name = input("Введіть ім'я контакта для редагування:")
            contact_book.data.get(name)
            if not contact_book.data.get(name):
                raise KeyError("Контакт не знайдено.")

            phone = input("Введить новий телефон (10 цифр):")
            email = input("Введить новий email:")
            birthday = input("Введить новий день народженя в форматі DD.MM.YYYY:")
            address = input("Введить нову адресу:")

            record = Record(name, phone, email, birthday, address)
            contact_book = ContactBook()
            contact_book.edit_contact(record)
            print(Colored.green('Контакт оновлено: ' + str(record)))
        except ValueError as e:
            print(Colored.red('Проблема валідації:' + str(e)))
        except KeyError as e:
            print(Colored.red('Проблема пошуку:' + str(e)))

    @staticmethod
    def delete_contact():
        try:
            name = input("Введіть ім'я контакта для видалення:")
            contact_book = ContactBook()
            contact_book.delete_contact(name)
            print("Контакт видалено")
        except KeyError as e:
            print(Colored.red('Проблема пошуку:' + str(e)))


    # Dictionary mapping command names to their handler functions
    COMMAND_HANDLERS = {
        'help': help_command,
        'exit': exit_command,

        'list': list_contacts,
        'add': add_contact,
        'edit': edit_contact,
        'del': delete_contact,
    }
