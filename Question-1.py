import tkinter as tk
import random
import json
import os

# Base class for flashcards
class Flashcard:
    """Class represents a Flashcard with a question and answer."""  
    def __init__(self, question, answer):
         # Encapsulation: attributes are private to this class
        self.question = question
        self.answer = answer

    def __str__(self):
        """String representation of the flashcard."""
        # polymorphism
        return f"Q: {self.__question} | A: {self.__answer}"

# Inherits Flashcard class and extends functionality
class EditableFlashcard(Flashcard):
    """Subclass of Flashcard to allow editing."""
    def edit(self, new_question, new_answer):
        """Edit the question and answer of the flashcard."""
        # Method overriding
        self.question = new_question
        self.answer = new_answer

# Decorator for validating inputs
def validate_input(func):
    def wrapper(self, *args, **kwargs):
        if not args[0] or not args[1]:
            # Update status label
            self.status_label.config(text="Both question and answer must be provided.")  
            return
        return func(self, *args, **kwargs)
    return wrapper

class FlashcardManager:
    """Class to manage a collection of flashcards."""
    def __init__(self, filename='flashcards.json'):
        # List to store flashcards
        self.flashcards = [] 
        # Filename for saving/loading 
        self.filename = filename  
        # Load flashcards when manager is initialized
        self.load_flashcards()

    def add_flashcard(self, question, answer):
        """Add a flashcard to the collection."""
        flashcard = EditableFlashcard(question, answer)
        self.flashcards.append(flashcard)  
        self.save_flashcards()  

    def edit_flashcard(self, index, new_question, new_answer):
        """Edit a flashcard at a specified index."""
        if 0 <= index < len(self.flashcards):
            self.flashcards[index].edit(new_question, new_answer) 
            self.save_flashcards()

    def delete_flashcard(self, index):
        """Delete a flashcard at a specified index."""
        if 0 <= index < len(self.flashcards):
            del self.flashcards[index]
            self.save_flashcards()  

    def get_flashcard_list(self):
        """Return a list of flashcards as strings."""
        # Polymorphism, uses __str__ method
        return [str(flashcard) for flashcard in self.flashcards]

    def get_random_flashcard(self):
        """Return a random flashcard."""
        if self.flashcards:
            return random.choice(self.flashcards)
        return None

    def save_flashcards(self):
        """Saves flashcards to file"""
        with open(self.filename, 'w') as f:
            json.dump([{'question': fc.question, 'answer': fc.answer} for fc in self.flashcards], f)

    def load_flashcards(self):
        """Loads flashcards from file"""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.flashcards = [EditableFlashcard(item['question'], item['answer']) for item in data]

