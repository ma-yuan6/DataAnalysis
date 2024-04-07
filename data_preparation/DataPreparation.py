from json import loads
import pandas as pd
from streamlitAPP.config import JSON_FILE_PATH, TRANSFORM_DATA_PATH


# 不是完整的 json,是一个 json 集合。 不能直接使用 pd.read_json ,所以创建函数读取数据
def readJsonFile(path, column=['id', 'submitter', 'authors', 'title', 'comments', 'journal-ref', 'doi',
                               'report-no', 'categories', 'license', 'abstract', 'versions',
                               'update_date', 'authors_parsed']):
    data = []
    with open(path) as f:
        for line, json in enumerate(f):
            data.append({col: loads(json)[col] for col in column})
    return pd.DataFrame(data)


# 根据第三个级别的分类简写找出它所在的大类
def groupOFcatANDarc(level_tabel, categroy):
    groupOFcate = level_tabel[level_tabel['categories'] == categroy].values
    if len(groupOFcate) == 0:
        # 有一些是 level2
        groupOFcate = level_tabel[level_tabel['archive_id'] == categroy].values
    if len(groupOFcate) == 0:
        return ''
    print(groupOFcate[0][0])
    return groupOFcate[0][0]


def find_level1(level3, leveltabel):
    print('--' * 50)
    cats_list = level3.split()
    print(cats_list)
    if len(cats_list) == 1:  # 测试过了, 不存在空值
        group = groupOFcatANDarc(leveltabel, cats_list[0])
        return group
    # 一篇论文存在多个 level3
    else:
        group_list = []
        for k in cats_list:
            group_list.append(groupOFcatANDarc(leveltabel, k))
        group_list = list(set(group_list))
        # 排序防止同一类别导致不一样
        group_list.sort()
        group = '&&'.join(group_list).strip('&&')
        print('>>', group)
        return group


if __name__ == '__main__':
    data = readJsonFile(JSON_FILE_PATH)
    leve_tabel = pd.read_csv('../source/categorys.csv')
    data['group'] = data['categories'].apply(find_level1, args=(leve_tabel,))
    data[
        ['group', 'submitter', 'title', 'comments', 'abstract', 'versions', 'authors_parsed', 'update_date']].to_pickle(
        TRANSFORM_DATA_PATH + 'arxiv-metadata-oai-2019.pkl')
    print('数据准备完成！！！')
