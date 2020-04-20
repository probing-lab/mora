
# gui

from tkinter import filedialog
import tkinter as tk
from mora.mora import mora


root=tk.Tk("")


program_frame = tk.Frame(root)
program_frame.grid()

text=tk.Text(program_frame)
text.insert(tk.END, "x = 0\ny = 0\nwhile true:\n    g = RV(gauss, 0, 1)\n    x = x+1 @ 1/2; x @ 1/2\n    y = y + g\n")
text.grid()

def saveas():
    global text
    t = text.get("1.0", "end-1c")
    if not t or t=="":
        t = "while true:\n    x = x + 2\n"
    savelocation=filedialog.asksaveasfilename()
    file1=open(savelocation, "w+")
    file1.write(t)
    file1.close()
buttonSA=tk.Button(program_frame, text="Save file", command=saveas)
buttonSA.grid()


mora_frame = tk.Frame(root)
mora_frame.grid(row=0, column=1)

#row 0: choose benchmark

goalrow=1
tk.Label(mora_frame, text="Goal (integer)").grid(row=goalrow)
goal=tk.Entry(mora_frame)
goal.insert(10, "1")
goal.grid(row=goalrow, column=1)

def runmora():
    global text
    t = text.get("1.0", "end-1c")
    g = goal.get()
    out = mora(t, goal=g ,output_format="text")
    out = "\n".join(out)
    print(out)
    label.config(text=out)
buttonM=tk.Button(mora_frame, text="MORA", command=runmora)
buttonM.grid(row=2)

label = tk.Label(mora_frame)
label.grid(row=3)
label.config(text="")

root.mainloop()
