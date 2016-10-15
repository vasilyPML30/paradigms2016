from yat import model
import printer

class ConstantFolder:

    def visit(self, tree):
        return tree.visit(self)

    def visitNumber(self, node):
        return node

    def visitFunctionDefinition(self, node):
        node.function.body = [self.visit(statement)
                                  for statement in node.function.body]
        return node

    def visitConditional(self, node):
        node.condition = self.visit(node.condition)
        node.if_true = [self.visit(line) for line in node.if_true]
        node.if_false = [self.visit(line) for line in node.if_false]
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
        node.args = [self.visit(arg) for arg in node.args]
        return node

    def visitBinaryOperation(self, node):
        node.lhs = self.visit(node.lhs)
        node.rhs = self.visit(node.rhs)
        if node.op == "*" and isinstance(node.lhs, model.Number) and not node.lhs.value:
            return model.Number(0)
        if node.op == "*" and isinstance(node.rhs, model.Number) and not node.rhs.value:
            return model.Number(0)
        if isinstance(node.lhs, model.Number) and isinstance(node.rhs, model.Number):
            return node.evaluate(None)
        if isinstance(node.lhs, model.Reference) and isinstance(node.rhs, model.Reference) and node.lhs.name == node.rhs.name and node.op == "-":
            return model.Number(0)
        return node

    def visitUnaryOperation(self, node):
        node.expr = self.visit(node.expr)
        if isinstance(node.expr, model.Number):
            return node.evaluate(None)
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
    prr.visit(oper)
    noper = folder.visit(oper)
    prr.visit(noper)
    
if __name__ == "__main__":
    test()
