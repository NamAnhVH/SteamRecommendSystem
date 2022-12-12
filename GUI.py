from tkinter import *
from tkinter import ttk
import dataProcessing as dp
import numpy as np
import tkinter as tk

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.window                = None
        self.panelButton           = None
        self.panelList             = None
        self.panelData             = None
        self.listNameGame          = None
        self.listUserId            = None
        self.Button1               = None
        self.Button2               = None
        self.Button3               = None
        self.listNameGameInvisible = FALSE
        self.listUserIdInvisible   = FALSE

    def CreateWindow(self):
        self.window = Tk()
        self.window.geometry("1080x600")
        self.window.title("test")

    def CreatePanel(self):
        self.CreateWindow()
        self.panelButton = PanedWindow(self.window,width = 50, height = 30)
        self.panelList = PanedWindow(self.window, width = 50, height = 30)
        self.panelData = PanedWindow(self.window, width = 50, height = 30)

        self.panelButton.grid(column = 0, row = 0)
        self.panelList.grid(column = 1, row = 0)
        self.panelData.grid(column = 2, row = 0)

    def ShowListGame(self):
        if self.listUserIdInvisible:
            self.listUserIdInvisible = FALSE
            self.listUserId.lower()
        self.listNameGame.grid(column = 0, row = 0)
        self.listNameGameInvisible = TRUE
   
    def ShowListUserId(self):
        if self.listNameGameInvisible:
            self.listNameGameInvisible = FALSE
            self.listNameGame.lower()
        self.listUserId.grid(column = 0, row = 0)
        self.listUserIdInvisible = TRUE

    def ShowUserData(self,event):
        selectedAllUser = self.listUserId.curselection()
        selectedUser = ",".join([self.listUserId.get(i) for i in selectedAllUser])
        dataUser = dp.test.listUser[(dp.test.listUser['userId'] == int(selectedUser))]
        locationUser = np.where((dp.test.listUser['userId'] == int(selectedUser)))
        listSelectedUser = Listbox(self.panelData,width = 50, height = 30)
        for line in range(len(dataUser)):
            listSelectedUser.insert(END,dataUser['name'][locationUser[0][line]])
        listSelectedUser.grid(column = 0, row = 0)    

    def ShowUserHaveGame(self,event):
        selectedAllGame = self.listNameGame.curselection()
        selectedGame = ",".join([self.listNameGame.get(i) for i in selectedAllGame])
        dataUserHaveGame = dp.test.listUser[(dp.test.listUser['name'] == selectedGame)]
        locationGame = np.where((dp.test.listUser['name'] == selectedGame))
        listSelectedUser = Listbox(self.panelData,width = 50, height = 30)
        for line in range(len(dataUserHaveGame)):
            listSelectedUser.insert(END,dataUserHaveGame['userId'][locationGame[0][line]])
        listSelectedUser.grid(column = 0, row = 0)

    def CreateListData(self):
        self.CreatePanel()
        self.listUserId = Listbox(self.panelList,width = 50, height = 30)
        for line in range(dp.test.numberOfUser):
            self.listUserId.insert(END,dp.test.listUserId['userId'][line])

        self.listNameGame =  Listbox(self.panelList,width = 50, height = 30)
        for line in range(dp.test.numberOfGame):
            self.listNameGame.insert(END,dp.test.listNameGame['name'][line])

        self.listUserId.bind('<<ListboxSelect>>',self.ShowUserData)
        self.listNameGame.bind('<<ListboxSelect>>',self.ShowUserHaveGame)

    def CreateButton(self):
        self.CreateListData()
        self.button1 = Button(self.panelButton, text = "ListUser", bg='orange', fg='red', command = self.ShowListUserId)
        self.button1.pack(fill = BOTH, expand = 1)

        self.button3 = Button(self.panelButton, text = "ListGame", bg='orange', fg='red', command = self.ShowListGame)
        self.button3.pack(fill = BOTH, expand = 1)


if __name__ == "__main__":
    window = GUI()
    window.CreateButton()
    window.mainloop()