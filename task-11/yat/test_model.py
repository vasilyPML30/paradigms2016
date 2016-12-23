from unittest import TestCase, main as runTests
from io import StringIO
from unittest.mock import patch
import model


class TestNumber(TestCase):

    def testNumber(self):
        scope = model.Scope
        number = model.Number(3)
        self.assertIsInstance(number, model.Number)
        self.assertIs(number, number.evaluate(scope))


class TestPrint(TestCase):

    def testPrint(self):
        patcher = patch("sys.stdout", new_callable=StringIO)
        output = patcher.start()
        scope = model.Scope()
        for num in range(20):
            model.Print(model.Number(num - 10)).evaluate(scope)
        self.assertEqual(output.getvalue(), "\n".join(str(num - 10)
                                                      for num in range(20)) + "\n")
        patcher.stop()


class TestRead(TestCase):

    def testRead(self):
        patcher = patch("sys.stdin", StringIO(
            "\n".join(str(num - 10) for num in range(20)) + "\n"))
        patcher.start()
        scope = model.Scope()
        for num in range(20):
            model.Read("var" + str(num)).evaluate(scope)
        patcher.stop()
        patcher = patch("sys.stdout", new_callable=StringIO)
        output = patcher.start()
        for num in range(20):
            model.Print(scope["var" + str(num)]).evaluate(scope)
        self.assertEqual(output.getvalue(), "\n".join(str(num - 10)
                                                      for num in range(20)) + "\n")
        patcher.stop()


class TestScope(TestCase):

    def testScope(self):
        scope1 = model.Scope()
        scope2 = model.Scope(scope1)
        a1 = model.Number(1)
        a2 = model.Number(2)
        b = model.Number(3)
        f = model.Function(None, None)
        scope1["a"] = a1
        scope2["a"] = a2
        scope1["b"] = b
        scope1["f"] = f
        self.assertIsInstance(scope1, model.Scope)
        self.assertIsInstance(scope2, model.Scope)
        self.assertIs(scope1["a"], a1)
        self.assertIs(scope2["a"], a2)
        self.assertIs(scope1["b"], b)
        self.assertIs(scope2["b"], b)
        self.assertIs(scope1["f"], f)
        self.assertIs(scope2["f"], f)


class TestReference(TestCase):

    def testReference(self):
        scope1 = model.Scope()
        scope2 = model.Scope(scope1)
        scope1["a"] = model.Number(1)
        scope2["a"] = model.Number(2)
        scope1["b"] = model.Number(3)
        scope1["f"] = model.Function([], [])
        self.assertIsInstance(model.Reference("a"), model.Reference)
        self.assertIs(scope1["a"], model.Reference("a").evaluate(scope1))
        self.assertIs(scope2["a"], model.Reference("a").evaluate(scope2))
        self.assertIs(scope1["b"], model.Reference("b").evaluate(scope1))
        self.assertIs(scope2["b"], model.Reference("b").evaluate(scope2))
        self.assertIs(scope1["f"], model.Reference("f").evaluate(scope1))
        self.assertIs(scope2["f"], model.Reference("f").evaluate(scope2))


class TestFunction(TestCase):

    def testFunction(self):
        scope = model.Scope()
        number = model.Number(3)
        function = model.Function(["arg"], [model.Number(1), model.Number(2)])
        self.assertIsInstance(function, model.Function)
        self.assertIsInstance(function.evaluate(scope), model.Number)
        patcher = patch("sys.stdout", new_callable=StringIO)
        output = patcher.start()
        model.Print(function.evaluate(scope)).evaluate(scope)
        self.assertEqual(output.getvalue(), "2\n")
        patcher.stop()


class TestBinaryOperation(TestCase):

    def testBinaryOperation(self):
        funcs = {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x // y,
            "%": lambda x, y: x % y,
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
            "<": lambda x, y: x < y,
            ">": lambda x, y: x > y,
            "<=": lambda x, y: x <= y,
            ">=": lambda x, y: x >= y,
            "&&": lambda x, y: x and y,
            "||": lambda x, y: x or y,
        }
        for a in range(-10, 10):
            for b in range(-10, 10):
                for oper, func in funcs.items():
                    if b or not oper in ("%", "/"):
                        with patch('sys.stdout', new_callable=StringIO) as output:
                            scope = model.Scope()
                            operation = model.BinaryOperation(
                                model.Number(a), oper, model.Number(b))
                            self.assertIsInstance(
                                operation, model.BinaryOperation)
                            model.Print(operation.evaluate(
                                scope)).evaluate(scope)
                            if oper in ("+", "-", "*", "/", "%"):
                                self.assertEqual(
                                    int(output.getvalue()), int(func(a, b)))
                            else: 
                                self.assertEqual(
                                    bool(int(output.getvalue())), bool(func(a, b)))

