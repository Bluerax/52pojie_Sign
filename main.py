# -*- coding: utf-8 -*-

import os
import requests
import json
from bs4 import BeautifulSoup

def pushplus_push(token, title, content, topic):
    url = 'http://www.pushplus.plus/send'
    headers = {'Content-Type': 'application/json'}
    data = {
        'token': token,
        'title': title,
        'content': content,
        'topic': topic
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()





def sign(cookie):
    result = ""
    headers = {
        "Cookie": cookie,
        "ContentType": "text/html;charset=gbk",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Referer': 'https://www.52pojie.cn/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    requests.session().put(
        "https://www.52pojie.cn/home.php?mod=task&do=apply&id=2referer=%2F", headers=headers
    )
    fa = requests.session().put(
        "https://www.52pojie.cn/home.php?mod=task&do=draw&id=2referer=%2F", headers=headers
    )
    fb = BeautifulSoup(fa.text, "html.parser")
    fc = fb.find("div", id="messagetext").find("p").text
    if "您需要先登录才能继续本操作" in fc:
        result += "Cookie 失效"
    elif "恭喜" in fc:
        result += "签到成功"
    elif "不是进行中的任务" in fc:
        result += "今日已签到"
    else:
        result += "签到失败"
    
    pushplus_push(token=token, title=result, content=result, topic='')
    return result 

def main():
    b = os.environ['PojieCookie']
    cookie = b
    token = os.environ['PushToken']
    sign_msg = sign(cookie=cookie)
    print(sign_msg)


if __name__ == "__main__":
    main()


