import re

def read_code(path):
    with open(path, 'r') as f:
        return f.read()

def tokenize(code):
    return re.findall(r'\w+', code.lower())

code1 = read_code("../data/code1.py")
code2 = read_code("../data/code2.py")

tokens1 = set(tokenize(code1))
tokens2 = set(tokenize(code2))

similarity = len(tokens1 & tokens2) / len(tokens1 | tokens2)

print("Tokens file1:", tokens1)
print("Tokens file2:", tokens2)
print("Similarity:", similarity)
