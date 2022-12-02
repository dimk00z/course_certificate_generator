import csv
import logging
from pathlib import Path

from entity.student import Student


class Loader:
    def __init__(self, file_name: str):
        self.file_name: str = file_name

    def _load_from_txt(self) -> list[Student]:
        # TODO check it!
        students: list[Student] = []
        try:
            with open(Path(".") / self.file_name) as file:
                for string in file.readlines():
                    string_words = string.replace("\t", " ").split()
                    students.append(
                        Student(
                            email=string_words[-1], name=" ".join(string_words[1::-1])
                        )
                    )
        except FileNotFoundError as ex:
            logging.info(ex)

        return students

    def _load_from_csv(self) -> list[Student]:
        students: list[Student] = []
        try:
            with open(Path(".") / self.file_name, encoding="utf8") as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=",")
                for line_index, row in enumerate(csv_reader):
                    if line_index == 0:
                        continue
                    students.append(Student(email=row[-1], name=row[-2]))
        except FileNotFoundError as ex:
            logging.info(ex)
        return students

    def load_students(self) -> list[Student]:
        file_extension: str = str(Path(self.file_name).suffix)
        match file_extension:
            case ".txt":
                return self._load_from_txt()
            case ".csv":
                return self._load_from_csv()
        return []
