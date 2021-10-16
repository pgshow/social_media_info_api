import datetime
import hashlib
import json
import re
import time
import requests
import fc
from loguru import logger
from bs4 import BeautifulSoup
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By


class Redbook:
    def __init__(self):
        self.scraping = False
        self.last_scrape_time = datetime.datetime.now()

    def scrape(self, url):
        """从小红书爬数据"""
        if self.scraping:
            return 'Try later, another url is scraping right now'

        if self.too_fast():
            return 'Please slow down, interval is 60 seconds'

        logger.info(f'scraping {url}')

        self.scraping = True  # 控制只启动一个爬虫

        try:
            json_data = self.fetch(url)

            if not isinstance(json_data, dict) or not json_data['success']:
                # 文章异常
                raise Exception(str(json_data['msg']))

            return self.extract(json_data)
        except Exception as e:
            return f'scrape {url} err: {e}'
        finally:
            self.scraping = False
            self.last_scrape_time = datetime.datetime.now()

    def too_fast(self):
        """频繁度"""
        if (datetime.datetime.now() - self.last_scrape_time).seconds < 59:
            return True
        else:
            return False

    def fetch(self, url):
        book_id = self.get_book_id(url)
        if not book_id:
            raise Exception('url is illegal')

        # 破解 x_sign
        api = f'/fe_api/burdock/weixin/v2/note/{book_id}/single_feed'
        x_sign = "X"
        m = hashlib.md5()
        m.update((api + "WSUDD").encode())
        x_sign = x_sign + m.hexdigest()

        headers = {
            'Host': 'www.xiaohongshu.com',
            'Connection': 'keep-alive',
            'Authorization': 'wxmp.5bcdd01c-1deb-4ba3-a02c-c43aa0d70622',
            'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/53.0.2785.143Safari/537.36MicroMessenger/7.0.9.501NetType/WIFIMiniProgramEnv/WindowsWindowsWechat',
            'X-Sign': x_sign,
            'content-type': 'application/json',
            'Referer': 'https://servicewechat.com/wxb296433268a1c654/59/page-frame.html',
            'Accept-Encoding': 'gzip,deflate,br',
        }

        # proxy_pool = {
        #     "http": "http://doge:doge@120.25.227.214:10000/",
        #     "https": "http://doge:doge@120.25.227.214:10000/",
        # }
        proxy_pool = {
            "http": "http://doge:doge@127.0.0.1:10000/",
            "https": "http://doge:doge@127.0.0.1:10000/",
        }

        url = 'https://www.xiaohongshu.com' + api
        try:
            r = requests.get(url=url, headers=headers, proxies=proxy_pool, timeout=45)
        except Exception as e:
            if 'Failed to establish a new connection' in str(e):
                raise Exception('Proxy host maybe not online')
            else:
                raise e

        if '该笔记已删除' in r.text:
            raise Exception('This note already been removed')

        # if r.status_code is not 200:
        #     raise Exception(f'fetch failed, status: {r.status_code}')

        return r.json()

    def get_book_id(self, url):
        """获取小红书文章ID"""
        match = re.search(r'/discovery/item/([a-f\d]{24})', url)
        if match:
            return match.group(1)

    def extract(self, data_json):
        """获取小红书文章属性"""
        if data_json['data']['title'] == '':
            data_json['data']['title'] = fc.first_sentence(data_json['data']['desc'])

        reply_data = {
            'author': data_json['data']['user']['nickname'],
            'fans': data_json['data']['user']['fans'],
            'title': data_json['data']['title'],
            'share': data_json['data']['shareCount'],
            'comments': int(data_json['data']['comments']),
            'likes': int(data_json['data']['likes'], )
        }

        return reply_data
