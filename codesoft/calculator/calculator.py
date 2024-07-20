from tkinter import *
import math

def calculate():
    try:
        num = e1.get()
        num = num.replace('÷', '/').replace('x', '*').replace('^', '**')
        result = eval(num)
        e1.delete(0, END)
        e1.insert(0, str(result))
        with open('History.txt', 'a') as f:
            f.write(f"{num} = {str(result)}\n")
    except Exception as e:
        e1.delete(0, END)
        e1.insert(0, "Error")

def click(key):
    current = e1.get()
    e1.delete(0, END)
    e1.insert(0, current + key)

def clear():
    e1.delete(0, END)

def trig_function(func):
    try:
        num = float(e1.get())
        result = func(math.radians(num))
        e1.delete(0, END)
        e1.insert(0, str(result))
    except Exception as e:
        e1.delete(0, END)
        e1.insert(0, "Error")

def factorial():
    try:
        num = int(e1.get())
        result = math.factorial(num)
        e1.delete(0, END)
        e1.insert(0, str(result))
    except Exception as e:
        e1.delete(0, END)
        e1.insert(0, "Error")

memory = 0

def memory_clear():
    global memory
    memory = 0

def memory_recall():
    e1.insert(END, str(memory))

def memory_add():
    global memory
    try:
        memory += float(e1.get())
        e1.delete(0, END)
    except Exception as e:
        e1.delete(0, END)
        e1.insert(0, "Error")

def memory_subtract():
    global memory
    try:
        memory -= float(e1.get())
        e1.delete(0, END)
    except Exception as e:
        e1.delete(0, END)
        e1.insert(0, "Error")

win = Tk()
win.geometry('400x590')
win.title("Scientific Calculator")

e1 = Entry(win, width=16, borderwidth=4, relief=SUNKEN, font=('Arial', 24), 
           highlightbackground="gold", highlightcolor="gold", highlightthickness=2, background='#5f9989')
e1.grid(row=0, column=0, columnspan=5, pady=10)

buttons = [
    ('C', 1, 0, clear), ('(', 1, 1, lambda: click('(')), (')', 1, 2, lambda: click(')')), ('%', 1, 3, lambda: click('%')), ('÷', 1, 4, lambda: click('/')),
    ('7', 2, 0, lambda: click('7')), ('8', 2, 1, lambda: click('8')), ('9', 2, 2, lambda: click('9')), ('x', 2, 3, lambda: click('*')), ('√', 2, 4, lambda: click('math.sqrt(')),
    ('4', 3, 0, lambda: click('4')), ('5', 3, 1, lambda: click('5')), ('6', 3, 2, lambda: click('6')), ('-', 3, 3, lambda: click('-')), ('^', 3, 4, lambda: click('^')),
    ('1', 4, 0, lambda: click('1')), ('2', 4, 1, lambda: click('2')), ('3', 4, 2, lambda: click('3')), ('+', 4, 3, lambda: click('+')), ('log', 4, 4, lambda: click('math.log(')),
    ('+/-', 5, 0, lambda: click('-')), ('0', 5, 1, lambda: click('0')), ('.', 5, 2, lambda: click('.')), ('=', 5, 3, calculate), ('ln', 5, 4, lambda: click('math.log(')),
    ('sin', 6, 0, lambda: trig_function(math.sin)), ('cos', 6, 1, lambda: trig_function(math.cos)), ('tan', 6, 2, lambda: trig_function(math.tan)), ('pi', 6, 3, lambda: click('math.pi')), ('e', 6, 4, lambda: click('math.e')),
    ('!', 7, 0, factorial), ('MC', 7, 1, memory_clear), ('MR', 7, 2, memory_recall), ('M+', 7, 3, memory_add), ('M-', 7, 4, memory_subtract)
]

for (text, row, col, cmd) in buttons:
    button = Button(win, text=text, command=cmd, width=6, height=2, font='Arial 14', background='black', foreground='white', activebackground='#eba834', highlightbackground="gold", highlightcolor="gold")
    button.grid(row=row, column=col, sticky="nsew")

for i in range(9):
    win.grid_rowconfigure(i, weight=1)
for j in range(5):
    win.grid_columnconfigure(j, weight=1)

win.mainloop()
