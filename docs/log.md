# 开发日志

## 2024.10.31

### bugfix

修复了无法建表的bug.
app/models/user.py: User 类将参数 Table 修正为 table
app/db/session.py: 引入了 app.models.user 内的所有类

## 2024.11.6

### feature

app/models/*.py: 完成了各 model 的初步建立

### chore

将 app/curd 重命名为 app/service
app/schemas 下文件合并到对应 app/models 内
app/util 下文件移动到 app/service 内
更新文档

### fix

app/models/schedule.py: 添加了课程容量的字段

## 2024.11.13

### fix

app/models/classroom.py, course.py, favour.py, teach.py: 添加了遗漏的字段。
app/models/section.py: 新增表，此表为课序信息表。
app/models/schedule.py: 更改此表为课序安排表。

## 2024.11.19

### fix

app/models/*.py: 修改正确格式的 foreign key
app/db/session.py: import 了遗漏的数据 model
app/service/authenticate.py: 读取数据源从 dict 改变到 database 中

## 2024.11.27

### fix

app/models/schedule.py, section.py: 修改了字段 le, ge 的错误
app/models/user.py: 添加了用户名的字段
app/service/user.py: 修改了 read_all_user 错误的路由

app/service/authenticate.py, user.py
app/routers/user.py: 隐藏了 user 的路由
