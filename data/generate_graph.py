import random
import pandas as pd
num_nodes = 100
nodelist = list(range(1, num_nodes + 1))
edge_list = []
for u in nodelist:
    for v in nodelist:
        rand = random.randint(5, 50)
        if rand >= 25:
            break
        if u == v:
            break
        else:
            rand = random.randint(1, 100)
            edge_list.append(('v'+str(u), 'v'+str(v), rand))
df = pd.DataFrame(edge_list, columns=['i', 'j', 't'])
df.to_csv('test.csv', index=False)
