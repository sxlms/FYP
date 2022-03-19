import numpy as np
import pandas as pd
import sys
from Utility.utility import Algorithm

graph_df = pd.read_csv('data.csv')

# Draw temporal graph
Algorithm.draw_graph(graph_df, "temporal_graph_delaying")
delta = 3
# Add one extra column delta-possible. If t<=possible, t+1 is delta-possible
graph_df['delta-possible'] = graph_df['t'] + delta - 1

# Input nodes
nodes_name = list(set(graph_df['i']).union(graph_df['j']))
nodes_number = len(nodes_name)
source = [1]
t_max = 1
# Initialization
earliest_time = np.full(nodes_number, fill_value=sys.maxsize)
for i in range(len(source)):
    earliest_time[source[i]] = 0
# initialize part for delta possible
earliest_index = np.full(nodes_number, fill_value=-1)
# the output dataframe(for the delta-possible)
temporal_updates = pd.DataFrame({'t': earliest_time, 'index': earliest_index})


# define the edge stream
edge_stream = graph_df.sort_values(by='t')
# start
for i in edge_stream.index:
    if edge_stream['t'][i] <= t_max and edge_stream['t'][i] >= earliest_time[edge_stream['i'][i]]:
        if edge_stream['t'][i] < earliest_time[edge_stream['j'][i]]:
            temporal_updates['t'][edge_stream['j'][i]] = edge_stream['t'][i]
            temporal_updates['index'][edge_stream['j'][i]] = i
    elif (edge_stream['t'][i] > t_max):
        break
print(edge_stream)
# REt(G,S) is in the temporal updates, update the edge stream
update_edge = temporal_updates[temporal_updates['t'] == t_max]['index']
for index, value in update_edge.items():
    if edge_stream['t'][value] <= edge_stream['delta-possible'][value]:
        edge_stream['t'][value] += 1
print(edge_stream)



