# Predicates and Clauses
Predicates are the contents of `if(...)` and `while(...)` statements. Example: For `if (a > 3 and b)`, `a > 3 and b` is the predicate.

Clauses are indivisible units which evaluate to `True` or `False`. For the above example `a > 3` and `b` would be clauses.

# Coverage Types
The coverage types are:
- cc - if ALL combinations of clauses were seen
- cacc - for each clause, if there is an evaluation of it as True and one as False, such that the value of the predicate changes.
- racc - for each clause, if there is an evaluation of it as True and one as False, AND NO MINOR CLAUSES MAY DIFFER, such that the value of the predicate changes.

# AST Compiling
We will compile source code into an Abstract Syntax Tree, and then modify the If and While nodes to add tracking code to them. This will let us record each time the node is evaluated.

Try `python3 tools/ast_testing.py` to see what the AST looks like for some expressions.

# Short Circuit Behavior
Consider this snippet.
```py
a = False
b = True
if(a and b):
    pass
```

b will never be evaulated because a is False, which means the whole and expression is gauranteed to be False. Similiar behavior exists for 'or'. If a clause is never executed, we will denote that with `-` in the report.