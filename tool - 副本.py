from tkinter import N
from urllib.parse import urljoin
import  hmac ,json
from bs4 import BeautifulSoup
from hashlib import sha1
from scapy.all import *
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
options = webdriver.ChromeOptions()
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time


mailto_list = [""]  #目标邮箱
mail_host = "smtp.163.com"
mail_user = "@163.com"
mail_pass = ""  #163邮箱smtp生成的密码



def send_mail(to_list, sub, content):
    me = "LogServer"+"<"+mail_user+">"
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    server = smtplib.SMTP()
    server.connect(mail_host)
    server.login(mail_user, mail_pass)
    server.sendmail(me, to_list, msg.as_string())
    server.close()
    return True


def getjson(strJson):
    i=strJson.find('{')
    j=strJson.find('}')
    strJson = strJson[i:j+1]

    return strJson

def loginPart():
    url = 'https://uniportal.huawei.com/uniportal/?redirect=https%3A%2F%2Fcareer.huawei.com%2Freccampportal%2Flogin_index.html%3Fredirect%3Dhttps%3A%2F%2Fcareer.huawei.com%2Freccampportal%2Fportal5%2Findex.html%3Fi%3D14298'  # 以该链接为例
    options.add_argument('--headless')  # 增加无界面选项
    options.add_argument('--disable-gpu')  # 如果不加这个选项，有时定位会出现问题
    # 启动浏览器，获取网页源代码
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)

    time.sleep(1)

    uid = browser.find_element_by_name('uid')
    uid.send_keys('') #user id 
    password = browser.find_element_by_name('password')
    password.send_keys('') #password
    butLog = browser.find_element_by_class_name('login_submit_pwd_v2')
    butLog.click()
    return browser
if __name__ == "__main__":
    countTime = 0
    #browser.get('https://career.huawei.com/reccampportal/portal5/job-progress.html')
    browser=loginPart()
    while 1:
        arr = str(round(time.time() * 1000, 0))
        arr = arr[0:13]
        urlJson = 'https://career.huawei.com/reccampportal/services/portal/portaluser/queryMyJobInterviewPortal5?reqTime='+arr
        print(urlJson)
        browser.get(urlJson)
        strJson =str(browser.page_source)
        strJson = getjson(strJson)
       
        if strJson[1] == 'I' and strJson[2]=='V':
            print('666')
            strContent = 'success'+'第'+str(countTime)+'次查询'
            send_mail(mailto_list, '恭喜！华为', strContent)
            break
        elif strJson[2]=='c':
            print("登录失效 重新连接")
            browser.quit()
            browser = loginPart()
            continue
        else:
            countTime+=1
            print('第%d次查询'%countTime+strJson)
        time.sleep(60*5)
    browser.quit()
    
    
