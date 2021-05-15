#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021-02-01 11:33
# @Author  : 
# @Site    :
# @File    : daka.py
# @Software: PyCharm

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.color import Color
from selenium.webdriver.support.ui import Select
import datetime
import time

start = time.time()
print("开始运行",datetime.datetime.now())

# 启动谷歌浏览器
options = Options()

service = Service('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
service.command_line_args()
service.start()
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe',options=options)
def dk(username, password, province, city):
    url = 'https://jksb.v.zzu.edu.cn/vls6sss/zzujksb.dll/first0'
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(1)

    driver.find_element_by_xpath('//*[@id="mt_5"]/div[2]/div[3]/input').send_keys(username)
    driver.find_element_by_xpath('//*[@id="mt_5"]/div[3]/div[3]/input').send_keys(password)
    driver.find_element_by_xpath('//*[@id="mt_5"]/div[5]/div/input').click()
    # driver.implicitly_wait(4)
    time.sleep(1)
    driver.implicitly_wait(8)
    # time.sleep(1)
    print(driver.current_url)
    iframe = driver.find_elements_by_tag_name("iframe")[0]
    driver.switch_to.frame(iframe)
    # driver.switch_to.frame('zzj_top_6s')
    date_color = driver.find_element_by_xpath("//body/form[1]/div[1]/div[9]/span[1]").value_of_css_property('color')
    date_color_hex = Color.from_string(date_color).hex
    print(date_color_hex)
    if date_color_hex == '#ff00ff':
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

username = ['201xxx', '201xxx']  # 健康打卡账号
password = ['xxx', 'xxx']        # # 健康打卡密码
province = ['河南省', '河南省']
city = ['郑州市', '郑州市']

num = len(username)
for i in range(num):
    dk(username[i], password[i], province[i], city[i])
driver.quit()
service.stop()
print("运行结束",datetime.datetime.now())
print('ok')
