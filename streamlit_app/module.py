import streamlit as st
import pandas as pd


@st.cache_data
def readDF(fil_loc):
    data = pd.read_pickle(fil_loc)
    return data


# 根据大类选出相对应的数据
@st.cache_data
def queryBycategrot(data, categrot):
    """
    根据类别查询数据的函数。

    参数：
        - data：要查询的数据。
        - categrot：要按照的类别进行过滤的字符串。

    返回：
        - 根据指定类别过滤后的数据。
    """
    return data[data['group'].str.contains(categrot)]


GROUP_NAME = ['Computer Science', 'Economics', 'Electrical Engineering and Systems Science',
              'Mathematics', 'Physics', 'Quantitative Biology', 'Quantitative Finance', 'Statistics']
