from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from utils.env import load_params
from utils.email import send_email
from time import sleep
import logging

TIMEOUT = 5


def load_names(file_name: str):
    names = {}
    with open(Path('.') / file_name) as file:
        for string in file.readlines():
            string_words = string.replace('\t', ' ').split()
            names[string_words[-1]] = ' '.join(string_words[1::-1])
    return names


def create_certificate(name, email, font_path,
                       template_path,
                       text_y_position=500,
                       font_size=150,
                       text_color='#41634a',
                       output_directory='certificates'):

    output_path = str(Path('.') / f'{output_directory}/{name} - {email}.pdf')
    try:
        with Image.open(template_path, mode='r') as img_template:
            image_width = img_template.width
            draw = ImageDraw.Draw(img_template)
            font = ImageFont.truetype(
                font_path,
                font_size
            )
            text_width, _ = draw.textsize(name, font=font)
            draw.text(
                (
                    (image_width - text_width) / 2,
                    text_y_position
                ),
                name,
                font=font, fill=text_color)
            with Image.new('RGB', img_template.size, (0, 0, 0)) as rgb_image:
                rgb_image.paste(img_template, mask=img_template.split()[3])
                rgb_image.save(output_path, 'PDF')
        return output_path
    except Exception as ex:
        print(ex)
        print(f'Could not create certificate for {name}')


def send_certificate(script_params, email, name,
                     certificate_file_name, email_template):
    contents = [
        email_template.format(name)
    ]
    attachments = [certificate_file_name]
    subject = 'Ваш сертификат курса по IELTS'
    return send_email(to_email=email, subject=subject,
                      contents=contents, attachments=attachments,
                      smtp_server=script_params['smtp_server'],
                      smtp_port=script_params['smtp_port'],
                      email_sender=script_params['email_sender'],
                      email_display_name=script_params['email_display_name'],
                      email_password=script_params['email_password'])


def main():
    logging.basicConfig(level=logging.INFO)
    graduates = load_names('names_list.txt')
    font_path = str(Path('.') / 'font.ttf')
    template_path = str(Path('.') / 'template/template.png')
    email_template_path = Path('.') / 'template/email_template.txt'
    with open(str(email_template_path)) as email_tamplate_file:
        email_template = email_tamplate_file.read()

    script_params = load_params(
        required_params=[
            "EMAIL_SENDER",
            "EMAIL_PASSWORD",
            "EMAIL_DISPLAY_NAME",
            "SMTP_SERVER",
            "SMTP_PORT",
        ])
    for email, name in graduates.items():
        certificate_file_name = create_certificate(name, email, font_path,
                                                   template_path,
                                                   text_y_position=700,
                                                   text_color='#fa3e51')
        graduates[email] = {'name': name,
                            'certificate_file_name': certificate_file_name}
        sended_email = send_certificate(script_params, email, name,
                                        certificate_file_name, email_template)
        if sended_email:
            logging.info(f'Sended to {email}')
        sleep(TIMEOUT)


if __name__ == '__main__':
    main()
