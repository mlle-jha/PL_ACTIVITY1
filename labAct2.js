class token {
    constructor(type, value){
        this.type = type;
        this.value = value;
    }
}
//Custom Lexer class using RegEx
class lexer {
    //lex separate each token, remove whitespce, etc
    //regex sets rule
    constructor(sourceText){
        this.sourceText = sourceText; //program being analyzed
        this.index = 0; //where start and current position in sourceText

        this.tokRules = [
            { type: "KEYWORD", regex: /^(if|else|while|for|return|let)\b/},
            { type: "IDENTIFIER", regex: /^[a-zA-Z_][a-zA-Z0-9_]*/ },
            { type: "ASSIGN", regex: /^=/},
            { type: "NUMBER", regex: /^[0-9]+/},
            { type: "WHITESPACE", regex: /^\s+/},
            { type: "ADD", regex: /^\+/ },
            { type: "MIN", regex: /^\-/ },
            { type: "MULTI", regex: /^\*/ },
            { type: "DIV", regex: /^\// },
            { type: "LPAREN", regex: /^\(/ },
            { type: "RPAREN", regex: /^\)/ },
            { type: "SEMICOLON", regex: /^;/},
        ]
    }
    tokenize(){
        const tokens = [];
        while (this.index < this.sourceText.length){ 
            let remText = this.sourceText.slice(this.index); //get remaining txt fr current inndex
            let matched = false; //if found

            for (const rule of this.tokRules) {
                const match = remText.match(rule.regex);
                if (match) {
                    let value = match[0];
                    this.index = this.index + value.length
                    matched = true;

                    if (rule.type !== "WHITESPACE") {
                        tokens.push(new token(rule.type, value)); //inaadd niya yung token sa token array
                    }
                    break;
                }
            }
            if (!matched) { //like 222+@, the @ have no match
                throw new Error(`Unexpected character at position ${this.index}`);
            }
        }
        return tokens;
    }
}

//hand-crafted Parser using Recursive Descent
class parser {
    constructor(tokens){
        this.tokens = tokens;
        this.index = 0;
    }
    
    parse() { //starting point of parsing. reads token + build ast
        const ast = this.expression();
        return ast;
    }

    expression() { //handles add and min. more like calls term() to do its job first before this
        let lNode = this.term();

        while (this.index < this.tokens.length && (this.tokens[this.index].type === "ADD" || this.tokens[this.index].type === "MIN")) {
            const operator = this.tokens[this.index];
            this.index++;
            const rNode = this.term();

            lNode = {
                type: "BinaryExpression",
                operator: operator.value,
                left: lNode,
                right: rNode
            };
        }
        return lNode;
    }

    term() { //handles multi and div
        let lNode = this.factor();

        while (this.index < this.tokens.length && (this.tokens[this.index].type === "MULTI" || this.tokens[this.index].type === "DIV")) {
            const operator = this.tokens[this.index];
            this.index++;
            const rNode = this.factor();

            lNode = {
                type: "BinaryExpression",
                operator: operator.value,
                left: lNode,
                right: rNode
            };
        }
        return lNode;
    }

    factor() { //handles numbers and identifiers
        const token = this.tokens[this.index];

        if (token.type === "IDENTIFIER") {
            this.index++;

            return {
                type: "Identifier",
                name: token.value
            };
        }

        if (token.type === "NUMBER") {
            this.index++;
            return {
                type: "NumericLiteral",
                value: parseFloat(token.value)
            };
        }
        
        if (token.type === "LPAREN") {
            this.index++; //skips the (
            const inNode = this.expression(); //only read what's inside
            if (this.tokens[this.index].type !== "RPAREN") {
                throw new Error("Missing: )"); //checks missing rparen
            }
            this.index++; //skips the )
            return inNode;
        }
        throw new Error(`Unexpected token: ${token.value}`);
    }
}

function evaluateAST(node) {
    if (node.type == "NumericLiteral") { //if num ang una, it will return the value
        return node.value;
    }

    if (node.type == "BinaryExpression") { //binexpression, will eval l and r to get values
        const lNodeVal = evaluateAST (node.left);
        const rNodeVal = evaluateAST (node.right);

        switch (node.operator) { //after getting values, proceed to operation
            case "+":
                return lNodeVal + rNodeVal;
            case "-":
                return lNodeVal - rNodeVal;
            case "*":
                return lNodeVal * rNodeVal;
            case "/":
                if (rNodeVal == 0){
                    throw new Error("Undefined");
                }
                return lNodeVal / rNodeVal;
        }
    }
}

const input = "222 + ((212 * 20) / 22)";

//tokenize
const lex = new lexer (input);
const tokens = lex.tokenize();

//parse to AST
const parse = new parser (tokens);
const ast = parse.parse();

//evaluate
console.log("TOKENS:");
console.log(tokens);

console.log("AST:");
console.log(JSON.stringify(ast, null, 2));

console.log("RESULT:");
console.log(evaluateAST(ast));