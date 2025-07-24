import tkinter as tk
from tkinter import messagebox, ttk
import math

class AdvancedCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Calculator")
        self.root.geometry("400x600")

        # Store calculation history
        self.history = []
        # Memory variable
        self.memory = 0

        # GUI Elements
        # Display
        self.display_var = tk.StringVar()
        self.display = tk.Entry(root, textvariable=self.display_var, font=("Arial", 20), bd=5, relief="sunken", justify="right")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="we")

        # Buttons layout
        button_layout = [
            ('C', 1, 0), ('(', 1, 1), (')', 1, 2), ('/', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('*', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('√', 5, 3),
            ('sin', 6, 0), ('cos', 6, 1), ('tan', 6, 2), ('log', 6, 3),
            ('^', 7, 0), ('M+', 7, 1), ('MR', 7, 2), ('MC', 7, 3),
            ('History', 8, 0, 2), ('Clear History', 8, 2, 2)
        ]

        # Create buttons
        for button in button_layout:
            text, row, col = button[0], button[1], button[2]
            colspan = button[3] if len(button) > 3 else 1
            cmd = lambda x=text: self.button_click(x)
            tk.Button(root, text=text, font=("Arial", 14), command=cmd, width=5).grid(row=row, column=col, columnspan=colspan, padx=5, pady=5, sticky="we")

        # Configure grid weights
        for i in range(9):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.root.grid_columnconfigure(i, weight=1)

    def button_click(self, char):
        if char == 'C':
            self.display_var.set("")
        elif char == '=':
            try:
                # Replace ^ with ** for power operation
                expression = self.display_var.get().replace('^', '**')
                # Evaluate with math functions
                result = eval(expression, {"__builtins__": None}, {
                    "sin": math.sin, "cos": math.cos, "tan": math.tan,
                    "log": math.log10, "sqrt": math.sqrt
                })
                self.display_var.set(str(result))
                self.history.append(f"{expression} = {result}")
            except ZeroDivisionError:
                messagebox.showerror("Error", "Division by zero!")
                self.display_var.set("")
            except Exception as e:
                messagebox.showerror("Error", f"Invalid expression: {str(e)}")
                self.display_var.set("")
        elif char == '√':
            self.display_var.set(self.display_var.get() + "sqrt(")
        elif char in ('sin', 'cos', 'tan', 'log'):
            self.display_var.set(self.display_var.get() + f"{char}(")
        elif char == 'M+':
            try:
                self.memory += float(self.display_var.get())
            except:
                messagebox.showerror("Error", "Invalid value for memory!")
        elif char == 'MR':
            self.display_var.set(str(self.memory))
        elif char == 'MC':
            self.memory = 0
        elif char == 'History':
            self.show_history()
        elif char == 'Clear History':
            self.history = []
            messagebox.showinfo("Success", "History cleared!")
        else:
            self.display_var.set(self.display_var.get() + char)

    def show_history(self):
        # Create a new window for history
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("400x300")

        # Create Listbox to display history
        listbox = tk.Listbox(history_window, font=("Arial", 12))
        listbox.pack(fill="both", expand=True, padx=10, pady=10)

        # Populate history
        for entry in self.history:
            listbox.insert(tk.END, entry)

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCalculatorApp(root)
    root.mainloop()
