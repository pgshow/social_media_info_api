import hashlib

import requests

id = '615e7699000000002103f773'
uid = '54f5d8c54fac6330047ba4fa'

api = f'/fe_api/burdock/weixin/v2/note/{id}/single_feed'
# api = f'/fe_api/burdock/weixin/v2/user/{uid}'
x_sign = "X"
m = hashlib.md5()
m.update((api + "WSUDD").encode())
x_sign = x_sign + m.hexdigest()
print(x_sign)

headers = {
    'Host': 'www.xiaohongshu.com',
    'Connection': 'keep-alive',
    'Authorization': 'wxmp.5bcdd01c-1deb-4ba3-a02c-c43aa0d70622',
    'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/53.0.2785.143Safari/537.36MicroMessenger/7.0.9.501NetType/WIFIMiniProgramEnv/WindowsWindowsWechat',
    'X-Sign': x_sign,
    'content-type': 'application/json',
    'Referer': 'https://servicewechat.com/wxb296433268a1c654/59/page-frame.html',
    # 'Device-Fingerprint': 'WHJMrwNw1k/EoDusEysSIKP/+TAIZAA6uSNy9VQTBtKV4wTBvWjnhXAdQTic3/9k5dhxPdQN6LyI27nRxz2JSXwZ0t42D2nEwdCW1tldyDzmauSxIJm5Txg==1487582755342',
    'Accept-Encoding': 'gzip,deflate,br',
}

url = 'https://www.xiaohongshu.com' + api

proxies = {
    "http": "http://doge:doge@120.25.227.214:10000/",
}

proxy_pool = {
    "http": "http://doge:doge@120.25.227.214:10000/",
    "https": "http://doge:doge@120.25.227.214:10000/",
}

r = requests.get(url=url, headers=headers, proxies=proxy_pool, timeout=45)
print(r.json())
