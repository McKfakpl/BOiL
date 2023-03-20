import networkx as nx
import matplotlib.pyplot as plt

def cpm(graph, source, sink):
    # Step 1: Topological Sort
    nodes = list(nx.topological_sort(graph))
    
    # Step 2: Forward Pass
    earliest_start_time = {node: 0 for node in nodes}
    for node in nodes:
        for successor in graph.successors(node):
            earliest_start_time[successor] = max(earliest_start_time[successor], earliest_start_time[node] + graph.edges[node, successor]['weight'])
    
    # Step 3: Backward Pass
    latest_completion_time = {node: earliest_start_time[sink] for node in nodes}
    for node in reversed(nodes):
        for predecessor in graph.predecessors(node):
            latest_completion_time[predecessor] = min(latest_completion_time[predecessor], latest_completion_time[node] - graph.edges[predecessor, node]['weight'])
    
    # Step 4: Calculate Critical Path
    critical_path = []
    for node in nodes:
        if earliest_start_time[node] == latest_completion_time[node]:
            critical_path.append(node)
    
    return earliest_start_time, latest_completion_time, critical_path

# Example Usage
graph = nx.DiGraph()
graph.add_edge('A', 'B', weight=3)
graph.add_edge('A', 'C', weight=2)
graph.add_edge('B', 'D', weight=5)
graph.add_edge('C', 'D', weight=4)
graph.add_edge('D', 'E', weight=6)

# Calculate CPM
earliest_start_time, latest_completion_time, critical_path = cpm(graph, 'A', 'E')

# Plot Graph
pos = nx.shell_layout(graph)
nx.draw_networkx_nodes(graph, pos)
nx.draw_networkx_labels(graph, pos, font_size=16)
# Draw all edges in black
nx.draw_networkx_edges(graph, pos, edge_color='black')
# Draw critical path edges in red
cp_edges = [(u, v) for u, v in graph.edges() if u in critical_path and v in critical_path]
nx.draw_networkx_edges(graph, pos, edgelist=cp_edges, edge_color='red')
nx.draw_networkx_edge_labels(graph, pos, edge_labels={(u, v): d['weight'] for u, v, d in graph.edges(data=True)})
plt.title('CPM for Project')
plt.show()