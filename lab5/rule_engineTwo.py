
import sys
import re

KEYWORDS = [
    "let", "if", "else", "while", "for", "in", "rule", "priority", "when", "then", "and", "or", "not", "true", "false", "null"
]

def lexer(source):
    pattern = r'''
        \s+ |
        \#[^\n]* |
        \d+(?:\.\d+)? |
        "(?:[^"\\]|\\.)*" |
        [a-zA-Z_][a-zA-Z_0-9]* |
        == | != | <= | >= |
        [+\-*/%<>=(){};,]
    '''
    
    words = re.findall(pattern, source, re.VERBOSE)
    tokens = []
    for word in words:
        if word.isspace() or word.startswith("#"):
            continue
        if word[0] == '"':
            tokens.append(("STRING", word[1:-1]))
        elif word[0].isdigit():
            if "." in word:
                tokens.append(("NUMBER", float(word)))
            else:
                tokens.append(("NUMBER", int(word)))
        elif word in KEYWORDS:
            tokens.append(("KEYWORD", word))
        elif word[0].isalpha() or word[0] == "_":
            tokens.append(("IDENT", word))
        else:
            tokens.append(("OP", word))
    tokens.append(("EOF", "EOF"))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
    def peek(self):
        return self.tokens[self.pos]
    def check(self, value):
        return self.peek()[1] == value
    def take(self):
        token = self.peek()
        self.pos += 1
        return token
    def expect(self, value):
        if not self.check(value):
            raise Exception("Expected " + value)
        return self.take()
    def parse(self):
        statements = []
        while not self.check("EOF"):
            statements.append(self.statement())
        return {"type": "block", "body": statements}
    def statement(self):
        if self.check("let"):
            self.take()
            name = self.expect_name()
            self.expect("=")
            value = self.expression()
            self.expect(";")
            return {"type": "let", "name": name, "value": value}
        if self.check("if"):
            self.take()
            condition = self.expression()
            body = self.block()
            other = None
            if self.check("else"):
                self.take()
                if self.check("if"):
                    other = self.statement()
                else:
                    other = self.block()
            return {
                "type": "if",
                "condition": condition,
                "body": body,
                "other": other
            }
        if self.check("while"):
            self.take()
            condition = self.expression()
            return {
                "type": "while",
                "condition": condition,
                "body": self.block()
            }
        if self.check("for"):
            self.take()
            name = self.expect_name()
            self.expect("in")
            items = self.expression()
            return {
                "type": "for",
                "name": name,
                "items": items,
                "body": self.block()
            }
        if self.check("rule"):
            self.take()
            name = self.take()[1]
            priority = 0
            if self.check("priority"):
                self.take()
                priority = self.take()[1]
            self.expect("when")
            condition = self.expression()
            self.expect("then")
            return {
                "type": "rule",
                "name": name,
                "priority": priority,
                "condition": condition,
                "body": self.block()
            }
        if self.check("{"):
            return self.block()
        if (self.peek()[0] == "IDENT"
                and self.tokens[self.pos + 1][1] == "="):
            name = self.take()[1]
            self.take()
            value = self.expression()
            self.expect(";")
            return {"type": "assign", "name": name, "value": value}
        value = self.expression()
        self.expect(";")
        return {"type": "expression", "value": value}
    def block(self):
        self.expect("{")
        statements = []
        while not self.check("}"):
            if self.check("EOF"):
                raise Exception("Missing closing brace")
            statements.append(self.statement())
        self.expect("}")
        return {"type": "block", "body": statements}
    def expect_name(self):
        token = self.take()
        if token[0] != "IDENT":
            raise Exception("Expected a variable name")
        return token[1]
    def expression(self):
        return self.logical_or()
    def logical_or(self):
        left = self.logical_and()
        while self.check("or"):
            op = self.take()[1]
            right = self.logical_and()
            left = {"type": "binary", "op": op, "left": left, "right": right}
        return left
    def logical_and(self):
        left = self.equality()
        while self.check("and"):
            op = self.take()[1]
            right = self.equality()
            left = {"type": "binary", "op": op, "left": left, "right": right}
        return left
    def equality(self):
        left = self.comparison()
        while self.check("==") or self.check("!="):
            op = self.take()[1]
            right = self.comparison()
            left = {"type": "binary", "op": op, "left": left, "right": right}
        return left
    def comparison(self):
        left = self.term()
        while any(self.check(op) for op in
                  ["<", ">", "<=", ">="]):
            op = self.take()[1]
            right = self.term()
            left = {"type": "binary", "op": op, "left": left, "right": right}
        return left
    def term(self):
        left = self.factor()
        while self.check("+") or self.check("-"):
            op = self.take()[1]
            right = self.factor()
            left = {"type": "binary", "op": op, "left": left, "right": right}
        return left
    def factor(self):
        left = self.unary()
        while any(self.check(op) for op in ["*", "/", "%"]):
            op = self.take()[1]
            right = self.unary()
            left = {"type": "binary", "op": op, "left": left, "right": right}
        return left
    def unary(self):
        if self.check("not") or self.check("-"):
            op = self.take()[1]
            return {
                "type": "unary", "op": op, "value": self.unary()
            }
        return self.primary()
    def primary(self):
        token = self.take()
        kind, value = token
        if kind == "NUMBER" or kind == "STRING":
            return {"type": "literal", "value": value}
        if kind == "KEYWORD" and value in [
            "true", "false", "null"
        ]:
            values = {
                "true": True,
                "false": False,
                "null": None
            }
            return {"type": "literal", "value": values[value]}
        if kind == "IDENT":
            if self.check("("):
                self.take()
                args = []
                if not self.check(")"):
                    args.append(self.expression())
                    while self.check(","):
                        self.take()
                        args.append(self.expression())
                self.expect(")")
                return {
                    "type": "call",
                    "name": value,
                    "args": args
                }
            return {"type": "variable", "name": value}
        if value == "(":
            result = self.expression()
            self.expect(")")
            return result
        raise Exception("Invalid expression: " + str(value))

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
        raise Exception("Undefined variable: " + name)
    def assign(self, name, value):
        if name in self.values:
            self.values[name] = value
        elif self.parent is not None:
            self.parent.assign(name, value)
        else:
            raise Exception("Undefined variable: " + name)

