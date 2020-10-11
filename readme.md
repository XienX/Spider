基于词频统计的英语同义词推荐系统--爬虫部分  
未完成
  
# 项目相关  
## 配置信息  
>python3.7  
>第三方库 pdfminer3k、retrying  

## 文件信息  
>main.py 项目启动入口  
>spider.py 下载pdf文件模块  
>pdf2txt.py pdf转txt模块  
>spider.bat  用于在windows上配置定时任务  

## 注意事项
>爬虫会在指定文件存放路径下生成配置文件config.txt

# 配置步骤  

### 1.确保有python环境（3.7或以上）  
### 2.安装第三方库  
>在命令行输入pip install pdfminer3k  
>在命令行输入pip install retrying
### 3.编辑main.py  
>配置filePath为文件存放路径  
>配置dataProcessPath为数据处理程序入口  
### 4.在Windows下配置定时任务  
>编辑spider.bat中的路径和时间  
>路径为Spider项目的绝对路径，时间为希望每天启动爬虫的时间  
>双击运行spider.bat即可
>可在Windows 10 的任务计划程序中查看是否配置成功  

#### 或手动运行爬虫：
`python main.py`
