from functools import lru_cache

from pydantic import BaseSettings, Field


class AppSettings(BaseSettings):
    email_sender: str = Field("email_sender", env="EMAIL_SENDER")
    email_password: str = Field("EMAIL_PASSWORD", env="EMAIL_PASSWORD")
    smtp_port: int = Field(465, env="SMTP_PORT")
    smtp_server: str = Field("smtp.yandex.ru", env="SMTP_SERVER")
    email_display_name: str = Field("send_name", env="EMAIL_DISPLAY_NAME")

    students_file: str = Field("names_list.txt", env="STUDENTS_FILE")

    font_file: str = Field("font.ttf", env="FONT_FILE")
    font_size: int = Field(150, env="FONT_SIZE")

    template_path: str = Field("template/template.png", env="TEMPLATE_PATH")
    email_template_path: str = Field(
        "template/email_template.txt", env="EMAIL_TEMPLATE_PATH"
    )

    text_y_position: int = Field(430, env="TEXT_Y_POSITION")
    text_color: str = Field("#c1183e", env="TEXT_COLOR")

    email_subject: str = Field("Ваш сертификат курса", env="EMAIL_SUBJECT")

    timeout: int = Field(60, env="TIMEOUT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
