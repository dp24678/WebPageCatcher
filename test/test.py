import asyncio
import time

from pyppeteer import launch

async def main():
    browser = await launch({
        'handleSIGINT': False,
        'handleSIGTERM': False,
        'handleSIGHUP': False,  # 以上禁用信号
        'headless': True,  # 无头模式
        'dumpio': True,
        'autoClose': False,  # 避免长时间运行 内存泄漏
        'ignoreDefaultArgs': ['--enable-automation'],  # 过滤掉列表中的默认参数
        'args': [
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
            # "--window-size=500,450",
            '--start-maximized',  # 浏览器启动最大化
            "--disable-infobars"  # 禁止提示 浏览器被驱动的提示信息
        ],
        'defaultViewport': None  # 网页默认大小  值为None 代表自适应浏览器大小
    })
    page = await browser.newPage()
    await page.goto('https://www.52pojie.cn/')
    await asyncio.sleep(2)
    # time.sleep(5)
    pdf_path = 'a2.pdf'
    # await page.setViewport({'isLandscape':True})
    await page.emulateMedia('screen')
    # await page.emulateMedia('print')
    await page.pdf({'path': pdf_path,
                    'printBackground': True,
                    'displayHeaderFooter': True,
                    'landscape': True  # 关键 可以将某些图标渲染出来（个人理解为是否渲染网页背景）
                    # 'margin': {'top': '1in',
                    #            'right': '1in',
                    #            'bottom': '1in',
                    #            'left': '1in'}
                    })
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
