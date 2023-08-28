import time
import urllib.parse
import os
import re
from lxml import etree
from ProcessingImage import *
from prettytable import PrettyTable
import pandas as pd
import execjs
from PIL import Image

base_url = 'http://119.6.108.206:777'  # 替换为你们学校正方教务url

HEADERS = {
    "Referer": "",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36",
}


def zf_login(s, number, pwd, model):
    url = f'{base_url}/default2.aspx'
    response = s.get(url)
    # 得到VIEWSTATE值后面提交参数需要
    selector = etree.HTML(response.content)
    VIEWSTATE = selector.xpath('//*[@id="form1"]/input/@value')[0]

    # 获取SafeKey
    SafeKey = selector.xpath("//div[@class='jympic']/img/@src")[0]

    # 得到PublicKeyModulus
    value = selector.xpath("//div[@class='login-tag']/input[@id='txtKeyModulus']")[0]
    PublicKeyModulus = value.get("value")

    # 获取验证码并下载到本地
    captcha_url = f'{base_url}{SafeKey}'

    captcha = s.get(captcha_url, stream=True).content

    try:
        with open("./tmp/captcha.jpg", "wb") as jpg:
            jpg.write(captcha)
    except IOError:
        print("IO Error\n")
    finally:
        jpg.close()

    img = Image.open('./tmp/captcha.jpg')
    new_img = SplitImage(GrayscaleAndBinarization(img))

    # 模型预测验证码
    result_pred = []
    i = 0
    for item in new_img:
        tmp = []
        i = i + 1
        item.save('./tmp/' + str(i + 1) + '.jpg')
        img_after_split = item.resize((14, 27))
        tmp.append(featuretransfer(img_after_split))
        result_pred.append(model.predict(tmp)[0])
    captcha = ''.join(result_pred)
    print('此次预测结果为：', captcha)

    # 密码处理
    with open('js.js', 'r') as f:
        js_code = f.read()  # 载入js代码文件

    ctx = execjs.compile(js_code)  # 加载js运行环境
    new_password = ctx.call('new_password', PublicKeyModulus, pwd)

    # 构建post数据
    data = {
        "__LASTFOCUS": '',
        "__VIEWSTATE": VIEWSTATE,
        "VIEWSTATEGENERATOR": "9BD98A7D",
        "__EVENTTARGET": '',
        "__EVENTARGUMENT": '',
        "TextBox1": number,
        "TextBox2": new_password,
        "txtSecretCode": captcha,
        "RadioButtonList1": "学生",
        "Button1": "登录",
        "txtKeyExponent": "010001",
        "txtKeyModulus": ""
    }

    # 提交表头，里面的参数是电脑各浏览器的信息。模拟成是浏览器去访问网页。
    headers = HEADERS.copy()
    # 登陆教务系统
    response = s.post(url, data=data, headers=headers)
    content = response.content.decode('utf-8')

    def getInfor(content, xpath):
        selector = etree.HTML(content)
        infor = selector.xpath(xpath)
        return infor

    # 获取学生基本信息
    student = getInfor(content, '//*[@id="xhxm"]/text()')
    # pq(response.text).find('#xhxm').text().replace('同学', '') from pyquery import PyQuery as pq
    if not student:
        print('登录失败！正在尝试重新登录')
        time.sleep(3)
        zf_login(s, number, pwd, model)
    else:
        student = student[0].replace('同学', '')
        print('登录成功！', student)
    return student


def zf_pj(s, xh, name):
    url = f'{base_url}/xsjxpj.aspx?'
    params = {'xh': xh, 'xm': name, 'gnmkdm': 'N121306'}
    headers = HEADERS.copy()
    headers["Referer"] = f'{base_url}/xs_main.aspx?xh={xh}'
    response = s.get(url, params=params, headers=headers)
    content = response.text

    if '你已经评价过!' in content:
        print('暂未开放评教')
    # 暂未实现
    pass


