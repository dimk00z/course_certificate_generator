import logging
from pathlib import Path
from time import sleep

from jinja2 import Template
from PIL import Image, ImageDraw, ImageFont

from entity.student import Student
from utils.loader import Loader
from utils.sender import EmailSender
from utils.settings import AppSettings, get_settings


def load_names(file_name: str) -> dict[str, str]:
    names: dict[str, str] = {}
    with open(Path(".") / file_name) as file:
        for string in file.readlines():
            string_words = string.replace("\t", " ").split()
            names[string_words[-1]] = " ".join(string_words[1::-1])
    return names


def create_certificate(
    *,
    name: str,
    email: str,
    font_path: str,
    template_path: str,
    index: int,
    text_y_position: int = 500,
    font_size: int = 150,
    text_color: str | None = "#41634a",
    output_directory: str = "certificates",
):
    index_text: str = f"_{index}" if index > 1 else ""
    output_path = str(
        Path(".") / f"{output_directory}/{name} - {email}{index_text}.pdf"
    )
    try:
        with Image.open(template_path, mode="r") as img_template:
            image_width = img_template.width
            draw = ImageDraw.Draw(img_template)
            font = ImageFont.truetype(font_path, font_size)
            text_width = draw.textlength(name, font=font)
            # Reverted colors for text
            rgb_im = img_template.convert("RGB")
            r, g, b = rgb_im.getpixel(
                (int((image_width - text_width) / 2), text_y_position)
            )
            r = 255 - r
            g = 255 - g
            b = 255 - b
            draw.text(
                ((image_width - text_width) / 2, text_y_position),
                name,
                font=font,
                fill=text_color or (r, g, b),
            )
            with Image.new("RGB", img_template.size, (0, 0, 0)) as rgb_image:
                rgb_image.paste(img_template, mask=img_template.split()[3])
                rgb_image.save(output_path, "PDF")
        return output_path
    except Exception as ex:
        logging.exception(ex)
        logging.error(f"Could not create certificate for {name}")


def main():
    logging.basicConfig(level=logging.INFO)

    script_params: AppSettings = get_settings()
    logging.info(script_params)

    students: list[Student] = Loader(script_params.students_file).load_students()
    logging.info("Loaded %d students", len(students))

    font_path: str = str(Path(".") / script_params.font_file)

    templates_paths: list[str] = [
        str(Path(".") / path) for path in script_params.templates_paths
    ]

    email_template_path: Path = Path(".") / script_params.email_template_path

    try:
        with open(str(email_template_path)) as email_template_file:
            email_template = email_template_file.read()
    except FileNotFoundError as ex:
        logging.info(ex)
        return

    for student_index, student in enumerate(students):
        students[student_index].certificate_files_names = [
            create_certificate(
                name=student.name,
                email=student.email,
                font_path=font_path,
                template_path=template_path,
                index=index + 1,
                text_y_position=script_params.text_y_position,
                text_color=script_params.text_color,
                font_size=script_params.font_size,
            )
            for index, template_path in enumerate(templates_paths)
        ]

    print()
    print(script_params.email_subject)
    print(email_template)
    print()

    question = "Have you check email's subject and template? y/n: "
    if input("%s" % question).lower() != "y":
        logging.info("Shut down")
        return
    email_sender: EmailSender = EmailSender(
        sender=script_params.email_sender,
        password=script_params.email_password,
        display_name=script_params.email_display_name,
        subject=script_params.email_subject,
    )
    for index, student in enumerate(students):
        contents = Template(
            email_template,
        ).render(name=student.name)

        # email_template.format(name=student.name)
        attachments = student.certificate_files_names
        email_sent: bool = email_sender(
            attachments=attachments, to_email=student.email, contents=contents
        )
        if email_sent:
            logging.info(f"Sent to {student.email}")
        if index + 1 == len(students):
            break
        sleep(script_params.timeout)


if __name__ == "__main__":
    main()
