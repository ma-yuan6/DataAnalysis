import os
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd

if not os.path.exists('../output/category.html'):
    if not os.path.exists('../output'):
        os.mkdir('../output')

    print('正在请求网页...')
    web_data = requests.get('https://arxiv.org/category_taxonomy').text

    # 存储请求的网页文件
    with open('../output/category.html', mode='w', encoding='utf-8') as f:
        f.write(web_data)
    print('网页请求成功, 正在解析网页...')

with open('../output/category.html') as f:
    web_data = f.read()

soup = BeautifulSoup(web_data, features='xml')
root = soup.find('div', attrs={'id': 'category_taxonomy_list'})

root.find_all(['h2', 'h3', 'h4', ])

tags = root.find_all(["h2", "h3", "h4", "p"], recursive=True)  # 因为要读取孙子辈，所以加 recursive参数
# print(tags)

level_1_name = ""
level_2_name = ""
level_2_code = ""
level_1_names = []
level_2_codes = []
level_2_names = []
level_3_codes = []
level_3_names = []
level_3_notes = []

# 进行
for t in tags:
    if t.name == "h2":
        level_1_name = t.text
        level_2_code = t.text
        level_2_name = t.text
    elif t.name == "h3":
        raw = t.text
        level_2_code = re.sub(r"(.*)\((.*)\)", r"\2", raw).strip()  # 正则表达式：模式字符串：(.*)\((.*)\)；被替换字符串"\2"；被处理字符串：raw
        level_2_name = re.sub(r"(.*)\((.*)\)", r"\1", raw).strip()
    elif t.name == "h4":
        raw = t.text
        level_3_code = re.sub(r"(.*) \((.*)\)", r"\1", raw).strip()
        level_3_name = re.sub(r"(.*) \((.*)\)", r"\2", raw).strip()
    elif t.name == "p":
        notes = t.text
        level_1_names.append(level_1_name)
        level_2_names.append(level_2_name)
        level_2_codes.append(level_2_code)
        level_3_names.append(level_3_name)
        level_3_codes.append(level_3_code)
        level_3_notes.append(notes)

# 根据以上信息生成dataframe格式的数据
df_taxonomy = pd.DataFrame({
    'group_name': level_1_names,
    'archive_name': level_2_names,
    'archive_id': level_2_codes,
    'category_name': level_3_names,
    'categories': level_3_codes,
    'category_description': level_3_notes

})

# 按照 "group_name" 进行分组，在组内使用 "archive_name" 进行排序
df_taxonomy.sort_values(["group_name", "archive_name"]).iloc[:-1, :].to_csv('../source/categorys.csv', index=False)
print('数据保存成功!')
