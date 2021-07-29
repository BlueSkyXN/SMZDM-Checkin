import requests 
from bs4 import BeautifulSoup
import time
import re
import rsa
import base64
import hashlib
import os
import sys
import json

sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass
from urllib import parse

result = '🏆什么值得买签到姬🏆\n'

cookie = os.environ.get("cookie")
TGBOTAPI = os.environ.get("TGBOTAPI")
TGID = os.environ.get("TGID")

def pushtg(data):
    global TGBOTAPI
    global TGID
    requests.post(
        'https://api.telegram.org/bot'+TGBOTAPI+'/sendMessage?chat_id='+TGID+'&text='+data)

# 【BOTAPI】格式为123456:abcdefghi
# 【TGID】格式为123456（人）或者-100123456（群组/频道）





def main(*arg):
    global result
    try:
        msg = ""
        s = requests.Session()
        s.headers.update({'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'})
        t = round(int(time.time() * 1000))
        url = f'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin?_={t}'

        headers = {
            "cookie" : cookie,
            'Referer': 'https://www.smzdm.com/'
            }

        r = s.get(url, headers=headers, verify=False)
        print(r.text.encode('latin-1').decode('unicode_escape'))
        if r.json()["error_code"] != 0:
            pusher("smzdm  Cookie过期", r.text[:200])
            msg += "smzdm cookie失效"
            result += "cookie失效"
        else:
            msg += "smzdm签到成功"
            result += "签到成功"
    except Exception as e:
        print('repr(e):', repr(e))
        msg += '运行出错,repr(e):'+repr(e)
        result += "运行出错"
    return msg + "\n"

def smzdm_pc(*arg):
    global result
    msg = ""
    global cookie
    if "\\n" in cookie:
        clist = cookie.split("\\n")
    else:
        clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += main(cookie)
        i += 1
    return msg


if __name__ == "__main__":
    if cookie:
        print("----------什么值得买开始尝试签到----------")
        smzdm_pc()
        print("----------什么值得买签到执行完毕----------")
        pushtg(result)

    
def main_handler(event, context):
    if cookie:
        print("----------什么值得买开始尝试签到----------")
        smzdm_pc()
        print("----------什么值得买签到执行完毕----------")
        pushtg(result)
