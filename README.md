
# python+selenium实现的web端自动打卡
## 说明
本打卡脚本适用于**xx大学健康打卡**，其他web端打卡也可借鉴学习。**（自己用的，从2月分稳定运行至今）**  
仅供学习交流使用，请勿依赖。开发者对使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。  
为防止疫情再次扩散，我们一定要如实汇报自己的个人情况，不隐瞒真实状况。  
**ps：喜欢请Star此项目**🤞🤞🤞。
![image](https://user-images.githubusercontent.com/39648485/118446437-37ed4600-b722-11eb-914a-51635ccc6676.png)
## 简明教程
### 环境
python 3.8.5  
使用到的一些包，需一步步install
### 代码
#### 打卡代码
> daka.py适用于windows，只实现打卡功能  
> daka_linux.py适用于linux，实现打卡 + 邮件发送打卡结果（金山词霸每日一句 + 毒鸡汤🤣）  
> 两个文件打卡部分几乎一致，只有配置差别
  
主要介绍daka_linux文件，以下是主要方法  
- webdriver配置  
- get_jsciba()：获取金山词霸每日一句
- get_djt()：   获取毒鸡汤
- dk()：        打卡逻辑
- send_mail()： 邮件发送逻辑

整体逻辑：  
- 循环用户，调用dk()，返回的打卡结果True or False存为res列表
- 调用get_jsciba()、get_djt()，组成邮件正文
- 循环res，打卡成功的发送邮件

简单介绍下dk()部分内容
使用的selenium自动化，其他技术请自行google  
使用的find_elements_by_xpath获取标签元素  
其他api可以参考https://www.jianshu.com/p/6c82c965c014
![image](https://user-images.githubusercontent.com/39648485/118361352-a8c71d80-b5bd-11eb-91f4-cb75fb0e4970.png)
```python
//*[@id="mt_5"]/div[2]/div[3]/input      #　copy结果
driver.find_element_by_xpath('//*[@id="mt_5"]/div[2]/div[3]/input')
```

#### 自动化
在Windows和Linux设置定时任务，前者Bat，后者Shell，前者任务计划程序，后者Contrab
linux 定时任务
```
01 5,7 * * * /usr/local/bin/python3 daka_linuxn.py >> daka_linux.log 2>&1
```
#### 其他
linux要注意chrome、chromedriver进程关闭，虽代码里写了关闭逻辑，保险起见，可以设置定时任务杀死这两个进程  
**ps：邮箱授权码可自行google，qq、163等均可**
