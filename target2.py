def the_function(a: int, b: bool) -> None:
    if (a > 0 and b):
        print('Howdy')

    if (a == 10 and b):
        print("Meowdy")


the_function(5, True)
the_function(10, True)
the_function(-10, False)
the_function(5, False)
the_function(10, False)