import networkx as nx
import matplotlib.pyplot as plt

class Task:
    def __init__(self, name, time, prev):
        self.name = name
        self.time = time
        self.prev = prev.split(',') if prev != '-' else []

def cpm(tasks, source, sink):
    # Step 1: Build Graph
    graph = nx.DiGraph()
    for task in tasks:
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

    return earliest_start_time, latest_completion_time, critical_path

# Example Usage
tasks = [
    Task('A', 3, '-'),
    Task('B', 5, 'A'),
    Task('C', 2, 'A'),
    Task('D', 4, 'B,C'),
    Task('E', 6, 'D')
]

# Calculate CPM
earliest_start_time, latest_completion_time, critical_path = cpm(tasks, 'A', 'E')

# Plot Graph
graph = nx.DiGraph()
for task in tasks:
    graph.add_node(task.name, task=task)
    for prev in task.prev:
        graph.add_edge(prev, task.name, weight = task.time)

pos = nx.shell_layout(graph)
nx.draw_networkx_nodes(graph, pos)
nx.draw_networkx_labels(graph, pos, font_size=16)
nx.draw_networkx_edges(graph, pos, edge_color='black')
cp_edges = [(u, v) for u, v in graph.edges() if u in critical_path and v in critical_path]
nx.draw_networkx_edges(graph, pos, edgelist=cp_edges, edge_color='red')
nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): d['weight'] for u, v, d in graph.edges(data=True)})
plt.title('CPM for Project')
plt.show()
