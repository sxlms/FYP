import numpy as np
import pandas as pd
import sys
from utility.utility import Algorithm
import timeit

start = timeit.default_timer()
""" This algorithm generate a reachable subtree with the reachability h.
    In practice, If there exist such reachable subtree in temporal graph, output it
    Otherwise, output no such tree.
    
    Input:  1. The edge stream of a temporal graph. Variable: EDGE_STREAM_PATH
            2. The reachability h
            
    Output: 1. .csv recorded the edge stream of such reachable subtree. File name: reachable_subtree.csv
            2. the diagram of input temporal graph. File name: temporal_graph
            3. the diagram of reachable subtree. File name: reachable_subtree
            4. two DOT text file record the graph nodes and edges
"""
h = 4
EDGE_STREAM_PATH = '../data/data.csv'


# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)

# Draw temporal graph
Algorithm.draw_graph(graph_df, "temporal_graph")
# Get the list of nodes name. This list can be used as the indexes of the dataframe to show the reachability clearly
nodes_name = list(set(graph_df['i']).union(graph_df['j']))
nodes_set = set(nodes_name)
nodes_number = len(nodes_name)

# Initialize one matrix named edge_df record the timestamp on each edge
edge_df = Algorithm.temporal_graph_matrix(graph_df)

# Output variable: Subtree of vertex with reachability is h, if exists
reachable_subtree = dict()

break_f = 0
subtree_root = 'not defined'
for root in nodes_name:
    # it will iterate each node to find an node that reachability of subtree rooted at is h+1
    max_reachability = 1  # Every vertex can reach itself. Record the current maximum number
    nodes = set(nodes_name)  # initialize the unvisited nodes
    nodes.remove(root)
    current_subtree_edges = dict()  # record the subtree edges of current node(root)

    # record the earliest timestamp from root to each nodes
    time_df = pd.DataFrame(data=np.full(len(nodes), fill_value=sys.maxsize).reshape(1, nodes_number - 1),
                           columns=list(nodes))
    tem_timestamp = -1
    tem_length = 0
    break_w = 0
    candidate = set()
    candidate.add(root)
    root_of_subtree = root

    while len(candidate):
        candidate.remove(root)
        for i in edge_df[root].index:
            # find the root's neighbor and update the len_df and edge_df
            if i != root_of_subtree and i != root \
                    and edge_df[root][i] != sys.maxsize and edge_df[root][i] > tem_timestamp:
                # this is the reachable neighbor from root
                # update the time_df to avoid cycle in tree
                if time_df[i][0] > edge_df[root][i]:
                    # reachability +1 only when the node is never reached before
                    if time_df[i][0] == sys.maxsize:
                        max_reachability += 1
                        candidate.add(i)
                    time_df[i][0] = edge_df[root][i]
                    path_to_node = []
                    if i in current_subtree_edges:
                        path_to_node = current_subtree_edges.get(i)
                    path_to_node.append((root, i, edge_df[root][i]))
                    current_subtree_edges.update({i: path_to_node})
                # check the reachability for each index
                if max_reachability == h:
                    break_w = 1
                    break
        if break_w == 1:
            break_f = 1
            break
        tem_timestamp = sys.maxsize
        for n in candidate:
            if tem_timestamp > time_df[n][0]:
                root = n
                tem_timestamp = time_df[n][0]
    if break_f == 1:
        reachable_subtree = current_subtree_edges
        subtree_root = root_of_subtree
        break

# Final output
tem_list = list()
if break_f == 1:
    for value in reachable_subtree.values():
        tem_list.append(value[0])
    reachable_subtree_df = pd.DataFrame(data=tem_list, columns=['i', 'j', 't'])
    Algorithm.draw_graph(reachable_subtree_df, "reachable_subtree")
    reachable_subtree_df.to_csv("reachable_subtree.csv", index=False)
else:
    print("No such subtree")
stop = timeit.default_timer()
print("Time:", stop-start)
