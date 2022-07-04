import json


class IAllRecords:
    def all_records(self):
        raise NotImplemented


class Record:

    def __init__(self, code, name) -> None:
        super().__init__()
        self.code = code
        self.name = name

    def as_dict(self):
        return {self.code: self.name}


class StoreExporter(IAllRecords):
    def to_json(self):
        result = json.dumps([x.as_dict() for x in self.all_records()])

        return result

    def save_to_file(self, path):
        with open(path, 'w') as f:
            f.write(self.to_json())


class RecordStore(StoreExporter, IAllRecords):

    def __init__(self) -> None:
        super().__init__()
        self._records = []

    def add_record(self, record):
        self._records.append(record)

    def del_record(self, record):
        self._records.remove(record)

    def all_records(self):
        return self._records