# Predicates and Clauses
Predicates are the contents of `if(...)` and `while(...)` statements. Example: For `if (a > 3 and b)`, `a > 3 and b` is the predicate.

Clauses are indivisible units which evaluate to `True` or `False`. For the above example `a > 3` and `b` would be clauses.

# AST Compiling
Try `python3 cruft/ast_testing.py` to see what the AST looks like for some expressions.

# Short Circuit Behavior
Consider this snippet.
```py
a = False
b = True
if(a and b):
    pass
```

b will never be evaulated because a is False, which means the whole and expression is gauranteed to be False. Similiar behavior exists for 'or'. If a clause is never executed, we will denote that with `-` in the report.