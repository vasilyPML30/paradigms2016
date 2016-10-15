from yat import model

class PrettyPrinter:

    def __init__(self):
        self.padding = 0
        self.padSize = 4

    def visit(self, tree):
        tree.visit(self)
        print(";")

    def visitNumber(self, node):
        print(" " * self.padding, end="")
        print(node.value, end="")

    def visitFunctionDefinition(self, node):
        print(" " * self.padding, end="")
        print("def " + node.name + "(", end="")
        print(", ".join(arg for arg in node.function.args), end="")
        print(") {")
        self.padding += self.padSize
        for statement in node.function.body:
            self.visit(statement)
        self.padding -= self.padSize
        print(" " * self.padding + "}", end="")

    def visitConditional(self, node):
        print(" " * self.padding, end="")
        print("if (", end="")
        tmpPadding = self.padding
        self.padding = 0
        node.condition.visit(self)
        self.padding = tmpPadding
        print(") {")
        self.padding += self.padSize
        for line in node.if_true:
            self.visit(line)
        self.padding -= self.padSize
        print(" " * self.padding + "}", end="")
        if node.if_false != None:
            print(" else {")
            self.padding += self.padSize
            for line in node.if_false:
                self.visit(line)
            self.padding -= self.padSize
            print(" " * self.padding + "}", end="")

    def visitPrint(self, node):
        print(" " * self.padding, end="")
        print("print ", end="")
        tmpPadding = self.padding
        self.padding = 0
        node.expr.visit(self)
        self.padding = tmpPadding

    def visitRead(self, node):
        print(" " * self.padding, end="")
        print("read " + node.name, end="")

    def visitReference(self, node):
        print(" " * self.padding, end="")
        print(node.name, end="")

    def visitFunctionCall(self, node):
        print(" " * self.padding, end="")
        tmpPadding = self.padding
        self.padding = 0
        node.fun_expr.visit(self)
        print("(", end="")
        if node.args:
            node.args[0].visit(self)
            for arg in node.args[1:]:
                print(", ", end="")
                arg.visit(self)
        print(")", end="")
        self.padding = tmpPadding

    def visitBinaryOperation(self, node):
        print(" " * self.padding, end="")
        tmpPadding = self.padding
        self.padding = 0
        print("(", end="")
        node.lhs.visit(self)
        print(" " + node.op + " ", end="")
        node.rhs.visit(self)
        print(")", end="")
        self.padding = tmpPadding

    def visitUnaryOperation(self, node):
        print(" " * self.padding, end="")
        print(node.op, end="")
        tmpPadding = self.padding
        self.padding = 0
        node.expr.visit(self)
        self.padding = tmpPadding


def mytest():
    printer = PrettyPrinter()
    cond2 = model.Conditional(model.Number(
        30), [model.Number(10)], [model.Number(20)])
    cond = model.Conditional(model.Number(42), [model.Number(
        1), cond2, model.Number(3)], [model.Number(4), model.Number(5)])
    cond3 = model.Conditional(model.Number(228), [], [])
    func2 = model.Function(('p111', 'p222'), [model.Reference(
        "x"), model.Print(model.Reference("p111")), model.Read("myVar")])
    fd2 = model.FunctionDefinition("anotherPrettyFunc", func2)
    func = model.Function((), [model.UnaryOperation(
        "-", model.Number(100000000)), fd2, cond, cond3])
    fd = model.FunctionDefinition("myPrettyFunc", func)
    printer.visit(fd)
    asd = model.BinaryOperation(
        model.BinaryOperation(model.Number(123), "+", model.Reference("xx")),
        "*",
        model.UnaryOperation(
            "-", model.BinaryOperation(model.Reference("xx"), "+", model.Reference("yy")))
    )
    printer.visit(asd)
    asd2 = model.BinaryOperation(
        model.BinaryOperation(model.Number(123), "/", model.Reference("xx")),
        "/",
        model.BinaryOperation(
            model.BinaryOperation(model.Reference(
                "xx"), "/", model.Reference("yy")),
            "/",
            model.BinaryOperation(model.Number(
                123), "/", model.Reference("yy"))
        )
    )
    printer.visit(asd2)
    printer.visit(model.FunctionCall(model.Reference("func"), [asd, asd2]))
    cond4 = model.Conditional(model.Number(228), [])
    printer.visit(cond4)
    
if __name__ == "__main__":
    mytest()