class TestUnaryOperation(TestCase):

    def testUnaryOperation(self):
        for a in range(-10, 10):
            scope = model.Scope()
            with patch('sys.stdout', new_callable=StringIO) as output:
                operation = model.UnaryOperation("-", model.Number(a))
                self.assertIsInstance(operation, model.UnaryOperation)
                model.Print(operation.evaluate(scope)).evaluate(scope)
                self.assertEqual(int(output.getvalue()), int(-a))
            with patch('sys.stdout', new_callable=StringIO) as output:
                operation = model.UnaryOperation("!", model.Number(a))
                self.assertIsInstance(operation, model.UnaryOperation)
                model.Print(operation.evaluate(scope)).evaluate(scope)
                self.assertEqual(bool(int(output.getvalue())), bool(not a))


class TestFunctionDefinition(TestCase):

    def testFunctionDefinition(self):
        scope = model.Scope()
        func1 = model.Function(["arg"], [model.Number(1)])
        func2 = model.Function([], [])
        func3 = model.Function(None, None)
        def1 = model.FunctionDefinition("f1", func1)
        def2 = model.FunctionDefinition("f2", func2)
        def3 = model.FunctionDefinition("f3", func3)
        self.assertIsInstance(def1, model.FunctionDefinition)
        self.assertIsInstance(def2, model.FunctionDefinition)
        self.assertIsInstance(def3, model.FunctionDefinition)
        self.assertIsInstance(def1.evaluate(scope), model.Function)
        self.assertIsInstance(def2.evaluate(scope), model.Function)
        self.assertIsInstance(def3.evaluate(scope), model.Function)
        self.assertIs(scope["f1"], func1)
        self.assertIs(scope["f2"], func2)
        self.assertIs(scope["f3"], func3)


class TestFunctionCall(TestCase):

    def testFunctionCall(self):
        scope = model.Scope()
        func1 = model.Function(
            ["argc", "argv"], [model.Number(1), model.Reference("argc")])
        func2 = model.Function([], [])
        def1 = model.FunctionDefinition("f1", func1)
        def2 = model.FunctionDefinition("f2", func2)
        call1 = model.FunctionCall(def1, [model.Number(1), model.Number(2)])
        call2 = model.FunctionCall(def2, [])
        self.assertIsInstance(call1, model.FunctionCall)
        self.assertIsInstance(call2, model.FunctionCall)
        with patch('sys.stdout', new_callable=StringIO) as output:
            model.Print(call1.evaluate(scope)).evaluate(scope)
            self.assertEqual(int(output.getvalue()), 1)
        call2.evaluate(scope)


class TestConditional(TestCase):

    def testConditional(self):
        scope = model.Scope()
        cond1 = model.Conditional(model.Number(1),
            [model.Number(1)], [model.Number(0)])
        cond2 = model.Conditional(model.Number(0),
            [model.Number(1)], [model.Number(0)])
        cond3 = model.Conditional(model.Number(1), [], [])
        cond4 = model.Conditional(model.Number(0), None, None)
        self.assertIsInstance(cond1, model.Conditional)
        self.assertIsInstance(cond2, model.Conditional)
        self.assertIsInstance(cond3, model.Conditional)
        self.assertIsInstance(cond4, model.Conditional)
        with patch('sys.stdout', new_callable=StringIO) as output:
            model.Print(cond1.evaluate(scope)).evaluate(scope)
            self.assertEqual(int(output.getvalue()), 1)
        with patch('sys.stdout', new_callable=StringIO) as output:
            model.Print(cond2.evaluate(scope)).evaluate(scope)
            self.assertEqual(int(output.getvalue()), 0)
        cond3.evaluate(scope)
        cond4.evaluate(scope)

if __name__ == '__main__':
    runTests()
