import tkinter as tk
import random
import json
import os

class Flashcard:
    """Class represents a Flashcard with a question and answer."""  
    def __init__(self, question, answer):
         # Encapsulation: attributes are private to this class
        self.__question = question
        self.__answer = answer

    def get_question(self):
        """Getter method for question."""
        return self.__question

    def get_answer(self):
        """Getter method for answer."""
        return self.__answer
    

    def __str__(self):
        """Returns Q and A string."""
        # polymorphism, can be overidden in EditableFlashcard
        return f"Q: {self.__question} | A: {self.__answer}"

class Taggable:
    """Class that adds tagging capability to flashcards."""
    def __init__(self, tags=""):
        self.tags = tags

    def add_tag(self, tag):
        """Add a tag to the tag string."""
        self.tags = tag

    def remove_tag(self, tag):
        """Remove a tag from the flashcard."""
        self.tag = ""

    def get_tag(self):
        """Return the tag."""
        return self.tags

# Inherits both Flashcard and Taggable classes (multiple inheritance)
class EditableFlashcard(Flashcard, Taggable):
    """Subclass of Flashcard and Taggable to allow editing and tagging."""
    
    def __init__(self, question, answer, tags):
        Flashcard.__init__(self, question, answer)
        Taggable.__init__(self, tags)

    def edit(self, new_question, new_answer,new_tags):
        # Method overiding
        """This method overrides the preset flashcard question and answer."""
        self._EditableFlashcard__question = new_question
        self._EditableFlashcard__answer = new_answer
        self.tags = new_tags

    def __str__(self):
        # Polymorphism
        """Overrides the Flashcard's __str__ method to include tags."""

        return f"Q: {self.get_question()} | A: {self.get_answer()} | Tags: {self.get_tag()}"

# Decorator for UI feedback
def provide_feedback(success_message):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            self.status_label.config(text=success_message)
            return result
        return wrapper
    return decorator

class FlashcardManager:
    """Class to manage a collection of flashcards."""
    
    def __init__(self, filename='flashcards.json'):
        # List to store flashcards
        self.flashcards = [] 
        # Filename for saving/loading
        self.filename = filename  
        # Load flashcards when manager is initialized
        self.load_flashcards()

    def add_flashcard(self, question, answer, tags):
        """Add a tagged flashcard to the collection."""
        flashcard = EditableFlashcard(question, answer, tags)
        self.flashcards.append(flashcard)
        self.save_flashcards()

    def edit_flashcard(self, index, new_question, new_answer, new_tags):
        """Edit a flashcard at a specified index."""
        if 0 <= index < len(self.flashcards):
            self.flashcards[index].edit(new_question, new_answer, new_tags) 
            self.save_flashcards()

    
    def delete_flashcard(self, index):
        """Delete a flashcard at a specified index."""
        if 0 <= index < len(self.flashcards):
            del self.flashcards[index]
            self.save_flashcards()

    def get_flashcard_list(self):
        """Return a list of flashcards as strings."""
        # Polymorphism 
        return [str(flashcard) for flashcard in self.flashcards]

    def get_random_flashcard(self):
        """Return a random flashcard."""
        if self.flashcards:
            return random.choice(self.flashcards)
        return None


    def save_flashcards(self):
        """Save flashcards to file."""
        with open(self.filename, 'w') as f:
            json.dump([{
                'question': fc.get_question(), 
                'answer': fc.get_answer(), 
                'tags': fc.get_tag()
            } for fc in self.flashcards], f)
    

    def load_flashcards(self):
        """Load flashcards from file."""
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.flashcards = [
                    EditableFlashcard(item['question'], item['answer'], item['tags']) 
                    for item in data
                ]

