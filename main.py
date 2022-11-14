import logging
from pathlib import Path
from time import sleep

from PIL import Image, ImageDraw, ImageFont

from entity.student import Student
from utils.email import send_email
from utils.loader import Loader
from utils.settings import AppSettings, get_settings


def load_names(file_name: str):
    names = {}
    with open(Path(".") / file_name) as file:
        for string in file.readlines():
            string_words = string.replace("\t", " ").split()
            names[string_words[-1]] = " ".join(string_words[1::-1])
    return names


def create_certificate(
    name,
    email,
    font_path,
    template_path,
    text_y_position=500,
    font_size=150,
    text_color="#41634a",
    output_directory="certificates",
):

    output_path = str(Path(".") / f"{output_directory}/{name} - {email}.pdf")
    try:
        with Image.open(template_path, mode="r") as img_template:
            image_width = img_template.width
            draw = ImageDraw.Draw(img_template)
            font = ImageFont.truetype(font_path, font_size)
            text_width, _ = draw.textsize(name, font=font)
            draw.text(
                ((image_width - text_width) / 2, text_y_position),
                name,
                font=font,
                fill=text_color,
            )
            with Image.new("RGB", img_template.size, (0, 0, 0)) as rgb_image:
                rgb_image.paste(img_template, mask=img_template.split()[3])
                rgb_image.save(output_path, "PDF")
        return output_path
    except Exception as ex:
        logging.exception(ex)
        logging.error(f"Could not create certificate for {name}")


def send_certificate(script_params: AppSettings, email, name, certificate_file_name, email_template):
    contents = [email_template.format(name)]
    attachments = [certificate_file_name]

    return send_email(
        to_email=email,
        subject=script_params.email_subject,
        contents=contents,
        attachments=attachments,
        smtp_server=script_params.smtp_server,
        smtp_port=script_params.smtp_port,
        email_sender=script_params.email_sender,
        email_display_name=script_params.email_display_name,
        email_password=script_params.email_password,
    )


def main():

    logging.basicConfig(level=logging.INFO)

    script_params: AppSettings = get_settings()
    logging.info(script_params)

    studets: list[Student] = Loader(script_params.students_file).load_students()
    logging.info("Loaded %d students", len(studets))

    font_path: str = str(Path(".") / script_params.font_file)

    template_path: str = str(Path(".") / script_params.template_path)

    email_template_path: Path = Path(".") / script_params.email_template_path

    try:
        with open(str(email_template_path)) as email_tamplate_file:
            email_template = email_tamplate_file.read()
    except FileNotFoundError as ex:
        logging.info(ex)
        return

    for student_index, student in enumerate(studets):
        studets[student_index].certificate_file_name = create_certificate(
            student.name,
            student.email,
            font_path,
            template_path,
            text_y_position=script_params.text_y_position,
            text_color=script_params.text_color,
            font_size=script_params.font_size,
        )

    print()
    print(script_params.email_subject)
    print(email_template)
    print()

    if input("Have you check email's subject and template? y/n: ").lower() != "y":
        logging.info("Shut down")
        return

    for (index, student) in enumerate(studets):
        sended_email = send_certificate(
            script_params, student.email, student.name, student.certificate_file_name, email_template
        )
        if sended_email:
            logging.info(f"Sended to {student.email}")
        if index + 1 == len(studets):
            break
        sleep(script_params.timeout)


if __name__ == "__main__":
    main()
