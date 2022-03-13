import numpy as np
import pandas as pd
import sys


# Import the data.csv into dataframe
graph_df = pd.read_csv('data.csv')

# Get the list of nodes name. This list can be used as the indexes of the dataframe to show the reachability clearly
nodes_name = list(set(graph_df['i']).union(graph_df['j']))

# initialize the graph
temporal_function_df = pd.DataFrame(data=np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize),
                                    columns=nodes_name,
                                    index=nodes_name)
for i in graph_df.index:
    temporal_function_df[graph_df['i'][i]][graph_df['j'][i]] = graph_df['t'][i]
    temporal_function_df[graph_df['j'][i]][graph_df['i'][i]] = graph_df['t'][i]
