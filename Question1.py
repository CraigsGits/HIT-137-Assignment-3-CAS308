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
    """
    GameApp is the main window for the application.
    It sets up the menu, toolbar, and main frames, organizing the overall layout.
    The AIFrame and UserFrame are managed here as well.
    """
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
        #AI grid
        self.ai_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
        #User grid
        self.user_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

    def create_menu(self):
        """
        Creates the main menu bar at the top of the window.
        """
        #Main Menu
        menu = Menu(self)
        self.config(menu=menu)
        #Sub menu
        subMenu = Menu(menu)
        menu.add_cascade(label="Game Options", menu=subMenu)
        subMenu.add_command(label="Option1", command=option1)
        subMenu.add_command(label="Option2", command=option2)
        subMenu.add_separator()
        subMenu.add_command(label="Exit", command=self.quit)
        #Edit menu
        editMenu = Menu(menu)
        menu.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Restart", command=restart)

    def create_toolbar(self):
        """
        Creates the toolbar with buttons for user actions.
        """
        toolbar = Frame(self, bg="Grey")
        toolbar.grid(row=0, column=0, sticky="ew")
        #Button setup
        insertButt = Button(toolbar, text="New Game", command=newGame)
        insertButt.grid(row=0, column=0, padx=2, pady=2)
        insertButt = Button(toolbar, text="Give Up", command=giveUp)
        insertButt.grid(row=0, column=1, padx=2, pady=2)
        insertButt = Button(toolbar, text="Get Hint", command=getHint)
        insertButt.grid(row=0, column=2, padx=2, pady=2)
        insertButt = Button(toolbar, text="Option3", command=option3)
        insertButt.grid(row=0, column=3, padx=2, pady=2)




#Build AI frame
class AIFrame(Frame):
    """
    AIFrame displays the AI's responses.
    Contains a text box with a scroll bar to navigate through the text history.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.grid(sticky="nsew", padx=10, pady=5)
        
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
        self.gameMaster("Welcome, press 'New Game' to start!\n")


    def gameMaster(self, message):
        """
        Adds a message from the 'Game Master' to the text box.
        """
        self.text.config(state=NORMAL)
        self.text.insert(END, f"Game Master: {message}\n")
        self.text.config(state=DISABLED)
        self.text.yview(END)

# Build User frame
class UserFrame(Frame):
    """
    UserFrame allows the user to interact with the game.
    It displays user inputs in the form of text history and provides an entry field for the user input.
    """
    def __init__(self, parent, ai_frame):
        super().__init__(parent)
        self.grid(sticky="nsew", padx=10, pady=5)

        # Reference to AIFrame
        self.ai_frame = ai_frame
        # Scrollbar
        self.scrollbar = Scrollbar(self)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        # Read-only input history
        self.text = Text(self, wrap=WORD, yscrollcommand=self.scrollbar.set, bg='#D0F0C0', state=DISABLED)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.text.yview)
        # Create a frame to hold the label and entry
        input_frame = Frame(self)
        input_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 0))  # Adjust padding here
        # Label to indicate input field
        self.input_label = Label(input_frame, text="User:", font=("Helvetica", 12))
        self.input_label.grid(row=0, column=0, sticky="w", padx=10)
        # User input entry, "Enter" bound
        self.entry = Entry(input_frame, bg='#F5DEB3', fg='#000000')
        self.entry.grid(row=0, column=1, sticky="ew", padx=10, pady=(5, 0))  # Column 1 for entry to align with label
        self.entry.bind("<Return>", self.on_user_enter)
        # Grid
        input_frame.grid_columnconfigure(1, weight=1)  # Allow entry to expand
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


    #Capture user input and append to the text history
    def capture_user_input(self):
        """
        Captures the user input from the Entry widget and displays it in the text history.
        """
        user_input = self.entry.get()

        if user_input.strip():
            #Enable write
            self.text.config(state=NORMAL)
            self.text.insert(END, f"User: {user_input}\n")
            #Disable write
            self.text.config(state=DISABLED)
            self.entry.delete(0, END)
            self.text.yview(END)

        return user_input

    #"Enter" sends to ai frame 'gameMaster'
    def on_user_enter(self, event):
        """
        Handles the 'Enter' key press by capturing user input and sending it to the AIFrame for processing.
        """
        user_input = self.capture_user_input()
    
        if user_input.strip():
            self.ai_frame.gameMaster(f"Processing input: {user_input}")
            #%%%%%%Add send info to ai for processing%%%%%%%


if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
