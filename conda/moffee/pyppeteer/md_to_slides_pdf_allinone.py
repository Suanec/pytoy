# !/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'enzhao'

import asyncio
# Created by enzhao on 2025/3/12.
import os
import sys
import tempfile
import logging
from moffee import cli as moffee_cli

from printMoffee.pyppeteer_save_slides_as_pdf import save_slides_as_pdf

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
UNDERLINE = "_"
# 程序名
SIGN_NAME = "md2slidepdf"
T_NAME_FMT = "{T_NAME}"
# PID
PID = str(os.getpid())
# 临时文件夹
KSP_NAME = UNDERLINE.join([SIGN_NAME, PID, ""])
# 临时文件夹路径
KSP_PATH = tempfile.mkdtemp(prefix=KSP_NAME)
# Markdown文件名模板
MD_FNAME_FMT = UNDERLINE.join(["stage_slide_markdown_content", PID, T_NAME_FMT, ".md"])
# HTML目录名模板
HTML_FNAME_FMT = UNDERLINE.join(["moffee_output", PID, T_NAME_FMT])
# Markdown文件路径模板
MD_FPATH = os.path.join(KSP_PATH, MD_FNAME_FMT)
# HTML目录路径模板
HTML_FPATH_FMT = os.path.join(KSP_PATH, HTML_FNAME_FMT)
INDEX_FPATH_FMT = os.sep.join(["file:/", HTML_FPATH_FMT, "index.html"])
OUTPUT_PDF_FPATH_FMT = os.sep.join([KSP_PATH, T_NAME_FMT + ".pdf"])


def export(_md: str, _output: str) -> str:
    moffee_cli.run(_md, output=_output, live=False)

def main(_md_content: str) -> None:
    cur_t_name = os.path.split(tempfile.mkdtemp(prefix=""))[1]
    print("Cur fname %s" % cur_t_name)
    md_fpath = MD_FPATH.format(T_NAME=cur_t_name)
    html_fpath = HTML_FPATH_FMT.format(T_NAME=cur_t_name)
    with open(md_fpath, "w", encoding="utf-8") as f:
        f.write(_md_content)
    export(md_fpath, html_fpath)

    url = INDEX_FPATH_FMT.format(T_NAME=cur_t_name)
    print("Open %s" % url)
    output_path = OUTPUT_PDF_FPATH_FMT.format(T_NAME=cur_t_name)
    print("Save to %s" % output_path)
    asyncio.run(save_slides_as_pdf(url, output_path))


if __name__ == '__main__':
    with open(os.path.abspath(sys.argv[1]), "r", encoding="utf-8") as f:
        main(f.read())
