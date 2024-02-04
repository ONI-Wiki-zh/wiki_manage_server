# 缺氧中文wiki管理
## 启动
### 初始化数据库

```shell
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py makemigrations WikiModel
python3 manage.py migrate WikiModel
```



### 加载wiki xml数据库

```shell
python3 manage.py load_wiki_xml
```



### 运行服务

```shell
python3 manage.py runserver
```

浏览器打开网址:

```
http://localhost:8000
```

