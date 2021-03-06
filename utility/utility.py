import numpy as np
import pandas as pd
import sys
from graphviz import Graph


class Algorithm:
    @staticmethod
    def find_reachability(graph_df):
        # return the reachability of the graph
        # Get the list of nodes name
        nodes_name = list(set(graph_df['i']).union(graph_df['j']))
        # Sort by timestamp on each edge
        graph_df = graph_df.sort_values(by=['t'])
        # The  earliest_arrival  matrix is nXn matrix. Each cell record the earliest arrival time between two nodes
        earliest_arrival_matrix = np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize)
        np.fill_diagonal(earliest_arrival_matrix, -1)  # Initialize every vertex reach itself at timestamp 0
        earliest_arrival_df = pd.DataFrame(data=earliest_arrival_matrix, columns=nodes_name, index=nodes_name)
        for i in graph_df.index:
            u = graph_df['i'][i]
            v = graph_df['j'][i]
            t = graph_df['t'][i]
            update_index = earliest_arrival_df[
                (earliest_arrival_df[u] < t) & (t < earliest_arrival_df[v])].index.tolist()
            earliest_arrival_df.loc[earliest_arrival_df.index.isin(update_index), v] = t
            update_index = earliest_arrival_df[
                (earliest_arrival_df[v] < t) & (t < earliest_arrival_df[u])].index.tolist()
            earliest_arrival_df.loc[earliest_arrival_df.index.isin(update_index), u] = t

        cols = earliest_arrival_df.columns
        r = earliest_arrival_df[cols].lt(sys.maxsize).sum(axis=1).max()
        return r, earliest_arrival_df

    @staticmethod
    def subgraph(layout, start, end, graph_df):
        # output the dataframe of subgraph
        subgraph_nodes = layout[start:end+1]
        nodes_set = set(subgraph_nodes)
        output_list = []
        for index in graph_df.index:
            if graph_df['i'][index] in nodes_set and graph_df['j'][index] in nodes_set:
                output_list.append((graph_df['i'][index], graph_df['j'][index], graph_df['t'][index]))
        output_df = pd.DataFrame(data=output_list, columns=['i', 'j', 't'])
        return output_df

    @staticmethod
    def span(layout, end, graph_df, output_list):
        subgraph_nodes = layout[0:end + 1]
        nodes_set = set(subgraph_nodes)
        update_df = graph_df.copy()
        for index in graph_df.index:
            if (graph_df['i'][index] in nodes_set and graph_df['j'][index] not in nodes_set) or \
               (graph_df['j'][index] in nodes_set and graph_df['i'][index] not in nodes_set):
                output_list.append((graph_df['i'][index], graph_df['j'][index], graph_df['t'][index]))
        for values in output_list:
            update_df.drop(update_df[(update_df.i == values[0]) &
                                     (update_df.j == values[1])].index, inplace=True)
        return output_list, update_df

    @staticmethod
    def dijkstra_subtree(graph_df, h):
        """
        :param graph_df: the temporal graph
        :param h: parameter
        :return: subtree whose reachability is h+1
        """
        # Get the list of nodes name.
        nodes_name = list(set(graph_df['i']).union(graph_df['j']))
        nodes_number = len(nodes_name)

        # Initialize one matrix named edge_df record the timestamp on each edge
        edge_df = pd.DataFrame(data=np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize),
                               columns=nodes_name,
                               index=nodes_name)
        for i in graph_df.index:
            edge_df[graph_df['i'][i]][graph_df['j'][i]] = graph_df['t'][i]
            edge_df[graph_df['j'][i]][graph_df['i'][i]] = graph_df['t'][i]

        # Output: Subtree of vertex with reachability is h + 1, if exist
        deleted_subtree = dict()
        break_f = 0
        for root in nodes_name:
            # it will iterate each node to find an node that reachability of subtree rooted at is h+1
            reachability = 1  # Every vertex can reach itself. Record the current maximum number
            unvisited_nodes = set(nodes_name)  # initialize the unvisited nodes
            unvisited_nodes.remove(root)
            current_subtree_edges = dict()  # record the subtree edges of current node(root)

            # record the earliest timestamp from root to each nodes
            time_df = pd.DataFrame(
                data=np.full(len(unvisited_nodes), fill_value=sys.maxsize).reshape(1, nodes_number - 1),
                columns=list(unvisited_nodes))
            tem_timestamp = -1
            break_w = 0
            candidate = set()
            candidate.add(root)
            root_of_subtree = root

            while len(candidate):
                candidate.remove(root)
                for i in edge_df[root].index:
                    # find the root's neighbor and update the len_df and edge_df
                    if i != root_of_subtree and \
                            i != root and edge_df[root][i] != sys.maxsize and \
                            edge_df[root][i] > tem_timestamp:
                        # this is the reachable neighbor of root
                        # update the time_df and len_df
                        if time_df[i][0] > edge_df[root][i]:
                            # reachability +1 only when the node
                            if time_df[i][0] == sys.maxsize:
                                reachability += 1
                                candidate.add(i)
                            time_df[i][0] = edge_df[root][i]
                            # update the subtree
                            path_to_node = []
                            if i in current_subtree_edges:
                                path_to_node = current_subtree_edges.get(i)
                            path_to_node.append((root, i, edge_df[root][i]))
                            current_subtree_edges.update({i: path_to_node})

                        # check the reachability for each index
                        if reachability == h + 1:
                            break_w = 1
                            break
                if break_w == 1:
                    break_f = 1
                    break
                tem_timestamp = sys.maxsize
                for n in candidate:
                    if tem_timestamp > time_df[n][0]:
                        root = n
                        tem_timestamp = time_df[n][0]

            if break_f == 1:
                deleted_subtree = current_subtree_edges
                break
        return deleted_subtree

    @staticmethod
    def draw_graph(df, file_path):
        """
        Draw temporal graph
        """
        temporal_graph = Graph(format='jpeg')
        temporal_graph.attr('node', shape='circle')
        nodelist = []
        for idx, row in df.iterrows():
            node1, node2, time = [str(i) for i in row]
            if node1 not in nodelist:
                temporal_graph.node(node1)
                nodelist.append(node2)
            if node2 not in nodelist:
                temporal_graph.node(node2)
                nodelist.append(node2)

            temporal_graph.edge(node1, node2, label=time)

        temporal_graph.render(str(file_path))

    @staticmethod
    def temporal_graph_matrix(df):
        nodes_name = list(set(df['i']).union(df['j']))
        graph_matrix = pd.DataFrame(data=np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize),
                                    columns=nodes_name,
                                    index=nodes_name)
        for i in df.index:
            graph_matrix[df['i'][i]][df['j'][i]] = df['t'][i]
            graph_matrix[df['j'][i]][df['i'][i]] = df['t'][i]
        return graph_matrix

    @staticmethod
    def delete_edge(etime_df, temporal_graph, h):
        """
        Find deleted edges according to delta approximation
        """
        edge_list = []
        # Count the reachability of each vertex
        reachability_series = etime_df[etime_df.columns].lt(sys.maxsize).sum(axis=1)
        reachability_df = reachability_series.to_frame()
        reachability_df.columns = ['reachability']
        # Get the vertex where reachability is the minimum value greater than h
        reachability_df = reachability_df[reachability_df['reachability'] > h]
        v = reachability_df['reachability'].idxmin()
        # Get the edge incident to that vertex has the largest time label
        graph_matrix = Algorithm.temporal_graph_matrix(temporal_graph)
        u = graph_matrix[graph_matrix.lt(sys.maxsize)][v].idxmax()
        t = graph_matrix[v][u]
        edge_list.append((v, u, t))
        return edge_list

    @staticmethod
    def reachable_edge_t(df, source, time_label):
        """
        Compute the REt(???G, T???, S, t)
        """
        delaying_edge_list = []
        reachability, time_df = Algorithm.find_reachability(df)
        time_df = time_df[time_df.index.isin(source)]
        time_df.drop(axis=1, labels=source, inplace=True)
        edge_df = Algorithm.temporal_graph_matrix(df)
        for index, row in time_df.iteritems():
            if time_df[index].min() == time_label:
                match_sources = edge_df[edge_df[index] == time_label].index.tolist()
                for vertex in match_sources:
                    remove_duplicate_set = set(delaying_edge_list)
                    item = (vertex, index)
                    item_reverse = (index, vertex)
                    if (item not in remove_duplicate_set) and (item_reverse not in remove_duplicate_set):
                        delaying_edge_list.append((vertex, index))

        return delaying_edge_list
