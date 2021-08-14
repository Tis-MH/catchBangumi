## 项目介绍
### 运行过程
1. 通过scrapy 抓取内容并放入redis(或其他数据库)
2. 通过background 构建app对象
3. app 对象中方法能够访问数据库中数据并对其操作(对象方法)

### scrapy 抓取方法
#### 方法1:
更改`tutorial/tutorial/spiders/kisssub.py`中的`start_url` 然后运行 `scrapy crawl kisssub` 爬取
#### 方法2:
使用scrapyrt 启动后使用background scrapyrt 方法抓取(应该未完成)

### 项目概览
应用拥有两个数据库
公共数据库和私有数据库  
公共数据库用来存储服务器端抓取的所用数据, 并提供给所用用户  
私有数据库为用户私有, 用于存放用户自己的数据, 如已经下载的番剧, 追番等.

