# 开发日志

## 2024.10.31

### bugfix

修复了无法建表的bug.
app/models/user.py: User类将参数Table修正为table
app/db/session.py: 引入了app.models.user内的所有类
