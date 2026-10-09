
from dataclasses import dataclass
from typing import Any

class Environment:
    def __init__(self, parent=None):
        self.values = {}
        self.parent = parent

    def define(self, name, value):
        self.values[name] = value

    def get(self, name):
        if name in self.values:
            return self.values[name]

        if self.parent is not None:
            return self.parent.get(name)

        raise NameError(f"Undefined variable: {name}")

    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
            return

        if self.parent is not None:
            self.parent.assign(name, value)
            return

        raise NameError(f"Undefined variable: {name}")

# Expressions
@dataclass
class Literal:
    value: Any


@dataclass
class Variable:
    name: str


@dataclass
class Binary:
    left: Any
    operator: str
    right: Any


@dataclass
class Unary:
    operator: str
    operand: Any


# Statements
@dataclass
class Let:
    name: str
    expression: Any


@dataclass
class Assign:
    name: str
    expression: Any


@dataclass
class Print:
    expression: Any


@dataclass
class Block:
    statements: list


@dataclass
class If:
    condition: Any
    then_branch: Any
    else_branch: Any = None


@dataclass
class While:
    condition: Any
    body: Any

class Evaluator:
    def __init__(self):
        self.environment = Environment()

    def evaluate(self, node):
        # Expressions
        if isinstance(node, Literal):
            return node.value

        if isinstance(node, Variable):
            return self.environment.get(node.name)

        if isinstance(node, Unary):
            value = self.evaluate(node.operand)

            if node.operator == "-":
                return -value

            if node.operator == "not":
                return not value

            raise ValueError(
                f"Unknown unary operator: {node.operator}"
            )

        if isinstance(node, Binary):
            left = self.evaluate(node.left)

            # Short-circuit logical operations
            if node.operator == "and":
                return bool(left) and bool(
                    self.evaluate(node.right)
                )

            if node.operator == "or":
                return bool(left) or bool(
                    self.evaluate(node.right)
                )

            right = self.evaluate(node.right)

            operations = {
                "+": lambda: left + right,
                "-": lambda: left - right,
                "*": lambda: left * right,
                "/": lambda: left / right,
                "%": lambda: left % right,
                "==": lambda: left == right,
                "!=": lambda: left != right,
                ">": lambda: left > right,
                "<": lambda: left < right,
                ">=": lambda: left >= right,
                "<=": lambda: left <= right,
            }

            if node.operator not in operations:
                raise ValueError(
                    f"Unknown operator: {node.operator}"
                )

            return operations[node.operator]()

        # Variable declaration
        if isinstance(node, Let):
            value = self.evaluate(node.expression)
            self.environment.define(node.name, value)
            return value

        # Variable assignment
        if isinstance(node, Assign):
            value = self.evaluate(node.expression)
            self.environment.assign(node.name, value)
            return value

        # Output
        if isinstance(node, Print):
            value = self.evaluate(node.expression)
            print(value)
            return value

        # Block with a child scope
        if isinstance(node, Block):
            previous = self.environment
            self.environment = Environment(previous)

            try:
                result = None

                for statement in node.statements:
                    result = self.evaluate(statement)

                return result
            finally:
                self.environment = previous

        # Conditional branches
        if isinstance(node, If):
            if self.evaluate(node.condition):
                return self.evaluate(node.then_branch)

            if node.else_branch is not None:
                return self.evaluate(node.else_branch)

            return None

        # Loop execution
        if isinstance(node, While):
            result = None

            while self.evaluate(node.condition):
                result = self.evaluate(node.body)

            return result

        raise TypeError(
            f"Unsupported AST node: {type(node).__name__}"
        )

program = Block([
    Let("score", Literal(0)),

    # Repeat while score < 5
    While(
        Binary(
            Variable("score"),
            "<",
            Literal(5)
        ),
        Block([
            Assign(
                "score",
                Binary(
                    Variable("score"),
                    "+",
                    Literal(1)
                )
            ),

            If(
                Binary(
                    Variable("score"),
                    "==",
                    Literal(3)
                ),
                Print(Literal("Score reached 3")),
                Print(Literal("Score is not 3"))
            )
        ])
    ),
    Print(Variable("score"))
])

if __name__ == "__main__":
    evaluator = Evaluator()
    evaluator.evaluate(program)
