from tkinter import *

#PALCEHOLDERS
def doNothing():
    print("Do nothing...")
def restart():
    pass
def option1():
    pass
def option2():
    pass
def newGame():
    pass
def giveUp():
    pass
def getHint():
    pass
def option3():
    pass

#***** Main game window *****
class GameApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Detective")
        self.geometry("1000x800")

        #Setup menu
        self.create_menu()
        #Setup toolbar
        self.create_toolbar()
        #Setup Frames
        self.ai_frame = AIFrame(self)
        #Pass the ai_frame to UserFrame
        self.user_frame = UserFrame(self, self.ai_frame) 

        #Configure the grid layout for main frames
        self.grid_rowconfigure(1, weight=3)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.ai_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        self.user_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

    #Main Menu
    def create_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        subMenu = Menu(menu)
        menu.add_cascade(label="Game Options", menu=subMenu)
        subMenu.add_command(label="Option1", command=option1)
        subMenu.add_command(label="Option2", command=option2)
        subMenu.add_separator()
        subMenu.add_command(label="Exit", command=self.quit)

        editMenu = Menu(menu)
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Restart", command=restart)

    #Toolbar
    def create_toolbar(self):
        toolbar = Frame(self, bg="Grey")
        toolbar.grid(row=0, column=0, sticky="ew")
        insertButt = Button(toolbar, text="New Game", command=newGame)
        insertButt.grid(row=0, column=0, padx=2, pady=2)
        insertButt = Button(toolbar, text="Give Up", command=giveUp)
        insertButt.grid(row=0, column=1, padx=2, pady=2)
        insertButt = Button(toolbar, text="Get Hint", command=getHint)
        insertButt.grid(row=0, column=2, padx=2, pady=2)
        printButt = Button(toolbar, text="Option3", command=option3)
        printButt.grid(row=0, column=3, padx=2, pady=2)


#Defines a basic frame encapsulation
class BaseFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid(sticky="nsew", padx=10, pady=5)


#Build AI frame, inherits basic frame
class AIFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg='lightblue')
        
        #Scrollbar
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        
        #Text box
        self.text = Text(self, wrap=WORD, yscrollcommand=self.scrollbar.set, bg='#ADD8E6', state=DISABLED)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.text.yview)
        
        #Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        #Welcome message
        self.update_text("Game Master: Welcome, press 'New Game' to start!\n")


    def update_text(self, message):
        #Enable write
        self.text.config(state=NORMAL)
        self.text.insert(END, message)
        #Disable write
        self.text.config(state=DISABLED)

    #Text update encapsulation
    def gameMaster(self, message):
        self.update_text(f"Game Master: {message}\n")


#Build User frame, inherits basic frame
class UserFrame(BaseFrame):
    def __init__(self, parent, ai_frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        # Reference to AIFrame
        self.ai_frame = ai_frame
        
        #Scrollbar
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # Read-only input history
        self.text = Text(self, wrap=WORD, yscrollcommand=self.scrollbar.set, bg='#D0F0C0', state=DISABLED)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.text.yview)
        
        #User input entry, "Enter" bound
        self.entry = Entry(self)
        self.entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.entry.bind("<Return>", self.on_user_enter)

        #Grid
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    #Capture user input and append to the text history
    def capture_user_input(self):
        user_input = self.entry.get()

        if user_input.strip():
            #Enable write
            self.text.config(state=NORMAL)
            self.text.insert(END, f"User: {user_input}\n")
            #Disable write
            self.text.config(state=DISABLED)
            self.entry.delete(0, END)
        return user_input

    #"Enter" sends to ai frame 'gameMaster'
    def on_user_enter(self, event):
        user_input = self.capture_user_input()
        if user_input.strip():
            self.ai_frame.gameMaster(f"Processing input: {user_input}")
            #%%%%%%Add send info to ai for processing%%%%%%%


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
