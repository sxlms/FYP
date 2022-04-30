import numpy as np
import pandas as pd
import sys
import timeit
start = timeit.default_timer()
EDGE_STREAM_PATH = '../data/data.csv'
# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)

# Get the list of nodes name. This list can be used as the indexes of the dataframe to show the reachability clearly
nodes_name = list(set(graph_df['i']).union(graph_df['j']))

# Sort by timestamp on each edge
graph_df = graph_df.sort_values(by=['t'])

# Initialize the earliest_arrival matrix and convert it into dataframe
# Suppose the temporal graph has n vertexes.
# The  earliest_arrival  matrix is nXn matrix. Each cell record the earliest arrival time between two nodes
earliest_arrival_matrix = np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize)
np.fill_diagonal(earliest_arrival_matrix, 0)  # Initialize every vertex reach itself at timestamp 0
earliest_arrival_df = pd.DataFrame(data=earliest_arrival_matrix, columns=nodes_name, index=nodes_name)

for i in graph_df.index:
    """ This is Algorithm used to find the earliest time from s to a vertex v. 
 
    The edge coming as edge stream. The edge labelled as smaller timestamp come first.
    For each coming edge (u,v,t), 
    Column named u and v of matrix record the current earliest arrival time from each node to u and v.
    for each row, if matrix[node][u] < t, which means node can reach v via u, 
                     and matrix[node][v] < t, which means the earliest arrival time from node to v is t. 
                     Update the matrix[node][v] = t.
    For undirected graph, edge (u,v,t) also means (v,u,t). Therefore, it needs the similarly operation.
    """

    u = graph_df['i'][i]
    v = graph_df['j'][i]
    t = graph_df['t'][i]
    update_index = earliest_arrival_df[(earliest_arrival_df[u] < t) & (t < earliest_arrival_df[v])].index.tolist()
    earliest_arrival_df.loc[earliest_arrival_df.index.isin(update_index), v] = t
    update_index = earliest_arrival_df[(earliest_arrival_df[v] < t) & (t < earliest_arrival_df[u])].index.tolist()
    earliest_arrival_df.loc[earliest_arrival_df.index.isin(update_index), u] = t

# Count the reachability of each vertex by counting the non-Maximum numbers of each row and convert into dataframe
reachability_series = earliest_arrival_df[earliest_arrival_df.columns].lt(sys.maxsize).sum(axis=1)
reachability_df = reachability_series.to_frame()
reachability_df.columns = ['reachability']

print("OUTPUT:the reachability of each vertex\n")
print(reachability_df)
stop = timeit.default_timer()
print("Time", stop-start)