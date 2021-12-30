import datetime
import json
import re
import time

import requests

import config
import fc
from loguru import logger
from lxml import etree
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def get_driver():
    options = webdriver.ChromeOptions()
    fc.init_base_cap(options)

    driver = webdriver.Chrome(executable_path=config.DRIVER_PATH, options=options)
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
        self.initialing = False
        self.last_scrape_time = datetime.datetime.now()

    def login(self):
        """维持一个有效cookie的浏览器"""
        logger.warning(f'Please login Weibo at {config.HOST_URL}weibo after web server launched')

        if self.initialing:
            return False

        if self.driver:
            self.driver.quit()

        driver = get_driver()

        self.initialing = True

        try:
            driver.get("https://weibo.com/login?tabtype=weibo")

            e = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '安全登录')]")))
            time.sleep(3)

            e.click()

            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@node-type="qrcode_form"]')))

            time.sleep(10)

            pic_base64 = driver.get_screenshot_as_base64()

            self.driver = driver

            return pic_base64

        except Exception as e:
            raise e
        finally:
            self.initialing = False

    def open_chrome(self):
        """维持一个有效cookie的浏览器"""
        if self.initialing:
            return False

        if self.driver:
            return True

        logger.info('Weibo Chrome initial')

        self.initialing = True

        driver = get_driver()

        try:
            # login_cookie = 'login_sid_t=e719ac3104610da6f80815f48a1cc174; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=4612985999019.135.1620747417166; SINAGLOBAL=4612985999019.135.1620747417166; ULV=1620747417170:1:1:1:4612985999019.135.1620747417166:; SSOLoginState=1620747482; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFj3gBW0dymecpoSwvYwlnH5JpX5KMhUgL.Fo27S0z4e05fe0z2dJLoIpqLxKML1h2LB-zLxKMLB.qLB.eEehz7; UOR=,,www.google.com.hk; SCF=ApaBBJYPakV8maW63U_0W0y5jeozeLnrOdLhRKGCdiwNNnkxF9bVwsXEL1fiGp3GCk6H6aGTI-5kJ-PbOKlSwhw.; SUB=_2A25MXBL1DeRhGedO7FAY8y7JyD6IHXVvKAM9rDV8PUNbmtAKLRT8kW9NXOXHn2Qc9QjjA6FuTy4FndZdAdcwk6a_; ALF=1664718372; XSRF-TOKEN=ubzfJRVwJ2KD9sHadgJfQ7zU; WBPSESS=NcY-Wj1EaEZEN7Rre1zkcFK5K8-iqLmYPKMmEY1p8wrIoqRK7rO_STtBfpwtzIG1jMs_rAyzMo-0Avtf8GbwngtOvmXriAIs9dZw8ZPRgZnMX3dviapQiU4PF0P0rY_w'
            # login_cookie = 'login_sid_t=e719ac3104610da6f80815f48a1cc174; cross_origin_proto=SSL; _s_tentry=passport.weibo.com; Apache=4612985999019.135.1620747417166; SINAGLOBAL=4612985999019.135.1620747417166; ULV=1620747417170:1:1:1:4612985999019.135.1620747417166:; SSOLoginState=1620747482; XSRF-TOKEN=yFTsmilEahokAOpoYjZqvpgx; UOR=,,www.google.com.hk; SCF=ApaBBJYPakV8maW63U_0W0y5jeozeLnrOdLhRKGCdiwNMavdCVnP6yU0dxMSO6Uq6dDw4ruXzk8wWCH2pXCZQXQ.; SUB=_2A25MXgNDDeRhGedO7FAY8y7JyD6IHXVvKnOLrDV8PUNbmtAKLXjYkW9NXOXHn5SODJQIuuzP9IyIs6yC_XB5GLiz; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFj3gBW0dymecpoSwvYwlnH5JpX5KMhUgL.Fo27S0z4e05fe0z2dJLoIpqLxKML1h2LB-zLxKMLB.qLB.eEehz7; ALF=1664853650; WBPSESS=NcY-Wj1EaEZEN7Rre1zkcFK5K8-iqLmYPKMmEY1p8woQ-oLKj0T-Z3Mmfuuhby4gqsShnTxRS587ioHgMnG8Ge9Yombed5XvUyGwGqQVqd_Ocxq-YeIo7oZcGEMG0CJf'
            login_cookie = 'UOR=,finance.sina.com.cn,; SCF=ApaBBJYPakV8maW63U_0W0y5jeozeLnrOdLhRKGCdiwNtWnUT7S9NA_DsB4CzIr1_dnK0icIHCqV93HBafJrSC4.; U_TRS1=0000004d.e4649fc3.609d466c.6074c172; U_TRS2=0000004d.e4739fc3.609d466c.c3c4ed38; Apache=4833856710607.0625.1622452086006; SINAGLOBAL=4833856710607.0625.1622452086006; FSINAGLOBAL=4833856710607.0625.1622452086006; ULV=1622452087516:2:2:1:4833856710607.0625.1622452086006:1620793761477; SessionID=ts8jcovq1opchrssuam3i5dvk5; bdshare_firstime=1633192286425; SINABLOGNUINFO=1072930532.3ff39ee4.pgshow; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFj3gBW0dymecpoSwvYwlnH5JpX5KzhUgL.Fo27S0z4e05fe0z2dJLoIpqLxKML1h2LB-zLxKMLB.qLB.eEehz7; SUB=_2A25MWCfwDeRhGedO7FAY8y7JyD6IHXVvLB44rDV_PUNbm9B-LXChkW9NXOXHn4uf6aMItGikkbjka-Q7dJZQsaee; ALF=1664977696; SGUID=1633441839541_38986892'
            cookies = fc.get_cookies(login_cookie)
            driver.get("http://my.sina.com.cn/#location=fav")
            driver.delete_all_cookies()

            for key, value in cookies.items():
                driver.add_cookie({
                    'domain': '.sina.com.cn',
                    'name': key,
                    'value': value,
                    'path': '/',
                    'expires': None
                })

            driver.get("http://my.sina.com.cn/#location=fav")

            # 等待页面加载
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, '//img[@alt="profile"]')))

            self.driver = driver
            self.initialing = False
            return True

        except Exception as e:
            print(e)
        finally:
            time.sleep(21)

    def scrape(self, url):
        """从微博爬数据"""
        if not self.driver:
            return f'Please login Weibo at {config.HOST_URL}weibo after web server launched'

        if self.scraping:
            return 'Try later, another url is scraping right now'

        if self.too_fast():
            return 'Please slow down, interval is 45 seconds'

        logger.info(f'scraping {url}')

        self.scraping = True  # 控制只启动一个爬虫

        try:
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

            if 'weibo.com' not in url:
                raise Exception('url is illegal')

            if url.startswith('https://weibo.com/u/'):
                raise Exception('url is illegal')

            print(url)

            html = self.chrome_url(url)

            return self.extract(html)
        except Exception as e:
            logger.error(e)
            return f'scrape {url} err: {e}'
        finally:
            self.scraping = False

    def too_fast(self):
        """频繁度"""
        if (datetime.datetime.now() - self.last_scrape_time).seconds < 44:
            return True
        else:
            return False

    def chrome_url(self, url):
        try:
            self.driver.get(url)

            # 等待页面加载
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//span[@class="woo-like-iconWrap" or @node-type="like_status"]')))

            time.sleep(2)

            if '来自小曲走丢了' in self.driver.page_source:
                raise Exception('page missing')

            return self.driver.page_source

        except Exception as e:
            raise e
        finally:
            self.last_scrape_time = datetime.datetime.now()

    def extract(self, html):
        """获取微博属性"""
        selector = etree.HTML(html)  # 将源码转化为能被XPath匹配的格式

        fans = self.get_fans(selector)

        data1 = re.findall(r'<\\/em><em>(\d+)<\\/em><\\/span>', html)
        if data1:
            # 属性获取第一种形式
            share = data1[0]
            comments = data1[1]
            likes = data1[2]
        else:
            # 属性获取第二种形式
            data2 = selector.xpath(r"//span[starts-with(@class, 'toolbar_num_')]/text()")
            if data2:
                share = str(data2[0]).strip()
                if share == '转发':
                    share = 0

                share = self.wan_convert(share)

                comments = str(data2[1]).strip()
                if comments == '评论':
                    comments = 0
            likes = selector.xpath(r"//span[@class='woo-like-count']")[0].text
            if '赞' in likes:
                likes = 0

            likes = self.wan_convert(likes)

        author = selector.xpath(r'//div[@class="f14 cla woo-box-flex woo-box-alignCenter woo-box-justifyCenter"]')[0].text.strip()

        titles = selector.xpath(r"//div[starts-with(@class, 'detail_wbtext_')]/text()")
        title = ''
        for t in titles:
            if len(t) > 1:
                title = str(t).strip()
                break

        try:
            post_date_tmp = selector.xpath(r"//a[contains(@class, 'head-info_time_')]")[0].text.strip()
            match = re.search(r'(\d{1,2}-\d{1,2}) ', post_date_tmp)
            if match:
                post_date = '2021-' + match.group(1)
            else:
                post_date = ''
        except:
            post_date = ''

        reply_data = {
            'author': author,
            'title': title,
            'fans': int(fans),
            'share': int(share),
            'comments': int(comments),
            'likes': int(likes),
            'post_date': post_date,
        }

        return reply_data

    def mobile2pc_url(self, mweb_url):
        """手机 url 转电脑 url"""
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:55.0) Gecko/20100101 Firefox/55.0'}

        mweb = requests.get(mweb_url, headers=headers, timeout=30)
        mweb.close()
        if mweb.status_code != 200:
            raise Exception(f'get {mweb_url} - {mweb.status_code}')

        if 'h5-404.png' in mweb.text:
            raise Exception('article is unavailable')

        pc_id = re.search(r'"id": (\d+),', mweb.text).group(1)
        pc_bid = re.search('"bid": "(.*?)",', mweb.text).group(1)
        pc_url = f"https://www.weibo.com/{pc_id}/{pc_bid}"

        return pc_url

    def wan_convert(self, text):
        """带万的数值转换"""
        if isinstance(text, str) and '万' in text:
            return str(int(float(text.replace('万', '')) * 10000))
        else:
            return text

    def get_fans(self, selector):
        """获取微博详细粉丝数"""
        fans_tmp = selector.xpath(r"//div[@class='f14 cla']/div")[0].text
        fans_tmp = self.wan_convert(fans_tmp)

        try:
            webo_url = self.driver.current_url
            pid = re.search(r'/(\d+)', webo_url).group(1)

            self.driver.get(f'https://weibo.com/ajax/profile/info?custom={pid}')

            # Selenium 网页源码转换为 json
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'lxml')
            ss = soup.select('pre')[0]
            res = json.loads(ss.text)

            fans = res['data']['user']['followers_count']
            return fans
        except:
            return fans_tmp
