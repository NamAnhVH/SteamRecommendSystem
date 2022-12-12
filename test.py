from tkinter import *
from tkinter import ttk
import dataProcessing as dp
import numpy as np

window = Tk()
window.geometry("1000x600")
window.title("test")

panelLeft = PanedWindow(window,width = 50, height = 30)
panelLeft.grid(column = 0, row = 0)

panelMid = PanedWindow(window, width = 50, height = 30)
panelMid.grid(column = 1, row = 0)

panelRight = PanedWindow(window, width = 50, height = 30)
panelRight.grid(column = 2, row = 0)

listUserId = Listbox(panelMid,width = 100, height = 30)
listNameGame =  Listbox(panelMid,width = 100, height = 30)

# scrollbar = Scrollbar(window,width=30)
# scrollbar.grid(column = 1, row = 0)
def ShowListGame():
    for line in range(dp.test.numberOfGame):
        listNameGame.insert(END,dp.test.listNameGame['name'][line])

    listNameGame.grid(column = 0, row = 0)
    

def ShowListUserId():
    
    
    for line in range(dp.test.numberOfUser):
        listUserId.insert(END,dp.test.listUserId['userId'][line])

    listUserId.grid(column = 0, row = 0)

def ShowUserData(event):
    selectedAllUser = listUserId.curselection()
    selectedUser = ",".join([listUserId.get(i) for i in selectedAllUser])
    dataUser = dp.test.listUser[(dp.test.listUser['userId'] == int(selectedUser))]
    locationUser = np.where((dp.test.listUser['userId'] == int(selectedUser)))
    # print(selectedUser)
   
    listSelectedUser = Listbox(panelRight,width = 100, height = 50)
    for line in range(len(dataUser)):
        listSelectedUser.insert(END,dataUser['name'][locationUser[0][line]])
    listSelectedUser.grid(column = 0, row = 0)    

def ShowUserHaveGame(event):
    selectedAllGame = listNameGame.curselection()
    selectedGame = ",".join([listNameGame.get(i) for i in selectedAllGame])

    dataUserHaveGame = dp.test.listUser[(dp.test.listUser['name'] == selectedGame)]
    # print(dataUserHaveGame)
    # print(len(dataUserHaveGame))
    locationGame = np.where((dp.test.listUser['name'] == selectedGame))

    listSelectedUser = Listbox(panelRight,width = 100, height = 50)
    for line in range(len(dataUserHaveGame)):
        listSelectedUser.insert(END,dataUserHaveGame['userId'][locationGame[0][line]])
    listSelectedUser.grid(column = 0, row = 0)    

button1 = Button(panelLeft, text = "ListUser", bg='orange', fg='red', command = ShowListUserId)
button1.pack(fill = BOTH, expand = 1)

button2 = Button(panelLeft, text = "button2", bg='orange', fg='red')
button2.pack(fill = BOTH, expand = 1)

button3 = Button(panelLeft, text = "ListGame", bg='orange', fg='red', command = ShowListGame)
button3.pack(fill = BOTH, expand = 1)

listUserId.bind('<<ListboxSelect>>',ShowUserData)
listNameGame.bind('<<ListboxSelect>>',ShowUserHaveGame)

window.mainloop()
