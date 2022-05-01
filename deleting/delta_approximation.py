import pandas as pd
from utility.utility import Algorithm
import sys

""" This algorithm minimize the reachability by delta-approximation algorithm

    Input:  1. The edge stream of a temporal graph. Variable: EDGE_STREAM_PATH
            2. The h parameter. Variable: h

    Output: 
            1. the diagram of input temporal graph. File name: d_temporal_graph
            2. the diagram of temporal graph after running this algorithm. File name: d_updated_graph
            3. the diagram of all deleted subtrees. File name: d_deleted_edges
            4. .csv recorded the edge stream of updated_graph. File name: d_updated_graph.csv
            5. three DOT text file record the graph nodes and edges
                6.  if the maximum reachability of temporal graph is h before any operation, 
                    it will output "The maximum reachability of original temporal graph is h"
"""

EDGE_STREAM_PATH = '../data/data.csv'
h = 4

# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)

# Draw Graph before h-approximation
Algorithm.draw_graph(graph_df, "d_temporal_graph")
reachability, time_df = Algorithm.find_reachability(graph_df)
deleted_edge = []

while reachability > h:
    delete_edge_list = Algorithm.delete_edge(time_df, graph_df)
    deleted_edge.append(delete_edge_list[0])  # add to the deleted edge
    # update the graph edge
    graph_df.drop(graph_df[((graph_df.i == delete_edge_list[0][0]) & (graph_df.j == delete_edge_list[0][1])) |
                           ((graph_df.j == delete_edge_list[0][0]) & (graph_df.i == delete_edge_list[0][1]))].index,
                  inplace=True)
    reachability, time_df = Algorithm.find_reachability(graph_df)

if len(deleted_edge) > 0:
    deleted_edge_df = pd.DataFrame(data=deleted_edge, columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "d_deleted_edges")
    Algorithm.draw_graph(graph_df, "d_updated_graph")
    graph_df.to_csv("d_updated_graph.csv", index=False)
else:
    print("The maximum reachability of temporal graph is h")
