import datetime
import json
import re
import time

import requests

import config
import fc
from loguru import logger
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


def get_driver():
    options = webdriver.ChromeOptions()
    fc.init_base_cap(options)

    driver = webdriver.Chrome(executable_path=config.DRIVER_PATH, options=options)
    fc.add_stealth_js(driver)

    return driver


class Douyin:
    def __init__(self):
        self.scraping = False
        self.driver = None
        self.initialing = False
        self.last_scrape_time = datetime.datetime.now()

    def open_chrome(self):
        """维持一个有效cookie的浏览器"""
        if self.initialing:
            return False

        if self.driver:
            return True

        self.initialing = True

        logger.info('Tiktok Chrome initial')

        driver = get_driver()

        try:
            login_cookie = 'ttwid=1%7Cx2OVp44JBK27bkjPqeantTwIMZ9VbLZTbzeiqxhCE-0%7C1632765612%7Cd6ee5428e2b3c1840e5505c3033b7f76c705968385e8851d6a379363eb5bb234; passport_csrf_token_default=cd81535ef2e25778891950a53afd042f; passport_csrf_token=cd81535ef2e25778891950a53afd042f; _tea_utm_cache_6383=undefined; s_v_web_id=verify_ku2yi1du_TnOxj2WV_9qgZ_47JA_BeOW_FK3KQQEeUPCK; ttcid=ab6501d623204f49aa403d9f150bd3fd39; douyin.com; msToken=at4nC5XpEAqFVH2_mXUoo08WNUDFgffGxQMXgm1pVsaykA9pPRGPS1ZjtfUoJdZOn8vigmfVNr-c5yeO3rX0ui5JW2xOaTwpeAKoXCc2yZKV4bveGhlqiyaThJs=; _tea_utm_cache_1243=undefined; _tea_utm_cache_2018=undefined; MONITOR_DEVICE_ID=bd32f029-b27b-4de5-9528-4ea660942473; n_mh=MYOf7VqbVUY5zLjDnb1gNA1-vNoFWL3UcjkP5MuS-PI; sso_uid_tt=74d48eedcc4f850c761e5cdd5a5ed752; sso_uid_tt_ss=74d48eedcc4f850c761e5cdd5a5ed752; toutiao_sso_user=9e4077dfa87e56c3be86a7ae2dcdb0af; toutiao_sso_user_ss=9e4077dfa87e56c3be86a7ae2dcdb0af; odin_tt=0ad28f49cbbf6273c106db40c7cbd776a45e6a124e037067359023cd737c206626a5b42477b3a3d9d13771a864d81f4a88d7410d01c51de8eef3e4645fde6ea3; passport_auth_status_ss=2ababe55f43c8f5a7694f053b319bd03%2C; sid_guard=9f25e3bd8b6950b724dab08d17ebc298%7C1633296283%7C5183999%7CThu%2C+02-Dec-2021+21%3A24%3A42+GMT; uid_tt=6c573c7ed57b16a82a3a66c530beaeec; uid_tt_ss=6c573c7ed57b16a82a3a66c530beaeec; sid_tt=9f25e3bd8b6950b724dab08d17ebc298; sessionid=9f25e3bd8b6950b724dab08d17ebc298; sessionid_ss=9f25e3bd8b6950b724dab08d17ebc298; sid_ucp_v1=1.0.0-KDA3ZWRkYzYzNDA1MzAwZjU4NDlhOTIxNDI2MzJhOGExZmYzN2JlNTcKFQjjgb_6-QIQm7_oigYY7zE4BkD0BxoCaGwiIDlmMjVlM2JkOGI2OTUwYjcyNGRhYjA4ZDE3ZWJjMjk4; ssid_ucp_v1=1.0.0-KDA3ZWRkYzYzNDA1MzAwZjU4NDlhOTIxNDI2MzJhOGExZmYzN2JlNTcKFQjjgb_6-QIQm7_oigYY7zE4BkD0BxoCaGwiIDlmMjVlM2JkOGI2OTUwYjcyNGRhYjA4ZDE3ZWJjMjk4; passport_auth_status=2ababe55f43c8f5a7694f053b319bd03%2C; __ac_nonce=0615a1f9c00a53ed0867d; __ac_signature=_02B4Z6wo00f01z87bMgAAIDBUkwoCoV93ms.H2hAAK6f9UutQozJO3bMWEdHidA1e014G2qVIgjX8X-I67csCFUNvFbubar4-sbMYeLGHyUENf-ngMQr3xjLps6MPkkTtF6xl20GqMwCIEtz18; FOLLOW_YELLOW_POINT_USER=MS4wLjABAAAA-NI4OHkRb6RtAhHAzK7WDn0qyJ0ujyNPRlvmLLS4iOI; FOLLOW_YELLOW_POINT_STATUE_INFO=1%2F1633297563503; MONITOR_WEB_ID=78ac419d-2be9-490b-98fd-d6ee5d93a595; msToken=RA35ENvojj0agIUIv5jL64UryTRvuLYzZQg2Wv46PbbtZ5s9zeRpoy54vdFpUyU0X-p7v5uhwOnBoE_lYoAgVJf17yhPAaF1P2riX6b1ZBCQQW1mb__Yd0Q=; tt_scid=YvDioZBCrFGw7udHRaMsW9pQjs2SOcGI-pqJqBIbO4cr7KvZlzscmXKmJFGA8QSNf2ab'
            cookies = fc.get_cookies(login_cookie)
            driver.get("https://www.douyin.com/recommend")
            driver.delete_all_cookies()

            for key, value in cookies.items():
                driver.add_cookie({
                    'domain': '.douyin.com',
                    'name': key,
                    'value': value,
                    'path': '/',
                    'expires': None
                })

            driver.get("https://www.douyin.com/recommend")

            # 等待页面加载
            WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), '发布视频')]")))

            self.driver = driver
            return True

        except Exception as e:
            print(e)
        finally:
            self.initialing = False

    def scrape(self, url):
        """从抖音爬数据"""
        # status = self.open_chrome()
        # if not status:
        #     return 'Try later, Chrome is initial right now'

        if not self.driver:
            return 'Try later, Chrome is initial right now'

        if self.scraping:
            return 'Try later, another url is scraping right now'

        if self.too_fast():
            return 'Please slow down, interval is 25 seconds'

        logger.info(f'scraping {url}')

        self.scraping = True  # 控制只启动一个爬虫

        try:
            html = self.chrome_url(url)

            return self.extract(html)
        except Exception as e:
            return f'scrape {url} err: {e}'
        finally:
            self.scraping = False

    def too_fast(self):
        """频繁度"""
        if (datetime.datetime.now() - self.last_scrape_time).seconds < 24:
            return True
        else:
            return False

    def chrome_url(self, url):
        try:
            self.driver.get(url)

            # 等待页面加载
            WebDriverWait(self.driver, 30).until(EC.presence_of_element_located(
                (By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[1]/div[1] | //div[contains(text(), "你要观看的视频不存在")]')))

            if '你要观看的视频不存在' in self.driver.page_source:
                raise Exception('video not exist')

            time.sleep(5)

            return self.driver.page_source

        except Exception as e:
            raise e
        finally:
            self.last_scrape_time = datetime.datetime.now()

    def extract(self, html):
        """获取抖音属性"""
        selector = etree.HTML(html)  # 将源码转化为能被XPath匹配的格式

        try:
            fans = selector.xpath(r'//*[@id="root"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/p/span[2]')[0].text.strip()
            if 'w' in fans:
                fans = str(int(float(fans.replace('w', '')) * 10000))
        except:
            fans = 0

        try:
            comments = selector.xpath(r'//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[1]/div[2]/span')[0].text.strip()
        except:
            comments = 0

        try:
            likes = selector.xpath(r'//*[@id="root"]/div/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div[1]/div[1]/span')[0].text.strip()
        except:
            likes = 0

        soup = BeautifulSoup(html, 'lxml')
        title = soup.select_one('h1').text

        try:
            author = selector.xpath(r'//*[@id="root"]/div/div[2]/div[1]/div[2]/div/div[1]/div[2]/a/div/span/span/span/span/span//text()')[0]
        except:
            raise Exception("can't find author")

        try:
            post_date = selector.xpath(r"//span[contains(text(), '发布时间')]/text()")[1]
        except:
            post_date = ""

        reply_data = {
            'author': author,
            'title': title,
            'fans': int(fans),
            'comments': int(comments),
            'likes': int(likes),
            'post_date': post_date,
        }

        return reply_data
