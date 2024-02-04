# 缺氧中文wiki管理
## 启动
### 初始化数据库

```shell
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations WikiModel
python3 manage.py migrate WikiModel
```



### 加载wiki备份数据

1. 浏览器访问wiki站点上标题为`Special:统计`的[页面](https://oxygennotincluded.fandom.com/zh/wiki/Special:%E7%BB%9F%E8%AE%A1)，找到`数据库转储`。

- 点击`当前和历史页面`这一行是日期格式的超链接文本。
- 或者点击`当前页面`这一行是日期格式的超链接文本。

2. 下载wiki站点的备份数据。下载完成后，得到格式为`.zip`的文件。

3. 打开目录`data_input`，将下载下来的`.zip`文件解压，将其中的`.xml`文件复制至该目录下。

4. 在项目目录下，执行命令

```shell
python3 manage.py load_wiki_xml
```



### 运行服务

运行命令，运行服务

```shell
python3 manage.py runserver
```

在浏览器中打开网址:

```
http://localhost:8000
```



## 服务器管理

### 创建一个超级管理员

```shell
python3 manage.py createsuperuser
```