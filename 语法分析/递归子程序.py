class RecursiveDescentParser:
    def __init__(self, input_str):
        self.input = input_str
        self.pos = 0
        self.current_char = input_str[0]

    def advance(self):
        """移动到下一个字符"""
        self.pos += 1
        if self.pos < len(self.input):
            self.current_char = self.input[self.pos]
        else:
            self.current_char = None

    def error(self):
        raise Exception("非法的符号串")

    def match(self, expected):
        if self.current_char == expected:
            self.advance()
        else:
            self.error()

    def factor(self):
        """处理因子: i 或 (E)"""
        if self.current_char == 'i':
            self.advance()
        elif self.current_char == '(':
            self.advance()
            self.expr()
            if self.current_char == ')':
                self.advance()
            else:
                self.error()
        else:
            self.error()

    def term(self):
        """处理项: factor (*|/ factor)*"""
        self.factor()
        while self.current_char in ['*', '/']:
            self.advance()
            self.factor()

    def expr(self):
        """处理表达式: term (+|- term)*"""
        self.term()
        while self.current_char in ['+', '-']:
            self.advance()
            self.term()

def parse_expression(input_str):
    if not input_str.endswith('#'):
        return "非法的符号串"
    
    parser = RecursiveDescentParser(input_str)
    try:
        parser.expr()
        if parser.current_char == '#':
            return f"{input_str}为合法符号串"
        else:
            return "非法的符号串"
    except Exception as e:
        return str(e)

# 测试代码
if __name__ == "__main__":
    while True:
        input_str = input("请输入符号串(以#结束): ")
        if input_str.lower() == 'exit':
            break
        result = parse_expression(input_str)
        print(result)
