# encoding: utf-8

# File: ShuntingYard.py
# Author: zzl0 (zhuzhaolong0@gmail.com)
#
# Wiki: https://www.wikiwand.com/en/Shunting-yard_algorithm
#
# In computer science, the shunting-yard algorithm is a method for parsing mathematical expressions
# specified in infix notation. It can produce either a postfix notation string, also known as
# Reverse Polish notation (RPN), or an abstract syntax tree (AST). The algorithm was invented by
# Edsger Dijkstra and named the "shunting yard" algorithm because its operation resembles that of
# a railroad shunting yard.
#
# infix: 1 + 2
# postfix (RPN): 1 2 +
# prefix (PN): + 1 2
#
# As an example, we can trace the execution of the algorithm on the input 1 + 2 * 3 - 4. We begin
# in this sate:
#
# input: 1 + 2 * 3 - 4
# stack:
# output:
#
# Put 1 to the output queue, since it's a number:
#
# input: + 2 * 3 - 4
# stack:
# output: 1
#
# Next, we shift the + onto the operator stack:
#
# input: 2 * 3 - 4
# stack: +
# output: 1
#
# Next, we put 2 to the output queue:
#
# input: * 3 - 4
# stack: +
# output: 1 2
#
# Now, we come to the next operator, *. Since * has higher precedence than +, it will bind to the
# 2 and the upcoming 3, and so we don't want to do the addition of the 1 and 2 yet. Consequently,
# we shift the * onto the operator stack:
#
# input: 3 - 4
# stack: + *
# output: 1 2
#
# We then shift the next number to the output queue:
#
# input: - 4
# stack: + *
# output: 1 2 3
#
# The next operator we hit is -. This has lower precedence than the * operator atop the operator stack,
# and so we continuously pop operators off the stack until we find an operator with strictly
# lower precedence than this -. This means we pop bot the * and + off the operator stack, as shown here:
#
# input: - 4
# stack:
# output: 1 2 3 * +
#
# Now that the stack is empty, the - has higher priority than all other operators, and so we can shift it:
#
# input: 4
# stack: -
# output: 1 2 3 * +
#
# We then shift the number 4 to the output queue:
#
# input:
# stack: -
# output: 1 2 3 * + 4
#
# After reading the expression, pop the operators off the stack and add them to the output.
# In this case there is only one, "-".
#
# input:
# stack:
# output: 1 2 3 * + 4 -
#
# This output is a correct RPN expression for the original infix expression.
#
# More generally, the algorithm is as follows:
#
# While there are tokens to be read from the input sequence:
#     If the token is a number, then put it to the output queue.
#     IF the token is an operator, then:
#         While the topmost operator of the operator stack does not have lower precedence:
#             pop operator from the operator stack, onto the output queue.
#         Push the the operator onto the operator stack.
#     If the token is "(", then push it onto the operator stack.
#     If the token is ")", then:
#         Pop all operators off the operator stack and shift them onto the output queue until an "(" is found.
#         Pop the "(" from the operator stack.
#         /* if the stack runs out without finding a "(", then there are mismatched parenthese */
# Finally, pop all the remaining operators off the operator stack and shift them onto the output queue.

PRECEDENCE = {
    '*': 3,
    '/': 3,
    '+': 2,
    '-': 2,
    '(': 1,
}

OPERATORS = '*/+-'


def tokenize(infix):
    return infix.split()


def infix2postfix(infix):
    stack = []
    postfix = []

    for token in tokenize(infix):
        if token[0] in OPERATORS:
            while stack and PRECEDENCE[stack[-1]] >= PRECEDENCE[token]:
                postfix.append(stack.pop())
            stack.append(token)
        elif token[0] == '(':
            stack.append(token)
        elif token[0] == ')':
            while stack and stack[-1] != '(':
                postfix.append(stack.pop())
            if stack:
                stack.pop()
            else:
                raise Exception('mismatched parenthese!')
        else:  # number
            postfix.append(token)

    while stack:
        postfix.append(stack.pop())

    return ' '.join(postfix)


def test():
    test_cases = [
        ('1 + 2 * 3 - 4', '1 2 3 * + 4 -'),
        ('3 + 4 * 1 + ( 2 - 3 )', '3 4 1 * + 2 3 - +'),
    ]

    for infix, postfix in test_cases:
        actual = infix2postfix(infix)
        assert actual == postfix, 'expected: %s, actual: %s' % (postfix, actual)

    print('Test passes!')


if __name__ == '__main__':
    test()

