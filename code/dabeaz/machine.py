#!/usr/bin/env python
# encoding: utf-8
import struct

class Function:
    def __init__(self, nparams, returns, code):
        self.nparams = nparams
        self.returns = returns
        self.code = code

class ImportFuction:
    def __init__(self, nparams, returns, call):
        self.nparams = nparams
        self.returns = returns
        self.call = call

class Machine:
    def __init__(self, functions, memsize=65536):
        self.functions = functions
        self.items = []
        self.memory = bytearray(memsize)

    def load(self, addr):
        return struct.unpack('<d', self.memory[addr: addr + 8])[0]

    def store(self, addr, val):
        self.memory[addr: addr+8] = struct.pack('<d', val)

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def call(self, func, *args):
        locals = dict(enumerate(args))
        if isinstance(func, Function):
            try:
                self.execute(func.code, locals)
            except Return:
                pass
            if func.returns:
                return self.pop()
        else:
            return func.call(*args)
        
    def execute(self, instructions, locals):
        for op, *args in instructions:
            print(op, args, self.items)
            if op == 'const':
                self.push(args[0])
            elif op == 'add':
                right = self.pop()
                left = self.pop()
                self.push(left + right)
            elif op == 'mul':
                right = self.pop()
                left = self.pop()
                self.push(left * right)
            elif op == 'sub':
                right = self.pop()
                left = self.pop()
                self.push(left - right)

            elif op == 'le':
                right = self.pop()
                left = self.pop()
                self.push(left <= right)
            elif op == 'ge':
                right = self.pop()
                left = self.pop()
                self.push(left >= right)

            elif op == 'load':
                addr = self.pop()
                self.push(self.load(addr))
            elif op == 'store':
                val = self.pop()
                addr = self.pop()
                self.store(addr, val)
            elif op == 'local_get':
                self.push(locals[args[0]])
            elif op == 'local_set':
                locals[args[0]] = self.pop()
            elif op == 'call':
                func = self.functions[args[0]]
                fargs = reversed([self.pop() for _ in range(func.nparams)])
                result = self.call(func, *fargs)
                if func.returns:
                    self.push(result)
            # if (test) {consequence} else {alternative}
            elif op == 'br':
                raise Break(args[0])
            elif op == 'br_if':
                if self.pop():
                    raise Break(args[0])
            elif op == 'block':
                try:
                    self.execute(args[0], locals)
                except Break as b:
                    if b.level > 0:
                        b.level -= 1
                        raise
            elif op == 'loop':
                while True:
                    try:
                        self.execute(args[0], locals)
                        break
                    except Break as b:
                        if b.level > 0:
                            b.level -= 1
                            raise
            # while (test) {body}
            # ('block', [
            #   ('loop', [ # lable 0
            #       not test
            #       ('br_if', 1) # Goto 1
            #       body
            #       ('br', 0), # Goto 0
            #     ]
            #   )
            # ]) # label 1
            elif op == 'return':
                raise Return()
            else:
                raise RuntimeError(f'Bad op {op}')


class Break(Exception):
    def __init__(self, level):
        self.level = level

class Return(Exception):
    pass

def example():
    def py_display_player(x):
        import time
        print(' '*int(x) + '<0:>')
        time.sleep(0.02)
    display_player = ImportFuction(nparams=1, returns=None,call=py_display_player)
    # def update_position(x, v, dt):
    #   return x + v * dt
    update_position = Function(nparams=3, returns=True, code=[
        ('local_get', 0),
        ('local_get', 1),
        ('local_get', 2),
        ('mul',),
        ('add',),
    ])
    functions = [update_position, display_player]
    #
    # x = 2
    # v = 3
    # x = x + v * 0.1
    x_addr = 22
    v_addr = 42
    code = [
        ('const', x_addr),
        ('const', x_addr),
        ('load',),
        ('const', v_addr),
        ('load',),
        ('const', 0.1),
        ('call', 0),
        ('store',),
    ]
    
    m = Machine(functions)
    m.store(x_addr, 2.0)
    m.store(v_addr, 3.0)

    # while  x > 0 {
    #     x = update_position(x, v, 0.1)
    #     if x > 70 {
    #         v = -v
    #     }
    # }
    m.execute([
        ('block', [
            ('loop', [
                ('const', x_addr),
                ('load',),
                ('call', 1),
                ('const', x_addr),
                ('load',),
                ('const', 0.0),
                ('le',),
                ('br_if', 1),
                ('const', x_addr),
                ('const', x_addr),
                ('load',),
                ('const', v_addr),
                ('load',),
                ('const', 0.1),
                ('call', 0),
                ('store',),
                ('block', [
                    ('const', x_addr),
                    ('load',),
                    ('const', 70),
                    ('ge',),
                    ('block', [
                        ('br_if', 0),
                        ('br', 1),
                    ]),
                    ('const', v_addr),
                    ('const', 0.0),
                    ('const', v_addr),
                    ('load',),
                    ('sub',),
                    ('store',),
                ]),
                ('br', 0),
            ])
        ])
    ], None)

    # m = Machine(functions)
    # m.store(x_addr, 2.0)
    # m.store(v_addr, 3.0)
    # m.execute(code, None)
    print(f'Result: {m.load(x_addr)}')


if __name__ == '__main__':
    example()


