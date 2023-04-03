import tkinter as tk
import re
class Task:
    def __init__(self, name, time, prev):
        self.name = name
        self.time = time
        self.prev = prev

# Create the main window
root = tk.Tk()
root.title("CPM GUI")

# Create the labels and entries
name_label = tk.Label(root, text="Name:")
name_label.grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(root, validate="key")
name_entry.config(validatecommand=(name_entry.register(lambda text: text.isupper() or text == ''), '%P'))
name_entry.grid(row=0, column=1, padx=5, pady=5)

time_label = tk.Label(root, text="Time:")
time_label.grid(row=1, column=0, padx=5, pady=5)
time_entry = tk.Entry(root, validate="key")
time_entry.config(validatecommand=(time_entry.register(lambda text: text.isdigit() or text == ''), '%P'))
time_entry.grid(row=1, column=1, padx=5, pady=5)

prev_label = tk.Label(root, text="Previous tasks (comma-separated):")
prev_label.grid(row=2, column=0, padx=5, pady=5)
prev_entry = tk.Entry(root)
prev_entry.config(validate="key")
prev_entry.config(validatecommand=(prev_entry.register(lambda text: re.match("^[A-Za-z,-]*$", text) is not None), '%P'))
prev_entry.grid(row=2, column=1, padx=5, pady=5)

# Create the listbox
task_list = tk.Listbox(root)
task_list.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

# Function to add a task to the listbox
def add_task():
    name = name_entry.get()
    time = time_entry.get()
    prev = prev_entry.get()
    task_list.insert(tk.END, f"{name} | {time} | {prev}")
    name_entry.delete(0, tk.END)
    time_entry.delete(0, tk.END)
    prev_entry.delete(0, tk.END)

# Create the "Add Task" button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=4, column=0, padx=5, pady=5)

# Create the "Run CPM" button
run_button = tk.Button(root, text="Run CPM")
run_button.grid(row=4, column=1, padx=5, pady=5)

def get_tasks():
    tasks = []
    for i in range(task_list.size()):
        task_str = task_list.get(i)
        name, time, prev = task_str.split(" | ")
        tasks.append(Task(name, time, prev))
    return tasks

# Start the GUI main loop
root.mainloop()
