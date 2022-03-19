import numpy as np
import pandas as pd
import sys
from utility.Utility import Algorithm

""" This algorithm is not optimal for the minimum edge set of a subtree with the reachability h rooted at v
    But, it can ensure that if there is a subtree with the reachability h rooted at v. The program will output that.
"""

# Import the data.csv into dataframe
graph_df = pd.read_csv('data.csv')
h = 4
# Draw temporal graph
Algorithm.draw_graph(graph_df, "original_temporal_graph")
# Get the list of nodes name. This list can be used as the indexes of the dataframe to show the reachability clearly
nodes_name = list(set(graph_df['i']).union(graph_df['j']))
nodes_set = set(nodes_name)
nodes_number = len(nodes_name)

# Initialize one matrix named edge_df record the timestamp on each edge
edge_df = pd.DataFrame(data=np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize),
                       columns=nodes_name,
                       index=nodes_name)
for i in graph_df.index:
    edge_df[graph_df['i'][i]][graph_df['j'][i]] = graph_df['t'][i]
    edge_df[graph_df['j'][i]][graph_df['i'][i]] = graph_df['t'][i]

# Output: Subtree of vertex with reachability is h + 1, if exist
deleted_subtree = dict()
break_f = 0
deleted_root = 'not defined'
for root in nodes_name:
    # it will iterate each node to find an node that reachability of subtree rooted at is h+1
    max_reachability = 1  # Every vertex can reach itself. Record the current maximum number
    unvisited_nodes = set(nodes_name)  # initialize the unvisited nodes
    unvisited_nodes.remove(root)
    current_subtree_edges = dict()  # record the subtree edges of current node(root)

    # record length of the shortest temporal path from root to each nodes
    len_df = pd.DataFrame(data=np.full(len(unvisited_nodes), fill_value=sys.maxsize).reshape(1, nodes_number - 1),
                          columns=list(unvisited_nodes))
    # record the earliest timestamp from root to each nodes
    time_df = pd.DataFrame(data=np.full(len(unvisited_nodes), fill_value=sys.maxsize).reshape(1, nodes_number - 1),
                           columns=list(unvisited_nodes))
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
            if i != root_of_subtree and i != root and edge_df[root][i] != sys.maxsize and edge_df[root][i] > tem_timestamp:
                # this is the reachable neighbor of root
                # update the time_df and len_df
                change_flag = 0  # indicate if it needs update the subtree
                if time_df[i][0] > edge_df[root][i]:
                    # reachability +1 only when the node
                    if time_df[i][0] == sys.maxsize:
                        max_reachability += 1
                        candidate.add(i)
                    time_df[i][0] = edge_df[root][i]
                    len_df[i][0] = tem_length + 1
                    change_flag = 1
                elif (time_df[i][0] == edge_df[root][i]) and (len_df[i][0] > tem_length + 1):
                    len_df[i][0] = tem_length + 1
                    change_flag = 1
                # update the subtree
                if change_flag == 1:
                    path_to_node = []
                    if i in current_subtree_edges:
                        path_to_node = current_subtree_edges.get(i)
                    path_to_node.append((root, i, edge_df[root][i]))
                    current_subtree_edges.update({i: path_to_node})
                # check the reachability for each index
                if max_reachability == h+1:
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
                tem_length = len_df[n][0]
    if break_f == 1:
        deleted_subtree = current_subtree_edges
        deleted_root = root_of_subtree
        break


# Final output
deleted_tree_list = list()
if break_f == 1:
    for value in deleted_subtree.values():
        deleted_tree_list.append(value[0])
    deleted_edge_df = pd.DataFrame(data=deleted_tree_list,columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "deleted_subtree")
else:
    print("No such subtree")

