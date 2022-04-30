import pandas as pd
from utility.utility import Algorithm
import sys
import timeit

EDGE_STREAM_PATH = '../data/data.csv'
# Import the temporal graph into dataframe
graph_df = pd.read_csv(EDGE_STREAM_PATH)

start = timeit.default_timer()
h = 3
# Draw Graph before h-approximation
Algorithm.draw_graph(graph_df, "temporal_graph_delta_approximation")
reachability, time_df = Algorithm.find_reachability(graph_df)
output_edge = []


def delete_edge(etime_df, temporal_graph):
    edge_list = []
    # Count the reachability of each vertex
    reachability_series = etime_df[etime_df.columns].lt(sys.maxsize).sum(axis=1)
    reachability_df = reachability_series.to_frame()
    reachability_df.columns = ['reachability']
    # Get the vertex where reachability is the minimum value greater than h
    reachability_df = reachability_df[reachability_df['reachability']>h]
    v = reachability_df['reachability'].idxmin()
    # Get the edge incident to that vertex has the largest time label
    graph_matrix = Algorithm.temporal_graph_matrix(temporal_graph)
    u = graph_matrix[graph_matrix.lt(sys.maxsize)][v].idxmax()
    t = graph_matrix[v][u]
    edge_list.append((v, u, t))
    return edge_list


while reachability > h:
    delete_edge_list = delete_edge(time_df, graph_df)
    output_edge.append(delete_edge_list[0])  # add to the deleted edge
    # update the graph edge
    graph_df.drop(graph_df[((graph_df.i == delete_edge_list[0][0]) & (graph_df.j == delete_edge_list[0][1])) |
                           ((graph_df.j == delete_edge_list[0][0]) & (graph_df.i == delete_edge_list[0][1]))].index,
                  inplace=True)
    reachability, time_df = Algorithm.find_reachability(graph_df)

if len(output_edge) > 0:
    deleted_edge_df = pd.DataFrame(data=output_edge, columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "deleted_edges_delta_approximation")
    Algorithm.draw_graph(graph_df, "after_deletion_delta_approximation")
else:
    print("The maximum reachability of temporal graph is already h")
stop = timeit.default_timer()
print('Time: ', stop - start)