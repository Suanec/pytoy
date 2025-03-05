# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/3.

import asyncio
from pyppeteer import launch

async def save_slides_as_pdf(url, output_path):
    browser = await launch(headless=True)
    try:
        page = await browser.newPage()

        # 导航到幻灯片页面
        await page.goto(url, waitUntil='networkidle2')

        # 获取页面的视口尺寸，这可能更接近幻灯片的实际显示尺寸
        viewport = await page.evaluate('''() => {
            return { width: document.documentElement.scrollWidth, height: document.documentElement.scrollHeight };
        }''')

        # 调整PDF生成的选项，保持与视口尺寸一致，去除边距以接近原始显示
        pdf_options = {
            "path": output_path,
            # "format": 'A4',  # 或者可以尝试 'Letter' 或者直接指定宽度和高度，如 width: viewport.width, height: viewport.height
            # "height": viewport["width"],
            # "width": viewport["height"],
            "width": 405,
            "height": 720,
            "margin": { "top": '0mm', "right": '0mm', "bottom": '0mm', "left": '0mm' },
            "printBackground": True,  # 如果页面有背景色或图像，确保它们被打印
            "landscape": True,  # 如果幻灯片横向展示，可以设置为True
            # 'preferCSSPageSize': False,  # 不尊重CSS定义的页面大小
        }
        #     pdf_options = {
        #     'path': output_path,
        #     'width': f"{dimensions['width']}px",  # 使用像素单位
        #     'height': f"{dimensions['height']}px",
        #     'margin': {'top': '0mm', 'right': '0mm', 'bottom': '0mm', 'left': '0mm'},
        #     'printBackground': True,  # 打印背景颜色和图像
        #     'preferCSSPageSize': False,  # 不尊重CSS定义的页面大小
        # }


        # 生成PDF
        await page.pdf(pdf_options)

        # 关闭浏览器
        await browser.close()
    except Exception as e:
        raise e
    finally:
        await browser.close()

if __name__ == '__main__':
    # 使用示例
    url = 'http://127.0.0.1:5500'  # 替换为实际幻灯片网址
    output_path = 'slides.pdf'
    asyncio.run(save_slides_as_pdf(url, output_path))
    # browser = launch(headless=True)
    # browser.close()
