import json


class BaseFileUtil:
    def __init__(self):
        self.FILE_PATH = ''
        self.data = None

    def init(self):
        pass

    def save(self):
        with open(self.FILE_PATH, 'w') as f:
            json.dump(self.data, f, indent=4)

    def load(self):
        try:
            with open(self.FILE_PATH, 'r') as f:
                self.data = json.load(f)
        except IOError:
            self.clear()

    def clear(self):
        self.init()
        self.save()
        self.load()

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value
        self.save()

