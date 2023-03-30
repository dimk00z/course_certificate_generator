from pydantic import BaseModel


class Student(BaseModel):
    name: str
    email: str
    certificate_files_names: list[str | None] = []
