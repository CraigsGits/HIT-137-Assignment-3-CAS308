from tkinter import *

def doNothing():
    print("Do nothing...")


#***** Main game window *****
class GameApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Text Detective")
        self.geometry("1000x800")

        # Setup menu
        self.create_menu()
        # Setup toolbar
        self.create_toolbar()
        # Setup Frames
        self.ai_frame = AIFrame(self)
        self.user_frame = UserFrame(self, self.ai_frame)  # Pass the ai_frame to UserFrame

        # Configure the grid layout for main frames
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.ai_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)
        self.user_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

    # Main Menu
    def create_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        subMenu = Menu(menu)
        menu.add_cascade(label="Game Options", menu=subMenu)
        subMenu.add_command(label="Option1", command=doNothing)
        subMenu.add_command(label="Option2", command=doNothing)
        subMenu.add_separator()
        subMenu.add_command(label="Exit", command=self.quit)

        editMenu = Menu(menu)
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Restart", command=doNothing)

    # Toolbar
    def create_toolbar(self):
        toolbar = Frame(self, bg="Grey")
        toolbar.grid(row=0, column=0, sticky="ew")
        insertButt = Button(toolbar, text="New Game", command=doNothing)
        insertButt.grid(row=0, column=0, padx=2, pady=2)
        insertButt = Button(toolbar, text="Give Up", command=doNothing)
        insertButt.grid(row=0, column=1, padx=2, pady=2)
        insertButt = Button(toolbar, text="Get Hint", command=doNothing)
        insertButt.grid(row=0, column=2, padx=2, pady=2)
        printButt = Button(toolbar, text="Print", command=doNothing)
        printButt.grid(row=0, column=3, padx=2, pady=2)


# Defines a basic frame encapsulation
class BaseFrame(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.grid(sticky="nsew", padx=10, pady=5)


# Build AI frame, inherits basic frame
class AIFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.config(bg='lightblue')
        
        # Scrollbar
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Text box
        self.text = Text(self, wrap=WORD, yscrollcommand=self.scrollbar.set, bg='#ADD8E6', state=DISABLED)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.text.yview)
        
        # Grid configuration for resizable text box
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Welcome message
        self.update_text("Game Master: Welcome, press 'New Game' to start!\n")


    def update_text(self, message):
        self.text.config(state=NORMAL)
        self.text.insert(END, message)
        self.text.config(state=DISABLED)
    #Text update encapsulation
    def gameMaster(self, message):
        self.update_text(f"Game Master: {message}\n")


# Build User frame, inherits basic frame
class UserFrame(BaseFrame):
    def __init__(self, parent, ai_frame, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        #
        self.ai_frame = ai_frame  # Reference to AIFrame for communication
        
        # Scrollbar
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        # Read-only input history
        self.text = Text(self, wrap=WORD, yscrollcommand=self.scrollbar.set, bg='#D0F0C0', state=DISABLED)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.text.yview)
        
        # User input entry
        self.entry = Entry(self)
        self.entry.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        # Grid configuration for resizable text box
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Bind "Enter" to input
        self.entry.bind("<Return>", self.on_user_enter)

    # Capture user input and append to the text history
    def capture_user_input(self):
        user_input = self.entry.get()

        if user_input.strip():
            self.text.config(state=NORMAL)
            self.text.insert(END, f"User: {user_input}\n")
            self.text.config(state=DISABLED)
            self.entry.delete(0, END)
        return user_input

    # "Enter" sends to ai frame for processing
    def on_user_enter(self, event):
        user_input = self.capture_user_input()
        if user_input.strip():
            self.ai_frame.gameMaster(f"Processing input: {user_input}")
            #%%%%%%Add send info to ai for processing%%%%%%%


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
