import threading
import time

from flask import Flask, request, jsonify, render_template
from loguru import logger

import config
import keep_cookie

# # 保持微博cookie有效
# x = keep_cookie.Weibo()
# x.start()

config.DOUYIN_OBJ.open_chrome()

logger.warning(f'Please login Weibo at {config.HOST_URL}weibo after web server launched')

app = Flask(__name__)


@app.route('/weibo')
def weibo_login():
    try:
        qr_code = config.WB_OBJ.login()  # 登录并初始化一个chrome
        html = render_template('weibo_qr_code.html', img=qr_code)
        return html
    except Exception as e:
        return str(e)


@app.route('/api', methods=['POST'])
def api():
    platform = request.form['platform']
    url = request.form['url']

    # json 返回数据
    data = {
        "platform": platform,
        "status": "",
        "msg": "",
        "profile": None
    }

    if platform == 'weibo':
        data['platform'] = 'weibo'

        reply = config.WB_OBJ.scrape(url)  # 爬取数据

        if isinstance(reply, dict):
            data['status'] = True
            data['msg'] = 'success'
            data['profile'] = reply
        else:
            data['status'] = False
            data['msg'] = reply

    elif platform == 'tiktok':
        data['platform'] = 'tiktok'

        reply = config.DOUYIN_OBJ.scrape(url)  # 爬取数据

        if isinstance(reply, dict):
            data['status'] = True
            data['msg'] = 'success'
            data['msg'] = reply
        else:
            data['status'] = False
            data['msg'] = reply

    elif platform == 'redbook':
        data['platform'] = 'redbook'

        reply = config.REDBOOK_OBJ.scrape(url)  # 爬取数据

        if isinstance(reply, dict):
            data['status'] = True
            data['msg'] = 'success'
            data['profile'] = reply
        else:
            data['status'] = False
            data['msg'] = reply
    else:
        data['status'] = "err"
        data['msg'] = "unknown platform"

    return jsonify(data)


if __name__ == '__main__':
    # # 保持微博cookie有效
    # x = keep_cookie.Weibo()
    # x.start()
    app.run(debug=False, host="0.0.0.0", use_reloader=False)
    pass