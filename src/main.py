import re
import tkinter as tk
from tkinter import OptionMenu, StringVar, filedialog
import os
import webbrowser
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk


history = []
MATH_FUNCS = {
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "log": np.log,
    "sqrt": np.sqrt,
    "exp": np.exp,
    "abs": np.abs,
}

CONSTANTS = {
    "pi": np.pi,
    "e": np.e,
}

currentFig = None


def writeHistory():
    if not history:
        return
    defaultDir = os.path.join(os.path.expanduser("~"), "Downloads")
    path = filedialog.asksaveasfilename(
        initialdir=defaultDir,
        initialfile="calculator_history.txt",
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
    )
    if not path:
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), "hist.txt"))

    with open(path, "w") as f:
        for item in history:
            f.write(item + "\n")


def plotGraph():
    global currentFig

    plt.close("all")

    exp = entry.get()
    exp = exp.replace("^", "**")
    for fn in MATH_FUNCS:
        exp = re.sub(rf"\b{fn}\(", f"np.{fn}(", exp)
    for c in CONSTANTS:
        exp = re.sub(rf"\b{c}", f"np.{c}", exp)

    if not exp:
        return

    expList = [e.strip() for e in exp.split(",")]

    x = np.linspace(-100, 100, 5000)

    fig, axes = plt.subplots()

    for e in expList:
        try:
            y = eval(
                e,
                {"__builtins__": None},
                {
                    "x": x,
                    "np": np,
                },
            )
            axes.plot(x, y, label=e)
        except:
            entry.delete(0, tk.END)
            entry.insert(0, f"Error in: {e}")
            return

    ttl = ""

    axes.margins(0.1)

    for i in expList:
        if ttl == "":
            ttl += f"y = {i}"
        else:
            ttl += f" , y = {i}"

    axes.set_title(ttl)
    axes.grid(True, which="both", linestyle="--", linewidth=0.5, alpha=0.6)
    axes.spines["left"].set_position("zero")
    axes.spines["bottom"].set_position("zero")
    axes.spines["right"].set_color("none")
    axes.spines["top"].set_color("none")

    axes.xaxis.set_ticks_position("bottom")
    axes.yaxis.set_ticks_position("left")

    axes.set_aspect("equal", adjustable="datalim")
    axes.set_xlim(-10, 10)
    axes.set_ylim(-10, 10)

    fig.canvas.mpl_connect("scroll_event", onScroll)

    currentFig = fig

    for w in root.grid_slaves():
        if int(w.grid_info()["row"]) >= 3:
            w.destroy()

    graphFrame = tk.Frame(root)
    graphFrame.grid(row=3, column=0, columnspan=4)

    can = FigureCanvasTkAgg(fig, master=graphFrame)
    can.draw()
    can.get_tk_widget().pack()

    tool = NavigationToolbar2Tk(can, graphFrame)
    tool.update()
    tool.pack()

    tool.pan()


def onScroll(event):
    ax = event.inaxes
    if ax is None:
        return
    base = 1.2
    scale = (
        1 / base if event.button == "up" else base if event.button == "down" else None
    )
    if scale is None:
        return

    cur_xlim = ax.get_xlim()
    cur_ylim = ax.get_ylim()

    xdata, ydata = event.xdata, event.ydata

    new_w = (cur_xlim[1] - cur_xlim[0]) * scale
    new_h = (cur_ylim[1] - cur_ylim[0]) * scale

    relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
    rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])

    ax.set_xlim([xdata - new_w * (1 - relx), xdata + new_w * relx])
    ax.set_ylim([ydata - new_h * (1 - rely), ydata + new_h * rely])

    ax.set_aspect("equal", adjustable="datalim")
    ax.figure.canvas.draw_idle()


def saveGraph(f):
    defaultDir = os.path.join(os.path.expanduser("~"), "Downloads")
    path = filedialog.asksaveasfilename(
        initialdir=defaultDir,
        initialfile="graph.png",
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
    )

    if not path:
        return
    f.savefig(path)


def destroyButtons():
    for w in root.grid_slaves():
        if int(w.grid_info()["row"]) >= 2:
            w.destroy()


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


def changeMode(calc_type):
    destroyButtons()
    if calc_type == "Graph":
        tk.Button(root, text="Plot Graph", width=20, height=2, command=plotGraph).grid(
            row=2, column=0, columnspan=2, pady=5
        )
        tk.Button(
            root,
            text="Save PNG",
            width=20,
            height=2,
            command=lambda: saveGraph(currentFig),
        ).grid(row=2, column=2, columnspan=2, pady=5)
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
icon_path = os.path.join(os.path.dirname(__file__), "calculator.png")
root.iconphoto(False, tk.PhotoImage(file=icon_path))
root.resizable(width=False, height=False)


calc_type = StringVar(value="Calc")
OptionMenu(root, calc_type, *["Calc", "Graph"], command=changeMode).grid(
    row=0, column=3, pady=10
)

entry = tk.Entry(width=20, font=("Arial", 20), borderwidth=5)
entry.grid(row=1, column=0, columnspan=4, pady=10)
entry.focus_force()
entry.bind(
    "<Return>", lambda event: equal() if calc_type.get() == "Calc" else plotGraph()
)


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

createButtons()

menu = tk.Menu(root)
root.config(menu=menu)
fileMenu = tk.Menu(menu)
menu.add_cascade(label="File", menu=fileMenu)
fileMenu.add_command(label="Clear", command=clearAll)
fileMenu.add_command(label="Save History", command=writeHistory)
fileMenu.add_command(label="Save Graph", command=lambda: saveGraph(currentFig))
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
