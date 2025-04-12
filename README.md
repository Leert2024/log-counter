# 中国大学生计算机设计大赛
## 简介
本项目是中国大学生计算机设计大赛的参赛作品，是一个负责统计电商平台网站访问量与商品热度的、基于B/S架构的Web应用程序。
本项目使用python编写，使用Flask框架进行Web开发，使用grpc进行远程过程调用，使用sqlite3进行数据库管理。项目结构的示意图请见[项目结构图](notes/项目结构图.bmp)。
需注意，本项目为分布式架构中的一部分，仅负责统计网站访问量与商品热度，而产品的主要功能则由项目组内其他成员负责。

## 项目结构
```
中国大学生计算机设计大赛
├─ 📁app
│  ├─ 📁static
│  │  └─ 📁images
│  │     ├─ 📄apple-touch-icon -precomposed.png
│  │     ├─ 📄apple-touch-icon.png
│  │     └─ 📄favicon.ico
│  ├─ 📁templates
│  │  ├─ 📄dashboard.html
│  │  ├─ 📄login.html
│  │  └─ 📄welcome.html
│  ├─ 📄app.py
│  └─ 📄provide_data.py
├─ 📁database
│  ├─ 📄account.db
│  ├─ 📄current_show.db
│  └─ 📄history.db
├─ 📁database_manage
│  ├─ 📄account_database_manage.py
│  ├─ 📄statistics_database_manage.py
│  └─ 📄server_message.py
├─ 📁grpc_client
│  ├─ 📄grpc_client.py
│  ├─ 📄grpc_server.py
│  ├─ 📄read_log.py
│  ├─ 📄statistics.proto
│  ├─ 📄statistics_pb2.py
│  ├─ 📄statistics_pb2_grpc.py
│  └─ 📄test.log
├─ 📁notes
│  ├─ 📄grpc相关说明.txt
│  ├─ 📄云服务器密钥.pem
│  ├─ 📄杂记.txt
│  └─ 📄项目结构图.bmp
└─ 📄README.md
```

## 基于Flask的后端服务程序
该部分代码位于app文件夹中，主程序为[app.py](app/app.py)中，使用Flask框架进行Web开发。

## 基于grpc的远程过程调用
该部分代码位于grpc_client文件夹中，主程序为[grpc_client.py](grpc_client/grpc_client.py)中，使用grpc进行远程过程调用。
文件夹中提供了一个简单的服务端[grpc_server.py](grpc_client/grpc_server.py)，用于测试远程过程调用。但是，该服务端仅用于开发时测试，并没有什么实际的功能。在实际使用时，应该编写专门的服务端程序，以实现特定功能。关于grpc接口的定义，请见[statistics.proto](grpc_client/statistics.proto)文件。

## log文件格式规定
两条事件之间须换行，内容仅可以为【登录事件】或【商品交易事件】中的一种。
登录事件：
xxxx-xx-xx xx:xx:xx INFO event:visit
商品交易事件：
xxxx-xx-xx xx:xx:xx INFO event:purchase tag:xx&xx&...
两种事件中的日期、时间格式规定如下：
日期    xxxx-xx-xx  例：2025-04-01、2024-12-12
时间    xx:xx:xx    例：12:01:23、01:00:59

## 数据库管理
该部分代码位于database_manage文件夹中，主程序为[statistics_database_manage.py](database_manage/statistics_database_manage.py)和[account_database_manage.py](database_manage/account_database_manage.py)中，使用sqlite3进行数据库管理。
须要注意的是，数据库一般由程序自动管理，只有在必需时（如数据库损坏、数据过多需要删除等）才需要手动管理。
数据库文件都位于database文件夹中，包括：
- account.db：用户账号数据库
- current_show.db：当前展示数据库，仅存储了当前会被展示的数据，会时不时更新
- history.db：历史数据库，存储了所有的历史数据，不会被自动更新（除非手动删除）

## 项目运行
1. 确保已经安装了Python 3.10及以上版本，且已经安装了Flask、grpc、sqlite3等依赖包。
2. 运行[database_init.py](database_manage/database_init.py)文件初始化数据库。
3. 运行[app.py](app/app.py)文件，即可启动Web服务。
4. 运行[grpc_client.py](grpc_client/grpc_client.py)文件，即可启动grpc服务。

## 后记
本作品可能还存在许多不足，欢迎大家批评指正。
作者：北京邮电大学未来学院 2024级本科生 李睿彤 学号2024212654 班级2024217803