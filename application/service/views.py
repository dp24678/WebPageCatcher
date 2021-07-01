# -*- coding: utf-8 -*-
"""pyppeteer 操作 访问浏览器"""
import asyncio
import hashlib
import os
import time
import validators
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    jsonify,
    send_from_directory,
)
# from flask_login import login_required, login_user, logout_user
from pyppeteer import launch, launcher
from application.settings import proxyUser, proxyPass, args_launch, proxyServer, TEMPORARY_FILES_PATH
from application.utils.utils import validators_url

WSE_DICT = {}  # 存储browserWSEndpoint
# 创建蓝图
blueprint = Blueprint("service", __name__, static_folder="../static")





async def intercept_request(req):
    """请求过滤"""
    if req.resourceType in ['image', 'media', "stylesheet", "font"]:
        await req.abort()
    else:
        await req.continue_()


async def runBrowser(url, path_dict, ua=None, need_proxy=None):
    print('runBrowser 函数')
    start_time = time.time()
    if len(WSE_DICT) == 0:
        print('创建浏览器对象')
        # 创建浏览器 不需要代理的
        browser = await launch({
            'handleSIGINT': False,
            'handleSIGTERM': False,
            'handleSIGHUP': False,  # 以上禁用信号
            'headless': True,  # 无头模式
            'dumpio': True,
            'autoClose': False,  # 避免长时间运行 内存泄漏
            'ignoreDefaultArgs': ['--enable-automation'],  # 过滤掉列表中的默认参数
            'args': args_launch,
            'defaultViewport': None  # 网页默认大小  值为None 代表自适应浏览器大小
        })
        print('浏览器创建成功')
        WSE_DICT['wsEndpoint'] = browser.wsEndpoint
    else:
        browserWSEndpoint = WSE_DICT['wsEndpoint']
        browser = await launcher.connect({'browserWSEndpoint': browserWSEndpoint})
        print('使用已存在的浏览器')

    page = await browser.newPage()  # "通过 Browser 对象创建页面 Page 对象"
    # await page.setCacheEnabled()
    if ua:
        await page.setUserAgent(ua)
    # await page.setViewport({"width": 1000, "height": 900})  # 改变 页面大小
    if need_proxy:
        await page.authenticate({'username': proxyUser, 'password': proxyPass})
    # await page.setRequestInterception(True)
    # page.on('request', intercept_request)
    await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator,'
                                     '{ webdriver:{ get: () => undefined } }) }')  # 本页刷新后值不变

    try:
        await page.goto(url, {'waitUntil': 'networkidle0'}),
        await asyncio.sleep(3)
        print(897398247)
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
        # content = await page.content()
        # iframes = page.frames
        # for iframe in iframes:
        #     content += await iframe.content()
    except Exception as e:
        content = '浏览器获取网页源码时异常： %s' % e

    # 获取截图  fullPage=True：获取整个网页的截图（滚动到底部）
    url_md5 = hashlib.md5(url.encode()).hexdigest()
    # screenshot_path = './screenshots/%s.png' % url_md5
    screenshot_path = TEMPORARY_FILES_PATH + url_md5 + '.' + 'png'
    await page.screenshot(path=screenshot_path, fullPage=True)
    path_dict['local_img_path'] = screenshot_path
    print('截图 ok')
    # 获取网页转成pdf
    await page.emulateMedia('screen')
    pdf_path = TEMPORARY_FILES_PATH + url_md5 + '.' + 'pdf'
    await page.pdf({'path': pdf_path,
                    'printBackground': True,
                    'displayHeaderFooter': True,
                    'landscape': True  # 关键 可以将某些图标渲染出来（个人理解为是否渲染网页背景）
                    # 'margin': {'top': '1in',
                    #            'right': '1in',
                    #            'bottom': '1in',
                    #            'left': '1in'}
                    })
    path_dict['local_pdf_path'] = pdf_path
    print('导出 ok')
    # await asyncio.sleep(50)
    await page.close()
    # await browser.close()
    end_time = time.time()
    print('耗时：%s' % (end_time - start_time))


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


def screenshot(url):
    print('screenshot 函数')
    path_dict = {}
    asyncio.run(runBrowser(url, path_dict))
    return path_dict


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
@blueprint.route("/get_html_content", methods=["GET", "POST"])
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


@blueprint.route("/screenshot", methods=["GET", "POST"])
def get_screenshot():
    """
    网页截屏
    :return:
    """
    # dirpath = os.path.join(current_app.root_path, 'temporay_files')
    dirpath = os.path.join(os.path.abspath(os.path.join(current_app.root_path, "..")), 'temporary_files')
    print(dirpath)
    statrt_time = time.time()
    url = request.args.get("url")
    print('获取到的url：', url, '校验结果：', validators_url(url))
    if not validators_url(url):
        return jsonify({'msg': '请传入正确的url'})
    # local_img_path = screenshot(url)['local_img_path']
    end_time = time.time()
    # return jsonify({'local_img_path': local_img_path, 'consuming_time': round(end_time - statrt_time, 2)})
    # return jsonify({'local_img_path': 43, 'consuming_time': round(end_time - statrt_time, 2)})
    # return send_from_directory('./', 'a')
    print('准备传递文件')
    return send_from_directory(dirpath, 'a.png',as_attachment=True)
    # return send_from_directory('../../../temporay_files', '58395ada196e86ed42909d75b290bd8f.png')
    # try:
    #     # return send_from_directory('../../../temporay_files', '58395ada196e86ed42909d75b290bd8f.png')
    #     return send_from_directory('./', 'a')
    # except Exception as e:
    #     print(e)
    #     return str(e)


@blueprint.route("/pdf", methods=["GET", "POST"])
def get_pdf():
    """
    网页转pdf
    :return:
    """
    url = request.args.get("url")
    print('获取到的url：', url)
    if validators_url(url):
        return jsonify({'msg': '请传入正确的url'})
    local_img_path = screenshot(url)['local_img_path']
    return jsonify({'local_img_path': local_img_path})
