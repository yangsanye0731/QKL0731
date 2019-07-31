#encoding=utf-8
'''
文件名称：EmailUtil
说明：
提供邮件发送服务
'''

import socket
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.utils import parseaddr,formataddr
import smtplib
import logging
import time
import configparser
from email import encoders
from os import path

#读取配置配置文件
config_file = path.join(path.dirname(__file__), 'config.conf')
cf = configparser.ConfigParser()
cf.read(config_file)

'''
###############################################################################
邮件地址格式化
###############################################################################
'''
def _format_addr(s):
    name,addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


'''
###############################################################################
邮件模板
###############################################################################
'''
def template1(content):
    str_body_br = '<br>'
    str_start = '<html><body>'
    str_body_0 = 'folder=/数据报告/量化跟踪/' + time.strftime('%Y-%m-%d', time.localtime(time.time()))

    str_body = str_body_0 + str_body_br + content
    str_end = '</body></html>'
    return str_start + str_body + str_end

def template2(content):
    str_body_br = '<br>'
    str_start = '<html><body>'
    #str_body_0 = 'folder=/数据报告/量化信息/' + time.strftime('%Y-%m-%d', time.localtime(time.time()))

    str_body = str_body_br + content
    str_end = '</body></html>'
    return str_start + str_body + str_end


'''
###############################################################################
邮件发送函数（发送QQ邮箱）
content 邮件发送内容
title 邮件标题
###############################################################################
'''
def sendMail(content,title):
    from_addr = cf['Email'] ['from3']
    password = cf.get("Email", "password3")
    code3 = cf.get("Email", "code3")
    to_addr = cf.get("Email", "to")
    smtp_server = 'smtp.qq.com'

    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'1看2想大势3快止损 <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(title, 'utf-8').encode()

    try:
        # 设置邮件发送服务器
        server = smtplib.SMTP_SSL(smtp_server, 465)
        # 登录邮件发送服务器
        server.login(from_addr, code3)
        # 发送邮件
        server.sendmail(from_addr, [to_addr], msg.as_string())

        # 邮件服务推出
        server.quit()
    except socket.gaierror as e:
        logging.exception(e)
    except smtplib.SMTPServerDisconnected as e:
        logging.exception(e)
    except smtplib.SMTPException as e:
        logging.exception(e)

'''
###############################################################################
邮件发送函数（发送QQ邮箱）
content 邮件发送内容
title 邮件标题
###############################################################################
'''
def sendQQMailWithAttatch(content,title,file_path, file_name):
    from_addr = cf.get("Email", "from3")
    password = cf.get("Email", "password3")
    code3 = cf.get("Email", "code3")
    to_addr = cf.get("Email", "to")
    smtp_server = 'smtp.qq.com'

    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'CoolSOLO <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(title, 'utf-8').encode()

    # 邮件正文是MIMEText:
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open(file_path, 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('text', 'txt', filename=file_name)
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=file_name)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

    try:
        # 设置邮件发送服务器
        server = smtplib.SMTP_SSL(smtp_server, 465)
        server.set_debuglevel(1)
        # 登录邮件发送服务器
        server.login(from_addr, code3)
        # 发送邮件
        server.sendmail(from_addr, [to_addr], msg.as_string())

        # 邮件服务推出
        server.quit()
    except socket.gaierror as e:
        logging.exception(e)
    except smtplib.SMTPServerDisconnected as e:
        logging.exception(e)
    except smtplib.SMTPException as e:
        logging.exception(e)


'''
###############################################################################
邮件发送函数（发送到为知笔记邮件）
content 邮件发送内容
title 邮件标题
###############################################################################
'''
def sendMailWiz(content, title):
    from_addr = cf.get("Email", "from")
    password = cf.get("Email", "password")
    to_addr = cf.get("Email", "to_wiz")
    smtp_server = 'smtp.163.com'

    msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = _format_addr(u'CoolSOLO <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(title, 'utf-8').encode()

    # 设置邮件发送服务器
    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    # 登录邮件发送服务器
    server.login(from_addr, password)
    # 发送邮件
    server.sendmail(from_addr, [to_addr], msg.as_string())

    # 邮件服务推出
    server.quit()

'''
###############################################################################
邮件发送函数带附件（发送到为知笔记邮件）
content 邮件发送内容
title 邮件标题
###############################################################################
'''
def sendMailAttatch(content, title, file_path, file_name):
    from_addr = cf.get("Email", "from")
    password = cf.get("Email", "password")
    to_addr = cf.get("Email", "to_wiz")
    smtp_server = 'smtp.163.com'
    # 邮件对象:
    msg = MIMEMultipart()
    msg['From'] = _format_addr(u'Python爱好者 <%s>' % from_addr)
    msg['To'] = _format_addr(u'管理员 <%s>' % to_addr)
    msg['Subject'] = Header(title, 'utf-8').encode()

    # 邮件正文是MIMEText:
    msg.attach(MIMEText(content, 'html', 'utf-8'))

    # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
    with open(file_path, 'rb') as f:
        # 设置附件的MIME和文件名，这里是png类型:
        mime = MIMEBase('text', 'txt', filename=file_name)
        # 加上必要的头信息:
        mime.add_header('Content-Disposition', 'attachment', filename=file_name)
        mime.add_header('Content-ID', '<0>')
        mime.add_header('X-Attachment-Id', '0')
        # 把附件的内容读进来:
        mime.set_payload(f.read())
        # 用Base64编码:
        encoders.encode_base64(mime)
        # 添加到MIMEMultipart:
        msg.attach(mime)

    server = smtplib.SMTP(smtp_server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()

#sendMail('<table><br><tr>dfdfdfd</tr></br></table>', 'dafdafdasf')
#sendMail2(template1("请上午准时出发"))
#sendMail3(template1("请上午准时出发"))
#sendMailWiz(template1("邮件内容测试邮件内容测试邮件内容测试邮件内容测试邮件内容测试邮件内容测试邮件内容测试邮件内容测试邮件内容测试邮件内容测试邮件"), "title")
#sendMailAttatch(template1('dasfdafdafdafdafdafda'),'dsafdaf', 'test2.txt', 'test2.txt');
#sendQQMailWithAttatch(template1('dasfdafdafdafdafdafda'),'dsafdaf', 'test2.txt', 'test2.txt');