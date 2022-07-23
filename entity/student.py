from pydantic import BaseModel


class Student(BaseModel):
    name: str
    email: str
    certificate_file_name: str = ""
