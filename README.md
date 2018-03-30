# NWPUgrade
NWPU自动成绩通知

## 简介
秉承着技术改变生活的态度写了这个脚本，那么你可以做到什么：

* 再也无需不厌其烦地登陆教务系统查看成绩

* 每次新成绩出炉都会有邮件发送至你邮箱

* 让你永远领先别人一步得到最新成绩

* 并且自动计算目前为止所有课程成绩的学分绩发送至邮箱

## 环境
Python 2.7

## 具体步骤

1. 你只需找一台云服务器(测试用的阿里云linux)

2. 将脚本中的 username 和 password 换成你的学号和密码
```
self.values = {}
self.values['username'] = "xxxxxxxxxx"  # username:学号
self.values['password'] = "xxxxxxxxxx"  # password:密码
```
3. 将 main() 中的 发送邮箱 邮箱密码 接收邮箱 以及smtp服务器 改成你的
```
from_addr = 'xxx@163.com'  # 发送邮件的邮箱
password = '你的邮箱密码'  # 发送邮箱的密码
to_addr = '123456@qq.com'  # 用于接收邮件的邮箱
smtp_server = 'smtp.163.com'  # smtp服务器
```
4. 输入命令后台执行代码

```
nohup python NWPUgrade.py &
```

值得一提的是，测试时用的是阿里云服务器，而阿里云服的25端口都是默认禁止的，所以脚本中的邮件端口改为456。如果你使用的环境没有这种限制，可以改回25端口。

## 其他版本

**basic.py**

这是一个简单版本的成绩查询爬虫，只需将学号和密码换成你的即可运行，输出目前为止的所有课程成绩以及学分绩
```
python basic.py
```

**input.py**

和 basic.py 大致相同，不过输入学号密码的过程在命令行完成
```
python input.py
```
