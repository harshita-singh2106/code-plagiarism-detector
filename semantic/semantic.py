import ast

def read_code(path):
    with open(path, 'r') as f:
        return f.read()

class SemanticExtractor(ast.NodeVisitor):
    def __init__(self):
        self.features = []

    def visit_For(self, node):
        self.features.append("LOOP")
        self.generic_visit(node)

    def visit_While(self, node):
        self.features.append("LOOP")
        self.generic_visit(node)

    def visit_If(self, node):
        self.features.append("IF")
        self.generic_visit(node)

    def visit_BinOp(self, node):
        self.features.append(type(node.op).__name__)
        self.generic_visit(node)

    def visit_Compare(self, node):
        self.features.append("COMPARE")
        self.generic_visit(node)

def extract_features(code):
    tree = ast.parse(code)
    ex = SemanticExtractor()
    ex.visit(tree)
    return set(ex.features)

code1 = read_code("../data/code1.py")
code2 = read_code("../data/code2.py")

f1 = extract_features(code1)
f2 = extract_features(code2)

similarity = len(f1 & f2) / len(f1 | f2) if (f1 | f2) else 1.0

print("Semantic features file1:", f1)
print("Semantic features file2:", f2)
print("Semantic Similarity:", similarity)
