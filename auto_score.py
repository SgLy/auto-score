# -*- coding=utf-8 -*-
import re
import os
import requests
from PIL import Image
import pytesseract
import hashlib


caption = ['xnd', 'xq', 'xs', 'resource_id', 'jxbh', 'kcmc', 'xh', 'cjzt', 'kclb', 'kch', 'xf', 'kcywmc', 'zzcj', 'zpcj', 'jd', 'bzw', 'sftg', 'jxbpm', 'cjlcId']

def login(id, key):
    s = requests.session()
    s.get('http://uems.sysu.edu.cn/jwxt')

    headers ={
        'Host' : 'uems.sysu.edu.cn',
        'Origin' : 'http://uems.sysu.edu.cn',
        'Referer' : 'http://uems.sysu.edu.cn/jwxt',
        'Content-Type' : 'application/x-www-form-urlencoded',
        'User-Agent' : 'User-Agent  Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; GWX:QUALIFIED)',
        'Upgrade-Insecure-Requests' : '1'
    }
    rnore = re.compile(r'name="rno" value=(.+)></input>')
    rnodata = re.findall(rnore, s.get('http://uems.sysu.edu.cn/jwxt').text)

    with open('captcha.jpg', 'wb') as f:
        f.write(s.get('http://uems.sysu.edu.cn/jwxt/jcaptcha').content)

    img = Image.open('captcha.jpg')
    img.load()
    capt = pytesseract.image_to_string(img)
    os.remove('captcha.jpg')

    passwd = hashlib.md5()
    passwd.update(key.encode('utf-8'))

    data = {
        'j_username' : str(id),
        'j_password' : passwd.hexdigest().upper(),
        'rno' : rnodata[0],
        'jcaptcha_response' : capt
    }

    url = 'http://uems.sysu.edu.cn/jwxt/j_unieap_security_check.do'

    r = s.post(url, data)
    return s


def successLogin(s):
    r = s.get('http://uems.sysu.edu.cn/jwxt/edp/index.jsp')

    if r.status_code == 200:
        if r.text.find('错误页面') != -1:
            return False
        if r.text.find('Error') != -1:
            return False
    return True

def getGrade(username, password):
    s = requests.session()

    while True:
        s = login(username, password)
        if (successLogin(s)):
            print('Login success')
            break
        print('Login failed')

    content = '{header:{"code": -100, "message": {"title": "", "detail": ""}},body:{dataStores:{kccjStore:{rowSet:{"primary":[],"filter":[],"delete":[]},name:"kccjStore",pageNumber:1,pageSize:200,recordCount:0,rowSetName:"pojo_com.neusoft.education.sysu.xscj.xscjcx.model.KccjModel",order:"t.xn, t.xq, t.kch, t.bzw"}},parameters:{"kccjStore-params": [{"name": "Filter_t.pylbm_0.130855769121068", "type": "String", "value": "\'01\'", "condition": " = ", "property": "t.pylbm"}], "args": ["student"]}}}'
    h = {"Accept": "text/plain", "render":"unieap", "content-type": "mulitpart/form-data"}
    a = s.post('http://uems.sysu.edu.cn/jwxt/xscjcxAction/xscjcxAction.action?method=getKccjList', data = content, headers = h)
    res = a.content

    ans = []

    for c in caption:
        tre = re.compile(r'"' + c + '":"(.+?)",')
        ans.append(re.findall(tre, res))

    tmpre = re.compile(r'\\/');
    for i in range(len(ans[0])):
        ans[17][i] = ans[17][i].replace('\/', '/')

    return ans

def printRaw(ans, filename):
    with open(filename, 'w') as f:
        f.write(str(len(ans[0])))
        f.write('\n')
        for i in range(len(ans[0])):
            for j in range(len(caption)):
                f.write(ans[j][i] + '\n')

def printMarkdown(ans, filename):
    with open(filename, 'w') as f:
        for i in range(len(caption)):
            f.write('|')
            f.write(caption[i])
        f.write('|\n')

        for i in range(len(caption)):
            f.write('|-')
        f.write('|\n')

        for i in range(len(ans[0])):
            for j in range(len(caption)):
                f.write('|')
                f.write(ans[j][i])
            f.write('|\n')
