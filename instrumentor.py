import ast

#
# This class will walk the Abstract Syntax Tree
# It will find predicates and modify them so that they call a record() 
# function that will record the values taken on by the predicates
#
class ClauseInstrumentor(ast.NodeTransformer):
    def __init__(self):
        self.clause_count = 0
        self.predicate_count = 0
        self.clause_ids = []
        self.clause_text_by_id = {}
        self.predicate_text_by_id = {}
        self.predicate_clause_ids = {}

    #
    # We will assign string IDs to EACH predicate and to each clause
    #
    def new_clause_id(self, expression: ast.expr) -> str:
        self.clause_count += 1
        clause_id = "clause" + str(self.clause_count)
        self.clause_ids.append(clause_id)
        self.clause_text_by_id[clause_id] = ast.unparse(expression)
        return clause_id

    def new_predicate_id(self, expression: ast.expr) -> str:
        self.predicate_count += 1
        predicate_id = "predicate" + str(self.predicate_count)
        self.predicate_text_by_id[predicate_id] = ast.unparse(expression)
        self.predicate_clause_ids[predicate_id] = []
        return predicate_id


    #
    # When ClauseInstrumentor.visit() is called, these specific methods will get called when the type of node is visited
    # Example: visit_If is called when a If node is visited
    # All of these are documented here: https://docs.python.org/3/library/ast.html
    #
    def visit_If(self, node: ast.If):
        predicate_id = self.new_predicate_id(node.test)
        node.test = self.wrap_predicate(predicate_id, node.test)
        self.generic_visit(node)
        return node

    def visit_While(self, node: ast.While):
        predicate_id = self.new_predicate_id(node.test)
        node.test = self.wrap_predicate(predicate_id, node.test)
        self.generic_visit(node)
        return node
    

    # visit_predicate will visit the thing that is inside if(...) and while(...) statements
    # it takes in the expression (...), and returns an expression with instrumentation added
    def visit_predicate(self, predicate_id: str, expression: ast.expr) -> ast.expr:
        
        # BoolOp: Recurse
        # Examples:  
        #   a and b
        #   a or b
        if isinstance(expression, ast.BoolOp):
            expression.values = [self.visit_predicate(predicate_id, v) for v in expression.values]
            return expression
        
        # UnaryOp: recurse
        # Examples:
        #  not x
        #  not (a or b)
        elif isinstance(expression, ast.UnaryOp) and isinstance(expression.op, ast.Not):
            expression.operand = self.visit_predicate(predicate_id, expression.operand)
            return expression

        # LEAF clause. Instrument it
        # Examples:
        #   True
        #   a > 3
        #   a
        elif isinstance(expression, ast.expr):
            clause_id = self.new_clause_id(expression)
            self.predicate_clause_ids[predicate_id].append(clause_id)
            return ast.Call(
                func=ast.Name(id="record_clause", ctx=ast.Load()),
                args=[ast.Constant(value=predicate_id), ast.Constant(value=clause_id), expression],
                keywords=[]
        )

        # Fallback: anything else, leave unchanged
        else:
            print('WARNING: not sure what to do with this kind of node')
            print(f"Type: {type(expression)}")
            print(f"Expression: {ast.unparse(expression)}")
            print()
            return expression

    def wrap_predicate(self, predicate_id: str, expression: ast.expr) -> ast.expr:
        instrumented_expression = self.visit_predicate(predicate_id, expression)
        return ast.Call(
            func=ast.Name(id="record_predicate", ctx=ast.Load()),
            args=[
                ast.Constant(value=predicate_id),
                ast.Lambda(
                    args=ast.arguments(
                        posonlyargs=[],
                        args=[],
                        kwonlyargs=[],
                        kw_defaults=[],
                        defaults=[]
                    ),
                    body=instrumented_expression
                )
            ],
            keywords=[]
        )