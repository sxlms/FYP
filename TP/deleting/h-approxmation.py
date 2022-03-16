import numpy as np
import pandas as pd
import sys



# Import the data.csv into dataframe
from Utility.utility import Algorithm

graph_df = pd.read_csv('data.csv')
h = 4

reachability = Algorithm.check_reachability()
output_edge = []
while reachability > h:
    edge_set = Algorithm.dijkstra_subtree(graph_df, h)


