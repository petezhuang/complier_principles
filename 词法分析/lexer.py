import sys

class Lexer:
    def __init__(self, sourceCode):
        self.sourceCode = sourceCode
        self.index = 0
        self.currentChar = self.sourceCode[self.index]
    
    keywords = {
        "main",
        "printf",
        "if",
        "int", 
        "for",
        "while",
        "do",
        "return",
        "break",
        "continue"
    }
    operators = {
        "+",
        "-", 
        "*",
        "/",
        "=",
        "++",
        "--",
        "%",
        ">",
        "<",
        ">=",
        "<=",
        "==",
        "+=",
        "-=",
        "!=",
        "/=",
        "&&",
        "||",
        "!",
        "->",
        ".",
        "&",
        "~",
        "<<",
        ">>",
    }
    delimiters = {
        " ",
        ",",
        ";",
        "'",
        "{",
        "}",
        "(",
        ")",
        "[",
        "]",
        "\""
    }

    # Token 类型
    TOKEN_KEYWORD = 1    # 关键字
    TOKEN_IDENTIFIER = 2 # 变量名
    TOKEN_NUMBER = 3     # 数字
    TOKEN_OPERATOR = 4   # 运算符
    TOKEN_DELIMITER = 5  # 分隔符
    TOKEN_STRING = 6    # 字符串字面量

    def get_next_char(self):
        """
        获取下一个字符
        Returns:
            str: 下一个字符,如果到达文件尾则返回None
        """
        if self.index >= len(self.sourceCode):
            return None
            
        c = self.sourceCode[self.index]
        self.index += 1
        return c
    def unget_char(self):
        """
        回退一个字符,将index减1
        """
        if self.index > 0:
            self.index -= 1
        
        
    def skip_whitespace(self):
        """
        跳过空白字符(空格、制表符、换行符)
        """
        while True:
            c = self.get_next_char()
            # 如果到达文件尾或不是空白字符,回退一个字符并返回
            if not c or not c.isspace():
                if c:
                    self.unget_char()
                return

    def get_identifier(self):
        """
        识别并返回标识符
        Returns:
            str: 识别出的标识符
        """
        identifier = ''
        
        # 获取第一个字符
        c = self.get_next_char()
        if c.isalpha() or c == '_':  # 标识符必须以字母或下划线开头
            identifier += c
        else:
            raise Exception("Invalid identifier")
            
        # 获取后续字符
        while True:
            c = self.get_next_char()
            if not c:  # 到达文件尾
                break
            if c.isalnum() or c == '_':  # 标识符后续字符可以是字母、数字或下划线
                identifier += c
            else:
                self.unget_char()
                break
                
        return identifier

    def recognize_number(self):
        """
        识别并返回数字（整数或浮点数）
        Returns:
            str: 识别出的数字字符串
        """
        number = ''
        
        # 获取第一个字符
        c = self.get_next_char()
        if not c.isdigit():  # 数字必须以数字开头
            raise Exception("Invalid number")
            
        number += c
        
        # 获取后续字符
        has_decimal = False  # 是否已经有小数点
        
        while True:
            c = self.get_next_char()
            if not c:  # 到达文件尾
                break
                
            if c.isdigit():  # 数字
                number += c
            elif c == '.' and not has_decimal:  # 第一次遇到小数点
                number += c
                has_decimal = True
            else:  # 其他字符
                self.unget_char()
                break
                
        return number
    

    def recognize_operator(self):
        """
        识别并返回运算符
        Returns:
            str: 识别出的运算符字符串
        """
        # 获取第一个字符
        c = self.get_next_char()
        if not c in '+-*/<>=!%':  # 运算符必须以这些符号开头
            raise Exception("Invalid operator")
            
        operator = c
        
        # 检查是否是双字符运算符
        next_c = self.get_next_char()
        if next_c:
            if (c == '<' and next_c == '=') or \
               (c == '>' and next_c == '=') or \
               (c == '=' and next_c == '=') or \
               (c == '!' and next_c == '='):
                operator += next_c
            else:
                self.unget_char()
                
        return operator

    def recognize_delimiter(self):
        """
        识别并返回分隔符
        Returns:
            str: 识别出的分隔符字符串
        """
        # 获取字符
        c = self.get_next_char()
        if not c in '(){}[];,':  # 分隔符必须是这些符号之一
            raise Exception("Invalid delimiter")
            
        return c
    
    def recognize_string(self):
        """
        识别并返回字符串字面量
        Returns:
            str: 识别出的字符串值(不包含引号)
        """
            
        string_value = ""

        while True:
            c = self.get_next_char()
            if not c:  # 到达文件尾
                raise Exception("未终止的字符串字面量")
            
            if c == '"':  # 字符串结束
                break

            
            # 处理转义字符
            if c == '\\':
                next_char = self.get_next_char()
                if not next_char:
                    raise Exception("未终止的字符串字面量")
                if next_char == 'n':  
                    string_value += '\n'
                elif next_char == 't': 
                    string_value += '\t'
                elif next_char == '"': 
                    string_value += '"'
                elif next_char == '\\': 
                    string_value += '\\'
                else:
                    string_value += next_char
                continue
                
            string_value += c
            
        return string_value


    def scan(self):
        """
        扫描源代码并返回下一个token
        Returns:
            tuple: (token_type, token_value) 
            token_type: TOKEN_KEYWORD, TOKEN_IDENTIFIER等
            token_value: token的具体值
        """
        self.skip_whitespace()
        
        # 获取下一个字符
        c = self.get_next_char()
        
        # 到达文件尾
        if not c:
            return None
            
        # 字符串
        if c == '"':
            string_value = self.recognize_string()
            return (self.TOKEN_STRING, string_value) 
        
        # 标识符或关键字
        if c.isalpha() or c == '_':
            self.unget_char()
            identifier = self.get_identifier()
            if identifier in self.keywords:
                return (self.TOKEN_KEYWORD, identifier)
            return (self.TOKEN_IDENTIFIER, identifier)
            
        # 数字
        if c.isdigit():
            self.unget_char()
            number = self.recognize_number()
            return (self.TOKEN_NUMBER, number)
            
        # 运算符
        if c in self.operators:
            self.unget_char()
            operator = self.recognize_operator()
            return (self.TOKEN_OPERATOR, operator)
            
        # 分隔符
        if c in self.delimiters:
            return (self.TOKEN_DELIMITER, c)
            
        raise Exception(f"Invalid character: {c}")
    
    def __main__(self):
        while True:
            token = self.scan()
            if not token:
                break
            print(token)

if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog
    
    root = tk.Tk()
    root.withdraw()
    
    # 打开文件选择对话框
    file_path = filedialog.askopenfilename(
        title='选择要分析的代码文件',
        filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
    )
    
    if not file_path:
        print("未选择文件")
        sys.exit(0)
        
    try:
        with open(file_path, 'r',encoding='utf-8') as f:
            code = f.read()
            
        lexer = Lexer(code)
        lexer.__main__()
            
    except FileNotFoundError:
        print(f"错误: 找不到文件 '{file_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"错误: {str(e)}")
        sys.exit(1)
