from handlers import Commands

def main():
    try:
        Commands.start_command()
        while True:
            command = input('> ')
            handler = Commands.COMMAND_HANDLERS.get(command)

            if handler:
                handler()
            else:
                Commands.invalid_command()
    except KeyboardInterrupt:
        Commands.graceful_exit()
    except EOFError:
        Commands.graceful_exit()

if __name__ == "__main__":
    main()
