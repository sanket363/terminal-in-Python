# terminal.py
import tkinter as tk
import subprocess

# Define color palette
class Colors:
    ROSEWATER = "#f2d5cf"
    FLAMINGO = "#eebebe"
    PINK = "#f4b8e4"
    MAUVE = "#ca9ee6"
    RED = "#e78284"
    MAROON = "#ea999c"
    PEACH = "#ef9f76"
    YELLOW = "#e5c890"
    GREEN = "#a6d189"
    TEAL = "#81c8be"
    SKY = "#99d1db"
    SAPPHIRE = "#85c1dc"
    BLUE = "#8caaee"
    LAVENDER = "#babbf1"
    TEXT = "#c6d0f5"
    SUBTEXT1 = "#b5bfe2"
    SUBTEXT0 = "#a5adce"
    BASE = "#303446"

class Terminal(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python Terminal")
        self.geometry("600x400")

        # Update text area colors
        self.text_area = tk.Text(self, bg=Colors.BASE, fg=Colors.TEXT, font=("Courier", 12))
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.text_area.bind("<Return>", self.execute_command)
        self.prompt()

    def prompt(self):
        self.text_area.insert(tk.END, f"{Colors.SAPPHIRE}> ")
        self.text_area.see(tk.END)

    def execute_command(self, event):
        # Get the full text and split into lines
        command_lines = self.text_area.get("1.0", tk.END).strip().split("\n")
        
        # Get the last command, stripping the prompt
        last_command = command_lines[-1]
        command = last_command.split(">")[-1].strip()  # Strip the prompt and whitespace

        self.text_area.insert(tk.END, "\n")  # Move to the next line

        if command.lower() in ["exit", "quit"]:
            self.destroy()  # Exit the terminal

        try:
            # Execute the command
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            self.text_area.insert(tk.END, output + "\n")
        except subprocess.CalledProcessError as e:
            self.text_area.insert(tk.END, f"Error: {e.output}\n")

        self.prompt()  # Prompt for the next command

if __name__ == "__main__":
    app = Terminal()
    app.mainloop()

