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
        
        # BoolOp: Recurse
        # Examples:  
        #   a and b
        #   a or b
        if isinstance(expression, ast.BoolOp):
            expression.values = [self.visit_predicate(v) for v in expression.values]
            return expression
        
        # UnaryOp: recurse
        # Examples:
        #  not x
        #  not (a or b)
        elif isinstance(expression, ast.UnaryOp) and isinstance(expression.op, ast.Not):
            expression.operand = self.visit_predicate(expression.operand)
            return expression

        # LEAF clause. Instrument it
        # Examples:
        #   True
        #   a > 3
        #   a
        elif isinstance(expression, (ast.Name, ast.Constant, ast.Compare)):
            self.clause_count += 1
            clause_id = "clause" + str(self.clause_count)
            self.clause_ids.append(clause_id)
            self.clause_text_by_id[clause_id] = ast.unparse(expression)
            return ast.Call(
                func=ast.Name(id="record", ctx=ast.Load()),
                args=[ast.Constant(value=clause_id), expression],
                keywords=[]
        )

        # Fallback: anything else, leave unchanged
        else:
            print('WARNING: not sure what to do with this kind of node')
            print(f"Type: {type(expression)}")
            print(f"Expression: {ast.unparse(expression)}")
            print()
            return expression