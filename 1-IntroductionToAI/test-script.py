
import sys

print(sys.version)
print(sys.executable)


def greet(who_to_greed):
    greeting = 'Hello, {}'.format(who_to_greed)
    if (greeting == 'Hello, mate'):
        return greeting
    else:
        return 'Kek'


print(greet('World'))
