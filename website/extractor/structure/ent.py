from pydantic_core.core_schema import none_schema

from document import Date

class Ent:
    def __init__(self, input_type, input_text, start, stop):
        if input_type not in ["DATE", "ORG"]:
            raise ValueError("Invalid type of object.")
        self.type = input_type
        self.text = input_text
        self.start = start
        self.stop = stop
        self.connection = None

class Object:
    def __init__(self, date, orgs: list):
        self.date = date
        self.org = orgs

    @property
    def text(self):
        result = f"{self.date.text}\n"

        for el in self.org:
            result += f"{el.text}\n"

        return result




