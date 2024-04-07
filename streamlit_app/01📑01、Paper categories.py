import pandas
import streamlit as st
import plotly.express as px
from pyecharts import options as opts
from pyecharts.charts import Pie
from streamlit_echarts import st_pyecharts
from config import DATA_SOURCE_PATH
from module import readDF, GROUP_NAME

st.title('Python 数据分析可视化交互 🎈')
st.write('')

df = readDF(DATA_SOURCE_PATH)

st.subheader('论文类别占比')

# 获取每大类的论文数量
group_num = []
for gr in GROUP_NAME:
    group_num.append(df[df['group'].str.contains(gr)].shape[0])
singale_catgr_data = pandas.DataFrame({'Group': GROUP_NAME, 'Amount': group_num})

graph_tab, data_tab = st.tabs(['图', '数据'])
with graph_tab:
    # 将数据转换为特定数据格式
    catgr_li = []
    for i in singale_catgr_data.itertuples():
        catgr_li.append([i.Group, i.Amount])
    # pyecharts 创建饼图
    c = (
        Pie()
        .add(
            "",
            catgr_li,
            radius=["35%", "70%"],
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b} {d}%"),
                         # 设置每个扇面圆角和 border 使得有分隔的效果
                         itemstyle_opts=opts.ItemStyleOpts(border_color='#fff', border_width=3, border_radius=10))
    )
    # 使用第三方支持, 在streamlit上绘制
    st_pyecharts(c, height='500px')
    # plotly 绘制
    with st.expander('plotly 实现'):
        fig = px.pie(singale_catgr_data, values='Amount', names='Group',
                     color_discrete_sequence=px.colors.sequential.RdBu)
        st.plotly_chart(fig, use_container_width=True)
# 数据
with data_tab:
    st.dataframe(singale_catgr_data, use_container_width=True, hide_index=True)

# 展示选择的论文类别
options = st.multiselect('选择论文类别👇🏻', GROUP_NAME, ['Computer Science'])
options = sorted(options)
if not options:
    st.warning('请选择论文类别', icon='🚨')
else:
    if len(options) > 1:
        st.write('同时分类为', '、'.join(options), '的数量为', df[df['group'] == '&&'.join(options)].shape[0])
    else:
        st.write('、'.join(options), '的数量为', df[df['group'] == '&&'.join(options)].shape[0])
st.write('')

# 展示所有论文类别
with st.expander('🔯点击显示数据'):
    st.write('')
    st.write('这里包括了所有论文的分类')
    group_df = df.groupby('group').size().to_frame().reset_index().sort_values(0, ascending=False)
    # 将 && 连接的字符串变为列表
    group_df['group'] = group_df['group'].map(lambda x: x.split('&&'))
    group_df.columns = ['Groups', 'Amount']
    # 使用 st.column_config 改变 Group 列样式
    st.dataframe(group_df, use_container_width=True, column_config={'论文大类': st.column_config.ListColumn()},
                 hide_index=True)
