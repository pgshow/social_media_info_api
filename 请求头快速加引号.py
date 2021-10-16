import re

#  下方引号内添加替换掉请求头内容
headers_str = """
Host: www.xiaohongshu.com
Connection: keep-alive
Authorization: wxmp.5bcdd01c-1deb-4ba3-a02c-c43aa0d70622
Device-Fingerprint: WHJMrwNw1k/EoDusEysSIKP/+TAIZAA6uSNy9VQTBtKV4wTBvWjnhXAdQTic3/9k5dhxPdQN6LyI27nRxz2JSXwZ0t42D2nEwdCW1tldyDzmauSxIJm5Txg==1487582755342
User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat
X-Sign: Xa63e8e56e4e967a8a6e6f71630ec3b92
content-type: application/json
Referer: https://servicewechat.com/wxb296433268a1c654/59/page-frame.html
Accept-Encoding: gzip, deflate, br
"""

pattern = '^(.*?):(.*)$'

for line in headers_str.splitlines():
    print(re.sub(pattern, '\'\\1\':\'\\2\',', line).replace(' ', ''))
