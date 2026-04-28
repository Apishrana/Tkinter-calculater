import tkinter as tk
import os
import webbrowser


def clear():
    entry.delete(first=len(entry.get()) - 1, last=tk.END)


def clearAll():
    entry.delete(first=0, last=tk.END)


def equal():
    v = entry.get()
    entry.delete(first=0, last=tk.END)
    try:
        v = eval(v)
        v = str(v)
        if int(v) >= 10**100:
            v = "Math error"
        try:
            float(v)
        except:
            v = "Math error"
    except:
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


entry = tk.Entry(width=20, font=("Arial", 20), borderwidth=5)
entry.grid(row=0, column=0, columnspan=4)
entry.focus_force()


buttons = [
    {
        "row": 1,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 2,
        "text": "ⓧ",
        # "fn": print("del"),
    },
    {
        "row": 1,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "AC",
        # "fn": print("clear"),
    },
    {
        "row": 1,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "÷",
        # "fn": print("/"),
    },
    {
        "row": 2,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "7",
        # "fn": print("7"),
    },
    {
        "row": 2,
        "col": 1,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "8",
        # "fn": print("8"),
    },
    {
        "row": 2,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "9",
        # "fn": print("9"),
    },
    {
        "row": 2,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "X",
        # "fn": print("*"),
    },
    {
        "row": 3,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "4",
        # "fn": print("4"),
    },
    {
        "row": 3,
        "col": 1,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "5",
        # "fn": print("5"),
    },
    {
        "row": 3,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "6",
        # "fn": print("6"),
    },
    {
        "row": 3,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "-",
        # "fn": print("-"),
    },
    {
        "row": 4,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "1",
        # "fn": print("1"),
    },
    {
        "row": 4,
        "col": 1,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "2",
        # "fn": print("2"),
    },
    {
        "row": 4,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "3",
        # "fn": print("3"),
    },
    {
        "row": 4,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "+",
        # "fn": print("+"),
    },
    {
        "row": 5,
        "col": 0,
        "rowSpan": 1,
        "colSpan": 2,
        "text": "0",
        # "fn": print("0"),
    },
    {
        "row": 5,
        "col": 2,
        "rowSpan": 1,
        "colSpan": 1,
        "text": ".",
        # "fn": print("."),
    },
    {
        "row": 5,
        "col": 3,
        "rowSpan": 1,
        "colSpan": 1,
        "text": "=",
        # "fn": print("="),
    },
]

for i in buttons:
    tk.Button(
        text=i["text"],
        width=5 * (i["colSpan"]) + 5 * (i["colSpan"] - 1),
        height=2 * (i["rowSpan"]) + 5 * (i["rowSpan"] - 1),
        command=lambda val=i["text"]: click(val),
    ).grid(
        row=i["row"],
        column=i["col"],
        columnspan=i["colSpan"],
        rowspan=i["rowSpan"],
        ipadx=5,
        ipady=5,
        padx=1,
        pady=1,
    )


menu = tk.Menu(root)
root.config(menu=menu)
fileMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Clear", command=clearAll)
fileMenu.add_command(label="Save History")
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
