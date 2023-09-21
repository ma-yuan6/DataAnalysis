import pandas
import streamlit as st
import matplotlib.pyplot as plt

st.sidebar.markdown('Main page')


@st.cache_data
def readDF(fil_loc):
    data = pandas.read_pickle(fil_loc)
    return data


df = readDF(r'D:\学校\专业\Python数据分析\arxiv-metadata-oai-2019.pkl')
st.title('Python 数据分析可视化交互 🎈 ')
group_name = ['Computer Science', 'Economics', 'Electrical Engineering and Systems Science',
              'Mathematics', 'Physics', 'Quantitative Biology', 'Quantitative Finance',
              'Statistics']
st.write('')
st.write('各个类别论文数量')

group_num = []
for gr in group_name:
    group_num.append(df[df['group'].str.contains(gr)].shape[0])
color = plt.get_cmap('Set3')(range(len(group_num)))
plt.pie(group_num, labels=group_name, autopct='%0.1f%%', colors=color)
plt.pie(group_num)
st.pyplot(plt)

options = st.multiselect('选择论文类别:point_down:', group_name, ['Computer Science'])
options = sorted(options)
if len(options) > 1:
    st.write('同时分类为', '、'.join(options), '的数量为', df[df['group'] == '&&'.join(options)].size)
else:
    st.write('、'.join(options), '的数量为', df[df['group'] == '&&'.join(options)].size)


if st.checkbox('点击显示数据'):
    st.dataframe(df.groupby('group').size())
