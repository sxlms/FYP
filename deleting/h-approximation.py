import pandas as pd
from utility.utility import Algorithm

""" This algorithm minimize the reachability by h-approximation algorithm

    Input:  1. The edge stream of a temporal graph. Variable: EDGE_STREAM_PATH
            2. The h parameter. Variable: h

    Output: 
            1. the diagram of input temporal graph. File name: h_temporal_graph
            2. the diagram of temporal graph after running this algorithm. File name: h_updated_graph
            3. the diagram of all deleted subtrees. File name: h_deleted_subtrees
            4. .csv recorded the edge stream of updated_graph. File name: h_updated_graph.csv
            5. three DOT text file record the graph nodes and edges
                6.  if the maximum reachability of temporal graph is h before any operation, 
                    it will output "The maximum reachability of original temporal graph is h"
"""

h = 4
EDGE_STREAM_PATH = '../data/data.csv'

# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)

# Draw Graph before h-approximation
Algorithm.draw_graph(graph_df, "h_temporal_graph")

reachability, time_df = Algorithm.find_reachability(graph_df)
deleted_edge = []

while reachability > h:
    edge_set_dict = Algorithm.dijkstra_subtree(graph_df, h)
    for values in edge_set_dict.values():
        deleted_edge.append(values[0])  # add to the deleted edge
        # update the graph edge
        graph_df.drop(graph_df[((graph_df.i == values[0][0]) & (graph_df.j == values[0][1])) |
                               ((graph_df.j == values[0][0]) & (graph_df.i == values[0][1]))].index, inplace=True)

    reachability, time_df = Algorithm.find_reachability(graph_df)

if len(deleted_edge) > 0:
    deleted_edge_df = pd.DataFrame(data=deleted_edge, columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "h_deleted_subtrees")
    Algorithm.draw_graph(graph_df, "h_updated_graph")
    graph_df.to_csv("h_updated_graph.csv", index=False)
else:
    print("The maximum reachability of original temporal graph is h")
