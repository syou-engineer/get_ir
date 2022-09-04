import re
import pandas as pd

# 日付の正規表現
# ◯◯◯◯年◯◯月◯◯日
# ◯◯◯◯/◯◯/◯◯/
# ◯◯◯◯.◯◯.◯◯
DATE_PATTERN = r'[12]\d{3}[./\-年](0?[1-9]|1[0-2])[./\-月](0?[1-9]|[12][0-9]|3[01])日?$'
URL_PATTERN = r'^https.*'


def is_date_format(date_str: str):
    return re.match(DATE_PATTERN, date_str)


def url_format(url: str):
    return re.match(URL_PATTERN, url)
