import pandas as pd

# Import the data.csv into dataframe
from Utility.utility import Algorithm

graph_df = pd.read_csv('data.csv')
h = 4

reachability = Algorithm.check_reachability(graph_df)
output_edge = []
while reachability > h:
    edge_set_dict = Algorithm.dijkstra_subtree(graph_df, h)
    for values in edge_set_dict.values():
        output_edge.append(values[0])  # add to the deleted edge
        # update the graph edge
        graph_df.drop(graph_df[((graph_df.i == values[0][0]) & (graph_df.j == values[0][1])) |
                               ((graph_df.j == values[0][0]) & (graph_df.i == values[0][1]))].index, inplace=True)

    reachability = Algorithm.check_reachability(graph_df)

if len(output_edge) > 0:
    print("delete edges are:")
    for values in output_edge:
        print(values)
else:
    print("the reachability of graph is at most h")
