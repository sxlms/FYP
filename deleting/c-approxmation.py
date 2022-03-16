import numpy as np
import pandas as pd
import sys
from Utility.utility import Algorithm

# prepare G and layout of the G :
start = 0
nodes_layout = ['vr', 'v1', 'v2', 'v3', 'v4', 'v5']
graph_df = pd.read_csv('data.csv')
h = 4
nodes_number = len(nodes_layout)
j = -1
# output delete edge
output_edge = []


while Algorithm.check_reachability(graph_df) > h:
    for index in range(nodes_number-1, start, -1):
        subgraph_df = Algorithm.subgraph(nodes_layout, start, index, graph_df)
        if Algorithm.check_reachability(subgraph_df) <= h:
            j = index
            break
    # span vj and vj+1 added into set and update the graph
    output,graph_df = Algorithm.span(nodes_layout, j, graph_df)
    output_edge.append(output)
    start = j+1

if len(output_edge)>0:
    print("delete edges are:")
    for v in output_edge:
        print(v)

