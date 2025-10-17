import re

def is_email(value):
    return re.match(r"^[^@]+@[^@]+\.[^@]+$", value) is not None

def is_phone(value):
    return re.match(r"^\+?\d{7,15}$", value) is not None