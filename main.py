from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


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
                       output_directory='certificates'):
    out_put_path = str(Path('.') / f'{output_directory}/{name} - {email}.pdf')
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
            font=font, fill=(0, 0, 0, 0))
        with Image.new('RGB', img_template.size, (0, 0, 0)) as rgb_image:
            rgb_image.paste(img_template, mask=img_template.split()[3])
            rgb_image.save(out_put_path, 'PDF')


def main():
    names = load_names('names_list.txt')
    font_path = str(Path('.') / 'font.ttf')
    template_path = str(Path('.') / 'template/template.png')
    for email, name in names.items():
        create_certificate(name, email, font_path,
                           template_path, text_y_position=700)


if __name__ == '__main__':
    main()
