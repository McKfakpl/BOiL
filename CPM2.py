import tkinter as tk
import re
import networkx as nx
import matplotlib.pyplot as plt
from tkinter import ttk
from tkinter import *
class Task:
    def __init__(self, name, time, prev):
        self.name = name
        self.time = time
        self.prev = prev.split(',') if prev != '-' else []

# Create the main window
root = tk.Tk()
root.title("CPM GUI")
s = ttk.Style()
s.theme_use("clam")
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

prev_label = tk.Label(root, text="Previous tasks (comma-separated)  Example:(A,B,C):")
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

def cpm(taski, source, sink):
    # Step 1: Build Graph
    graph = nx.DiGraph()
    for task in taski:
        graph.add_node(task.name, task=task)
        for prev in task.prev:
            graph.add_edge(prev, task.name, weight = task.time)

    # Step 2: Topological Sort
    nodes = list(nx.topological_sort(graph))

    # Step 3: Forward Pass
    earliest_start_time = {node: 0 for node in nodes}
    for node in nodes:
        task = graph.nodes[node]['task']
        for predecessor in graph.predecessors(node):
            earliest_start_time[node] = max(earliest_start_time[node], earliest_start_time[predecessor] + graph.edges[predecessor, node]['weight'])
    
    # Step 4: Backward Pass
    latest_completion_time = {node: earliest_start_time[sink] for node in nodes}
    for node in reversed(nodes):
        task = graph.nodes[node]['task']
        for successor in graph.successors(node):
            latest_completion_time[node] = min(latest_completion_time[node], latest_completion_time[successor] - graph.edges[node, successor]['weight'])

    # Step 5: Calculate Critical Path
    critical_path = []
    for node in nodes:
        task = graph.nodes[node]['task']
        if earliest_start_time[node] == latest_completion_time[node]:
            critical_path.append(node)
            
    return earliest_start_time, latest_completion_time, critical_path, nodes

def show_task_times(et,lt,tasks, nodes, cp):
    window = tk.Toplevel()
    window.title("Task Times")

    # Create a listbox to display the task data
    tree = ttk.Treeview(window, column=("c1", "c2", "c3", "c4"), show='headings', height=6)

    tree.column("# 1", anchor=CENTER)
    tree.heading("# 1", text="Name")
    tree.column("# 2", anchor=CENTER)
    tree.heading("# 2", text="Longest Time")
    tree.column("# 3", anchor=CENTER)
    tree.heading("# 3", text="Earliest Time")
    tree.column("# 4", anchor=CENTER)
    tree.heading("# 4", text="Reserve")
    
    sum = et[nodes[len(tasks) -1 ] ]
    sum += tasks[0].time

    label = tk.Label(window, text="Critical Path Time: " + str(sum))
    label.pack()
 
    # Add task data to the listbox
    for i in range(len(tasks)):
        name = tasks[i].name
        if(i == 0):
            earliest_time = 0
            longest_time = 0
            reserve = 0
        else:
            earliest_time = et[nodes[i]] + tasks[0].time
            print(earliest_time)
            longest_time = lt[nodes[i]] + tasks[0].time
            reserve = int(lt[nodes[i]]) - int(et[nodes[i]])
        tree.insert('', 'end', values=(name, str(longest_time), str(earliest_time),str(reserve)))

    tree.pack()
    # Set the window size
    window.geometry("800x500")
    window.mainloop()

def diagram():
    taski = get_tasks()
    earliest_start_time, latest_completion_time, critical_path, nodes = cpm(taski, 'A', taski[-1].name)

    # Plot Graph
    graph = nx.DiGraph()
    for task in taski:
        graph.add_node(task.name, task=task)
        for prev in task.prev:
            graph.add_edge(prev, task.name, weight = task.time)

    pos = nx.shell_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_labels(graph, pos, font_size=16)
    nx.draw_networkx_edges(graph, pos, edge_color='black')
    cp_edges = [(u, v) for u, v in graph.edges() if u in critical_path and v in critical_path]
    nx.draw_networkx_edges(graph, pos, edgelist=cp_edges, edge_color='red')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): i for i, (u, v) in enumerate(graph.edges(), start=1)})
    plt.title('CPM for Project')
    plt.show()
    show_task_times(earliest_start_time,latest_completion_time,taski, nodes, critical_path)

# Create the "Add Task" button
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.grid(row=4, column=0, padx=5, pady=5)

# Create the "Run CPM" button
run_button = tk.Button(root, text="Run CPM", command= diagram)
run_button.grid(row=4, column=1, padx=5, pady=5)

def get_tasks():
    tasks = []
    for i in range(task_list.size()):
        task_str = task_list.get(i)
        name, time, prev = task_str.split(" | ")
        tasks.append(Task(name, int(time) , prev))
    print(tasks)
    return tasks

# Start the GUI main loop
root.mainloop()
