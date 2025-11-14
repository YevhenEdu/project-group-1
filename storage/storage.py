import pickle

class Storage:
    @staticmethod
    def load(filename):
        path = Storage.create_path(filename)
        try:
            with open(path, "rb") as file:
                loaded = pickle.load(file)
                return loaded
        except FileNotFoundError:
            return {}

    @staticmethod
    def save(filename, data=None):
        path = Storage.create_path(filename)
        with open(path, "wb") as file:
            pickle.dump(data, file)

    @staticmethod
    def create_path(filename):
        return f"./storage/{filename}"
