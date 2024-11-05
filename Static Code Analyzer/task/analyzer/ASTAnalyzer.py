import ast
import re
class CodeAnalyzer(ast.NodeVisitor):
    def __init__(self,path):
        self.errors = []
        self.path = path
    def check_snake_case(self, name):
        return bool(re.match(r'^[a-z]+(_[a-z]+)*$', name))

    def visit_FunctionDef(self, node):
        for arg in node.args.defaults:
            if isinstance(arg, (ast.List, ast.Dict, ast.Set)):
                print(f"{self.path}: Line {node.lineno}: S012 The default argument value is mutable.")

        for arg in node.args.args:
            if not self.check_snake_case(arg.arg):
                print(f"{self.path}: Line {node.lineno}: S010 Argument name '{arg.arg}' should be written in snake_case")
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and not self.check_snake_case(target.id):
                print(f"{self.path}: Line {node.lineno}: S011 Variable '{target.id}' should be written in snake_case")
        self.generic_visit(node)

    def report(self):
        for error in self.errors:
            lineno, message = error
            print(f"Line {lineno}: {message}")

def analyze_file(filename):
    with open(filename, "r") as file:
        tree = ast.parse(file.read(), filename=filename)

    analyzer = CodeAnalyzer(filename)
    analyzer.visit(tree)
    analyzer.report()


