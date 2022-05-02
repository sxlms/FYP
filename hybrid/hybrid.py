import pandas as pd
from utility.utility import Algorithm
import sys

""" This algorithm minimize the reachability by hybrid algorithm

    Input:  1. The edge stream of a temporal graph. Variable: EDGE_STREAM_PATH
            2. The h parameter. Variable: h
            3. The delta for delaying. variable: delta

    Output: 
            1. the diagram of input temporal graph. File name: hy_temporal_graph
            2. the diagram of temporal graph after running this algorithm. File name: hy_updated_graph
            3. the diagram of all deleted subtrees. File name: hy_deleted_edges
            4. .csv recorded the edge stream of updated_graph. File name: hy_updated_graph.csv
            5. three DOT text file record the graph nodes and edges
                6.  if the maximum reachability of temporal graph is h before any operation, 
                    it will output "The maximum reachability of original temporal graph is h"
"""

EDGE_STREAM_PATH = '../data/data.csv'
h = 4
delta = 3

# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)
# Draw Graph before h-approximation
Algorithm.draw_graph(graph_df, "hy_temporal_graph")
reachability, time_df = Algorithm.find_reachability(graph_df)
deleted_edges = []

# if there exists vertices has reachability > h. Those vertices are the source vertices
reachability_series = time_df[time_df.columns].lt(sys.maxsize).sum(axis=1)
reachability_df = reachability_series.to_frame()
reachability_df.columns = ['reachability']
source_nodes = reachability_df[reachability_df.reachability > h].index.tolist()

# Do delta-delaying
# Add one extra column delta-possible. This is the upper bound of timestamp allowing any delaying
graph_df['delta-possible'] = graph_df['t'] + delta - 1

# Define the edge stream
edge_stream_df = graph_df.sort_values(by='t')
# Get the nodes name
nodes_name = list(set(graph_df['i']).union(graph_df['j']))
nodes_number = len(nodes_name)

t_max = graph_df['t'].max()+delta
t_min = graph_df['t'].min()

for time in range(t_min, t_max):
    # Compute the REt(⟨G, T⟩, S, t)
    ret_list = Algorithm.reachable_edge_t(graph_df, source_nodes, time)
    for v in ret_list:
        update_index = graph_df[((graph_df['i'] == v[0]) & (graph_df['j'] == v[1])) |
                                ((graph_df['j'] == v[0]) & (graph_df['i'] == v[1]))].index
        if (graph_df['t'][update_index] <= graph_df['delta-possible'][update_index]).bool():
            t = graph_df['t'][update_index].values[0]
            graph_df.loc[update_index, 't'] = t+1
graph_df.drop(columns=['delta-possible'], inplace=True)

# Do delta-approximation
while reachability > h:
    delete_edge_list = Algorithm.delete_edge(time_df, graph_df, h)
    deleted_edges.append(delete_edge_list[0])  # add to the deleted edge
    # update the graph edge
    graph_df.drop(graph_df[((graph_df.i == delete_edge_list[0][0]) & (graph_df.j == delete_edge_list[0][1])) |
                           ((graph_df.j == delete_edge_list[0][0]) & (graph_df.i == delete_edge_list[0][1]))].index,
                  inplace=True)
    reachability, time_df = Algorithm.find_reachability(graph_df)

if len(deleted_edges) > 0:
    deleted_edge_df = pd.DataFrame(data=deleted_edges, columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "hy_deleted_edges")
    Algorithm.draw_graph(graph_df, "hy_updated_graph")
else:
    print("The maximum reachability of temporal graph is h")
