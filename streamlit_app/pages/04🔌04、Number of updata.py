import pandas as pd
import streamlit as st
import pandas
from pyecharts import options as opts
from pyecharts.charts import Bar
from streamlit_echarts import st_pyecharts
from module import readDF, queryBycategrot, GROUP_NAME
from config import DATA_SOURCE_PATH

st.title('Python 数据分析可视化交互 🎈')
st.write('')


def get_version_num(df):
    df['Version'] = df['versions'].map(len)
    return df.groupby('Version').size().to_frame('Number').reset_index()


df = readDF(DATA_SOURCE_PATH)
st.subheader('论文更新情况')

version_data = get_version_num(df)
compare_data = pandas.DataFrame({'Version': []})
for i in GROUP_NAME:
    single_version_data = get_version_num(queryBycategrot(df, i))
    single_version_data.rename(columns={'Number': i}, inplace=True)
    compare_data = pd.merge(compare_data, single_version_data, on='Version', how='outer')

graph_tab, data_tab, comparison_tab = st.tabs(['全部', '数据', '各类对比', ])
with graph_tab:
    c = (
        Bar()
        .add_xaxis(list(version_data['Version']))
        .add_yaxis(
            "个数",
            list(version_data['Number']),
            color="#00CD96",
            label_opts=opts.LabelOpts(position='top')
        )
        .set_global_opts(
            # 设置操作图表缩放功能，默认 x 轴
            datazoom_opts=opts.DataZoomOpts(type_="slider"),
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title='更新次数条形图')
        )
    )
    st_pyecharts(c, height='500px')
with data_tab:
    st.dataframe(version_data, use_container_width=True, hide_index=True)
with comparison_tab:
    st.bar_chart(compare_data, x='Version')
    with st.expander('🔯点击查看数据'):
        st.dataframe(compare_data, use_container_width=True, hide_index=True)
