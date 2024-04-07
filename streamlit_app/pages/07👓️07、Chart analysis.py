import pandas as pd
import streamlit as st
from pyecharts import options as opts
from pyecharts.charts import Radar
import plotly.express as px
from streamlit_echarts import st_pyecharts  # streamlit 的 pyecharts 第三方支持

st.title('Python 数据分析可视化交互 🎈')
st.write('')

page_descriptions_df = pd.read_csv('output/pages-descriptions.csv')
figure_descriptions_df = pd.read_csv('output/figures-descriptions.csv')
table_descriptions_df = pd.read_csv('output/tables-descriptions.csv')

st.subheader('各类别论文页数、图、表的描述信息')

# 定义不同类别的颜色
colors = [['#FF917C'], ['#56A3F1'], ['#67F9D8']]
# 创建 RadarIndicatorItem 对象的列表
sec = [opts.RadarIndicatorItem(name=i, min_=0, max_=30) for i in page_descriptions_df['Group']]

# 生成雷达图
c = (
    Radar()
    .add_schema(
        schema=sec,
        start_angle=180,
    )
    .add('论文', [list(page_descriptions_df['Mean'])], color=colors[0])
    .add('图', [list(figure_descriptions_df['Mean'])], color=colors[1])
    .add('表', [list(table_descriptions_df['Mean'])], color=colors[2])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False), areastyle_opts=opts.AreaStyleOpts(
        opacity=0.5,
    ), linestyle_opts=opts.LineStyleOpts(width=2))
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=True, trigger='item'),
        legend_opts=opts.LegendOpts(border_width=0)
    )
)
st_pyecharts(c, height='600px')

with st.expander('点击展开箱线图'):
    tabs = st.tabs(['页数箱线图', '图箱线图', '表箱线图'])
    for i, tab in enumerate(tabs):
        with tab:
            t = ['pages', 'figures', 'tables'][i]
            page_data = pd.read_csv(f'output/{t}-data.csv')
            fig_page = px.box(page_data, x="variable", y="value")
            st.plotly_chart(fig_page, use_container_width=True)

with st.expander('🔯点击查看各类别论文页数、图、表的描述信息'):
    page_tab, figure_tab, table_tab = st.tabs(['页数', '图', '表'])
    with page_tab:
        st.dataframe(page_descriptions_df, use_container_width=True, hide_index=True)

    with figure_tab:
        st.dataframe(figure_descriptions_df, use_container_width=True, hide_index=True)

    with table_tab:
        st.dataframe(table_descriptions_df, use_container_width=True, hide_index=True)
