import pandas as pd
import networkx as nx
from streamlitAPP.config import DATA_SOURCE_PATH
from streamlitAPP.module import GROUP_NAME, queryBycategrot

df = pd.read_pickle(DATA_SOURCE_PATH)
gr_author_dic = {'Group': [], 'Nodes': [], 'Edges': [], 'Author': [], 'Collaborators': []}
for group in GROUP_NAME:
    group_df = queryBycategrot(df, group)
    # ~ 表示取反
    group_df = group_df[~ group_df['submitter'].isnull()]
    # 创建网络
    G = nx.Graph()
    for row in group_df.itertuples():
        submitter = row.submitter
        authors = row.authors_parsed
        authors = [' '.join(reversed(au)) for au in authors]
        for i in authors:
            if i != submitter:
                G.add_edge(submitter, i)
    C = sorted(nx.connected_components(G), key=len, reverse=True)
    sub_G = G.subgraph(C[0])
    gr_author_dic['Group'].append(group)
    gr_author_dic['Nodes'].append(len(sub_G.nodes))
    gr_author_dic['Edges'].append(len(sub_G.edges))
    gr_author_dic['Author'].append(max(sub_G.degree, key=lambda x: x[1])[0])
    gr_author_dic['Collaborators'].append(max(sub_G.degree, key=lambda x: x[1])[1])
    gr_author_df = pd.DataFrame(gr_author_dic)
gr_author_df.to_csv('../output/auther.csv', index=False)
print('作者信息提取成功！！！')