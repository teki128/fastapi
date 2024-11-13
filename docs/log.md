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
