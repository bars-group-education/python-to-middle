import json


class Record:

    def __init__(self, code, name) -> None:
        super().__init__()
        self.code = code
        self.name = name

    def as_dict(self):
        return {self.code: self.name}


class RecordStore:

    def __init__(self) -> None:
        super().__init__()
        self._records = []
        self._rc = Tojson(self._records)
        self._sv = Savetofile(self._rc)

    def add_record(self, record):
        self._records.append(record)

    def del_record(self, record):
        self._records.remove(record)

    def to_json(self):

        return self._rc.convert()

    def save_to_file(self, path):
        self._sv.save_to_file(path)


class Tojson:

    def __init__(self, store):
        self._store = store

    def convert(self):
        result = json.dumps([x.as_dict() for x in self._store])

        return result


class Savetofile:

    def __init__(self, path):
        self._path = path

    def save_to_file(self, path):
        with open(path, 'w') as f:
            f.write(self._path.convert())
