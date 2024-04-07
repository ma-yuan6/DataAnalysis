import altair as alt
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line
import streamlit as st
from streamlit_echarts import st_pyecharts
from module import readDF, queryBycategrot, GROUP_NAME
from config import DATA_SOURCE_PATH

st.title('Python 数据分析可视化交互 🎈 ')
st.write('')

df = readDF(DATA_SOURCE_PATH)

st.subheader('各月总论文发表数量')
# 获取每月总论文数量
df['Month'] = df['update_date'].map(lambda x: x.split('-')[1] + '月')
moth_data = df.groupby('Month').size().to_frame('Amount')
moth_data.reset_index(inplace=True)


data_show = pd.DataFrame()
# 获取每个大类的每月论文数量
for op in GROUP_NAME:
    opdata = queryBycategrot(df, op).groupby('Month').size().to_frame(op)
    data_show = data_show.join(opdata, how='outer', sort=False)
data_show.reset_index(inplace=True)
# 将数据反透视为特定格式
melt_data = data_show.melt(id_vars='Month')
melt_data.rename({'variable': 'Group', 'value': 'Amount'}, axis=1, inplace=True)

grap_tab, Bubble_tab, data_tab = st.tabs(['时序图', '气泡图', '数据'])
# 绘制折线图
with grap_tab:
    st.line_chart(moth_data, x='Month')
# 绘制气泡图
with Bubble_tab:
    c = (alt.Chart(melt_data).mark_circle(
        opacity=0.8,
        stroke='black',
        strokeWidth=1,
        strokeOpacity=0.4
    ).encode(
        alt.X('Month')
        .title('Month'),
        alt.Y('Group:N')
        .title('Group')
        # 按平均值排序
        .sort(field="Amount", op="sum", order='descending'),
        alt.Size('Amount')
        .scale(range=[0, 3000])
        .title('Amounts')
        .legend(clipHeight=28, format='s'),
        alt.Color('Group:N').legend(None),
        tooltip=[
            "Group:N",
            alt.Tooltip("Month"),
            alt.Tooltip("Amount:Q", format='~s'),
        ],
    ).configure_axisY(
        domain=False,
        ticks=False,
    ).configure_axisX(
        grid=False,
    ).configure_view(
        stroke=None
    ))
    st.altair_chart(c, use_container_width=True)
# 数据
with data_tab:
    st.dataframe(moth_data, use_container_width=True, hide_index=True)

st.subheader('各月论文发表数量对比')
st.write('')

# 绘制区域图
line_chart = Line().add_xaxis(xaxis_data=data_show['Month'])
# 循环加入每一行
for i, chat in enumerate(GROUP_NAME):
    line_chart.add_yaxis(
        series_name=chat,
        stack='数量',
        y_axis=data_show[chat],
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
        label_opts=opts.LabelOpts(is_show=False),
    )
# 设置样式
line_chart.set_global_opts(
    tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    yaxis_opts=opts.AxisOpts(
        type_="value",
        axistick_opts=opts.AxisTickOpts(is_show=True),
        splitline_opts=opts.SplitLineOpts(is_show=True),
    ),
    xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),
    legend_opts=opts.LegendOpts(border_width=0, pos_left='left'),
)
st_pyecharts(line_chart, height='500px')

with st.expander('🔯点击显示数据'):
    st.dataframe(data_show, use_container_width=True, hide_index=True)
