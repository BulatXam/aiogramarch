"""Код должен быть по PEP8 чтобы все работало!"""

from typing import List


class Code:
    def __init__(self, file):
        self._file = file
        self.code_strings = file.read().split("\n")

    def _search(self, text) -> List:
        return [(num, string) for num, string in enumerate(self.code_strings) if text in string]
    
    def add_import_from(self, from_, import_) -> None:
        import_code = f"from {from_} import {import_}"
        self.code_strings.insert(0, import_code)

    def add_import_from_as(self, from_, import_, as_) -> None:
        import_code = f"from {from_} import {import_} as {as_}"
        self.code_strings.insert(0, import_code)

    def add_import(self, import_) -> None:
        import_code = f"import {import_}"
        self.code_strings.insert(0, import_code)
    
    def add_import_as(self, import_, as_) -> None:
        import_code = f"import {import_} as {as_}"
        self.code_strings.insert(0, import_code)

    def append_in_lists(self, var: str, value: str):
        strings = self._search(var + " = ")

        for num, string in strings:
            var_values = string[string.find("[")+1:string.find("]")]
            self.code_strings[num] = f"{var} = [{var_values}, {value}]"

        return self.code_strings
    
    def save(self):
        self._file.seek(0)
        self._file.write("\n".join(self.code_strings))
