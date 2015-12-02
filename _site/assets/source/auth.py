#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Build-in/std packages
import os, sys, time, platform, random
import re, json, cookielib

# Requirements packages
import requests, termcolor

# 申请一次会话并加载cookie
requests = requests.Session()
requests.cookies = cookielib.LWPCookieJar('cookies')
try:
    requests.cookies.load(ignore_discard=True)
except:
    pass


# 抽象的日志记录类
class Logging:
    flag = True
    @staticmethod
    def error(msg):
        if Logging.flag:
            print "".join([termcolor.colored("ERROR", "red"),\
                          ": ", termcolor.colored(msg, "white")])
    @staticmethod
    def warn(msg):
        if Logging.flag:
            print "".join([termcolor.colored("WARN", "yellow"),\
                          ": ", termcolor.colored(msg, "white")])
    @staticmethod
    def info(msg):
        if Logging.flag:
            print "".join([termcolor.colored("INFO", "magenta"),\
                          ": ", termcolor.colored(msg, "white")])
    @staticmethod
    def debug(msg):
        if Logging.flag:
            print "".join([termcolor.colored("DEBUG", "magenta"),\
                           ": ", termcolor.colored(msg, "white")])
    @staticmethod
    def success(msg):
        if Logging.flag:
            print "".join([termcolor.colored("SUCCES", "green"),\
                          ": ", termcolor.colored(msg, "white")])

# 开始记录日志
Logging.flag = True


# 抽象的网络错误异常类，继承Exception
class NetworkError(Exception):
    def __init__(self, message=""):
        if message == "": self.message = u"网络异常"
        else: self.message = message
        Logging.error(self.message)

# 抽象的帐号类型错误异常类，继承Exception
class AccountError(Exception):
    def __init__(self, message=""):
        if message == "": self.message = u"帐号类型错误"
        else: self.message = message
        Logging.error(self.message)


# 下载登陆时的验证码图片，并通过输入读取验证码
def download_captcha():
    url = "http://www.zhihu.com/captcha.gif"
    r = requests.get(url, params={"r": random.random()})
    if int(r.status_code) != 200:
        raise NetworkError(u"验证码请求失败")
    image_name = u"verify." + r.headers['content-type'].split("/")[1]
    open(image_name, "wb").write(r.content)
    """
        System platform: https://docs.python.org/2/library/platform.html
    """
    Logging.info(u"正在调用外部程序渲染验证码 ... ")
    if platform.system() == "Linux":
        Logging.info(u"Command: xdg-open %s &" % image_name )
        os.system("xdg-open %s &" % image_name )
    elif platform.system() == "Darwin":
        Logging.info(u"Command: open %s &" % image_name )
        os.system("open %s &" % image_name )
    elif platform.system() == "SunOS":
        os.system("open %s &" % image_name )
    elif platform.system() == "FreeBSD":
        os.system("open %s &" % image_name )
    elif platform.system() == "Unix":
        os.system("open %s &" % image_name )
    elif platform.system() == "OpenBSD":
        os.system("open %s &" % image_name )
    elif platform.system() == "NetBSD":
        os.system("open %s &" % image_name )
    elif platform.system() == "Windows":
        os.system("open %s &" % image_name )
    else:
        Logging.info(u"请自行打开验证码文件, 并输入验证码!")
        Logging.info(u"验证码文件: %s" % os.path.join(os.getcwd(), image_name))
    captcha_code = raw_input(termcolor.colored("请输入验证码: ", "cyan"))
    return captcha_code

# 获取表单中的参数: _xsrf
def search_xsrf():
    url = "http://www.zhihu.com/"
    r = requests.get(url)
    if int(r.status_code) != 200:
        raise NetworkError(u"验证码请求失败")
    _xsrf_pat = r"\<input\stype=\"hidden\"\sname=\"_xsrf\"\svalue=\"(\S+)\""
    results = re.compile(_xsrf_pat, re.DOTALL).findall(r.text)
    if len(results) < 1:
        Logging.info(u"提取XSRF 代码失败" )
        return None
    return results[0]
 
