import hashlib

import requests

id = '6131f4350000000021039981'

api = f'/fe_api/burdock/weixin/v2/note/{id}/single_feed'
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
    'Accept-Encoding': 'gzip,deflate,br',
}

url = 'https://www.xiaohongshu.com' + api
r = requests.get(url=url, headers=headers, timeout=45)
print(r.json())