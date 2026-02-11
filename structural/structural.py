import ast

class NormalizeAST(ast.NodeTransformer):
    def visit_Constant(self, node):
        return ast.copy_location(ast.Constant(value="CONST"), node)

def read_code(path):
    with open(path, 'r') as f:
        return f.read()

def get_normalized_ast(code):
    tree = ast.parse(code)
    tree = NormalizeAST().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.dump(tree, include_attributes=False)

code1 = read_code("../data/code1.py")
code2 = read_code("../data/code2.py")

ast1 = get_normalized_ast(code1)
ast2 = get_normalized_ast(code2)

print("Normalized AST file1:", ast1)
print("Normalized AST file2:", ast2)
print("Structural Match:", ast1 == ast2)
