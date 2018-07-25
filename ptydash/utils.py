import base64


def bytes_to_base64(bytes):
    return base64.b64encode(bytes).decode('utf-8')
