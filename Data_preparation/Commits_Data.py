import re
import pandas as pd
from streamlitAPP.config import DATA_SOURCE_PATH


def queryBycategrot(data, categrot):
    return data[data['group'].str.contains(categrot)]


# 生成描述信息
def get_description(df, opt):
    group_name = ['Computer Science', 'Economics', 'Electrical Engineering and Systems Science',
                  'Mathematics', 'Physics', 'Quantitative Biology', 'Quantitative Finance', 'Statistics']
    page_descriptions = {'Group': [], 'Len': [], 'Count': [], 'Percentage': [], 'Mean': [], 'Std': [], 'Min': [],
                         '25%': [],
                         '50%': [], '75%': [], 'Max': []}
    for i in group_name:
        gr_comments_df = queryBycategrot(df, i)
        re_str = '[1-9][0-9]* *' + opt
        gr_comments_df['pages'] = gr_comments_df['comments'].map(lambda x: re.findall(re_str, str(x)))
        # data_1 = gr_comments_df.copy()
        # data_1 = data_1[data_1['pages'].apply(len) > 0]
        ownpages_df = gr_comments_df.copy()
        ownpages_df = ownpages_df[ownpages_df['pages'].apply(len) > 0]
        ownpages_df['pages'] = ownpages_df['pages'].apply(lambda x: float(x[0].replace(opt, '')))
        gr_desc = ownpages_df['pages'].describe().astype(int)
        page_descriptions['Group'].append(i)
        page_descriptions['Len'].append(gr_comments_df.shape[0])
        page_descriptions['Count'].append(gr_desc['count'])
        page_descriptions['Percentage'].append(int((gr_desc['count'] / gr_comments_df.shape[0]) * 100) / 100)
        page_descriptions['Mean'].append(gr_desc['mean'])
        page_descriptions['Std'].append(gr_desc['std'])
        page_descriptions['Min'].append(gr_desc['min'])
        page_descriptions['25%'].append(gr_desc['25%'])
        page_descriptions['50%'].append(gr_desc['50%'])
        page_descriptions['75%'].append(gr_desc['75%'])
        page_descriptions['Max'].append(gr_desc['max'])
        page_descriptions['Mean'] = page_descriptions['Mean']
    return pd.DataFrame(page_descriptions)


# 生成具体数据
def get_datasofcommits(df, opt):
    group_name = ['Computer Science', 'Economics', 'Electrical Engineering and Systems Science',
                  'Mathematics', 'Physics', 'Quantitative Biology', 'Quantitative Finance', 'Statistics']
    page_data = pd.DataFrame()
    for i in group_name:
        gr_comments_df = queryBycategrot(df, i)
        re_str = '[1-9][0-9]* *' + opt
        gr_comments_df['pages'] = gr_comments_df['comments'].map(lambda x: re.findall(re_str, str(x)))
        # data_1 = gr_comments_df.copy()
        # data_1 = data_1[data_1['pages'].apply(len) > 0]
        ownpages_df = gr_comments_df.copy()
        ownpages_df = ownpages_df[ownpages_df['pages'].apply(len) > 0]
        ownpages_df['pages'] = ownpages_df['pages'].apply(lambda x: float(x[0].replace(opt, '')))
        page_data[i] = ownpages_df['pages']
    return page_data.melt()


if __name__ == '__main__':
    all_df = pd.read_pickle(DATA_SOURCE_PATH)
    for i in ['pages', 'tables', 'figures']:
        desc_df = get_description(all_df, i)
        desc_df.to_csv(f'../output/{i}-descriptions.csv', index=False)
        desc_data_df = get_datasofcommits(all_df, i)
        desc_data_df.to_csv(f'../output/{i}-data.csv', index=False)
        print('论文信息提取成功！！！')