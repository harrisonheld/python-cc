import ast

#
# This class will walk the Abstract Syntax Tree
# It will find predicates and modify them so that they call a record() 
# function that will record the values taken on by the predicates
#
class ClauseInstrumentor(ast.NodeTransformer):
    def __init__(self):
        self.clause_count = 0
        self.clause_ids = []
        self.clause_text_by_id = {}


    #
    # When ClauseInstrumentor.visit() is called, these specific methods will get called when the type of node is visited
    # Example: visit_If is called when a If node is visited
    # All of these are documented here: https://docs.python.org/3/library/ast.html
    #
    def visit_If(self, node: ast.If):
        node.test = self.visit_predicate(node.test)
        self.generic_visit(node)
        return node

    def visit_While(self, node: ast.While):
        node.test = self.visit_predicate(node.test)
        self.generic_visit(node)
        return node
    

    # visit_predicate will visit the thing that is inside if(...) and while(...) statements
    # it takes in the expression (...), and returns an expression with instrumentation added
    def visit_predicate(self, expression: ast.expr) -> ast.expr:
        self.clause_count += 1
        clause_id = "clause" + str(self.clause_count)
        self.clause_ids.append(clause_id)
        # ast.unparse returns source code
        self.clause_text_by_id[clause_id] = ast.unparse(expression)

        return ast.Call(
            func=ast.Name(id="record", ctx=ast.Load()),
            args=[ast.Constant(value=clause_id), expression],
            keywords=[]
        )