import datetime

import Parser

def log(message, color=-1, nl=True):
    print_func = print
    if not nl:
        print_func = lambda x: print(x, end="")
    outFormat = "[%s] %s"
    date = datetime.datetime.utcnow().strftime("%H:%M:%S.%f")[:-3]
    if color == -1:
        print_func("\033[0m" + outFormat % (date, message))
    else:
        print_func("\033[38;5;%dm" % color + outFormat % (date, message) + "\033[0m")

def assertEq(method, args, expected):
    log("Testing " + method + "(" + repr(args) + ")... ", 36, False)
    method = eval(method)
    res = method(*args)
    if res == expected:
        print("\033[38;5;40mCorrect")
    else:
        print("\033[38;5;1mCorrect")
        log("Wrong. Expected " + repr(expected))

assertEq("Parser.tokenize", ["hej"], [])
