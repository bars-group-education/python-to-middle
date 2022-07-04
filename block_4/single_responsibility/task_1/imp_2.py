import json


class Record:

    def __init__(self, code, name) -> None:
        super().__init__()
        self.code = code
        self.name = name

    def as_dict(self):
        return {self.code: self.name}


class ConverterJSON:
    @staticmethod
    def convert_to_json(data):
        return json.dumps(data)

    @staticmethod
    def save_to_file(path, json_data):
        with open(path, 'w') as f:
            f.write(json_data)


class RecordStore:

    def __init__(self) -> None:
        super().__init__()
        self._records = []
        self._json_converter = ConverterJSON()

    def add_record(self, record):
        self._records.append(record)

    def del_record(self, record):
        self._records.remove(record)

    def to_json(self):
        return self._json_converter.convert_to_json([x.as_dict() for x in self._records])

    def save_to_file(self, path):
        self._json_converter.save_to_file(path, self.to_json())