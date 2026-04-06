# target4.py
def the_function(a: bool, b: bool) -> None:
    if (a or b):
        print("either")

the_function(True, False)   # short-circuits OR
the_function(False, True)   # both evaluated
the_function(False, False)  # both evaluated