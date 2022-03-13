import numpy as np
import pandas as pd
import sys


# Import the data.csv into dataframe
graph_df = pd.read_csv('data.csv')
h = 3

# Get the list of nodes name. This list can be used as the indexes of the dataframe to show the reachability clearly
nodes_name = list(set(graph_df['i']).union(graph_df['j']))
nodes_set = set(nodes_name)

# Initialize one dataframe record the timestamp on each edge
temporal_function_df = pd.DataFrame(data=np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize),
                                    columns=nodes_name,
                                    index=nodes_name)
for i in graph_df.index:
    temporal_function_df[graph_df['i'][i]][graph_df['j'][i]] = graph_df['t'][i]
    temporal_function_df[graph_df['j'][i]][graph_df['i'][i]] = graph_df['t'][i]

# Output: Subtree
subtree = []
while len(nodes_set):
    root = nodes_set.pop()  # Root node
    max_reachability = 1  # Every vertex can reach itself. Record the current maximum number
    unvisited_nodes = set(nodes_name)
    delete_edges = dict()
    timestamps_of_vertex = pd.DataFrame(data=np.full(len(nodes_name), fill_value=sys.maxsize).reshape(1, 5),
                                        columns=nodes_name)
    edge_number_of_vertex = pd.DataFrame(data=np.full(len(nodes_name), fill_value=sys.maxsize).reshape(1, 5),
                                         columns=nodes_name)

    tem_edge_number = 0 if edge_number_of_vertex[root][0] == sys.maxsize else edge_number_of_vertex[root][0]
    tem_timestamp = -1 if timestamps_of_vertex[root][0] == sys.maxsize else timestamps_of_vertex[root][0]
    neighbor = set()
    neighbor.add(root)
    # start loop, find the tree of maximum reachability of h+1 of root vertex
    while len(neighbor) and max_reachability < h:
        root = neighbor.pop()
        for i in temporal_function_df[root].index:
            if temporal_function_df[root][i] != sys.maxsize and temporal_function_df[root][i] > tem_timestamp:
                # can reach i
                if i in unvisited_nodes:
                    neighbor.add(i)
                if edge_number_of_vertex[i][0] < tem_edge_number + 1:
                    break
                else:
                    if edge_number_of_vertex[i][0] > tem_edge_number + 1:
                        max_reachability += 1
                        edge_number_of_vertex[i][0] = tem_edge_number + 1
                    timestamps_of_vertex[i][0] = temporal_function_df[root][i]
                    path_to_node = []
                    if temporal_function_df[root][i] in delete_edges:
                        path_to_node = delete_edges.get(root)
                    path_to_node.append((root, i))
                    delete_edges.update({i: path_to_node})
        unvisited_nodes.remove(root)
