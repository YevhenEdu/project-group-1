from contacts.contact_book import ContactBook, Record
from .colored import Colored
from notes import NotesBook

class Commands:

    _notes_book = NotesBook()

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


# --------------------- NOTES ---------------------------------------------------------
    @staticmethod
    def list_notes():
        notes = Commands._notes_book.list_notes()
        if not notes:
            print(Colored.red("Немає жодної нотатки"))
            return

        for i, note in enumerate(notes, 1):
            print(Colored.blue(f"{i}. {note.title}"))

    @staticmethod
    def add_note():
        title = input("Введіть назву нотатки: ")
        text = input("Введіть текст: ")
        tags_input = input("Введіть теги (#tag1 #tag2): ")

        tags = [t.lstrip('#') for t in tags_input.split() if t.startswith("#")]

        try:
            Commands._notes_book.add_note(title, text, tags)
            print(Colored.green("Нотатку додано"))
        except ValueError as e:
            print(Colored.red(str(e)))

    @staticmethod
    def edit_note():
        title = input("Введіть назву нотатки для редагування: ")
        note = Commands._notes_book.find_by_title(title)

        if not note:
            print(Colored.red("Нотатку не знайдено"))
            return

        new_text = input("Новий текст: ")
        tags_input = input("Нові теги (#tag): ")
        new_tags = [t.lstrip("#") for t in tags_input.split() if t.startswith("#")]

        Commands._notes_book.edit_note(title, new_text, new_tags)
        print(Colored.green("Нотатку оновлено"))

    @staticmethod
    def delete_note():
        title = input("Введіть назву нотатки для видалення: ")
        if Commands._notes_book.delete_note(title):
            print(Colored.green("Нотатку видалено"))
        else:
            print(Colored.red("Нотатку не знайдено"))

    @staticmethod
    def find_note():
        keyword = input("Введіть ключове слово: ")
        results = Commands._notes_book.find_notes(keyword)

        if not results:
            print(Colored.red("Нічого не знайдено"))
        else:
            for note in results:
                print(Colored.blue(f"- {note.title}"))

    @staticmethod
    def show_note():
        title = input("Введіть назву нотатки: ")
        note = Commands._notes_book.find_by_title(title)

        if note:
            print(Colored.green(str(note)))
        else:
            print(Colored.red("Нотатку не знайдено"))

    @staticmethod
    def list_tags():
        tags = Commands._notes_book.get_all_tags()

        if not tags:
            print(Colored.red("Тегів немає"))
        else:
            print("Теги:", ", ".join(f"#{t}" for t in tags))

    @staticmethod
    def find_by_tag():
        tag = input("Введіть тег без решітки: ").lower()
        results = Commands._notes_book.find_notes_by_tag(tag)

        if not results:
            print(Colored.red("За цим тегом нічого немає"))
        else:
            for note in results:
                print(Colored.blue(f"- {note.title}"))
# -------------------- NOTES END -----------------------------------------

    # Dictionary mapping command names to their handler functions
    COMMAND_HANDLERS = {
        'help': help_command,
        'exit': exit_command,

        'list': list_contacts,
        'add': add_contact,
        'edit': edit_contact,
        'del': delete_contact,

        # Notes commands
        'notes': list_notes,
        'add-note': add_note,
        'edit-note': edit_note,
        'del-note': delete_note,
        'find-note': find_note,
        'show-note': show_note,
        'tags': list_tags,
        'find-by-tag': find_by_tag,
    }
