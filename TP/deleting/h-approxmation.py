import numpy as np
import pandas as pd
import sys

# Utilising the Dijkstra's Algorithm
nodes_name = ['vr', 'v1', 'v2', 'v3', 'v4']
h = 5
temporal_graph_nodes = set(nodes_name)
graph_pd = pd.read_csv('testdata.csv')

# initialize the graph
data = pd.DataFrame(data=np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize),
                    columns=nodes_name,
                    index=nodes_name)
for i in graph_pd.index:
    data[graph_pd['i'][i]][graph_pd['j'][i]] = graph_pd['t'][i]
    data[graph_pd['j'][i]][graph_pd['i'][i]] = graph_pd['t'][i]


while len(temporal_graph_nodes):
    # initialize the graph
    root = temporal_graph_nodes.pop()
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
    # start loop, find the tree of maximum reachability of h+1 of current vertex
    while len(neighbor) and max_reachability < h:
        root = neighbor.pop()
        for i in data[root].index:
            if data[root][i] != sys.maxsize and data[root][i] > tem_timestamp:  # can reach i
                if i in unvisited_nodes:
                    neighbor.add(i)
                if edge_number_of_vertex[i][0] < tem_edge_number + 1:
                    break
                else:
                    if edge_number_of_vertex[i][0] > tem_edge_number + 1:
                        max_reachability += 1
                        edge_number_of_vertex[i][0] = tem_edge_number + 1
                    timestamps_of_vertex[i][0] = data[root][i]
                    path_to_node = []
                    if data[root][i] in delete_edges:
                        path_to_node = delete_edges.get(root)
                    path_to_node.append((root, i))
                    delete_edges.update({i: path_to_node})
        unvisited_nodes.remove(root)
    # delete the edges if reachability = h+1
    if max_reachability == h+1:
        for value in delete_edges.values():
            for index, v in enumerate(value):
                data[v[0]][v[1]] = sys.maxsize
                data[v[1]][v[0]] = sys.maxsize
