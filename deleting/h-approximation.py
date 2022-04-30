import pandas as pd
from utility.utility import Algorithm
import timeit

""" This algorithm minimize the reachability by h-approximation algorithm

    Input:  1. The edge stream of a temporal graph. Variable: EDGE_STREAM_PATH
            2. The h parameter. Variable: h

    Output: 
            1. the diagram of input temporal graph. File name: temporal_graph
            2. the diagram of temporal graph after running this algorithm. File name: updated_graph.csv
            3. the diagram of deleted subtree. File name: 
            3. .csv recorded the edge stream of updated_graph. File name: updated_graph.csv
            4. three DOT text file record the graph nodes and edges
"""

start = timeit.default_timer()
h = 4
EDGE_STREAM_PATH = '../data/data.csv'
# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)

# Draw Graph before h-approximation
Algorithm.draw_graph(graph_df, "temporal_graph_h")
reachability, time_df = Algorithm.find_reachability(graph_df)
output_edge = []
while reachability > h:
    edge_set_dict = Algorithm.dijkstra_subtree(graph_df, h)
    for values in edge_set_dict.values():
        output_edge.append(values[0])  # add to the deleted edge
        # update the graph edge
        graph_df.drop(graph_df[((graph_df.i == values[0][0]) & (graph_df.j == values[0][1])) |
                               ((graph_df.j == values[0][0]) & (graph_df.i == values[0][1]))].index, inplace=True)

    reachability, time_df = Algorithm.find_reachability(graph_df)

if len(output_edge) > 0:
    deleted_edge_df = pd.DataFrame(data=output_edge, columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "deleted_edges_h_approximation")
    Algorithm.draw_graph(graph_df, "after_deletion_h_approximation")
else:
    print("The maximum reachability of temporal graph is already h")
stop = timeit.default_timer()
print('Time: ', stop - start)