# 依据密码帐号，构造表单
def build_form(account, password):
    if re.match(r"^1\d{10}$", account): account_type = "phone_num"
    elif re.match(r"^\S+\@\S+\.\S+$", account): account_type = "email"
    else: raise AccountError(u"帐号类型错误")
    # 构造表单的各项参数
    form = {account_type:account, "password":password, "remember_me":True}
    form['_xsrf'] = search_xsrf()
    form['captcha'] = download_captcha()
    return form

# 上传表单
def upload_form(form):
    if "email" in form: url = "http://www.zhihu.com/login/email"
    elif "phone_num" in form: url = "http://www.zhihu.com/login/phone_num"
    else: raise AccountError(u"账号类型错误")
    # post请求的消息头
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"\
             + " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36",
        'Host': "www.zhihu.com",
        'Origin': "http://www.zhihu.com",
        'Pragma': "no-cache",
        'Referer': "http://www.zhihu.com/",
        'X-Requested-With': "XMLHttpRequest"
    }
    # 发送post请求 
    r = requests.post(url, data=form, headers=headers)
    if int(r.status_code) != 200:
        raise NetworkError(u"表单上传失败!")
    if r.headers['content-type'].lower() == "application/json":
        try:
            # 修正justkg提出的问题: 
            # https://github.com/egrcc/zhihu-python/issues/30
            result = json.loads(r.content)
        except Exception as e:
            Logging.error(u"JSON解析失败！")
            Logging.debug(e)
            Logging.debug(r.content)
            result = {}
        if result["r"] == 0:
            Logging.success(u"登录成功！" )
            return {"result": True}
        elif result["r"] == 1:
            Logging.success(u"登录失败！" )
            return {"error": 
                           {
                           "code": int(result['errcode']), 
                           "message": result['msg'], 
                           "data": result['data'] 
                           } 
                   }
        else:
            Logging.warn(u"表单上传出现未知错误:\n\t%s)" % (str(result)))
            return {"error": {"code": -1, "message": u"unknow error"}}
    else:
        Logging.warn(u"无法解析服务器的响应内容:\n\t%s" % r.text)
        return {"error": {"code": -2, "message": u"parse error"}}

# 判断是否已经登陆成功
def islogin():
    url = "https://www.zhihu.com/settings/profile"
    r = requests.get(url, allow_redirects=False)
    status_code = int(r.status_code)
    if status_code == 301 or status_code == 302:
        return False
    elif status_code == 200:
        return True
    else:
        Logging.warn(u"网络故障")
        return None

# 从配置文件读取配置数据
def read_account_from_config_file(config_file="config.ini"):
    from ConfigParser import ConfigParser
    cf = ConfigParser()
    if os.path.exists(config_file) and os.path.isfile(config_file):
        Logging.info(u"正在加载配置文件 ...")
        cf.read(config_file)
        email = cf.get("info", "email")
        password = cf.get("info", "password")
        if email == "" or password == "":
            Logging.warn(u"帐号信息无效")
            return (None, None)
        else: 
            return (email, password)
    else:
        Logging.error(u"配置文件加载失败！")
        return (None, None)

# 登陆过程
def login(account=None, password=None):
    if islogin() == True:
        Logging.success(u"你已经登录过咯")
        return True
    if account == None:
        (account, password) = read_account_from_config_file()
    if account == None:
        account  = raw_input("请输入登录帐号: ")
        password = raw_input("请输入登录密码: ")
    form_data = build_form(account, password)
    result = upload_form(form_data)
    if "error" in result:
        if result["error"]['code'] == 1991829:
            Logging.error(u"验证码输入错误，请准备重新输." )
            return login()
        else:
            Logging.warn(u"unknow error." )
            return False
    elif "result" in result and result['result'] == True:
        Logging.success(u"登录成功！" )
        requests.cookies.save()
        return True

# 如果单独执行auth.py，则调用登陆函数
if __name__ == "__main__":
    # login(account="xxxx@email.com", password="xxxxx")
    login()
