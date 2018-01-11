#!/usr/bin/python
# _*_coding:utf-8_*_

import urllib
import urllib2
import cookielib
import re
import time
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

class NWPUgrade:
    def __init__(self):
        try:
            self.values = {}
            self.values['username'] = "xxxxxxxxxx"	#username:学号
            self.values['password'] = "xxxxxxxxxx"	#password:密码
            self.loginUrl = "http://us.nwpu.edu.cn/eams/login.action"
            self.gradeUrl = "http://us.nwpu.edu.cn/eams/teach/grade/course/person!historyCourseGrade.action?projectType=MAJOR"
            self.message = ''
            self.cookie = cookielib.CookieJar()
            self.handler = urllib2.HTTPCookieProcessor(self.cookie)
            self.opener = urllib2.build_opener(self.handler)
            self.data = urllib.urlencode(self.values)
            self.grades = {}
        except:
            print 'ERROR'

    def login(self):
        try:
            result = self.opener.open(self.loginUrl, self.data)
            result = self.opener.open(self.gradeUrl)
            content = result.read().decode('UTF-8')
            return content
        except:
            print 'ERROR'

    def grade(self):
        try:
            content = self.login()
            pattern = re.compile('<tr>.*?<td>(.*?)</td.*?<a.*?>(.*?)</a.*?<td.*?<td>(.*?)</td>.*?<td.*?<td.*?<td.*?<td.*?<td.*?<td.*?>\s*(.*?)\r\n</td>.*?</td>.*?</tr>', re.S)
            self.grades = re.findall(pattern, content)
        except:
            print 'ERROR'

    def printgrade(self):
        try:
            mark = 0
            credit = 0
            for grade in self.grades:
                print grade[0]					#学期
                print grade[1]					#课程名称
                print u'学分：', grade[2]		#学分
                print u'最终成绩：', grade[3]	#成绩
                if grade[3] != 'P':
                    mark += float(grade[3]) * float(grade[2])
                    credit += float(grade[2])
            print u'你的学分绩', mark/credit
        except:
            print 'ERROR'

    def getgrades(self):
        try:
            return self.grades
        except:
            print 'ERROR'

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
    Header(name, 'utf-8').encode(), \
    addr.encode('utf-8') if isinstance(addr, unicode) else addr))


if __name__ == '__main__':
    from_addr = '' #发送邮箱
    password = '' #邮箱密码
    to_addr = '' #目标邮箱
    smtp_server = '' #smtp服务器

    NWPU = NWPUgrade()
    NWPU.grade()
    NWPU.printgrade()
    grades = NWPU.getgrades()
    SubjectNumber = len(grades)
    while True:
        try:
            time.sleep(20*60) #20分钟检测一次
            NWPU.grade()
            Newgrades = NWPU.getgrades()
            NewNumber = len(Newgrades)
            if NewNumber != SubjectNumber: #有新成绩
                SubjectNumber = NewNumber
                mark = 0
                credit = 0
                Newgrade = []
                for grade in Newgrades:
                    if grade not in grades:
                        Newgrade.append(grade) #可能同时更新复数个
                    if grade[3] != 'P':
                        mark += float(grade[3]) * float(grade[2])
                        credit += float(grade[2])
                GPA = mark / credit #计算学分绩
                grades = Newgrades
                text = ''
                for grade in Newgrade:
                    text = text + u"学期：%s  \n课程名称：%s  \n学分：%s  \n成绩：%s  \n" % (grade[0], grade[1], grade[2], grade[3])
                text = text + u'学分绩：%f' % GPA
                msg = MIMEText(text, 'plain', 'utf-8')
                msg['From'] = _format_addr(u'Python <%s>' % from_addr)
                msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
                msg['Subject'] = Header(u'您的成绩单', 'utf-8').encode()
                server = smtplib.SMTP(smtp_server, 25)
                server.set_debuglevel(1)
                server.login(from_addr, password)
                server.sendmail(from_addr, [to_addr], msg.as_string())
                server.quit()
        except:
            continue
