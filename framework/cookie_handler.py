from hashlib import sha256

SECRET = "MqpBbx7sK50UCAfYh9IkbCMjhxcTRvB6uQdYA6VfIZlgHLB/Rk47T9COuUWmJj0f7ZoQ3Zv2cvqVDluxtYqhw"

def sign_cookie(value):
    string_value = str(value)
    signature = sha256(SECRET + string_value).hexdigest()
    return signature + "|" + string_value

def check_cookie(value):
    signature = value[:value.find('|')]
    declared_value = value[value.find('|') + 1:]

    if sha256(SECRET + declared_value).hexdigest() == signature:
        return declared_value
    else:
        return None



