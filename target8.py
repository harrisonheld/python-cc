# nested if predicates
def the_function(a: bool, b: bool) -> None:
    if a:
        if b:
            pass

the_function(True, True)
the_function(True, False)
the_function(False, False)