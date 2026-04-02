
import tkinter as tk
from tkinter import messagebox

# створюємо головне вікно
root = tk.Tk()
root.title("Калькулятор")
root.geometry("300x400")  # розмір вікна

# змінна для збереження введеного виразу
expression = ""

# функція оновлення поля вводу
def press(num):
    global expression
    expression += str(num)
    equation.set(expression)

# функція очищення
def clear():
    global expression
    expression = ""
    equation.set(expression)

# функція обчислення
def equal():
    global expression
    try:
        result = str(eval(expression))
        equation.set(result)
        expression = ""
    except:
        messagebox.showerror("Помилка", "Невірний вираз")
        expression = ""
        equation.set("")

# змінна для поля вводу
equation = tk.StringVar()

# поле вводу
entry = tk.Entry(root, textvariable=equation, font=('Arial', 20), bd=5, relief='ridge', justify='right')
entry.pack(fill='both', ipadx=8, pady=10, padx=10)

# створення кнопок
buttons = [
    ['7','8','9','/'],
    ['4','5','6','*'],
    ['1','2','3','-'],
    ['0','.','=','+'],
]

for row in buttons:
    frame = tk.Frame(root)
    frame.pack(expand=True, fill='both')
    for btn in row:
        action = lambda x=btn: press(x) if x not in ['='] else equal()
        b = tk.Button(frame, text=btn, font=('Arial',18), command=action)
        b.pack(side='left', expand=True, fill='both', padx=2, pady=2)

# кнопка очищення
clear_btn = tk.Button(root, text='C', font=('Arial',18), command=clear, bg='red', fg='white')
clear_btn.pack(fill='both', padx=10, pady=5)

# запускаємо головний цикл
root.mainloop()