import pandas as pd
import streamlit as st
import pandas
from pyecharts import options as opts
from pyecharts.charts import Graph
import networkx as nx
from streamlit_echarts import st_pyecharts
from module import readDF, queryBycategrot, GROUP_NAME
from config import DATA_SOURCE_PATH

st.title('Python 数据分析可视化交互 🎈')
st.write('')

df = readDF(DATA_SOURCE_PATH)
st.subheader('每个类别最大联通图')
select_group = st.selectbox('请在这里选择论文分类👇🏻', ['Economics', 'Quantitative Biology', 'Quantitative Finance'])
sub_number = st.slider('请选择要显示第几个连通图:', min_value=1, max_value=20)
st.write('')

group = queryBycategrot(df, select_group)
group = group[~ group['submitter'].isnull()]
nodes = []
links = []
# 创建网络
G = nx.Graph()
max_len = 0
for row in group.itertuples():
    submitter = row.submitter
    authors = row.authors_parsed
    authors = [' '.join(reversed(au)) for au in authors]
    if len(authors) > max_len:
        max_len = len(authors)
    for i in authors:
        if i != submitter:
            # 添加节点
            G.add_edge(submitter, i)
# 排序
C = sorted(nx.connected_components(G), key=len, reverse=True)
# 选出连通图
sub_G = G.subgraph(C[sub_number - 1])  # 因为第一个对应的下标是 0
# 转换为列表
nodes = list(map(lambda x: opts.GraphNode(name=x[0], symbol_size=x[1] * 5),
                 list(sub_G.degree)))
links = list(map(lambda x: opts.GraphLink(source=x[0], target=x[1]), list(sub_G.edges)))
# 创建图
c = (
    Graph()
    .add("", nodes, links, layout="circular",
         is_rotate_label=True,
         linestyle_opts=opts.LineStyleOpts(color="source", curve=0.3),
         label_opts=opts.LabelOpts(position="right"),
         )
    .set_global_opts(title_opts=opts.TitleOpts(title=select_group + ' 的作者关系图'),
                     legend_opts=opts.LegendOpts(is_show=False),
                     )
)
# 绘图
st_pyecharts(c, height='600px')

with st.expander('🔯点击查看各类作者信息'):
    gr_author_df = pd.read_csv('output/auther.csv')
    st.dataframe(gr_author_df, use_container_width=True, hide_index=True)
