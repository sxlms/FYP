import pandas as pd
from utility.Utility import Algorithm

# prepare G and layout of the G :
start = 0
nodes_layout = ['vr', 'v1', 'v3', 'v5', 'v4', 'v2']
graph_df = pd.read_csv('data.csv')
# Draw temporal graph
Algorithm.draw_graph(graph_df, "temporal_graph_c_approximation")
h = 4
nodes_number = len(nodes_layout)
j = -1
# output delete edge
output_edge = []
reachability, time_df = Algorithm.check_reachability(graph_df)

while reachability > h:
    for index in range(nodes_number-1, start, -1):
        subgraph_df = Algorithm.subgraph(nodes_layout, start, index, graph_df)
        reachability, time_df = Algorithm.check_reachability(subgraph_df)
        if reachability <= h:
            j = index
            # span vj and vj+1 added into set and update the graph
            output_edge, graph_df = Algorithm.span(nodes_layout, j, graph_df, output_edge)
            break
    start = j+1
    reachability, time_df = Algorithm.check_reachability(graph_df)

if len(output_edge) > 0:
    deleted_edge_df = pd.DataFrame(data=output_edge, columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "deleted_edges_c_approximation")
    Algorithm.draw_graph(graph_df, "after_deletion_c_approximation")
else:
    print("The maximum reachability of temporal graph is already h")

