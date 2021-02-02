import re
import readline
import operator
import math

OP = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
}
NUMBER = re.compile(r'^([+-]?(\d*\.\d+|\d+))')


class CalcException(Exception):
    pass


def calc(s):
    """An Infix Calculator.

    expr -> term
            | expr [+-] term
    term -> factor
            | term [*/] factor
    factor -> NUMBER
            | "(" expr ")"
    """
    def expr():
        # term | term [+-] term
        e = term()
        c = peek()
        while c in ('+', '-'):
            advance()
            e = OP[c](e, term())
            c = peek()
        return e

    def term():
        # factor | factor [*/] factor
        e = factor()
        c = peek()
        while c in ('*', '/'):
            advance()
            e = OP[c](e, factor())
            c = peek()
        return e

    def factor():
        # number | (expr)
        if peek() == '(':
            advance()
            e = expr()
            if advance() != ')':
                raise CalcException(f'error: missing ) at {i} in "{s}"')
            return e
        elif NUMBER.match(s[i:]):
            m = NUMBER.match(s[i:])
            num = float(m.group())
            advance(m.end())
            return num
        else:
            raise CalcException(f'error: expected number or ( at {i} in "{s}"')

    def peek():
        return s[i] if i < n else None

    def advance(step=1):
        nonlocal i
        i += step
        return s[i - step]

    s = s.replace(' ', '')  # remove spaces
    i, n = 0, len(s)
    rs = expr()
    if i != n:
        raise CalcException(f'error: unexpected char "{s[i]}" at {i} in "{s}"')
    return rs


def test():
    eq = math.isclose
    test_cases = [
        ('.5 + 2 *3', 6.5),
        ('(.5+2)*3', 7.5),
        ('(-.5 -2) /2', -1.25),
    ]

    for s, expected in test_cases:
        rs = calc(s)
        assert eq(rs, expected), f"expect '{expected}', but got '{rs}'"


def repl(prompt='calc> '):
    while True:
        try:
            rs = calc(input(prompt))
            print(rs)
        except CalcException as e:
            print(e)


if __name__ == '__main__':
    test()
    repl()
