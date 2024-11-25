"""
使用栈来实现预测分析法，分析简单的算术表达式
"""
import tkinter as tk
from tkinter import ttk, scrolledtext

class PredictiveParser:
    def __init__(self, input_str):
        self.input = input_str
        self.pos = 0
        self.stack = ['#', 'E']  # 初始化分析栈
        self.step = 1
        self.output = []
        
        # 预测分析表
        self.parse_table = {
            'E': {'i': 'TG', '(': 'TG'},
            'G': {'+': '+TG', '-': '-TG', ')': 'ε', '#': 'ε'},
            'T': {'i': 'FS', '(': 'FS'},
            'S': {'*': '*FS', '/': '/FS', '+': 'ε', '-': 'ε', ')': 'ε', '#': 'ε'},
            'F': {'i': 'i', '(': '(E)'}
        }
        
        self.output.append("步骤\t\t分析栈\t\t剩余输入串\t\t所用产生式")
        
    def get_current_symbol(self):
        if self.pos < len(self.input):
            return self.input[self.pos]
        return None
        
    def parse(self):
        while len(self.stack) > 1:  # 当栈不为空时
            top = self.stack[-1]  # 栈顶符号
            current = self.get_current_symbol()  # 当前输入符号
            
            if current is None:
                return "非法的符号串"
                
            # 记录当前状态
            line = f"{self.step}\t\t{''.join(self.stack)}\t\t{self.input[self.pos:]}\t\t"
            
            # 如果栈顶是终结符
            if top in ['+', '-', '*', '/', '(', ')', 'i', '#']:
                if top == current:  # 匹配成功
                    self.stack.pop()
                    self.pos += 1
                    if len(self.stack) == 1 and self.stack[0] == '#' and current == '#':
                        line += "接受"
                    else:
                        line += "匹配" + top
                else:  # 匹配失败
                    return "非法的符号串"
            
            # 如果栈顶是非终结符
            else:
                if top in self.parse_table and current in self.parse_table[top]:
                    production = self.parse_table[top][current]
                    self.stack.pop()
                    if production != 'ε':  # 如果不是空产生式
                        for char in reversed(production):
                            self.stack.append(char)
                    # 检查是否分析结束
                    if len(self.stack) == 1 and self.stack[0] == '#' and current == '#':
                        line += "接受"
                    else:
                        line += f"{top}->{production}"
                else:
                    return "非法的符号串"
            
            self.output.append(line)
            self.step += 1
            
        return "合法的符号串"

class ParserGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2250801430庄珺尧预测分析器")
        
        # 创建输入框和按钮
        input_frame = ttk.Frame(root, padding="10")
        input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        ttk.Label(input_frame, text="请输入符号串(以#结束):").grid(row=0, column=0, padx=5)
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(input_frame, textvariable=self.input_var)
        self.input_entry.grid(row=0, column=1, padx=5)
        
        ttk.Button(input_frame, text="分析", command=self.analyze).grid(row=0, column=2, padx=5)
        ttk.Button(input_frame, text="清空", command=self.clear).grid(row=0, column=3, padx=5)
        
        # 创建输出文本区域
        self.output_text = scrolledtext.ScrolledText(root, width=60, height=20)
        self.output_text.grid(row=1, column=0, padx=10, pady=10)
        
    def analyze(self):
        input_str = self.input_var.get()
        if not input_str:
            return
            
        parser = PredictiveParser(input_str)
        result = parser.parse()
        
        # 显示分析过程
        self.output_text.delete(1.0, tk.END)
        for line in parser.output:
            self.output_text.insert(tk.END, line + '\n')
        self.output_text.insert(tk.END, f"\n输入符号串{input_str}为{result}")
        
    def clear(self):
        self.input_var.set("")
        self.output_text.delete(1.0, tk.END)

def analyze_expression():
    root = tk.Tk()
    app = ParserGUI(root)
    root.mainloop()

if __name__ == "__main__":
    analyze_expression()