#Software Development Module 8 Final Submission
#Author: Jamius Smith
#Purpose: A simple note taking app that allows the user to add and delete notes.

import tkinter as tk
from tkinter import simpledialog, messagebox, Listbox, Scrollbar

# Class to create Tooltips on hover over widgets
class ToolTip(object):
    def __init__(self, widget, text):  # Constructor for the tooltip
        self.widget = widget        # The widget over which the tooltip is displayed
        self.text = text            # The text displayed in the tooltip
        self.tooltip_window = None  # Placeholder for the tooltip window (initialized as None)

    # Function to display the tooltip when mouse hovers over the widget
    def display_tooltip(self, event):
        # Get the widget's x, y coordinates
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25

        # Create the tooltip as a top-level window
        self.tooltip_window = tk.Toplevel(self.widget)
        self.tooltip_window.wm_overrideredirect(True)  # Removes the window border
        self.tooltip_window.wm_geometry(f"+{x}+{y}")   # Position of the tooltip
        label = tk.Label(self.tooltip_window, text=self.text, background="yellow", relief=tk.SOLID, borderwidth=1)
        label.pack()

    # Function to hide the tooltip when mouse leaves the widget
    def hide_tooltip(self, event):
        if self.tooltip_window:
            self.tooltip_window.destroy()  # Destroy the tooltip window
            self.tooltip_window = None     # Reset the tooltip window

# Global variable to store notes
notes = []

# Function to update the notes displayed in the listbox
def update_display():
    """Update the listbox with current notes."""
    listbox.delete(0, tk.END)
    for note in notes:
        listbox.insert(tk.END, note)

# Callback function when 'Add Note' button is pressed
def add_note():
    """Callback function to add a note."""
    note = simpledialog.askstring("Input", "Enter your note:")
    # Check if note is not empty and less than 100 characters
    if note and len(note) <= 100:
        notes.append(note)
        update_display()
    elif not note:
        messagebox.showwarning("Warning", "Note can't be empty!")
    else:
        messagebox.showwarning("Warning", "Note too long! Max 100 characters allowed.")

# Callback function when 'Delete Note' button is pressed
def delete_note():
    """Callback function to delete a selected note."""
    try:
        index = listbox.curselection()[0]
        del notes[index]
        update_display()
    except:
        messagebox.showwarning("Warning", "Select a note to delete!")

# Function to display the content of a clicked note in a new window
def show_note():
    """Display the content of a clicked note in a new window."""
    try:
        index = listbox.curselection()[0]
        selected_note = notes[index]

        new_window = tk.Toplevel(root)
        new_window.title("Note Content")

        lbl_note_content = tk.Label(new_window, text=selected_note)
        lbl_note_content.pack(padx=20, pady=20)

    except:
        messagebox.showwarning("Warning", "Select a note to view!")

# The main application window
def main_window():
    """Main Application Window."""
    global listbox

    root.title("Simple Note Keeper")

    # Create and pack labels
    lbl_title = tk.Label(root, text="Simple Note Keeper", font=('Arial', 16))
    lbl_title.pack(pady=10)

    lbl_instruction = tk.Label(root, text="Select a note to delete it or add a new one:", font=('Arial', 12))
    lbl_instruction.pack(pady=10)

    # Listbox with Scrollbar to display notes
    scrollbar = Scrollbar(root)
    scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

    listbox = Listbox(root, yscrollcommand=scrollbar.set)
    listbox.pack(pady=15, padx=15, fill=tk.BOTH, expand=True)
    scrollbar.config(command=listbox.yview)

    # Bind double click event to listbox to show note content
    listbox.bind('<Double-Button-1>', lambda event: show_note())

    # Images for buttons (Ensure images 'note.png' and 'delete.png' are present)
    img_note = tk.PhotoImage(file="note.png")
    img_delete = tk.PhotoImage(file="delete.png")

    # Buttons with images and corresponding actions
    btn_add = tk.Button(root, text="Add Note", command=add_note, image=img_note, compound=tk.LEFT)
    btn_add.pack(pady=5)

    btn_delete = tk.Button(root, text="Delete Note", command=delete_note, image=img_delete, compound=tk.LEFT)
    btn_delete.pack(pady=5)

    btn_exit = tk.Button(root, text="Exit", command=root.quit)
    btn_exit.pack(pady=5)

    # Tooltips for the buttons
    tooltip_add = ToolTip(btn_add, "Click to add a note")
    btn_add.bind("<Enter>", tooltip_add.display_tooltip)
    btn_add.bind("<Leave>", tooltip_add.hide_tooltip)

    tooltip_delete = ToolTip(btn_delete, "Click to delete a selected note")
    btn_delete.bind("<Enter>", tooltip_delete.display_tooltip)
    btn_delete.bind("<Leave>", tooltip_delete.hide_tooltip)

    tooltip_exit = ToolTip(btn_exit, "Click to exit the application")
    btn_exit.bind("<Enter>", tooltip_exit.display_tooltip)
    btn_exit.bind("<Leave>", tooltip_exit.hide_tooltip)

    root.mainloop()

# Entry point of the application
if __name__ == "__main__":
    root = tk.Tk()  # Create the root window
    main_window()   # Start the main application window