class Interpreter:
    def __init__(self):
        self.global_env = Environment()
        self.rules = []
    def evaluate(self, node, env):
        kind = node["type"]
        if kind == "literal":
            return node["value"]
        if kind == "variable":
            return env.get(node["name"])
        if kind == "unary":
            value = self.evaluate(node["value"], env)
            if node["op"] == "not":
                return not value
            return -value
        if kind == "binary":
            op = node["op"]
            left = self.evaluate(node["left"], env)
            if op == "and":
                return (left and
                        self.evaluate(node["right"], env))
            if op == "or":
                return (left or
                        self.evaluate(node["right"], env))
            right = self.evaluate(node["right"], env)
            if op == "+":
                if isinstance(left, str) or isinstance(right, str):
                    return str(left) + str(right)
                return left + right
            if op == "-":
                return left - right
            if op == "*":
                return left * right
            if op == "/":
                if right == 0:
                    raise Exception("Division by zero")
                return left / right
            if op == "%":
                return left % right
            if op == "==":
                return left == right
            if op == "!=":
                return left != right
            if op == ">":
                return left > right
            if op == "<":
                return left < right
            if op == ">=":
                return left >= right
            if op == "<=":
                return left <= right
        if kind == "call":
            name = node["name"]
            args = [
                self.evaluate(arg, env)
                for arg in node["args"]
            ]
            functions = {
                "print": print,
                "len": len,
                "min": min,
                "max": max,
                "abs": abs,
                "int": int,
                "str": str,
                "range": range
            }
            if name not in functions:
                raise Exception("Unknown function: " + name)
            return functions[name](*args)
        raise Exception("Unknown expression: " + kind)
    def execute(self, node, env):
        kind = node["type"]
        if kind == "block":
            for statement in node["body"]:
                self.execute(statement, env)
        elif kind == "let":
            value = self.evaluate(node["value"], env)
            env.define(node["name"], value)
        elif kind == "assign":
            value = self.evaluate(node["value"], env)
            env.assign(node["name"], value)
        elif kind == "expression":
            self.evaluate(node["value"], env)
        elif kind == "if":
            condition = self.evaluate(node["condition"], env)
            if condition:
                self.execute(node["body"], env)
            elif node["other"] is not None:
                self.execute(node["other"], env)
        elif kind == "while":
            count = 0
            while self.evaluate(node["condition"], env):
                count += 1
                if count > 100000:
                    raise Exception("Loop limit reached")
                self.execute(node["body"], env)
        elif kind == "for":
            items = self.evaluate(node["items"], env)
            for item in items:
                loop_env = Environment(env)
                loop_env.define(node["name"], item)
                self.execute(node["body"], loop_env)
        elif kind == "rule":
            self.rules.append(node)
    def run(self, program):
        self.execute(program, self.global_env)
    def fire_rules(self):
        self.rules.sort(
            key=lambda rule: rule["priority"], reverse=True
        )
        fired = []
        for rule in self.rules:
            rule_env = Environment(self.global_env)
            condition = self.evaluate(
                rule["condition"], rule_env
            )
            if condition:
                fired.append(rule["name"])
                self.execute(rule["body"], rule_env)
        return fired

