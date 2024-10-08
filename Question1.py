

from tkinter import *



def doNothing():
    print("Do nothing...")

def leftClick(event):
    print("Left")

def rightClick(event):
    print("Right")

def newScenario():
    pass

def giveUp():
    pass

def getHint():
    pass

root = Tk()

#***** Main Menu *****
menu = Menu(root)
root.config(menu = menu)

subMenu = Menu(menu)
menu.add_cascade(label = "Game Options", menu = subMenu)
subMenu.add_command(label = "New Scenario", command = newScenario)
subMenu.add_command(label = "Give Up ", command = doNothing)
subMenu.add_separator()
subMenu.add_command(label = "Exit", command = root.quit)

editMenu = Menu(menu)
menu.add_cascade(label = "Edit", menu = editMenu)
editMenu.add_command(label = "Redo", command = doNothing)

#***** Toolbar *****
toolbar = Frame(root, bg = "Grey")

insertButt = Button(toolbar, text = "Get Hint", command = getHint)
insertButt.pack(side = LEFT, padx = 2, pady = 2)
printButt = Button(toolbar, text = "Print", command = doNothing)
printButt.pack(side = LEFT, padx = 2, pady = 2)

toolbar.pack(side = TOP, fill = X)

#***** Screen *****
#AI Output Frame (Top)
frameAI = Frame(root, width = 300, height = 300, bg='lightblue')
frameAI.bind("<Button-1>", leftClick)
frameAI.pack(side=TOP, fill=BOTH, padx=10, pady=(10, 5))

#Separator Frame
separator = Frame(root, height=2, bg="black", border= 1, borderwidth= 2)
separator.pack(fill=X, padx=10, pady=5)

#User Input Frame (Bottom)
frameUser = Frame(root, width = 300, height = 200, bg='lightgreen')
frameUser.bind("<Button-3>", rightClick)
frameUser.pack(side=TOP, fill=BOTH, padx=10, pady=(5, 10))


#History Frame (Right)
frameHistory = Frame(root, width=200, bg="lightgrey")
frameHistory.pack(side=RIGHT, fill=Y, padx=10, pady=10)

# Add a scrollable Text widget to display the history
scrollbar = Scrollbar(frameHistory)
scrollbar.pack(side=RIGHT, fill=Y)

historyText = Text(frameHistory, wrap=WORD, yscrollcommand=scrollbar.set)
historyText.pack(side=LEFT, fill=BOTH, expand=True)

# Configure the scrollbar to scroll the Text widget
scrollbar.config(command=historyText.yview)


#***** Status Bar *****
status = Label(root, text ="Preparing to do nothing...", bd = 1, relief = SUNKEN, anchor = W)
status.pack(side = BOTTOM, fill = X)

root.mainloop()
