from yat import model


class ConstantFolder:

    def __init__(self):
        self.UnaryFuncs = {
            "-": lambda x: -x.value,
            "!": lambda x: not x.value
        }
        self.BinaryFuncs = {
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

    def visit(self, tree):
        return tree.visit(self)

    def visitNumber(self, node):
        return node

    def visitFunctionDefinition(self, node):
        node.function.body = list(self.visit(statement)
                                  for statement in node.function.body)
        return node

    def visitConditional(self, node):
        node.condition = self.visit(node.condition)
        node.if_true = list(self.visit(line) for line in node.if_true)
        node.if_false = list(self.visit(line) for line in node.if_false)
        return node

    def visitPrint(self, node):
        node.expr = self.visit(node.expr)
        return node

    def visitRead(self, node):
        return node

    def visitReference(self, node):
        return node

    def visitFunctionCall(self, node):
        node.fun_expr = self.visit(node.fun_expr)
        node.args = list(self.visit(arg) for arg in node.args)
        return node

    def visitBinaryOperation(self, node):
        node.lhs = self.visit(node.lhs)
        node.rhs = self.visit(node.rhs)
        if node.op == "*" and type(node.lhs) == type(model.Number(0)) and not node.lhs.value:
            return model.Number(0)
        if node.op == "*" and type(node.rhs) == type(model.Number(0)) and not node.rhs.value:
            return model.Number(0)
        if type(node.lhs) == type(model.Number(0)) and type(node.rhs) == type(model.Number(0)):
            return model.Number(self.BinaryFuncs[node.op](node.lhs, node.rhs))
        if type(node.lhs) == type(model.Reference("")) and type(node.rhs) == type(model.Reference("")) and node.lhs.name == node.rhs.name and node.op == "-":
            return model.Number(0)
        return node

    def visitUnaryOperation(self, node):
        node.expr = self.visit(node.expr)
        if type(node.expr) == type(model.Number(0)):
            return model.Number(self.UnaryFuncs[node.op](node.expr))
        return node


def test():
    folder = ConstantFolder()
    prr = printer.PrettyPrinter()
    oper = model.BinaryOperation(
        model.BinaryOperation(
            model.BinaryOperation(
                model.BinaryOperation(model.Number(2), "+", model.Number(3)),
                "/",
                model.BinaryOperation(model.Number(
                    2), "+", model.Reference("x"))
            ),
            "/",
            model.BinaryOperation(
                model.BinaryOperation(model.Reference(
                    "x"), "-", model.Reference("x")),
                "/",
                model.BinaryOperation(model.Reference(
                    "x"), "-", model.Reference("y"))
            )
        ),
        "/",
        model.BinaryOperation(
            model.BinaryOperation(
                model.BinaryOperation(model.Number(
                    0), "*", model.Reference("x")),
                "/",
                model.UnaryOperation("!", model.Reference("x"))
            ),
            "/",
            model.UnaryOperation("-", model.Number(30))
        ),
    )
    noper = folder.visit(oper)

if __name__ == "__main__":
    test()
