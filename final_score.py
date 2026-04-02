import ast

# ---------- READ FILE ----------
def read_code(path):
    with open(path, 'r') as f:
        return f.read()

# ---------- SEMANTIC ANALYSIS ----------
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

# ---------- EXTRACT FEATURES ----------
def extract_features(code):
    tree = ast.parse(code)
    ex = SemanticExtractor()
    ex.visit(tree)
    return set(ex.features)

# ---------- LOAD FILES ----------
code1 = read_code("data/code1.py")
code2 = read_code("data/code2.py")

# ---------- COMPUTE SEMANTIC SCORE ----------
f1 = extract_features(code1)
f2 = extract_features(code2)

semantic_score = len(f1 & f2) / len(f1 | f2) if (f1 | f2) else 1.0

# ---------- TEMP (still static for now) ----------
lexical_score = 0.6
structural_score = 1.0

lexical_reason = "Most keywords and identifiers are similar."
structural_reason = "Both programs share similar structure."
semantic_reason = "Similarity based on control flow and operations."

# ---------- FINAL SCORE ----------
final_score = (
    0.3 * lexical_score +
    0.4 * structural_score +
    0.3 * semantic_score
)

# ---------- OUTPUT ----------
print("Lexical Score:", lexical_score)
print("Lexical Reason:", lexical_reason)

print("Structural Score:", structural_score)
print("Structural Reason:", structural_reason)

print("Semantic Score:", semantic_score)
print("Semantic Reason:", semantic_reason)

print("Final Plagiarism Score:", round(final_score, 2))