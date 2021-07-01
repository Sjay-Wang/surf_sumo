import traci
import tkinter as tk
from tkinter import ttk
from tkinter import *
def get_screen_size(window):
    return window.winfo_screenwidth(), window.winfo_screenheight()


def get_window_size(window):
    return window.winfo_reqwidth(), window.winfo_reqheight()


def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    print(size)
    root.geometry(size)

def setWindow():
    root = tk.Tk()
    root.title('checkspeed')

    center_window(root, 300, 240)
    root.maxsize(600, 400)
    root.minsize(300, 240)
    Labela = ttk.Label(root,text="Enter the vehicle")
    Labela.place(x=20,y=10)
    Entrya = ttk.Entry(root)
    Entrya.place(x=130,y=10)
    text = Text(root, width=40, height=12, undo=True, autoseparators=True)
    text.place(x=10, y=70)
    def checkspeed():
        getVehicle = Entrya.get()
        text.insert(INSERT, getVehicle)
    Buttona = ttk.Button(root, text="Enter" ,command=checkspeed)
    Buttona.place(x=100, y=40)
    root.mainloop()  # 进入消息循环




if __name__ == "__main__":
     setWindow()