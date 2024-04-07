import pandas as pd
import streamlit as st
from PIL import Image
from module import readDF, queryBycategrot, GROUP_NAME
from config import DATA_SOURCE_PATH

st.title('Python 数据分析可视化交互 🎈 ')
st.write('')
st.subheader('论文标题及概要词云图')


# 定义统计函数
def word_count(txt):
    word_dic = {}
    for ch in '''!"$%&()*+,-./;:<=>?@[\\]^_{|}~''\n\t ''':
        txt = txt.replace(ch, ' ')
    for word in txt.split(' '):
        word = word.lower()
        if word_dic.get(word):
            word_dic[word] += 1
        else:
            word_dic[word] = 1
    return word_dic


# 使用停词库过滤掉部分无用词
def wordsfilter(word_dic):
    stopwords = []
    # 读取停词库
    with open('source/stopwords.txt') as f:
        for word in f:
            stopwords.append(word.split('\n')[0])
    for word in list(word_dic.keys()):  # 不能在遍历字典的同时修改字典, 所以转换成 list
        if word in stopwords:
            del word_dic[word]
    # 字典可以使用空字符串来作为 key 所以需要特殊处理一下
    del word_dic['']


# worldcloud 库 实现词云图
def creat_wordcloudImg(word_dic, file_name, word_num=50):
    import wordcloud
    img = wordcloud.WordCloud(background_color='white', font_path='msyh.ttc', width=2000, height=1500,
                              max_words=word_num).generate_from_frequencies(word_dic)
    img.to_file(f'output/{file_name}.png')


def word_count2df(column, data, word_num, if_filter=True):
    word_dic = {}
    process_prompt = {'title': '标题词云图生成中, 请等待...', 'abstract': '概要词云图生成中, 请等待...'}
    bar = st.progress(0, text=process_prompt[column])
    total_procass = data.shape[0]
    procsss = 0
    for i in data[column]:
        procsss += 1
        bar.progress(procsss / total_procass, text=process_prompt[column])
        for word in word_count(i):
            if word_dic.get(word):
                word_dic[word] += 1
            else:
                word_dic[word] = 1
    bar.empty()
    if if_filter:
        wordsfilter(word_dic)
    # 排序
    # print(sorted(word_dic.items(), key=lambda x: x[1], reverse=True))
    # 创建词云图
    creat_wordcloudImg(word_dic, column, word_num=word_num)

    words_data = {'word': [], 'amount': []}
    for t in word_dic:
        words_data['word'].append(t)
        words_data['amount'].append(word_dic[t])
    return pd.DataFrame(words_data).sort_values(by='amount', ascending=False)


df = readDF(DATA_SOURCE_PATH)

# 侧边栏
op = st.selectbox('请在这里选择论文分类👇🏻', options=GROUP_NAME)
word_number = st.slider('选择要生成的单词数量', max_value=200)
row = st.sidebar.number_input('在这里调整行数🗒️', min_value=5, max_value=170618, step=1)
if_filter = st.sidebar.toggle('过滤无意义词', value=True)

if word_number > 0:
    data_categrot = queryBycategrot(df, op)[['title', 'abstract']]
    title_word_data = word_count2df('title', data_categrot.head(row), word_number, if_filter=if_filter)
    abstract_word_data = word_count2df('abstract', data_categrot.head(row), word_number, if_filter=if_filter)
    st.success('词云图生成成功！', icon='🎉')
    # 词云图
    with st.expander('👀查看生成的词云图'):
        title_img_tab, abstract_img_tab = st.tabs(['标题词云图', '概要词云图'])
        with title_img_tab:
            image = Image.open('output/title.png')
            st.image(image)
        with abstract_img_tab:
            image = Image.open('output/abstract.png')
            st.image(image)
    # 单词数据
    with st.expander('🔯点击这里查看单词数量'):
        title_data_tab, abstract_data_tab = st.tabs(['标题', '概要'])
        with title_data_tab:
            st.dataframe(title_word_data, use_container_width=True, hide_index=True)
        with abstract_data_tab:
            st.dataframe(abstract_word_data, use_container_width=True, hide_index=True)
else:
    st.warning('请设置单词数量', icon='🚨')
