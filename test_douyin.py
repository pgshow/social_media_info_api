import time

import requests

douyin_urls = """https://v.douyin.com/J3deAu1/
https://v.douyin.com/J31X861/
https://v.douyin.com/J3JSm82/
https://v.douyin.com/J31qP7g/
https://v.douyin.com/J31td8d/
https://v.douyin.com/J3RGgDW/
https://v.douyin.com/J31dQaK/
https://v.douyin.com/J31fDDq/
https://v.douyin.com/J3eKSSL/
https://v.douyin.com/J3e2oq8/
https://v.douyin.com/eaAPrvH/
https://v.douyin.com/eaAWNcJ/
https://v.douyin.com/eaATF2B/
https://v.douyin.com/eaDRYsf/
https://v.douyin.com/eahK9uC/
https://v.douyin.com/eaAQ9FA/
https://v.douyin.com/earnyPe/
https://v.douyin.com/earvTy4/
https://v.douyin.com/eaAk49h/
https://v.douyin.com/eakNao3/
https://v.douyin.com/emDwPPT
https://v.douyin.com/e5QV4rh/
https://v.douyin.com/emDGsTr
https://v.douyin.com/e541T1n/
https://v.douyin.com/e541T1n/
https://v.douyin.com/e5AYxWd/
https://v.douyin.com/e5SMWdV/
https://v.douyin.com/e5A6tWF/
https://v.douyin.com/ePfXkhn/
https://v.douyin.com/ePjfsQx/
https://v.douyin.com/ePeCF3F/
https://v.douyin.com/ePeBmo1/
https://v.douyin.com/ePRo878/
https://v.douyin.com/ePeKgRp/
https://v.douyin.com/efo98WA/
https://v.douyin.com/efofHB9/
https://v.douyin.com/efoM7WU/
https://v.douyin.com/eUbu5MD/
https://v.douyin.com/eUg4w9J/
https://v.douyin.com/eUUd8NH/
https://v.douyin.com/eU8tPN3/
https://v.douyin.com/eDWVygo/
https://v.douyin.com/eDtWS5G/
https://v.douyin.com/eDLwa7N/
https://v.douyin.com/eDeCBNN/
https://v.douyin.com/eD8kYLg/
https://v.douyin.com/eDLMB4u/
https://v.douyin.com/eDLDdRR/
https://v.douyin.com/eDLtRyB/
https://v.douyin.com/eAvxquv/
https://v.douyin.com/eAcURa8/
https://v.douyin.com/eAvfCAe/
https://v.douyin.com/eAv653W/
https://v.douyin.com/eBwxPMu/
https://v.douyin.com/eBKSAGs/
https://v.douyin.com/eBwb2Gt/
https://v.douyin.com/eS1FDHq/
https://v.douyin.com/ePR4B5w/
https://v.douyin.com/ePYHeES/
https://v.douyin.com/efo661y/
https://v.douyin.com/ePF4oWY/
https://v.douyin.com/ePJD2DK/
https://v.douyin.com/ePJQMQQ/
https://v.douyin.com/ePeR7Ps/
https://v.douyin.com/ePYbjvN/
https://v.douyin.com/eP6mKkC/
https://v.douyin.com/eyW31KH/
https://v.douyin.com/eyCDXRc/
https://v.douyin.com/eybCFhx/
https://v.douyin.com/eykFp3j/
https://v.douyin.com/eBwfL5Q/
https://v.douyin.com/eBK2Lxs/
https://v.douyin.com/eBbteoM/
https://v.douyin.com/eBgeJyU/
https://v.douyin.com/eBbnoLN/
https://v.douyin.com/eBbxJbj/
https://v.douyin.com/eBUSSKe/
https://v.douyin.com/eBAKSPg/
https://v.douyin.com/eBAsgRA/
https://v.douyin.com/eBDHRGk/
https://v.douyin.com/eBA7cd5/
https://v.douyin.com/eBD5dTP/
https://v.douyin.com/eBAvcqS/
https://v.douyin.com/eBUMNhJ/
https://v.douyin.com/eBDgU6k/
https://v.douyin.com/eBFr4V1/
https://v.douyin.com/eBrb9pj/
https://v.douyin.com/eBFwsuA/
https://v.douyin.com/eBN7FuQ/
https://v.douyin.com/eBFhxVy/
https://v.douyin.com/eBFsq9G/
https://v.douyin.com/eBY57NL/
https://v.douyin.com/eBrKHeu/
https://v.douyin.com/eBYRbRb/
https://v.douyin.com/eB2eHCR/
https://v.douyin.com/eBNEKPk/
"""

if __name__ == '__main__':
    urls = douyin_urls.split('\n')
    for url in urls:
        try:
            print('access', url)
            post_data = {
                'url': url,
                'platform': 'tiktok'
            }
            r = requests.post('http://localhost:5000/api', data=post_data, timeout=60)
            print(r.status_code, r.text)

        except Exception as e:
            print(e)
        finally:
            time.sleep(22)
