# 介绍
Python 数据分析及可视化交互。

1. 使用 request + BeautifulSoup 实现网站数据爬取及解析 
2. 使用 pandas 分析数据 
3. 使用 streamlit 搭建网页应用实现交互
4. 使用 networkx 构建关系网
5. 使用 wordcloud 绘制词云图 
6. 使用 altair、plotly、pyecharts 绘制图形


# 项目结构
- . /Jupyter_source下主要是一些分析步骤
- . /source 包括一些辅助文件停词库和爬取的数据
- . /Data_preparation 下主要是数据预处理，并保存
- . /streamlitAPP 主要是 Web 应用运行文件以及配置文件
- . /output 用于存放输出的图片以及数据


# 项目运行步骤
1、使用当前环境或者使用 Anaconda 创建虚拟环境
~~~
conda create --name environment_name python=3.6
~~~
2、下载依赖
~~~
pip download -r requirements.txt
~~~
速度慢的可以使用国内源
~~~
pip download -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
~~~
3、源数据283MB就不上传了（可联系作者获取 QQ：311064561）你需要将 . /streamlitAPP  下的config.py 中的JSON_FILE_PATH 改为你 JSON 文件的位置。TRANSFORM_DATA_PATH 的位置改为你需要将数据输出的位置。

4、依次运行 Data_preparation 文件夹中的 `Crawler.py`、`DataPreparation.py`、`Commits_Data.py`、`Authors_data.py`文件。
过程中可能会出现警告，不用管它，只要最后打印执行成功就行。

5、在控制台运行下面命令

~~~
 streamlit run '.\streamlitAPP\01📑01、Paper categories.py'
~~~
