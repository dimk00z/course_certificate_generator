# 


# Course certificate generator

I had a task from my wife to develop a simple solution to create certificates for her course.

So course certificate generator is a Python script for creating PDF personal certificate from PNG template.

I used [this PIL manual](https://www.geeksforgeeks.org/create-certificates-using-python-pil/) 
## Installation

Script was tested with Python 3.7

```bash
pip install -r requirements.txt
```

## Usage

`.env` should have this parameters
```
EMAIL_SENDER=woo
EMAIL_PASSWORD=email_pass
EMAIL_DISPLAY_NAME=send_name
SMTP_SERVER=smtp.yandex.ru
SMTP_PORT=465
```

For correct working folder `template` contains two files `template.png` and `email_template.txt`(don't forget to add `{}` for adding name in email)

## License
[MIT](https://choosealicense.com/licenses/mit/)