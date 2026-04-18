import re

def tokenize(code):
    return re.findall(r'[A-Za-z_]\w+', code.lower())