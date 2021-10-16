# 微博，抖音，小红书 带 web api 的爬虫
打开 post_demo.html

向 api 提交对应的链接，爬虫会自动从社交媒体里获取信息，然后从api返回信息

#api说明
api 接收参数很简单，可以看 post_demo.html

api 返回json：

成功:

{"status":true, "msg":"success","platform":"redbook","profile":{"author":"\u5305\u5bb9\","comments":1,"fans":1124,"likes":18,"share":0,"title":"\u5b9d\u5988\u7231"}}

失败:

{"status":false,"msg":"failed reason","platform":"redbook"}

频率太快会提示：

{"status":false,"platform":"weibo","msg":"Please slow down, interval is 25 seconds"}

#注意：
- 刚启动 main.py，需要登录微博，访问 http://ip:5000/weibo ，扫描截图里面的二维码。
- 由于是单IP单账户，所以频率不能太快。微博，抖音爬虫间隔限制在25秒，小红书爬虫间隔为45秒
- 抖音没有分享数 share
- 小红书有部分文章无法获取到文章信息，提示 note censoring