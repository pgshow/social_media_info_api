import re
from selenium_stealth.selenium_stealth import stealth


def init_base_cap(options):
    options.add_argument("--headless")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--no-sandbox")
    # options.add_argument("--start-maximized")
    options.add_argument("--disable-impl-side-painting")
    options.add_argument("--disable-accelerated-2d-canvas")
    options.add_argument("--disable-accelerated-jpeg-decoding")
    options.add_argument("--test-type=ui")
    options.add_argument("--ignore-certificate-errors")

    prefs = {
        'profile.default_content_setting_values': {
            # 'images': 2,
            'permissions.default.stylesheet': 2,
        }
    }
    options.add_experimental_option("prefs", prefs)


def add_stealth_js(driver):
    stealth(driver,
            languages=["en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Google Inc. (NVIDIA)",
            renderer="ANGLE (NVIDIA, NVIDIA GeForce RTX 3060 Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.7005)",
            fix_hairline=True,
            )


def get_cookies(cookie_raw):
    """
    通过原生cookie获取cookie字段
    :param cookie_raw: {str} 浏览器原始cookie
    :return: {dict} cookies
    """
    dic = {}
    for line in cookie_raw.split("; "):
        if '=' not in line:
            continue
        item = line.split("=", 1)
        dic[item[0]] = item[1]

    return dic


def first_sentence(text):
    """分句，返回段落第一句话"""
    if not text:
        return''

    text = re.sub(r'([。！？;；,，\?])([^”])', r"\1\n\2", text)  # 单字符断句符
    text = re.sub(r'(\.{6})([^”])', r"\1\n\2", text)  # 英文省略号
    text = re.sub(r'(\…{2})([^”])', r"\1\n\2", text)  # 中文省略号
    text = re.sub('(”)', '”\n', text)  # 把分句符\n放到双引号后，注意前面的几句都小心保留了双引号
    text = text.rstrip()  # 段尾如果有多余的\n就去掉它
    sentences = text.split("\n")
    if len(sentences) > 0:
        return sentences[0]
    else:
        return ''
