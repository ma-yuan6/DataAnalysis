import pandas as pd
import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from module import readDF, queryBycategrot, GROUP_NAME
from config import DATA_SOURCE_PATH

st.title('Python 数据分析可视化交互 🎈')
st.write('')

df = readDF(DATA_SOURCE_PATH)

group_selected = st.selectbox('请在这里选择论文分类👇🏻', options=GROUP_NAME)
st.subheader(group_selected + ' 作者 TOP10')

auther_dic = {}
author_pages_dic = {'Auther': [], 'Amount': []}
group_df = queryBycategrot(df, group_selected)
# 获取所有作者的论文数量
for row in group_df.itertuples():
    authors = row.authors_parsed
    authors = [' '.join(reversed(au)) for au in authors]
    for i in authors:
        if auther_dic.get(i):
            auther_dic[i] += 1
        else:
            auther_dic[i] = 1
for au in auther_dic:
    author_pages_dic['Auther'].append(au)
    author_pages_dic['Amount'].append(auther_dic[au])
auther_pages_df = pd.DataFrame(author_pages_dic)
auther_pages_df = auther_pages_df.sort_values('Amount', ascending=False)

tabel_tab, data_tab = st.tabs(['表', '数据'])
with tabel_tab:
    colors = ["#d14a61", "#675bba"]
    # 获取前 10
    numberofpages = sorted(list(auther_pages_df['Amount'].head(10)), reverse=False)
    c = (
        Bar()
        .add_xaxis(list(auther_pages_df['Auther'].head(10)))
        .add_yaxis(group_selected, numberofpages)
        .reversal_axis()
        .set_global_opts(xaxis_opts=opts.AxisOpts(
            type_="value",
            name='论文数量',
            min_=0,
            max_=int(numberofpages[-1] / 10) * 10 + 10,
            offset=20,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color=colors[0])
            )),
            yaxis_opts=opts.AxisOpts(
                axisline_opts=opts.AxisLineOpts(
                    # linestyle_opts=opts.LineStyleOpts(color=colors[1])
                )
            ), tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
            # 设置颜色映射
            visualmap_opts=opts.VisualMapOpts(type_='color', min_=numberofpages[-1],
                                              max_=numberofpages[0],
                                              dimension=0, pos_left='75%'),
            legend_opts=opts.LegendOpts(is_show=False)
        )
    )
    st_pyecharts(c, height='600px')
# 数据
with data_tab:
    st.dataframe(auther_pages_df, use_container_width=True, hide_index=True)
