import tkinter as tk
from tkinter import OptionMenu, StringVar, filedialog
import os
import webbrowser


history = []


def writeHistory():
    if not history:
        return

    defaultDir = os.path.join(os.path.expanduser("~"), "Downloads")
    defaultFile = "calculator_history.txt"
    path = filedialog.asksaveasfilename(
        initialdir=defaultDir,
        initialfile=defaultFile,
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
    )

    if not path:
        path = os.path.join(os.path.dirname(__file__), "hist.txt")

    with open(path, "w") as f:
        for item in history:
            f.write(item + "\n")
    webbrowser.open(path)


def destroyButtons():
    for i in buttonList:
        i.destroy()
    buttonList.clear()


def createButtons():
    for i in buttons:
        btn = tk.Button(
            text=i["text"],
            width=5 * (i["colSpan"]) + 5 * (i["colSpan"] - 1),
            height=2 * (i["rowSpan"]) + 5 * (i["rowSpan"] - 1),
            command=lambda val=i["text"]: click(val),
        )
        btn.grid(
            row=i["row"],
            column=i["col"],
            columnspan=i["colSpan"],
            rowspan=i["rowSpan"],
            ipadx=5,
            ipady=5,
            padx=1,
            pady=1,
        )
        buttonList.append(btn)


def changeMode(calc_type):
    if calc_type == "Graph":
        destroyButtons()
    else:
        createButtons()


def clear():
    if entry.get():
        entry.delete(first=len(entry.get()) - 1, last=tk.END)


def clearAll():
    entry.delete(first=0, last=tk.END)


def equal():
    v = entry.get()
    history.append(v)
    history[-1] += " = "
    entry.delete(first=0, last=tk.END)
    try:
        v = eval(v)
        v = str(v)
        try:
            if float(v) >= 10**100:
                v = "Math error"
            else:
                history[-1] += v
        except:
            history.pop()
            v = "Math error"
    except Exception as e:
        print(e)
        history.pop()
        v = "Syntax error"
    entry.insert(string=v, index=tk.END)


def click(val):
    if val == "ⓧ":
        clear()
        return
    if val == "AC":
        clearAll()
        return
    if val == "=":
        equal()
        return
    if val == "X":
        entry.insert(tk.END, "*")
    elif val == "÷":
        entry.insert(tk.END, "/")
    else:
        entry.insert(tk.END, val)


root = tk.Tk()
root.title("Calculator")
icon_path = os.path.join(os.path.dirname(__file__), "..", "assets", "calculator.png")
root.iconphoto(False, tk.PhotoImage(file=icon_path))
root.resizable(width=False, height=False)


calc_type = StringVar(value="Calc")
OptionMenu(root, calc_type, *["Calc", "Graph"], command=changeMode).grid(
    row=0, column=3, pady=10
)

entry = tk.Entry(width=20, font=("Arial", 20), borderwidth=5)
entry.grid(row=1, column=0, columnspan=4, pady=10)
entry.focus_force()
entry.bind("<Return>", lambda event: equal())


buttons = [
    {
        "row": 2,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 2,
        "text": "ⓧ",
        # "fn": print("del"),
    },
    {
        "row": 2,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "AC",
        # "fn": print("clear"),
    },
    {
        "row": 2,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "÷",
        # "fn": print("/"),
    },
    {
        "row": 3,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "7",
        # "fn": print("7"),
    },
    {
        "row": 3,
        "col": 1,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "8",
        # "fn": print("8"),
    },
    {
        "row": 3,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "9",
        # "fn": print("9"),
    },
    {
        "row": 3,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "X",
        # "fn": print("*"),
    },
    {
        "row": 4,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "4",
        # "fn": print("4"),
    },
    {
        "row": 4,
        "col": 1,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "5",
        # "fn": print("5"),
    },
    {
        "row": 4,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "6",
        # "fn": print("6"),
    },
    {
        "row": 4,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "-",
        # "fn": print("-"),
    },
    {
        "row": 5,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "1",
        # "fn": print("1"),
    },
    {
        "row": 5,
        "col": 1,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "2",
        # "fn": print("2"),
    },
    {
        "row": 5,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "3",
        # "fn": print("3"),
    },
    {
        "row": 5,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "+",
        # "fn": print("+"),
    },
    {
        "row": 6,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 2,
        "text": "0",
        # "fn": print("0"),
    },
    {
        "row": 6,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": ".",
        # "fn": print("."),
    },
    {
        "row": 6,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "=",
        # "fn": print("="),
    },
]
buttonList = []

createButtons()

menu = tk.Menu(root)
root.config(menu=menu)
fileMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Clear", command=clearAll)
fileMenu.add_command(label="Save History", command=writeHistory)
fileMenu.add_separator()
fileMenu.add_command(label="Exit", command=root.destroy)

helpMenu = tk.Menu(menu)
menu.add_cascade(label="Help", menu=helpMenu)
helpMenu.add_command(
    label="About",
    command=lambda: webbrowser.open_new(
        "https://github.com/Apishrana/Tkinter-calculater/blob/main/README.md"
    ),
)


root.mainloop()
