from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re, json

def login():
    driver = webdriver.Chrome()
    driver.get('http://wjw.sysu.edu.cn')
    input('Hit enter when finished login...')
    return driver

def getScore(driver):
    driver.get('http://wjw.sysu.edu.cn/api/score')
    res = re.findall(data_re, driver.page_source)[0].replace('\\/', '/')
    s = json.loads(res)
    return s

def toFile(grade, add):
    with open('config/category.txt', 'r') as f:
        keys = f.read().split('\n')[:-1]
    with open(add, 'w') as f:
        f.write('%d\n' % len(grade))
        for g in grade:
            for k in keys:
                try:
                    s = g[k]
                except KeyError:
                    s = ''
                f.write('%s\n' % s)

data_re = re.compile(r'primary:(\[.+?\])')
