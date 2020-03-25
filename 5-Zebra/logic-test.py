from logic2 import AND, OR, ATOM, NOT

x = AND([ATOM("A"), OR([ATOM("B"), NOT(ATOM("C"))])])


def f(x): return x + x


print(x)
print(x.map(f))
