class Colored:
    @staticmethod
    def green(text):
        return '\033[92m' + text + '\033[0m'

    @staticmethod
    def red(text):
        return '\033[91m' + text + '\033[0m'

    @staticmethod
    def blue(text):
        return '\033[94m' + text + '\033[0m'