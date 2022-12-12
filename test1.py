import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # self.window     = None
        # self.panelLeft  = None
        # self.PanelMid   = None
        # self.PanelRight = None

    # def CreateWindow(self):
        self.window = Tk()
        self.window.geometry("1080x600")
        self.window.title("test")

    
        
        self.panelLeft = PanedWindow(self.window,width = 50, height = 30)
        self.panelMid = PanedWindow(self.window, width = 50, height = 30)
        self.panelRight = PanedWindow(self.window, width = 50, height = 30)

if __name__ == "__main__":
    app = App()
    app.mainloop()