import re

def normalize_code(code):
    # remove comments
    code = re.sub(r'//.*|/\*[\s\S]*?\*/|#.*', '', code)

    # remove extra whitespace
    code = re.sub(r'\s+', ' ', code)

    return code.strip()