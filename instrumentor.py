import ast

class ClauseInstrumentor(ast.NodeTransformer):
    def __init__(self):
        self.counter = 0
        self.clause_ids = []
        self.clause_text_by_id = {}

    def new_id(self):
        self.counter += 1
        return f"clause_{self.counter}"

    def wrap_clause(self, node):
        """Wrap a node so that record(...) is called but original value returned"""
        clause_id = self.new_id()
        self.clause_ids.append(clause_id)
        try:
            clause_text = ast.unparse(node)
        except Exception:
            clause_text = "<unknown>"
        self.clause_text_by_id[clause_id] = clause_text
        return ast.Call(
            func=ast.Lambda(
                args=ast.arguments(posonlyargs=[], args=[ast.arg(arg="v")], kwonlyargs=[], kw_defaults=[], defaults=[]),
                body=ast.Call(
                    func=ast.Name(id="record", ctx=ast.Load()),
                    args=[ast.Constant(value=clause_id), ast.Name(id="v", ctx=ast.Load())],
                    keywords=[]
                )
            ),
            args=[node],
            keywords=[]
        )

    #
    # When ClauseInstrumentor.visit() is called, these specific methods will get called when the type of node is visited
    # Example: visit_Compare is called when a Compare node is visited
    # All of these are documented here: https://docs.python.org/3/library/ast.html
    # In each method I paraphrased some notes from the above link
    #
    def visit_Compare(self, node):
        # Example "a > 3"
        self.generic_visit(node)
        return self.wrap_clause(node)

    def visit_BoolOp(self, node):
        # A bool op is 'or' or 'and'.
        # values are the expressions involved. so for "a or b", "a" and "b" would be the values.
        # There may be more than 2, such as "a and b and c".
        self.generic_visit(node)
        node.values = [self.wrap_clause(value) for value in node.values]
        return node

    def visit_UnaryOp(self, node):
        # A UnaryOp is something that takes one argument, such as "not x".
        # "not" would be the op
        # "x" would be the operand
        self.generic_visit(node)
        if isinstance(node.op, ast.Not):
            return self.wrap_clause(node)
        return node