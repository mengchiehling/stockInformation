import sys

import requests
from lxml import etree
import numpy as np
import pandas as pd
from user_agent import generate_user_agent

if sys.platform == 'win32':
    operating_system = 'win'
elif sys.platform == 'darwin':
    operating_system = 'mac'
else:
    operating_system = 'linux'


def get_resp(code) -> etree._Element:

    """
    擷取網頁內容

    :param code:
    :return:
    """

    url_base = "https://goodinfo.tw/tw/StockBzPerformance.asp?STOCK_ID="

    headers = {'User-Agent': generate_user_agent(os=operating_system, navigator='chrome')}

    resp = requests.get(f"{url_base}{code}", headers=headers)
    resp.encoding = 'utf-8'

    # Create DOM (document object model) from HTML text
    dom = etree.HTML(resp.text)

    return dom


def extract_column_names_from_table(table: etree._Element):

    column_names = []

    # 上層欄位
    th_level_1 = table.xpath(".//tr[@class='bg_h2']")[0].xpath("./th")
    # 下層欄位
    th_level_2 = table.xpath(".//tr[@class='bg_h2']")[1].xpath("./th")

    # 觀察規律
    # 1. 上層欄位有些有rowspan這個屬性(attribute)，有些有colspan這個屬性
    # 2. 有colspan這個屬性的欄位會有下層子欄位

    for th in th_level_1:
        colspan = th.get("colspan")
        rowspan = th.get("rowspan")

        if rowspan is not None:
            # 沒有子欄位
            column_name = extract_column_name_from_th(th)
            column_names.append(column_name)
        else:
            # 有子欄位
            column_name = extract_column_name_from_th(th)
            for _ in range(int(colspan)):
                th_2 = th_level_2.pop(0)
                column_name_2 = extract_column_name_from_th(th_2)
                column_names.append(f"{column_name}: {column_name_2}")

    return column_names


def extract_column_name_from_th(th: etree._Element):

    nobr = th.xpath("./nobr")[0]
    col_name = "".join(nobr.xpath('./text()'))

    return col_name


def extract_values_from_tr(tr: etree._Element):

    values = []

    tds = tr.xpath("./td")

    for td in tds:
        nobr = td.xpath("./nobr")[0]
        a = nobr.xpath("./a")
        if len(a) != 0:
            values.append(a[0].text)
        else:
            values.append(nobr.text)

    return values


def extract_values_from_table(table: etree._Element):

    trs = table.xpath(".//tr[@align='center']")

    data = []

    for tr in trs:
        values = extract_values_from_tr(tr)
        data.append(values)

    return data


def access_data_as_dataframe(code):

    """
    The main entrance point for all the work
    :param code:
    :return:
    """

    dom = get_resp(code=code)

    table = dom.xpath('//*[@id="tblDetail"]')[0]

    column_names = extract_column_names_from_table(table=table)

    values = extract_values_from_table(table=table)

    return pd.DataFrame(data=values, columns=column_names)
