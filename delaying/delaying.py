import numpy as np
import pandas as pd
import sys
from Utility.utility import Algorithm

graph_df = pd.read_csv('data.csv')

# Draw temporal graph
Algorithm.draw_graph(graph_df, "temporal_graph_delaying")
delta = 3
# Add one extra column delta-possible. This is the upper bound of timestamp allowing any delaying
graph_df['delta-possible'] = graph_df['t'] + delta - 1
# Define the edge stream
edge_stream_df = graph_df.sort_values(by='t')
# Get the nodes name
nodes_name = list(set(graph_df['i']).union(graph_df['j']))
nodes_number = len(nodes_name)
# Source nodes
source_nodes = ['v1', 'v2']
t_max = graph_df['t'].max()+delta
t_min = graph_df['t'].min()

def timestamp_matrix(graph_df):
    edge_df = pd.DataFrame(data=np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize),
                           columns=nodes_name,
                           index=nodes_name)
    for i in graph_df.index:
        edge_df[graph_df['i'][i]][graph_df['j'][i]] = graph_df['t'][i]
        edge_df[graph_df['j'][i]][graph_df['i'][i]] = graph_df['t'][i]
    return edge_df


def reachable_edge_t(df, source, t):
    delaying_edge_list = []
    reachability, time_df = Algorithm.check_reachability(df)
    time_df = time_df[time_df.index.isin(source)]
    time_df.drop(axis=1, labels=source, inplace=True)
    edge_df = timestamp_matrix(df)
    for index, row in time_df.iteritems():
        if time_df[index].min() == t:
            match_sources = edge_df[edge_df[index] == t].index.tolist()
            for v in match_sources:
                remove_duplicate_set = set(delaying_edge_list)
                item = (v, index)
                item_reverse = (index, v)
                if (item not in remove_duplicate_set) and (item_reverse not in remove_duplicate_set):
                    delaying_edge_list.append((v, index))

    return delaying_edge_list


for time in range(t_min, t_max):
    # Compute the REt(⟨G, T⟩, S, t)
    ret_list = reachable_edge_t(graph_df, source_nodes, time)
    for v in ret_list:
        update_index = graph_df[((graph_df['i'] == v[0]) & (graph_df['j'] == v[1])) |
                                ((graph_df['j'] == v[0]) & (graph_df['i'] == v[1]))].index
        if (graph_df['t'][update_index] <= graph_df['delta-possible'][update_index]).bool():
            t = graph_df['t'][update_index].values[0]
            graph_df.loc[update_index,'t'] = t+1

# Draw temporal graph after delaying
Algorithm.draw_graph(graph_df, "temporal_graph_after_delaying")
