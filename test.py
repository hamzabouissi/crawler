def b():
    global x
    print(x)


def a():
    x = 15
    b()

a()