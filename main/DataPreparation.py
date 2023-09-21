from json import loads
import pandas as pd


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
def find_level1(level3, leveltabel):
    leveq = level3
    level3 = level3.split(' ')[0]
    if len(leveltabel[leveltabel['categories'] == level3].values) == 0:
        level1 = leveltabel[leveltabel['archive_id'] == level3]['group_name']
    else:
        level1 = leveltabel[leveltabel['categories'] == level3]['group_name']
    if len(level1) == 0:
        print(leveq)
        return 'Not Exit'
    else:
        return level1.values[0]


if __name__ == '__main__':
    data = readJsonFile('../../arxiv-metadata-oai-2019.json', )
    leve_tabel = pd.read_csv('../source/categorys.csv')
    data['group'] = data['categories'].apply(find_level1, args=(leve_tabel,))
    # data.to_pickle('../../arxiv-metadata-oai-2019.pkl')
