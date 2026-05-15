import base64


def encode_password(password):
    return base64.b64encode(password.encode()).decode()


def decode_password(encoded):
    return base64.b64decode(encoded.encode()).decode()



