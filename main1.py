import ast
import operator
import tkinter as tk
from tkinter import messagebox

# Safe calculator implementation: supports + - * / // % ** and parentheses.
OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def safe_eval(expr: str) -> float:
    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        if isinstance(node, ast.Num):
            return node.n
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Only numbers are allowed")
        if isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)
            if op_type in OPS:
                return OPS[op_type](left, right)
            raise ValueError(f"Operator {op_type} is not supported")
        if isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            op_type = type(node.op)
            if op_type in OPS:
                return OPS[op_type](operand)
            raise ValueError(f"Operator {op_type} is not supported")

        raise ValueError(f"Unsupported expression: {type(node).__name__}")

    expr_ast = ast.parse(expr, mode="eval")
    return _eval(expr_ast)


class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор")
        self.geometry("340x460")
        self.resizable(False, False)
        self.configure(bg="#2b2d42")
        self.create_widgets()

    def create_widgets(self):
        self.entry = tk.Entry(self, font=("Segoe UI", 24, "bold"), borderwidth=3, relief="ridge", justify="right", bg="#edf2f4", fg="#2b2d42")
        self.entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=10, pady=12)

        buttons = [
            ('7', 1, 0, '#8d99ae'), ('8', 1, 1, '#8d99ae'), ('9', 1, 2, '#8d99ae'), ('/', 1, 3, '#ef233c'),
            ('4', 2, 0, '#8d99ae'), ('5', 2, 1, '#8d99ae'), ('6', 2, 2, '#8d99ae'), ('*', 2, 3, '#ef233c'),
            ('1', 3, 0, '#8d99ae'), ('2', 3, 1, '#8d99ae'), ('3', 3, 2, '#8d99ae'), ('-', 3, 3, '#ef233c'),
            ('0', 4, 0, '#8d99ae'), ('.', 4, 1, '#8d99ae'), ('%', 4, 2, '#8d99ae'), ('+', 4, 3, '#ef233c'),
            ('(', 5, 0, '#a8dadc'), (')', 5, 1, '#a8dadc'), ('^', 5, 2, '#a8dadc'), ('C', 5, 3, '#d00000'),
            ('=', 6, 0, '#06d6a0', 4),
        ]

        for btn in buttons:
            text = btn[0]
            r = btn[1]
            c = btn[2]
            color = btn[3]
            colspan = btn[4] if len(btn) == 5 else 1
            action = lambda x=text: self.on_button_click(x)
            tk.Button(self, text=text, width=5, height=2, font=("Segoe UI", 16, "bold"), fg="#ffffff", bg=color, activebackground="#ffb703", activeforeground="#000000", bd=0, relief="raised", command=action).grid(row=r, column=c, columnspan=colspan, sticky="nsew", padx=5, pady=5)

        for i in range(7):
            self.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

    def on_button_click(self, label):
        if label == 'C':
            self.entry.delete(0, tk.END)
            return
        if label == '=':
            self.calculate()
            return

        if label == '^':
            label = '**'

        self.entry.insert(tk.END, label)

    def calculate(self):
        expression = self.entry.get().strip()
        if not expression:
            return

        try:
            result = safe_eval(expression)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
        except ZeroDivisionError:
            messagebox.showerror("Помилка", "Ділення на нуль")
        except Exception as e:
            messagebox.showerror("Помилка", f"Невірний вираз: {e}")


if __name__ == '__main__':
    app = CalculatorApp()
    app.mainloop()
