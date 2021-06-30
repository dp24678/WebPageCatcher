# -*- coding: utf-8 -*-
import asyncio
import json
import time
from flask import Flask, jsonify, request
from pyppeteer import launcher, launch
from pyppeteer.chromium_downloader import chromium_excutable, chromium_executable
from config import MAX_WSE, WSE_DICT, proxyServer, proxyUser, proxyPass

args_launch = [
    '--disable-dev-shm-usage',
    '--no-first-run',
    '--no-zygote',

    '--no-sandbox',  # 禁止沙箱模式
    '--no-default-browser-check',  # 不检查默认浏览器
    '--disable-extensions',
    '--hide-scrollbars',
    '--disable-bundled-ppapi-flash',
    '--mute-audio',
    '--disable-setuid-sandbox',
    '--disable-gpu',
    "--window-size=500,450",
    "--disable-infobars"  # 禁止提示 浏览器被驱动的提示信息
]

app = Flask(__name__)


async def intercept_request(req):
    """请求过滤"""
    if req.resourceType in ['image', 'media', "stylesheet", "font"]:
        await req.abort()
    else:
        await req.continue_()


async def runBrowser(url, html_content_dict, ua=None, need_proxy=None):
    if need_proxy:
        if WSE_DICT.get('is_proxy'):
            browserWSEndpoint = WSE_DICT.get('is_proxy')
            browser = await launcher.connect({'browserWSEndpoint': browserWSEndpoint})
        else:
            # 创建浏览器 需要代理的
            args_launch.append("--proxy-server=" + proxyServer)
            browser = await launch({
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False,  # 以上禁用信号
                'headless': False,
                'dumpio': True,
                'autoClose': False,  # 避免长时间运行 内存泄漏
                'ignoreDefaultArgs': ['--enable-automation'],  # 过滤掉列表中的默认参数
                'args': args_launch
            })
            WSE_DICT['is_proxy'] = browser.wsEndpoint
    else:
        if WSE_DICT.get('no_proxy'):
            browserWSEndpoint = WSE_DICT.get('no_proxy')
            browser = await launcher.connect({'browserWSEndpoint': browserWSEndpoint})
        else:
            # 创建浏览器 不需要代理的
            browser = await launch({
                'handleSIGINT': False,
                'handleSIGTERM': False,
                'handleSIGHUP': False,  # 以上禁用信号
                'headless': False,
                'dumpio': True,
                'autoClose': False,  # 避免长时间运行 内存泄漏
                'ignoreDefaultArgs': ['--enable-automation'],  # 过滤掉列表中的默认参数
                'args': args_launch
            })
            WSE_DICT['no_proxy'] = browser.wsEndpoint





    page = await browser.newPage()  # "通过 Browser 对象创建页面 Page 对象"
    # await page.setCacheEnabled()
    if ua:
        await page.setUserAgent(ua)
    # await page.setViewport({"width": 1000, "height": 900})  # 改变 页面大小
    if need_proxy:
        await page.authenticate({'username': proxyUser, 'password': proxyPass})
    await page.setRequestInterception(True)
    page.on('request', intercept_request)
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                     '{ webdriver:{ get: () => undefined } }) }')  # 本页刷新后值不变

    try:
        await page.goto(url, {'waitUntil': 'networkidle0'}),
        await asyncio.sleep(4)
        # await page.waitForNavigation({
        #     'waitUntil': "load",
        #     'timeout': 5000
        # })
        # await asyncio.gather(
        #     await page.goto(url, {'timeout': 60000}),
        #     await page.waitForNavigation({'timeout': 30000})
        # )
        # await asyncio.wait([
        #     await page.goto(url, {'timeout': 30000}),
        #     await page.waitForNavigation({'timeout': 30000})
        # ])
        content = await page.content()
        iframes = page.frames
        for iframe in iframes:
            content += await iframe.content()
    except Exception as e:
        content = '浏览器获取网页源码时异常： %s' % e

    html_content_dict['html_content'] = content
    await page.close()
    # await browser.close()


