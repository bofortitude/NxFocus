import random


def genMalString(loadLength=None, maxLength=1024):
    if loadLength is not None:
        stringLength = int(loadLength)
    else:
        if maxLength <= 1:
            maxLength = 1024
        stringLength = random.randint(1, maxLength)
    rString = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789~!@#$%^&*()_+-=;:",.<>/?'
    length = len(chars) - 1
    for i in range(stringLength):
        rString += chars[random.randint(0, length)]
    return rString
