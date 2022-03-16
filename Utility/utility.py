import numpy as np
import pandas as pd
import sys


class Algorithm:
    @staticmethod
    def check_reachability(graph_df):
        # return the reachability of the graph
        # Get the list of nodes name
        nodes_name = list(set(graph_df['i']).union(graph_df['j']))
        # Sort by timestamp on each edge
        graph_df = graph_df.sort_values(by=['t'])
        # The  earliest_arrival  matrix is nXn matrix. Each cell record the earliest arrival time between two nodes
        earliest_arrival_matrix = np.full((len(nodes_name), len(nodes_name)), fill_value=sys.maxsize)
        np.fill_diagonal(earliest_arrival_matrix, 0)  # Initialize every vertex reach itself at timestamp 0
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
        return r

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
    def span(layout, end, graph_df):
        subgraph_nodes = layout[0:end + 1]
        nodes_set = set(subgraph_nodes)
        output_list = []
        update_df = graph_df.copy()
        for index in graph_df.index:
            if (graph_df['i'][index] in nodes_set and graph_df['j'][index] not in nodes_set) or \
               (graph_df['j'][index] in nodes_set and graph_df['i'][index] not in nodes_set):
                output_list.append((graph_df['i'][index], graph_df['j'][index]))
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

            # record length of the shortest temporal path from root to each nodes
            len_df = pd.DataFrame(
                data=np.full(len(unvisited_nodes), fill_value=sys.maxsize).reshape(1, nodes_number - 1),
                columns=list(unvisited_nodes))
            # record the earliest timestamp from root to each nodes
            time_df = pd.DataFrame(
                data=np.full(len(unvisited_nodes), fill_value=sys.maxsize).reshape(1, nodes_number - 1),
                columns=list(unvisited_nodes))
            tem_timestamp = -1
            tem_length = 0
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
                        change_flag = 0  # indicate if it needs update the subtree
                        if time_df[i][0] > edge_df[root][i]:
                            # reachability +1 only when the node
                            if time_df[i][0] == sys.maxsize:
                                reachability += 1
                                candidate.add(i)
                            time_df[i][0] = edge_df[root][i]
                            len_df[i][0] = tem_length + 1
                            change_flag = 1
                        elif (time_df[i][0] == edge_df[root][i]) and (len_df[i][0] > tem_length + 1):
                            len_df[i][0] = tem_length + 1
                            change_flag = 1
                        # update the subtree
                        if change_flag == 1:
                            path_to_node = []
                            if i in current_subtree_edges:
                                path_to_node = current_subtree_edges.get(i)
                            path_to_node.append((root, i))
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
                        tem_length = len_df[n][0]
            if break_f == 1:
                deleted_subtree = current_subtree_edges
                break

        return deleted_subtree
