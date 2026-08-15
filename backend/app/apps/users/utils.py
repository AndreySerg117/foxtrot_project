import secrets


def generate_verification_code():
    num = secrets.randbelow(1000000)
    code = str(num)
    while len(code) < 6:
        code = "0" + code
    return code


