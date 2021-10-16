import time
from multiprocessing import Process
import requests
from loguru import logger


class Weibo(Process):
    def run(self):
        """通过不断刷新来保持微博cookie有效"""
        time.sleep(5)
        while 1:
            try:
                post_data = {
                    'url': 'https://weibo.com/',
                    'platform': 'weibo'
                }
                r = requests.post('http://localhost:5000/api', data=post_data, timeout=60)
                if r.status_code == 200:
                    logger.info('keep weibo session')

            except:
                pass
            finally:
                time.sleep(3600)