def get_html(host, ua, need_proxy):
    html_content_dict = {}
    # new_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(new_loop)
    # loop = asyncio.get_event_loop()  # 创建一个事件循环
    # new_loop.run_until_complete(runBrowser(host, html_content_dict, ua, need_proxy))  # 将协程加入到事件循环loop
    # loop.close()
    asyncio.run(runBrowser(host, html_content_dict, ua, need_proxy))
    # print(html_content_dict)
    return html_content_dict


@app.route('/')
def index():
    return jsonify({'cookiesDict': {}})


# @app.route('/cookie', methods=['POST', 'get'])
# def get_cookie():
#     url = 'https://www.msxf.com/news/msxw'
#     cookiesDict = {}
# 
#     loop1 = asyncio.new_event_loop()  # 创建一个事件循环
#     asyncio.set_event_loop(loop1)
#     loop = asyncio.get_event_loop()  # 创建一个事件循环
#     loop.run_until_complete(runBrowser(url, cookiesDict))  # 将协程加入到事件循环loop
#     loop.close()
#     return jsonify({'cookiesDict': cookiesDict})
# 
# 
# @app.route('/get_cookie_from_redis', methods=['POST', 'get'])
# def get_cookie_from_redis():
#     host = request.args.get("host")
#     if not host:
#         return jsonify({'msg': '请传入host'})
#     cookieStr = redis_queue.get_cookie(host)
#     if cookieStr:
#         cookiesDict = json.loads(cookieStr)
#     else:  # 没有获取到对应的cookie
#         # 1、看看是不是已经在 update_cookie了
#         if host in requesting_queue:
#             while True:
#                 time.sleep(0.5)
#                 print('requesting_queue:', requesting_queue)
#                 if host not in requesting_queue:
#                     cookieStr = redis_queue.get_cookie(host)
#                     cookiesDict = json.loads(cookieStr)
#                     break
#         else:
#             # 没有
#             cookiesDict = update_cookie(host)
#     print('最终返回的cookies；', cookiesDict)
#     return jsonify({'cookiesDict': cookiesDict})
# 
# 
# @app.route('/get_update_cookie', methods=['POST', 'get'])
# def get_update_cookie():
#     host = request.args.get('host')
#     cookiesDict = update_cookie(host)
#     return jsonify({'cookiesDict': cookiesDict})
@app.route('/get_html_content', methods=['POST', 'get'])
def get_html_content():
    host = request.args.get("host")
    ua = request.args.get('ua')
    need_proxy = request.args.get('need_proxy')
    if not host:
        return jsonify({'msg': '请传入host'})
    elif not ua:
        return jsonify({'msg': '请传入user-agent'})
    elif need_proxy not in ['1', '0']:
        return jsonify({'msg': '参数need_proxy 必须是 1 或 0'})
    need_proxy = int(need_proxy)
    html_content = get_html(host, ua, need_proxy)['html_content']
    return jsonify({'html_content': html_content})


@app.route('/runcode', methods=['POST', 'get'])
def run_code():
    formData = request.form.to_dict()
    code_str = formData.get('code_str')
    try:
        exec(code_str)  # 执行爬虫脚本
        # code_str 中必须返回名为 data的变量
        return jsonify({'data': formData['data']})
    except Exception as e:
        print(e)
        return jsonify({'data': str(e)})


if __name__ == '__main__':
    # 删除本地缓存数据
    # await page.evaluate("window.localStorage.clear();")
    # 删除Cookies
    # await page.deleteCookie()
    # 当前正在请求的链接 队列
    requesting_queue = []
    # new_loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(new_loop)
    # new_loop.run_until_complete(runBrowser('http://baidu.com', {}))  # 将协程加入到事件循环loop
    # new_loop.close()
    asyncio.run(runBrowser('http://baidu.com', {}))
    app.run(host='0.0.0.0', port=5001, threaded=True)
