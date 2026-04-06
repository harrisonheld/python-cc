# Predicates and Clauses
Predicates are the contents of if(...) and while(...) statements.
For `if (a > 3 and b)`, `a > 3 and b` is the predicate.

Clauses are the most indivisible units which evaluate to True or False. For the above example `a > 3` and `b` would be clauses.

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

b will never be evaulated because a is False, which means the whole and expression is gauranteed to be False anyway. So Python never bothers to execute b. Similiar behavior exists for 'or'. In these cases, b will never be observed to be True.