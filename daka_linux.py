#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-02-01 17:26
# @Author  :  
# @Site    :
# @File    : daka_linux.py
# @Software: PyCharm
import os
import platform
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.color import Color
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
import datetime
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import requests


start = time.time()
print("开始运行",datetime.datetime.now())


# 启动谷歌浏览器
options = Options()
#开启无头模式（无界面启动）
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
#这个命令禁止沙箱模式，否则肯能会报错遇到chrome异常。
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
#建议加上user-agent，因为liunx下有时候会被当成手机版的，所以你会发现代码会报错
num=str(float(random.randint(500,600)))
#此参数最好建议最好带上，不然有些网站会识别liunx系统进行拦截，这里把它伪装成windows下的
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/{} (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/{}".format(num,num))
sys_str = platform.system()

service = Service('./chromedriver')    ###　linux

service.command_line_args()
service.start()
if sys_str=="Linux":

    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
else:
    driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',options=options)




today_md = datetime.datetime.now().strftime('%m%d')
today_ymd = datetime.datetime.now().strftime('%Y%m%d')
first_day = datetime.datetime.strptime('2021-02-01','%Y-%m-%d')

def get_jsciba():
    #获取金山词霸每日一句，英文和翻译
    url = "http://open.iciba.com/dsapi/"
    r = requests.get(url)
    fenxiang_img = r.json()['fenxiang_img']
    return fenxiang_img

def get_djt():
    #获取毒鸡汤文案
    url ='https://soul-soup.fe.workers.dev/'
    r = requests.get(url)
    title = r.json()['title']
    return title


def dk(username, password, province, city):
    url = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0'
    driver.get(url)
    driver.implicitly_wait(10)
    ran = random.randint(10,100)
    print(ran)
    time.sleep(ran)

    driver.find_element_by_xpath('//*[@id="mt_5"]/div[2]/div[3]/input').send_keys(username)
    driver.find_element_by_xpath('//*[@id="mt_5"]/div[3]/div[3]/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="mt_5"]/div[5]/div/input').click()
    time.sleep(1)
    driver.implicitly_wait(8)
    print(driver.current_url)
    iframe = driver.find_elements_by_tag_name("iframe")[0]
    driver.switch_to.frame(iframe)
    date_color = driver.find_element_by_xpath("//body/form[1]/div[1]/div[9]/span[1]").value_of_css_property('color')
    date_color_hex = Color.from_string(date_color).hex
    print(date_color_hex)
    if date_color_hex != '#ff00ff':
        driver.find_element_by_xpath('//*[@id="bak_0"]/div[13]/div[5]/div[4]/span').click()
        driver.implicitly_wait(3)
        time.sleep(1)
        
        select_province = Select(driver.find_element_by_xpath('//*[@id="myvs_13a"]'))
        select_province.select_by_visible_text(province)
        driver.find_element_by_xpath('//*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/input[1]').click()
        select_city = Select(driver.find_element_by_xpath('//*[@id="myvs_13b"]'))
        select_city.select_by_visible_text(city)
        
        dili = driver.find_element_by_xpath('//*[@id="bak_0"]/div[8]/div[2]/div[2]/div[2]/input[6]')
        print(dili.get_attribute("value"))
        driver.execute_script("arguments[0].value = '请求超时'", dili)
        print('2', dili.get_attribute("value"))
        driver.find_element_by_xpath('//*[@id="bak_0"]/div[8]/div[2]/div[2]/div[6]/div[4]').click()
        return True
    else:
        return True

username = ['201xxx', '201xxx']
password = ['xxx', 'xxx']
province = ['河南省', '河南省']
city = ['郑州市', '郑州市']
receiver=['@qq.com','@163.com']

num = len(username)
res = []
for i in range(num):
    res.append(dk(username[i], password[i], province[i], city[i]))

driver.quit()
service.stop()
os.system('taskkill /im chromedriver.exe /F')
os.system('taskkill /im chrome.exe /F')


#sender_username为发件人的账号
sender_username = 'xxx'
#pwd为邮箱的授权码
pwd = 'xxx'

#邮件的正文内容
fenxiang_img = get_jsciba()
djt = get_djt()
mail_content = f'''
            <p>{today_md}打卡完成</p>
            <img src="{fenxiang_img}">
            <p>{djt}</p>
            <p>今日也要加油哟！</p>
            '''
#邮件标题
mail_title = '今日打卡完成，献上每日两句'

def send_mail(sender_username='',pwd='',receiver='',mail_title='',mail_content=''):
    res = True
    # 邮箱smtp服务器
    try:
        host_server = 'smtp.163.com'
        sender_username = sender_username + '@163.com'

        msg = MIMEMultipart('related')
        msg["Subject"] = Header(mail_title, 'utf-8')
        msg["From"] = sender_username
        msg["To"] = receiver

        msg_content = mail_content
        msgAlternative = MIMEMultipart('alternative')
        msgAlternative.attach(MIMEText(msg_content, 'html', 'utf-8'))
        msg.attach(msgAlternative)

        # ssl登录
        smtp = smtplib.SMTP_SSL(host_server)
        # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
        smtp.set_debuglevel(1)
        smtp.ehlo(host_server)
        smtp.login(sender_username, pwd)

        smtp.sendmail(sender_username, receiver, msg.as_string())
        smtp.quit()
    except Exception:
        res = False
    return res


def send_qq(qq):
    return send_mail(sender_username,pwd,qq,mail_title,mail_content)
if datetime.datetime.now().strftime('%H') > '06':
    for i in range(num):
        if res[i]:
            mail_res = send_qq(receiver[i])
            if mail_res:
                print(i, '邮件发送成功')
            else:
                print(i, '邮件发送失败')

print("运行结束",datetime.datetime.now())
print('ok')
