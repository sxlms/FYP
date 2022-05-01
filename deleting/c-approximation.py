import pandas as pd
from utility.utility import Algorithm

""" This algorithm minimize the reachability by c-approximation algorithm

    Input:  1. The edge stream of a temporal graph. Variable: EDGE_STREAM_PATH
            2. The h parameter. Variable: h
            3. The layout of the graph. Variable: layout

    Output: 
            1. the diagram of input temporal graph. File name: c_temporal_graph
            2. the diagram of temporal graph after running this algorithm. File name: c_updated_graph
            3. the diagram of all deleted subtrees. File name: c_deleted_edges
            4. .csv recorded the edge stream of updated_graph. File name: c_updated_graph.csv
            5. three DOT text file record the graph nodes and edges
                6.  if the maximum reachability of temporal graph is h before any operation, 
                    it will output "The maximum reachability of original temporal graph is h"
"""


EDGE_STREAM_PATH = '../data/data.csv'
h = 4
layout = ['vr', 'v1', 'v2', 'v3', 'v4', 'v5']

# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)
start = 0

# Draw temporal graph
Algorithm.draw_graph(graph_df, "c_temporal_graph")
nodes_number = len(layout)
j = -1
# output delete edge
output_edge = []
reachability, time_df = Algorithm.find_reachability(graph_df)

while reachability > h:
    for index in range(nodes_number-1, start, -1):
        subgraph_df = Algorithm.subgraph(layout, start, index, graph_df)
        reachability, time_df = Algorithm.find_reachability(subgraph_df)
        if reachability <= h:
            j = index
            # span vj and vj+1 added into set and update the graph
            output_edge, graph_df = Algorithm.span(layout, j, graph_df, output_edge)
            break
    start = j+1
    reachability, time_df = Algorithm.find_reachability(graph_df)

if len(output_edge) > 0:
    deleted_edge_df = pd.DataFrame(data=output_edge, columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "c_deleted_edges")
    Algorithm.draw_graph(graph_df, "c_updated_graph")
    graph_df.to_csv("c_updated_graph.csv", index=False)
else:
    print("The maximum reachability of original temporal graph is h")
