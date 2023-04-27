# -*- coding: utf-8 -*-

import os
import asyncio
import requests
import pyppeteer
import json
from bs4 import BeautifulSoup

async def main():
    # 启动无头浏览器
    await pyppeteer.chromium_downloader.download_chromium()
    browser = await pyppeteer.launch(headless=True)
    
    page = await browser.newPage()

    # 52签到页
    await page.goto("https://www.52pojie.cn/home.php?mod=task&do=apply&id=2")
    

    # 设置cookies
    cookies_list = os.environ['PjCookie']
    for cookie in cookies_list:
        # 添加cookies
        await page.setCookie(cookie)

    # 刷新页面
    await page.reload()
    await asyncio.sleep(2)
    content = await page.content()
    
 
    # 获取签到结果并推送
    result, fc = check(content)
    
    token = os.environ['PushToken']
    pushplus_push(token= token, title=result, content=fc, topic='')

    # 关闭浏览器
    await browser.close()

def check(content):
    fb = BeautifulSoup(content, "html.parser")
    fc = fb.find("div", id="messagetext").find("p").text
    if "您需要先登录才能继续本操作" in fc:
        result = "52Cookie失效"
    elif "恭喜" in fc:
        result = "52签到成功"
    elif "已申请过此任务" in fc:
        result = "52今日已签到"
    else:
        result = "52签到失败"
    return result, fc

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
    print(response.json())
    return response.json()


if __name__ == '__main__':
    # 启动事件循环
    asyncio.get_event_loop().run_until_complete(main())


