import pandas as pd
from utility.Utility import Algorithm

# Import the data.csv into dataframe
graph_df = pd.read_csv('data.csv')
h = 4
# Draw Graph before h-approximation
Algorithm.draw_graph(graph_df, "temporal_graph_h_approximation")
reachability, time_df = Algorithm.check_reachability(graph_df)
output_edge = []
while reachability > h:
    edge_set_dict = Algorithm.dijkstra_subtree(graph_df, h)
    for values in edge_set_dict.values():
        output_edge.append(values[0])  # add to the deleted edge
        # update the graph edge
        graph_df.drop(graph_df[((graph_df.i == values[0][0]) & (graph_df.j == values[0][1])) |
                               ((graph_df.j == values[0][0]) & (graph_df.i == values[0][1]))].index, inplace=True)

    reachability, time_df = Algorithm.check_reachability(graph_df)

if len(output_edge) > 0:
    deleted_edge_df = pd.DataFrame(data=output_edge, columns=['i', 'j', 't'])
    Algorithm.draw_graph(deleted_edge_df, "deleted_edges_h_approximation")
    Algorithm.draw_graph(graph_df, "after_deletion_h_approximation")
else:
    print("The maximum reachability of temporal graph is already h")