def zf_cj(s, xh, name):
    # 得到VIEWSTATE参数
    url = f'{base_url}/xscjcx.aspx?'

    params = {'xh': xh, 'xm': name, 'gnmkdm': 'N121605'}

    headers = HEADERS.copy()
    headers["Referer"] = f'{base_url}/xs_main.aspx?xh={xh}'
    response = s.get(url, params=params, headers=headers)
    selector = etree.HTML(response.content)
    VIEWSTATE = selector.xpath('//*[@id="__VIEWSTATE"]/@value')[0]

    # 开始获取历年所有成绩
    data = {
        "__EVENTTARGET": "",
        "__EVENTARGUMENT": "",
        "__LASTFOCUS": "",
        "__VIEWSTATE": VIEWSTATE,
        "__VIEWSTATEGENERATOR": "B0C8BF1A",
        "ddlXN": "",
        "ddlXQ": "",
        "ddl_kcxz": "",
        "btn_zcj": "历年成绩"
    }
    url = url + "?" + urllib.parse.urlencode(params)
    headers["Referer"] = url

    response = s.post(url, data=data, headers=headers, params=params)
    selector = etree.HTML(response.text)
    trs = selector.xpath('//table[@id="Datagrid1"]//tr')
    head = trs[0].xpath('./td/text()')
    head.insert(0, '学年')
    head.insert(1, '学期')
    head.insert(3, '课程名称')
    head = head[:13]
    table = PrettyTable(head)
    for tr in trs[1:]:
        tds = tr.xpath('./td/text()')
        table.add_row(tds)
    print(table)

    df = pd.DataFrame(table._rows, columns=table.field_names)
    df.to_excel('{}成绩.xlsx'.format(name), index=False)
    print(os.path.abspath('{}成绩.xlsx'.format(name)))


# Function to get personal information
def get_personal_info(s, xh, name):
    info_url = f"{base_url}/xsgrxx.aspx?xh={xh}&xm={name}&gnmkdm=N121501"
    headers = HEADERS.copy()
    headers["Referer"] = f"{base_url}/xs_main.aspx?xh={xh}"
    response = s.get(info_url, headers=headers)
    html = response.content.decode("utf-8")
    # Process the HTML as needed


# Function to get the course schedule
def get_course_schedule(s, xh):
    kburl = f"{base_url}/xskbcx.aspx?xh={xh}&xm=%C2%AC%BC%CC%B9%E2&gnmkdm=N121603"
    headers = HEADERS.copy()
    headers["Referer"] = f"{base_url}/xs_main.aspx?xh={xh}"
    response = s.get(kburl, headers=headers)
    html = response.content.decode("gb2312")
    selector = etree.HTML(html)
    content = selector.xpath('//*[@id="Table1"]/tr/td/text()')
    # Process the content as needed


# Function to specify the academic year and semester for the course schedule
def specify_course_schedule(s, xh, __VIEWSTATE):
    kburl = f"{base_url}/xskbcx.aspx?xh={xh}&xm=%C2%AC%BC%CC%B9%E2&gnmkdm=N121603"
    data = {
        "__EVENTTARGET": "xqd",
        "__EVENTARGUMENT": "",
        "__VIEWSTATE": __VIEWSTATE,
        "xnd": "2021-2022",
        "xqd": "2",
    }
    headers = HEADERS.copy()
    headers["Referer"] = f"{base_url}/xs_main.aspx?xh={xh}&xm=%C2%AC%BC%CC%B9%E2&gnmkdm=N121603"
    response = s.post(kburl, data=data, headers=headers)
    html = response.content.decode("gb2312")
    pattern = re.compile(r'(?<=name="__VIEWSTATE" value=").*?(?=")')
    matcher = re.search(pattern, html)
    __VIEWSTATE = matcher.group(0)
    content = selector.xpath('//*[@id="Table1"]/tr/td/text()')
    for each in content:
        print(each)
