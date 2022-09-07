
import unicodedata
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup, NavigableString
import time

from urllib.parse import urljoin

from utils import is_date_format, url_format
from slack import Slack

import os
import pandas as pd


class WebScraping:
    driver = None

    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        # options.add_argument("--disable-gpu")
        # options.add_argument("--hide-scrollbars")
        # options.add_argument("--single-process")
        # options.add_argument("--ignore-certificate-errors")
        # options.add_argument("--window-size=880x996")
        # options.add_argument("--no-sandbox")
        # options.add_argument("--homedir=/tmp")

        self.driver = webdriver.Chrome(
            # ChromeDriverManager().install(),
            options=options
        )

    def get_ir_info(self, company_name, url, target_class):
        """スクレイピングでIR情報を取得する"""
        self.driver.get(url)
        time.sleep(2)
        html = self.driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, 'html.parser')

        # デバッグ用としてテキストファイルに書き込む
        f = open(f'./result/text_{company_name}.txt', 'w', encoding='UTF-8')
        print(f"【{company_name}】")
        counter = 0

        data_list = []
        for content in soup.find(class_=target_class).contents:
            # print("--------------------------")
            link = ""
            link = content.find_next("a").get("href")
            re_text = content.get_text().strip()

            re_text_list = content.get_text(
                ',').strip().replace("\n", "").replace("\t", "").replace("\xa0", "").split(',')

            # ブランクと改行コードのみの要素を配列から削除する
            re_text_list = list(filter(None, re_text_list))

            # HTMLの空要素は飛ばす
            if link is None or not re_text:
                continue

            # 文字列が長い順に並び替える（本文を配列の一番最後にしたい）
            re_text_list.sort(key=len)

            # 中身の確認
            body = ""
            date = ""
            for text in re_text_list:
                if is_date_format(text):
                    date = text
            body = re_text_list[-1]

            # 相対パスならURLを結合する
            # isabs は相対パスなら FALSE を返す
            if os.path.isabs(link) or url_format(link) is None:
                link = urljoin(url, link)

            f.write(f"{re_text_list}\n")
            f.write(f"{link}\n")
            f.write("\n")
            counter = counter + 1

            data_list.append([company_name, date, body, link])
            # print("--------------------------")

        f.close()

        return data_list

    def close(self):
        self.driver.close()
