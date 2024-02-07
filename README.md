# 缺氧中文wiki管理

## 快速开始

1. 系统已安装python3.x开发环境

2. 浏览器访问wiki站点上标题为`Special:统计`的[页面](https://oxygennotincluded.fandom.com/zh/wiki/Special:%E7%BB%9F%E8%AE%A1)，下载wiki站点的全站备份数据。

3. 解压下载的`.zip`压缩包后，复制`.xml`文件至项目根目录下的`data_output`目录下。

   打开命令窗口（mac系统打开Terminal），进入项目根目录下。运行配置脚本。

   ```shell
   sh install.sh
   ```

4. 脚本运行结束后，输入命令，启动服务

   ```shell
   python3 manage.py runserver
   ```
   
   根据提示，复制网址，在浏览器打开。
   
   

## 手动运行步骤

### 安装python3.x

在安装 Django 前，系统需要已经安装了 Python 的开发环境。

如果你还没有安装 Python，请先从 Python 官网 https://www.python.org/ 下载并安装Python3.x的版本。

安装完后，可以使用以下命令来判断安装是否完成

```shell
python3 --version
pip3 --version
```



### 安装Django依赖

打开shell命令窗口(mac系统打开Terminal)，进入到项目所在的目录中。

使用包管理工具pip安装项目所需的依赖，输入以下安装命令。

```shell
pip3 install Django
pip3 install xmltodict
```

安装完成后，你可以通过运行以下命令验证 Django 是否成功安装：

```
python3 -m django --version
```

如果一切顺利，你将看到安装的 Django 版本号，如：**4.2.7**。

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

3. 将下载下来的`.zip`文件解压，将其中的`.xml`文件复制至项目根目录下的`data_input`目录下。

4. 在项目目录下，执行命令

```shell
python3 manage.py load_wiki_xml
```



### 部署前端项目

1. 打开*缺氧中文管理前端项目*，打包项目。

2. 打包完成后，将*缺氧中文管理前端项目*下的`dist`目录，复制至*缺氧中文管理后端项目*的`根目录`下。



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

在项目根目录下，打开Terminal，运行以下指令

```shell
python3 manage.py createsuperuser
```

根据提示输入管理员的`用户名`和`密码`。

完成配置后，在浏览器打开网址：

```
http://localhost:8000/admin
```

