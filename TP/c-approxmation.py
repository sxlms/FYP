import numpy as np
import pandas as pd
import sys

# input, G and sequence of vertices:
nodes_name = ['vr', 'v1', 'v2', 'v3', 'v4', 'v5']
temporal_graph_nodes = set(nodes_name)
graph_df = pd.read_csv('c_test.csv')

# undirected_graph_pd = pd.concat([graph_pd, pd.DataFrame({'i': graph_pd['j'],
#                                                          'j': graph_pd['i'],
#                                                          't': graph_pd['t']})])
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
    # first for v->u, v, u, t
    update_index = reachability_df[(reachability_df[v] < t) & (t < reachability_df[u])].index.tolist()
    reachability_df.loc[reachability_df.index.isin(update_index), u] = t

# sapn the vj and vj+1



