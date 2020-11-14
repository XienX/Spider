基于词频统计的英语同义词推荐系统--爬虫部分  
  
# 项目相关  
## 配置信息  
>python3.7  
>第三方库 pdfminer3k、retrying、python-dateutil  

## 文件信息  
>main.py 项目启动入口  
>spider.py 网页爬虫模块和单个pdf网页爬虫启动入口  
>pdf2txt.py pdf转txt模块   

## 注意事项  
>请确保数据存储文件夹下为空或只有上次运行留下的单个命名为年月的文件夹  
>数据存储文件夹下为空时默认爬取上月的数据  
>每月最多运行一次  
>  
>对单个pdf网址爬虫功能，爬取成功后不会保留pdf和txt文件

# 配置步骤  

### 1.确保有python环境（3.7或以上）  
### 2.安装第三方库  
>在命令行输入pip install pdfminer3k  
>在命令行输入pip install retrying  
>在命令行输入pip install python-dateutil  
### 3.编辑main.py  
>配置filePath为数据文件存放路径  
>配置dataProcessJar为数据处理程序jar包  
### 4.运行  
>在Web网页上点击按钮运行  

#### 或手动运行爬虫：
>`python main.py`进行批量数据爬取  
  
>`python spider.py [pdf网址]`进行单个pdf数据爬取  
>例如`python spider.py python spider.py https://export.arxiv.org/pdf/2010.00288.pdf`   
>或`python spider.py https://www.nature.com/articles/1001604.pdf?origin=ppub`  
>理论上对所有在浏览器端能正常打开的pdf网址都可运行  
>

