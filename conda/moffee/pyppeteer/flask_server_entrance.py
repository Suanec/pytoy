# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'
# Created by enzhao on 2025/3/13.

import logging
import json
from flask import Flask
from flask import request
from md_to_slides_pdf_allinone import md_to_slide_entrance
app = Flask(__name__)
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
def get_local_ip():
    local_ip = ''
    try:
        import socket
        socket_objs = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]
        ip_from_ip_port = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in socket_objs][0][1]
        ip_from_host_name = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith('127.')][:1]
        local_ip = [l for l in (ip_from_ip_port, ip_from_host_name) if l][0]
    except Exception as e:
        print('get_local_ip found exception : %s' % e)
    return local_ip if('' != local_ip and None != local_ip) else socket.gethostbyname(socket.gethostname())

# @app.route('/md_to_slide',methods = ['GET', 'POST'])
@app.route('/md_to_slide',methods = ['POST'])
def md_to_slide():
    try:
        params = request.get_json()
        md_content = params.get("md", [])
        if md_content:
            return json.dumps(md_to_slide_entrance(_md_content=md_content), ensure_ascii=False)
        else:
            return json.dumps({}, ensure_ascii=False)
    except Exception as e:
        raise e
        return json.dumps({"message" : str(e)}, ensure_ascii=False)

if __name__ == '__main__':
    app.run(host=get_local_ip(), port=13333, threaded=False) # , threaded=True, debug=True)

# demo-1
'''
md_str = r"""
#### sub_omni_popup
## 行间公式的示例
(@layout=center)
* 这是一个行间公式的示例，解析

$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$

并正确显示
<->
===
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

## 行间公式的示例
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

## 行间公式的示例
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

## 行间公式的示例
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

## 行间公式的示例
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

"""
requests.post("http://10.222.100.101:13333/md_to_slide", json={"md": md_str}).text
'''
# demo-2
'''
requests.post("http://10.222.100.101:13333/md_to_slide", json={"md":open("/tmp/moffee-latex-ppt-demo/pi.md","r").read()}).text
===
pi.md
===
#### sub_omni_popup
## 行间公式的示例
(@layout=center)
* 这是一个行间公式的示例，解析

$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$

并正确显示
<->
===
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

## 行间公式的示例
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

## 行间公式的示例
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

## 行间公式的示例
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

## 行间公式的示例
* 这是一个行间公式的示例，解析
$y=\frac{2.5}{\sqrt{2\pi}}\cdot2^\frac{{(\frac{x}{1800})^3}}{2}
$ 并正确显示

'''