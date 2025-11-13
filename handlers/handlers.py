from .colored import Colored
from storage import Storage

class Commands:
    @staticmethod
    def start_command():
        print(Colored.green("Привіт! Це бот-помічник!"))
        Storage.load()

    @staticmethod
    def help_command():
        commands = '\n'.join([f"/{cmd}" for cmd in Commands.COMMAND_HANDLERS.keys()])
        print(Colored.blue(f"Доступні команди:\n{commands}"))

    @staticmethod
    def invalid_command():
        print(Colored.red("Неправильна команда. Введіть 'help' для переліку команд."))

    @staticmethod
    def exit_command():
        Storage.save()
        print(Colored.green("На все добре!"))
        exit()

    @staticmethod
    def graceful_exit():
        print()
        Commands.exit_command()

    # Dictionary mapping command names to their handler functions
    COMMAND_HANDLERS = {
        'help': help_command,
        'exit': exit_command
    }