class FlashcardApp:
    """Main class for the Flashcard App."""
    
    def __init__(self, master):
        self.master = master
        self.master.title("Flashcard App")
        self.master.geometry("550x700")
        self.manager = FlashcardManager()
        self.current_flashcard = []
        self.previous_flashcards = []
        self.setup_main_menu()

        # Status label (persistent)
        self.status_label = tk.Label(self.master, text="", fg="red", bg="#F0F0F0", font=('Arial', 12))
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_main_menu(self):
        """Set up the main menu UI."""
        for widget in self.master.winfo_children():
            if widget != self.status_label:
                widget.destroy()

        self.menu_frame = tk.Frame(self.master, bg="#A7C6ED")
        self.menu_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        #Title:
        self.title_label = tk.Label(self.menu_frame, text="Flashcards", font=('Arial', 20), bg="#A7C6ED")
        self.title_label.pack(pady=20)
        # Main Menu Buttons
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
        # Category box (tags)
        self.tag_label = tk.Label(self.frame, text="Category:", bg="#A7C6ED", font=('Arial', 14))
        self.tag_label.pack(pady=5)
        self.tag_text = tk.Text(self.frame, width=50, height=2, font=('Arial', 12))
        self.tag_text.pack(pady=5)
        # Buttons!
        self.add_button = tk.Button(self.frame, text="Add Flashcard", command=self.add_flashcard, width=20, height=2)
        self.add_button.pack(pady=5)

        self.back_button = tk.Button(self.frame, text="Back to Menu", command=self.setup_main_menu, width=20, height=2)
        self.back_button.pack(pady=5)

    @provide_feedback("Flashcard added successfully!")
    def add_flashcard(self):
        """Submit a new flashcard."""
        # Get question, answer, and tags
        question = self.question_text.get("1.0", tk.END).strip()
        answer = self.answer_text.get("1.0", tk.END).strip()
        tags = self.tag_text.get("1.0", tk.END).strip()
        # Error handling
        if not question or not answer:
            self.status_label.config(text="Error: Question and Answer fields cannot be blank!")
            return
        # Add flashcard using manager
        self.manager.add_flashcard(question, answer, tags)
        self.question_text.delete("1.0", tk.END)
        self.answer_text.delete("1.0", tk.END)
        self.tag_text.delete("1.0", tk.END)

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
        # Listbox
        self.flashcard_listbox = tk.Listbox(self.flashcard_frame, width=50, height=20, font=('Arial', 12))
        self.flashcard_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.flashcard_frame, command=self.flashcard_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.flashcard_listbox.config(yscrollcommand=self.scrollbar.set)
        # Populate the listbox with flashcards
        self.update_flashcard_listbox()
        # Buttons!
        self.delete_button = tk.Button(self.edit_frame, text="Delete Flashcard", command=self.delete_flashcard, width=20, height=2)
        self.delete_button.pack(pady=10)

        self.edit_button = tk.Button(self.edit_frame, text="Edit Flashcard", command=self.edit_flashcard, width=20, height=2)
        self.edit_button.pack(pady=10)

        self.back_button = tk.Button(self.edit_frame, text="Back to Menu", command=self.setup_main_menu, width=20, height=2)
        self.back_button.pack(pady=10)

    def update_flashcard_listbox(self):
        """Update the listbox to show current flashcards."""
        self.flashcard_listbox.delete(0, tk.END)
        for index, flashcard in enumerate(self.manager.flashcards):
            # Display question, answer, and tags
            self.flashcard_listbox.insert(tk.END, f"Q{index + 1}: {flashcard.get_question()}| Ans: {flashcard.get_answer()} | Tags: {flashcard.get_tag()}")

    @provide_feedback("Flashcard deleted successfully!")
    def delete_flashcard(self):
        """Delete the selected flashcard."""
        selected_index = self.flashcard_listbox.curselection()
        if selected_index:
            self.manager.delete_flashcard(selected_index[0])
            self.update_flashcard_listbox() 

    def edit_flashcard(self):
        """Open the edit window for the selected flashcard."""
        # Get selected flashcard
        selected_index = self.flashcard_listbox.curselection()
        # Error handling
        if not selected_index:
            self.status_label.config(text="Select a flashcard to edit.")
            return
        self.selected_flashcard_index = selected_index[0]
        self.selected_flashcard = self.manager.flashcards[self.selected_flashcard_index]
        # Clear previous widgets for editing
        for widget in self.edit_frame.winfo_children():
            widget.destroy()
        # Edit question label and text box
        self.edit_question_label = tk.Label(self.edit_frame, text="Edit Question:", bg="#A7C6ED", font=('Arial', 14))
        self.edit_question_label.pack()
        self.edit_question_text = tk.Text(self.edit_frame, width=50, height=5, font=('Arial', 12))
        self.edit_question_text.pack()
        self.edit_question_text.insert("1.0", self.selected_flashcard.get_question())
        # Edit answer label and text box
        self.edit_answer_label = tk.Label(self.edit_frame, text="Edit Answer:", bg="#A7C6ED", font=('Arial', 14))
        self.edit_answer_label.pack()
        self.edit_answer_text = tk.Text(self.edit_frame, width=50, height=5, font=('Arial', 12))
        self.edit_answer_text.pack()
        self.edit_answer_text.insert("1.0", self.selected_flashcard.get_answer())
        # Edit tag label and text box
        self.edit_tag_label = tk.Label(self.edit_frame, text="Edit Category:", bg="#A7C6ED", font=('Arial', 14))
        self.edit_tag_label.pack()
        self.edit_tag_text = tk.Text(self.edit_frame, width=50, height=5, font=('Arial', 12))
        self.edit_tag_text.pack()
        self.edit_tag_text.insert("1.0", self.selected_flashcard.get_tag())
        # Buttons!
        self.save_button = tk.Button(self.edit_frame, text="Save Changes", command=self.save_changes, width=20, height=2)
        self.save_button.pack(pady=5)
        self.back_button = tk.Button(self.edit_frame, text="Back to Edit Menu", command=self.setup_edit_flashcards, width=20, height=2)
        self.back_button.pack(pady=5)

    @provide_feedback("Flashcard saved successfully!")
    def save_changes(self):
        """Save changes to the selected flashcard."""
        # Get new question and answer
        new_question = self.edit_question_text.get("1.0", tk.END).strip() 
        new_answer = self.edit_answer_text.get("1.0", tk.END).strip() 
        new_tags = self.edit_tag_text.get("1.0", tk.END).strip()
        # Error handling
        if not new_question or not new_answer:
            self.status_label.config(text="Error: Question and Answer fields cannot be blank!")
            return
        # Save changes and return to edit mode
        self.manager.edit_flashcard(self.selected_flashcard_index, new_question, new_answer, new_tags)
        self.setup_edit_flashcards()

    def test_mode(self):
        """Set up the test mode UI."""
        # Clear previous widgets except for the status label
        for widget in self.master.winfo_children():
            if widget != self.status_label:
                widget.destroy()

        self.test_frame = tk.Frame(self.master, bg="#A7C6ED")
        self.test_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        # Tag display
        self.tag_label = tk.Label(self.test_frame, text="", font=('Arial', 18), bg="#A7C6ED", wraplength=500)
        self.tag_label.pack(pady=20)
        # Question display
        self.question_label = tk.Label(self.test_frame, text="", font=('Arial', 18), bg="#A7C6ED", wraplength=500)
        self.question_label.pack(pady=20)
        # Answer display
        self.answer_label = tk.Label(self.test_frame, text="", font=('Arial', 18), bg="#A7C6ED", wraplength=500)
        self.answer_label.pack(pady=20)
        # Buttons!
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
            self.tag_label.config(text="")
            self.question_label.config(text="")
            self.answer_label.config(text="")
            return

        while True:
            flashcard = self.manager.get_random_flashcard()
            if flashcard not in self.previous_flashcards:
                # Record shown flashcards
                self.previous_flashcards.append(flashcard)  
                # Display tag
                self.tag_label.config(text="Category: " + flashcard.get_tag())
                # Display question
                self.question_label.config(text="Q:" + flashcard.get_question())  
                # Clear answer until 'Show Answer' is clicked
                self.answer_label.config(text="Ans: ?")
                break

    def show_answer(self):
        """Show the answer for the current flashcard."""
        # Error handling
        if self.question_label.cget("text") == "":
            self.status_label.config(text="No flashcard to show answer for.")
        # Show answer
        else:
            current_question = self.question_label.cget("text").replace("Q:", "").strip()
            current_flashcard = next((fc for fc in self.manager.flashcards if fc.get_question() == current_question), None)
            
            if current_flashcard:
                self.answer_label.config(text="Ans: " + current_flashcard.get_answer())
            else:
                self.status_label.config(text="Flashcard not found.")

# Execute
if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardApp(root)
    root.mainloop()



