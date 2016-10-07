class Scope:

    def __init__(self, parent=None):
        self.content = {}
        self.parent = parent

    def __setitem__(self, key, value):
        self.content[key] = value


    def __getitem__(self, key):
        if key in self.content:
            return self.content[key]
        elif self.parent:
            return self.parent[key]
        else:
            raise KeyError


class Number:

    def __init__(self, value):
        self.value = int(value)

    def evaluate(self, scope):
        return self


class Function:

    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        cur = Number(0)
        for expr in self.body:
            cur = expr.evaluate(scope)
        return cur


class FunctionDefinition:

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        cur = Number(0)
        branch = self.if_true if self.condition.evaluate(scope).value else self.if_false
        for expr in branch:
            cur = expr.evaluate(scope)
        return cur


class Print:

    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        number = self.expr.evaluate(scope)
        print(number.value)
        return number


class Read:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        scope[self.name] = Number(int(input()))
        return scope[self.name]


class FunctionCall:

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        call_scope = Scope(scope)
        func = self.fun_expr.evaluate(scope)
        for name, arg in zip(func.args, self.args):
            call_scope[name] = arg.evaluate(scope)
        return func.evaluate(call_scope)


class Reference:

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    def __init__(self, lhs, op, rhs):
        self.op = op
        self.lhs = lhs
        self.rhs = rhs
        self.funcs = {
            "+": lambda x, y: x.value + y.value,
            "-": lambda x, y: x.value - y.value,
            "*": lambda x, y: x.value * y.value,
            "/": lambda x, y: x.value // y.value,
            "%": lambda x, y: x.value % y.value,
            "==": lambda x, y: x.value == y.value,
            "!=": lambda x, y: x.value != y.value,
            "<": lambda x, y: x.value < y.value,
            ">": lambda x, y: x.value > y.value,
            "<=": lambda x, y: x.value <= y.value,
            ">=": lambda x, y: x.value >= y.value,
            "&&": lambda x, y: x.value and y.value,
            "||": lambda x, y: x.value or y.value,
        }

    def evaluate(self, scope):
        return Number(self.funcs[self.op](self.lhs.evaluate(scope), self.rhs.evaluate(scope)))


class UnaryOperation:

    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        self.funcs = {
            "-": lambda x: -x.value,
            "!": lambda x: not x.value
        }

    def evaluate(self, scope):
        return Number(self.funcs[self.op](self.expr.evaluate(scope)))


def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    FunctionCall(FunctionDefinition("foo", parent["foo"]), [
                 Number(10), Number(20)]).evaluate(parent)
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    FunctionCall(FunctionDefinition('foo', parent['foo']),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)


def test():
    parent = Scope()
    parent["a"] = Number(42)
    Print(Reference("a")).evaluate(parent)
    scope = Scope(parent)
    Read("mode").evaluate(scope)
    Read("a").evaluate(scope)
    Read("b").evaluate(scope)
    Print(Reference("a")).evaluate(scope)
    Print(Reference("b")).evaluate(scope)
    scope["func"] = Function(('first', 'second'),
                             [
        Read("a"),
        Read("b"),
        Conditional(BinaryOperation(Reference("mode"), "==", Number(1)),
                    [
            Print(Reference("a")),
            Print(Reference("b"))
        ],
            [
            Print(Reference("first")),
            Print(Reference("second"))
        ]
        )
    ])
    FunctionCall(FunctionDefinition("func", scope["func"]),
                 [Reference("a"), Reference("b")]).evaluate(scope)


if __name__ == '__main__':
    test()
