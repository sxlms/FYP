import numpy as np
import pandas as pd
import sys


# get the reachability of the graph
def reachability_graph(graph_df, nodes_name):
    # create edge stream
    # undirected_graph_pd = undirected_graph_pd.sort_values(by=['t'])
    graph_df = graph_df.sort_values(by=['t'])
    # initialize the reachability matrix
    data = np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize)
    np.fill_diagonal(data, 0)
    reachability_df = pd.DataFrame(data=data, columns=nodes_name, index=nodes_name)
    # start the algorithms(advanced)
    for i in graph_df.index:
        # first for u->v, u,v, t
        u = graph_df['i'][i]
        v = graph_df['j'][i]
        t = graph_df['t'][i]
        update_index = reachability_df[(reachability_df[u] < t) & (t < reachability_df[v])].index.tolist()
        reachability_df.loc[reachability_df.index.isin(update_index), v] = t
        # second for v->u, v, u, t
        update_index = reachability_df[(reachability_df[v] < t) & (t < reachability_df[u])].index.tolist()
        reachability_df.loc[reachability_df.index.isin(update_index), u] = t

    cols = reachability_df.columns
    r = reachability_df[cols].lt(sys.maxsize).sum(axis=1).max()
    return r


def update_graph(graph_df, j, nodes_name, output):
    # span edge of the vj and vj+1 and delete the edge of the graph
    left_nodes_list = nodes_name[0:j + 1]
    right_nodes_list = np.setdiff1d(nodes_name, left_nodes_list)
    delete_span_edge = []
    for i in graph_df.index:
        if (graph_df['i'][i] in left_nodes_list and graph_df['j'][i] in right_nodes_list) or \
                (graph_df['j'][i] in left_nodes_list and graph_df['i'][i] in right_nodes_list):
            delete_span_edge.append((graph_df['i'][i], graph_df['j'][i]))
            output.append((graph_df['i'][i], graph_df['j'][i]))
    for row in delete_span_edge:
        graph_df.drop(graph_df[(graph_df['i'] == row[0]) & (graph_df['j'] == row[1])].index, inplace=True)
    return graph_df, output


# prepare G and layout of the G :
i = 0
nodes_name = ['vr', 'v1', 'v2', 'v3', 'v4', 'v5']
temporal_graph_nodes = set(nodes_name)
graph_df = pd.read_csv('c_test.csv')
h = 3
n = len(nodes_name)

# output delete edge
output = []

while reachability_graph(graph_df, nodes_name) > h:
    j = -1
    for index in range(n-1, i+h, -1):
        subgraph_nodes = nodes_name[i:index]
        subgraph_nodes = graph_df[(graph_df['i'].isin(subgraph_nodes)) & (graph_df['j'].isin(subgraph_nodes))]
        if reachability_graph(subgraph_nodes, subgraph_nodes) <= h:
            j = index
            break
    # span vj and vj+1 added into set and update the graph
    graph_df, output = update_graph(graph_df, j, nodes_name, output)
    i = j+1


















