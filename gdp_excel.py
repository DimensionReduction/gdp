import os
import requests
import parsel
import pandas as pd
from openpyxl import load_workbook

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="98", "Google Chrome";v="98"'}

for i in range(1980, 2022):
    url = 'http://www.8pu.com/gdp/ranking_' + str(i) + '.html'
    response = requests.get(url, headers=headers)
    response.encoding = response.apparent_encoding
    selector = parsel.Selector(response.text)
    lis = selector.css('#table01')
    for li in lis:
        rank = li.css('#US_ > td.rank > font > font::text').getall()
        rank = ','.join(rank).replace('排名第', '').split(',')
        country = li.css('#US_ > td:nth-child(2) > a > font::text').getall()
        dollar = li.css('#US_ > td.value > font::text').getall()
        dollar = ','.join(dollar).replace('$', '').split(',')
        rmb = li.css('#US_ > td.rank_prev > font::text').getall()
        rmb = ','.join(rmb).replace('￥', '').replace('亿元', '').split(',')
        continent = li.css('#US_ > td.area > font > font::text').getall()
        continent = ','.join(continent).replace('国家', '').replace('州','洲').split(',')
        dict = {'排名': rank, '国家/地区': country, 'GDP总量(美元核算)': dollar, 'GDP总量(人民币核算)': rmb, '所属洲': continent}
    d = list(zip(rank, country, dollar, rmb, continent))
    print('\n//////////  ' + str(i) + '年全球GDP  //////////\n')
    for x1, x2, x3, x4, x5 in d:
        print(x1, x2, x3, x4, x5)
    df = pd.DataFrame(d)
    if os.path.exists('./历年GDP数据')==False:
        os.mkdir('./历年GDP数据')
    df.to_excel('./历年GDP数据/GDP' + str(i) + '.xlsx', sheet_name=str(i), encoding='gbk', index=0, header=dict)

    wb = load_workbook('./历年GDP数据/GDP' + str(i) + '.xlsx')
    ws = wb.active
    ws.column_dimensions['A'].width = 15
    ws.column_dimensions['B'].width = 20
    ws.column_dimensions['C'].width = 25
    ws.column_dimensions['D'].width = 25
    ws.column_dimensions['E'].width = 15
    wb.save('./历年GDP数据/GDP' + str(i) + '.xlsx')
