import re

url_pattern = re.compile(r"^(http|https):\/\/")  # http:// or https://
phone_pattern = re.compile(r'^09\d{9}$')

def is_valid_url(url):
    return bool(url_pattern.match(url))


def is_valid_phone_number(phone_number):
    return bool(phone_pattern.match(phone_number))