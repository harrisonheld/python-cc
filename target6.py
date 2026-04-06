# target6.py
def the_function(a: bool, b: bool, c: bool) -> None:
    if (a and b) or c:
        print("yes")

the_function(True, True, False)   # (T∧T)∨F = True
the_function(True, False, False)  # (T∧F)∨F = False
the_function(False, False, True)  # (F∧F)∨T = True
the_function(False, False, False) # (F∧F)∨F = False