class FlashcardApp:
    """Main class for the Flashcard App."""

    def __init__(self, master):
        self.master = master
        self.master.title("Flashcard App")
        self.master.geometry("550x700")
        # Create a FlashcardManager instance
        self.manager = FlashcardManager()
        # Current flashcard to display
        self.current_flashcard = None 
        # For storing previously shown flashcards 
        self.previous_flashcards = []
        # Set up the main menu
        self.setup_main_menu()

        # Create a persistent status label
        self.status_label = tk.Label(self.master, text="", fg="red", bg="#A7C6ED", font=('Arial', 12))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_main_menu(self):
        """Set up the main menu UI."""

        # Clear previous widgets except for the status label
        for widget in self.master.winfo_children():
            if widget != self.status_label:
                widget.destroy()

        # Main menu frame
        self.menu_frame = tk.Frame(self.master, bg="#A7C6ED")
        self.menu_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        # Title
        self.title_label = tk.Label(self.menu_frame, text="Flashcards", font=('Arial', 20), bg="#A7C6ED")
        self.title_label.pack(pady=20)
        # Buttons
        self.create_flashcard_button = tk.Button(self.menu_frame, text="Create Flashcard", command=self.setup_create_flashcard, width=20, height=2)
        self.create_flashcard_button.pack(pady=10)

        self.edit_flashcard_button = tk.Button(self.menu_frame, text="Edit Flashcards", command=self.setup_edit_flashcards, width=20, height=2)
        self.edit_flashcard_button.pack(pady=10)

        self.test_button = tk.Button(self.menu_frame, text="Test Me", command=self.test_mode, width=20, height=2)
        self.test_button.pack(pady=10)

        self.exit_button = tk.Button(self.menu_frame, text="Exit", command=self.master.quit, width=20, height=2)
        self.exit_button.pack(pady=10)

    def setup_create_flashcard(self):
        """Open the create flashcard window."""
        
        # Clear previous widgets except for the status label
        for widget in self.master.winfo_children():
            if widget != self.status_label:
                widget.destroy()

        self.frame = tk.Frame(self.master, bg="#A7C6ED") 
        self.frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Question box
        self.question_label = tk.Label(self.frame, text="Question:", bg="#A7C6ED", font=('Arial', 14))
        self.question_label.pack(pady=5)
        self.question_text = tk.Text(self.frame, width=50, height=5, font=('Arial', 12))
        self.question_text.pack(pady=5)
        # Answer box
        self.answer_label = tk.Label(self.frame, text="Answer:", bg="#A7C6ED", font=('Arial', 14))
        self.answer_label.pack(pady=5)
        self.answer_text = tk.Text(self.frame, width=50, height=5, font=('Arial', 12))
        self.answer_text.pack(pady=5)

        #Buttons
        self.add_button = tk.Button(self.frame, text="Add Flashcard", command=self.add_flashcard, width=20, height=2)
        self.add_button.pack(pady=5)

        self.back_button = tk.Button(self.frame, text="Back to Menu", command=self.setup_main_menu, width=20, height=2)
        self.back_button.pack(pady=5)

    def add_flashcard(self):
        """Submit a new flashcard."""
        # Get question and answer
        question = self.question_text.get("1.0", tk.END).strip()
        answer = self.answer_text.get("1.0", tk.END).strip()

        # Error handling
        if not question or not answer:
            self.status_label.config(text="Both question and answer must be provided.")
            return
        
        # Add flashcard using manager
        self.manager.add_flashcard(question, answer)
        self.question_text.delete("1.0", tk.END) 
        self.answer_text.delete("1.0", tk.END)  
        self.status_label.config(text="Flashcard added!")

    def setup_edit_flashcards(self):
        """Open the edit flashcard window."""
        # Clear previous widgets except for the status label
        for widget in self.master.winfo_children():
            if widget != self.status_label:
                widget.destroy()

        # Setup display
        self.edit_frame = tk.Frame(self.master, bg="#A7C6ED")
        self.edit_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        self.edit_title_label = tk.Label(self.edit_frame, text="Edit Flashcards", font=('Arial', 14), bg="#A7C6ED")
        self.edit_title_label.pack(pady=5)

        self.flashcard_frame = tk.Frame(self.edit_frame)
        self.flashcard_frame.pack(pady=5)

        self.flashcard_listbox = tk.Listbox(self.flashcard_frame, width=50, height=10, font=('Arial', 12))
        self.flashcard_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.flashcard_frame, command=self.flashcard_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.flashcard_listbox.config(yscrollcommand=self.scrollbar.set)

        # Populate the listbox with flashcards
        self.update_flashcard_listbox()

        # Buttons
        self.delete_button = tk.Button(self.edit_frame, text="Delete Flashcard", command=self.delete_flashcard, width=20, height=2)
        self.delete_button.pack(pady=10)

        self.edit_button = tk.Button(self.edit_frame, text="Edit Flashcard", command=self.edit_flashcard, width=20, height=2)
        self.edit_button.pack(pady=10)

        self.back_button = tk.Button(self.edit_frame, text="Back to Menu", command=self.setup_main_menu, width=20, height=2)
        self.back_button.pack(pady=10)

    def update_flashcard_listbox(self):
        """Clear and update the flashcard listbox."""
        self.flashcard_listbox.delete(0, tk.END)
        for index, flashcard in enumerate(self.manager.flashcards):
            self.flashcard_listbox.insert(tk.END, f"Q{index + 1}: '{flashcard.question}' Ans: '{flashcard.answer}'")  

    def delete_flashcard(self):
        """Delete the selected flashcard."""
        selected_index = self.flashcard_listbox.curselection()
        if selected_index:
            self.manager.delete_flashcard(selected_index[0])
            self.update_flashcard_listbox() 
            self.status_label.config(text="Flashcard deleted.")

    def edit_flashcard(self):
        """Open the edit window for the selected flashcard."""

        # Get selected index
        selected_index = self.flashcard_listbox.curselection()
        # Update status label
        if not selected_index:
            self.status_label.config(text="Select a flashcard to edit.")
            return
        # Store selected index
        self.selected_flashcard_index = selected_index[0]
        # Get selected flashcard
        self.selected_flashcard = self.manager.flashcards[self.selected_flashcard_index]

        # Clear previous widgets for editing
        for widget in self.edit_frame.winfo_children():
            widget.destroy()
        # Label
        self.edit_question_label = tk.Label(self.edit_frame, text="Edit Question:", bg="#A7C6ED", font=('Arial', 14))
        self.edit_question_label.pack()
         # Insert current question
        self.edit_question_text = tk.Text(self.edit_frame, width=50, height=5, font=('Arial', 12))
        self.edit_question_text.insert(tk.END, self.selected_flashcard.question) 
        self.edit_question_text.pack()
        # Label
        self.edit_answer_label = tk.Label(self.edit_frame, text="Edit Answer:", bg="#A7C6ED", font=('Arial', 14))
        self.edit_answer_label.pack()
        # Insert current answer
        self.edit_answer_text = tk.Text(self.edit_frame, width=50, height=5, font=('Arial', 12))
        self.edit_answer_text.insert(tk.END, self.selected_flashcard.answer)  
        self.edit_answer_text.pack()

        # Buttons
        self.save_button = tk.Button(self.edit_frame, text="Save Changes", command=self.save_changes, width=20, height=2)
        self.save_button.pack(pady=10)

        self.back_button = tk.Button(self.edit_frame, text="Back to List", command=self.setup_edit_flashcards, width=20, height=2)
        self.back_button.pack(pady=10)

    def save_changes(self):
        """Save changes to the selected flashcard."""
        # Get new question and answer
        new_question = self.edit_question_text.get("1.0", tk.END).strip() 
        new_answer = self.edit_answer_text.get("1.0", tk.END).strip() 
        # Error handling
        if not new_question or not new_answer:
            self.status_label = tk.Label(self.edit_frame, text="", fg="red", bg="#A7C6ED", font=('Arial', 12))
            self.status_label.pack()
            return
        # Save changes and return to edit mode
        self.manager.edit_flashcard(self.selected_flashcard_index, new_question, new_answer)
        self.setup_edit_flashcards()

    def test_mode(self):
        """Set up the test mode UI."""
        # Clear previous widgets except for the status label
        for widget in self.master.winfo_children():
            if widget != self.status_label:
                widget.destroy()

        self.test_frame = tk.Frame(self.master, bg="#A7C6ED")
        self.test_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Question display
        self.question_label = tk.Label(self.test_frame, text="", font=('Arial', 18), bg="#A7C6ED", wraplength=500)
        self.question_label.pack(pady=20)

        # Answer display
        self.answer_label = tk.Label(self.test_frame, text="", font=('Arial', 18), bg="#A7C6ED", wraplength=500)
        self.answer_label.pack(pady=20)

        # Buttons
        self.show_answer_button = tk.Button(self.test_frame, text="Show Answer", command=self.show_answer, width=20, height=2)
        self.show_answer_button.pack(pady=10)

        self.next_button = tk.Button(self.test_frame, text="Next Card", command=self.next_flashcard, width=20, height=2)
        self.next_button.pack(pady=10)

        self.back_button = tk.Button(self.test_frame, text="Back to Menu", command=self.setup_main_menu, width=20, height=2)
        self.back_button.pack(pady=10)

        # Reset & load first flashcard
        self.previous_flashcards = []
        self.next_flashcard()

    def next_flashcard(self):
        """Show a random flashcard that has not yet been displayed."""
        # Error handling
        if len(self.previous_flashcards) == len(self.manager.flashcards):
            self.status_label.config(text="No more flashcards available.")
            self.question_label.config(text="")
            self.answer_label.config(text="")
            return
        
        while True:
            flashcard = self.manager.get_random_flashcard()
            if flashcard not in self.previous_flashcards:
                # Record shown flashcards
                self.previous_flashcards.append(flashcard)  
                # Display question
                self.question_label.config(text=flashcard.question)  
                # Clear answer until 'Show Answer' is clicked
                self.answer_label.config(text="")
                break

    def show_answer(self):
        """Show the answer for the current flashcard."""
        # Error handling
        if self.question_label.cget("text") == "":
            self.status_label.config(text="No flashcard to show answer for.")
        # Show answer
        else:
            current_flashcard = next((fc for fc in self.manager.flashcards if fc.question == self.question_label.cget("text")), None)
            if current_flashcard:
                self.answer_label.config(text=current_flashcard.answer)

# Execute
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()



