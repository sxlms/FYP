import numpy as np
import pandas as pd
import sys
import timeit
start = timeit.default_timer()
"""
 This program is used for finding the reachability of each vertex in temporal graph.
 Input: The edge stream of a temporal graph. Variable: EDGE_STREAM_PATH
 Output: Dataframe recorded the reachability of each vertex. Variable: reachability_df
"""
EDGE_STREAM_PATH = '../data/data.csv'
# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)

# Get the list of nodes name. This list can be used as the indexes of the dataframe to show the reachability clearly
nodes_name = list(set(graph_df['i']).union(graph_df['j']))

# Sort by timestamp on each edge
graph_df = graph_df.sort_values(by=['t'])

# Initialize the earliest_arrival matrix and convert it into dataframe
# Suppose the temporal graph has n vertices, the earliest_arrival dataframe is a n*n matrix.
# Each cell record the earliest arrival time from row to column

earliest_arrival_matrix = np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize)
np.fill_diagonal(earliest_arrival_matrix, 0)  # Initialize every vertex reach itself at timestamp 0
earliest_arrival_df = pd.DataFrame(data=earliest_arrival_matrix, columns=nodes_name, index=nodes_name)

for i in graph_df.index:
    """ This is used to find the earliest time from s to a vertex v. 
    For each coming edge (u,v,t) in edge stream, 
    columns named u and v of matrix record the current earliest arrival time from row vertex to u and v.
    for each row, if matrix[vertex][u] < t, which means vertex can reach v via u, 
                  then, check matrix[vertex][v] < t, which means the current earliest arrival time from vertex to v is t
                        Update it with matrix[vertex][v] = t.
    For undirected temporal graph, edge (u,v,t) also means (v,u,t). Therefore, it needs the similar operation.
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
