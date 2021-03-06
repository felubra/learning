from typing import List, Optional


EOF, L_PAREN, R_PAREN, L_SQUARE, R_SQUARE, L_CURLY, R_CURLY = 'EOF', 'L_PAREN', 'R_PAREN', 'L_SQUARE', 'R_SQUARE', 'L_CURLY', 'R_CURLY'

OPEN_TOKENS = [L_PAREN, L_SQUARE, L_CURLY]
CLOSE_TOKENS = [R_PAREN, R_SQUARE, R_CURLY]

TOKEN_KIND_FOR_SYMBOL = {
    '(': L_PAREN,
    ')': R_PAREN,
    '[': L_SQUARE,
    ']': R_SQUARE,
    '{': L_CURLY,
    '}': R_CURLY
}

REVERSE_FOR_TOKEN = {
    L_PAREN: R_PAREN,
    R_PAREN: L_PAREN,
    L_SQUARE: R_SQUARE,
    R_SQUARE: L_SQUARE,
    L_CURLY: R_CURLY,
    R_CURLY: L_CURLY
}


class Token:
    def __init__(self, kind: str) -> None:
        self.kind = kind

    def __str__(self) -> str:
        return f"Token ({self.kind})"

    def __repr__(self) -> str:
        return self.__str__()


class Interpreter:
    def __init__(self, text: str):
        self.text = text

        self.pos = 0
        self.current_token: Optional[Token] = None

    @property
    def current_char(self) -> Optional[str]:
        try:
            return self.text[self.pos]
        except IndexError:
            return None

    def advance(self):
        self.pos += 1

    def get_next_token(self):
        if self.pos > len(self.text) - 1:
            return Token(EOF)

        try:
            if self.current_char is None:
                raise
            kind = TOKEN_KIND_FOR_SYMBOL[self.current_char]
            self.advance()
            return Token(kind)
        except KeyError:
            raise ValueError("Invalid token")

    def eat(self, expected_tokens_kinds: List[str]):
        if self.current_token is None:
            return

        if self.current_token.kind in expected_tokens_kinds:
            self.current_token = self.get_next_token()
        else:
            raise ValueError("Unexpected token")

    def expr(self, provided_left=None):
        try:
            if provided_left is not None:
                left = provided_left
            else:
                self.current_token = self.get_next_token()
                left = self.current_token

            self.eat(OPEN_TOKENS)

            right = self.current_token
            try:
                self.eat([REVERSE_FOR_TOKEN[left.kind]])
            except ValueError:
                if right.kind in OPEN_TOKENS:
                    self.expr(provided_left=right)
                    self.eat([REVERSE_FOR_TOKEN[left.kind]])
                else:
                    raise ValueError

            return 'YES'
        except ValueError:
            return 'NO'


def test_interpreter_walk():
    interpreter = Interpreter("()[]{}")

    assert(interpreter.current_char == '(')
    assert(interpreter.get_next_token().kind == L_PAREN)
    assert(interpreter.current_char == ')')
    assert(interpreter.get_next_token().kind == R_PAREN)

    assert(interpreter.current_char == '[')
    assert(interpreter.get_next_token().kind == L_SQUARE)
    assert(interpreter.current_char == ']')
    assert(interpreter.get_next_token().kind == R_SQUARE)

    assert(interpreter.current_char == '{')
    assert(interpreter.get_next_token().kind == L_CURLY)
    assert(interpreter.current_char == '}')
    assert(interpreter.get_next_token().kind == R_CURLY)

    assert(interpreter.current_char is None)
    assert(interpreter.get_next_token().kind == EOF)


def test_interpreter_pairs():
    interpreter = Interpreter("()[]{}")
    assert(interpreter.expr() == 'YES')


def test_interpreter_no_pairs():
    interpreter = Interpreter("(([({{")
    assert(interpreter.expr() == 'NO')


def test_interpreter_concentric_pairs():
    interpreter = Interpreter("{[()]}")
    assert(interpreter.expr() == 'YES')


def test_nested_pairs_no_pattern():
    inputs = {
        '{(([])[])[]}': 'YES',
        '{(([])[])[]]}': 'NO',
        '{(([])[])[]}[]': 'YES'
    }
    for string, expected_output in inputs.items():
        interpreter = Interpreter(string)
        assert(interpreter.expr() == expected_output)
