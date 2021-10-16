import json
import re
import time

import requests

import fc
from loguru import logger
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_driver():
    options = webdriver.ChromeOptions()
    fc.init_base_cap(options)

    driver = webdriver.Chrome(options=options)
    fc.add_stealth_js(driver)

    return driver


# 10进制转为62进制
def base62_encode(num, alphabet=ALPHABET):
    """Encode a number in Base X
    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    """
    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


# 62进制转为10进制
def base62_decode(string, alphabet=ALPHABET):
    """Decode a Base X encoded string into the number
    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0
    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num


# mid转换为id
def mid2id(mid):
    mid = str(mid)[::-1]
    size = int(len(mid) / 7) if len(mid) % 7 == 0 else int(len(mid) / 7 + 1)
    result = []
    for i in range(size):
        s = mid[i * 7: (i + 1) * 7][::-1]
        s = base62_encode(int(s))
        s_len = len(s)
        if i < size - 1 and len(s) < 4:
            s = '0' * (4 - s_len) + s
        result.append(s)
    result.reverse()
    return ''.join(result)


# id转换为mid
def id2mid(id):
    id = str(id)[::-1]
    size = int(len(id) / 4) if len(id) % 4 == 0 else int(len(id) / 4 + 1)
    result = []
    for i in range(size):
        s = id[i * 4: (i + 1) * 4][::-1]
        s = str(base62_decode(str(s)))
        s_len = len(s)
        if i < size - 1 and s_len < 7:
            s = (7 - s_len) * '0' + s
        result.append(s)
    result.reverse()
    return ''.join(result)


class Weibo:
    def __init__(self):
        self.driver = get_driver()

    def renew_cookie(self):
        driver = get_driver()


    def access_weibo(self):
        try:
            self.driver.get("https://weibo.com/")

            # 等待页面加载
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@node-type='searchInput']")))

            cookies = self.driver.get_cookies()
            json_cookies = json.dumps(cookies)
            with open('cookies.json', 'w', encoding='utf-8') as f:
                f.write(json_cookies)

            return True
        except Exception as e:
            print(e)

    def scrape(self, url):
        # 从微博爬数据
        if re.search(r'(/status/\d{16})', url):
            # 手机url需转换为PC端url - 手机端链接形式1
            url = self.mobile2pc_url(url)
        else:
            match = re.search(r'/(\d{10})/(\d{16})', url)
            if match:
                # 手机url需转换为PC端url - 手机端链接形式1
                uid = match.group(1)  # 用户id
                mid = mid2id(match.group(2))
                url = f"https://www.weibo.com/{uid}/{mid}"

        html = self.fetch_url(url)

        if html == '':
            return

        self.extract(html)

    def fetch_url(self, url):
        # self.access_weibo()
        with open('cookies.json', 'r', encoding='utf-8') as f:
            list_cookies = json.loads(f.read())
            cookie = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in list_cookies])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'cookie': cookie
        }
        try:
            r = requests.get(url, headers=headers, timeout=30)

            if r.status_code != 200:
                raise Exception(f'get {url} - {r.status_code}')

            return r.text
        except Exception as e:
            logger.error("error when fetch", url, e)
            return ''

    def chrome_url(self, url):
        self.driver.get(url)

        # 等待页面加载
        WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@node-type='searchInput']")))

    def extract(self, html):
        selector = etree.HTML(html)  # 将源码转化为能被XPath匹配的格式
        data1 = re.findall(r'<strong class=\\"W_f16\\">(\d+)<\\/strong>', html)
        fans = data1[1]

        data2 = selector("//div[@class='WB_handle']//span[@class='line S_line1']")
        share = data2[1].text
        comments = data2[1].text
        likes = data2[1].text

        print(fans)

    def mobile2pc_url(self, mweb_url):
        """手机 url 转电脑 url"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        try:
            mweb = requests.get(mweb_url, headers=headers, timeout=30)
            if mweb.status_code != 200:
                raise Exception(f'get {mweb_url} - {mweb.status_code}')

            pc_id = re.search(r'"id": (\d+),', mweb.text).group(1)
            pc_bid = re.search('"bid": "(.*?)",', mweb.text).group(1)
            pc_url = f"https://www.weibo.com/{pc_id}/{pc_bid}"

            return pc_url
        except:
            logger.error("error when mobileUrl 2 pcUrl")
            return ''
