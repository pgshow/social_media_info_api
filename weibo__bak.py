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
        self.scraping = False
        self.driver = None

    def renew_cookie(self):
        """更新 cookie"""
        try:
            self.driver.quit()
        except:
            pass

        self.driver = get_driver()

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
        """从微博爬数据"""
        self.renew_cookie()

        for i in range(1, 21):
            if not self.scraping:
                self.scraping = True
                break

            time.sleep(1)

            i += 1
            if i >= 20:
                raise Exception('overtime')

        # 先转换url格式
        if re.search(r'(/status/\d{16})', url):
            # 手机url需转换为PC端url - 手机端链接形式1
            url = self.mobile2pc_url(url)
            time.sleep(5)
        else:
            match = re.search(r'/(\d{10})/(\d{16})', url)
            if match:
                # 手机url需转换为PC端url - 手机端链接形式1
                uid = match.group(1)  # 用户id
                mid = mid2id(match.group(2))
                url = f"https://www.weibo.com/{uid}/{mid}"

        try:
            if not re.search(r'weibo\.com/\d{10}/[a-zA-Z0-9]{9}$', url):
                raise Exception('url is illegal')

            html = self.chrome_url(url)

            time.sleep(5)
            return self.extract(html)
        except Exception as e:
            return f'scrape {url} err: {e}'

    def chrome_url(self, url):
        try:
            self.driver.get(url)

            # 等待页面加载
            WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, "//input[@node-type='searchInput']")))

            if '来自小曲走丢了' in self.driver.text:
                raise Exception('page missing')

            if r.text == '':
                raise Exception('html is empty')

            return r.text

        except Exception as e:
            print(e)

    def fetch_url(self, url):
        # self.renew_cookie()
        # time.sleep(5)
        with open('cookies.json', 'r', encoding='utf-8') as f:
            list_cookies = json.loads(f.read())
            cookie = '; '.join(item for item in [item["name"] + "=" + item["value"] for item in list_cookies])

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0',
            'cookie': 'login_sid_t=e719ac3104610da6f80815f48a1cc174; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=4612985999019.135.1620747417166; SINAGLOBAL=4612985999019.135.1620747417166; ULV=1620747417170:1:1:1:4612985999019.135.1620747417166:; SSOLoginState=1620747482; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFj3gBW0dymecpoSwvYwlnH5JpX5KMhUgL.Fo27S0z4e05fe0z2dJLoIpqLxKML1h2LB-zLxKMLB.qLB.eEehz7; UOR=,,www.google.com.hk; SCF=ApaBBJYPakV8maW63U_0W0y5jeozeLnrOdLhRKGCdiwNNnkxF9bVwsXEL1fiGp3GCk6H6aGTI-5kJ-PbOKlSwhw.; SUB=_2A25MXBL1DeRhGedO7FAY8y7JyD6IHXVvKAM9rDV8PUNbmtAKLRT8kW9NXOXHn2Qc9QjjA6FuTy4FndZdAdcwk6a_; ALF=1664718372; XSRF-TOKEN=ubzfJRVwJ2KD9sHadgJfQ7zU; WBPSESS=NcY-Wj1EaEZEN7Rre1zkcFK5K8-iqLmYPKMmEY1p8wrIoqRK7rO_STtBfpwtzIG1jMs_rAyzMo-0Avtf8GbwngtOvmXriAIs9dZw8ZPRgZnMX3dviapQiU4PF0P0rY_w'
        }

        r = requests.get(url, headers=headers, timeout=30)
        r.close()

        if r.status_code != 200:
            raise Exception(f'get status {r.status_code}')

        if '来自小曲走丢了' in r.text:
            raise Exception('page missing')

        if r.text == '':
            raise Exception('html is empty')

        return r.text

    def extract(self, html):
        """获取微博属性"""
        fans = re.search(r'[她他]的粉丝\((\d+)\)', html).group(1)

        data2 = re.findall(r'<\\/em><em>(\d+)<\\/em><\\/span>', html)
        share = data2[0]
        comments = data2[1]
        likes = data2[2]

        author = re.search(r"CONFIG\['onick']='(.+?)';", html).group(1)
        title = re.search(r"CONFIG\['title_value']='(.+?)\.\.\. 来自.+?'; ", html).group(1)

        reply_data = {
            'author': author,
            'title': title,
            'fans': fans,
            'share': share,
            'comments': comments,
            'likes': likes
        }

        return reply_data

    def mobile2pc_url(self, mweb_url):
        """手机 url 转电脑 url"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}
        try:
            mweb = requests.get(mweb_url, headers=headers, timeout=30)
            mweb.close()
            if mweb.status_code != 200:
                raise Exception(f'get {mweb_url} - {mweb.status_code}')

            pc_id = re.search(r'"id": (\d+),', mweb.text).group(1)
            pc_bid = re.search('"bid": "(.*?)",', mweb.text).group(1)
            pc_url = f"https://www.weibo.com/{pc_id}/{pc_bid}"

            return pc_url
        except:
            logger.error("error when mobileUrl 2 pcUrl")
            return ''