class RuleEngine:
    def __init__(self):
        self.interpreter = Interpreter()
    def set_fact(self, name, value):
        self.interpreter.global_env.define(name, value)
    def get_fact(self, name):
        return self.interpreter.global_env.get(name)
    def load(self, source):
        tokens = lexer(source)
        parser = Parser(tokens)
        program = parser.parse()
        self.interpreter.run(program)
    def fire(self):
        return self.interpreter.fire_rules()

DEMO = """
let discount = 0;
let shipping = 10;
let notes = "";

rule "Bulk order" priority 10 when quantity >= 10 then {
    discount = discount + 5;
}

rule "Loyalty member" priority 5 when is_member and total > 100 then {
    discount = discount + 10;
}

rule "Free shipping" priority 5 when total >= 100 then {
    shipping = 0;
}

rule "Tier bonus" priority 1 when discount > 0 then {
    if discount >= 15 {
        notes = "Gold tier";
    } else if discount >= 10 {
        notes = "Silver tier";
    } else {
        notes = "Bronze tier";
    }
}

rule "Loyalty points" priority 0 when is_member then {
    let points = 0;
    let i = 1;
    while i <= 3 {
        points = points + i * 10;
        i = i + 1;
    }
    print("Points earned:", points);
}
"""

SCOPE_DEMO = """
let x = "global";
{
    let x = "block";
    print("Inside block:", x);
    {
        x = "changed";
        print("Inside inner block:", x);
    }
}

print("Global x:", x);
let total = 0;
for n in range(1, 6) {
    if n % 2 == 0 {
        total = total + n;
    }
}
print("Sum of even numbers:", total);
let k = 10;
while k > 0 {
    k = k - 4;
}
print("Final k:", k);
"""

def demo():
    print("PART 1: SCOPES AND LOOPS")
    engine = RuleEngine()
    engine.load(SCOPE_DEMO)

    print()
    print("PART 2: RULE ENGINE")
    engine = RuleEngine()
    engine.set_fact("total", 250)
    engine.set_fact("quantity", 12)
    engine.set_fact("is_member", True)
    engine.load(DEMO)
    fired = engine.fire()

    print("Rules fired:", ", ".join(fired))
    print("Discount:", engine.get_fact("discount"), "%")
    print("Shipping:", engine.get_fact("shipping"))
    print("Tier:", engine.get_fact("notes"))

def main():
    try:
        if len(sys.argv) > 1:
            with open(sys.argv[1], "r", encoding="utf-8") as file:
                source = file.read()
            engine = RuleEngine()
            engine.load(source)
            print("Rules fired:", ", ".join(engine.fire()))
        else:
            demo()
    except Exception as error:
        print("Error:", error)

if __name__ == "__main__":
    main()