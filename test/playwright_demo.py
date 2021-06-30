# -*- encoding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto("https://www.52pojie.cn/")
        print(await page.title())
        await page.emulate_media(media="screen")

        await page.pdf(path='./test.pdf', print_background=True)
        await browser.close()

asyncio.run(main())