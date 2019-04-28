import requests
from requests.exceptions import *
from bs4 import BeautifulSoup
import re


# 检查url地址
def check_link(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except ConnectionError:
        print('无法链接服务器！！！，请输入正确的url或者联系开发人员')
        return -1
    except Timeout:
        print('请求超时！！')
        return -1
    except HTTPError:
        print('网站返回异常')
        return -1


def get_power_type(vehicle_type):
    if vehicle_type[0:3] == '纯电动':
        return 'BEV'
    elif vehicle_type[0:4] == '燃料电池':
        return 'FCV'
    elif vehicle_type[0:4] == '混合动力':
        return 'HEV'
    elif vehicle_type[0:2] == '插电':
        return 'PHEV'
    elif vehicle_type[0:2] == '插电':
        return 'PHEV'
    elif vehicle_type[0:7] == '甲醇重整制氢燃':
        return 'FCV'
    elif vehicle_type[0:7] == '平头纯电动':
        return 'BEV'
    else:
        return '未知'


def get_contents(page_text):
    table_body = []
    if page_text == -1:
        return table_body
    else:
        soup = BeautifulSoup(page_text, 'lxml')
        # filename.append(str.strip(soup.find(text='新能源汽车推广应用推荐车型目录').next_element.next_element.next_element)[1:-1])

        # 遍历表格，存储内容
        tables = soup.find_all('table', 'list-table')
        for table in tables:
            table_header = {}
            # 先初始化表头
            # 获取的 title 原值： 1、东风汽车股份有限公司 东风牌 DFA6118LBEV纯电动客车
            title = str.split(table.find_previous('strong').string)
            # print(title)
            table_header['型号'] = "".join(i for i in title[2] if ord(i) < 256)
            table_header['生产企业'] = re.sub(r'、|[0-9]', '', title[0])
            table_header['品牌'] = title[1]
            table_header['车辆类型'] = "".join(i for i in title[2] if ord(i) > 256)
            table_header['动力类型'] = get_power_type(table_header['车辆类型'])

            trs = table.find_all('tr')
            # num 表示每一个表配置ID个数，一个配置ID又对应一个tableLine，即写入CSV 的 一行
            # num = int(len(trs[0]) / 2 - 1)
            # 只要其中一个配置，其他配置略去
            num = 1
            table_line = [{}] * num
            for i in range(num):
                table_line[i] = table_header.copy()
                table_line[i]['配置ID'] = trs[0].find_all('td')[(i + 1)].get_text().split('ID：')[1].strip()
                for tr in trs:
                    ui = []
                    for td in tr:
                        str1 = re.sub(',', '/', str.strip(str(td.string)))
                        str2 = re.sub('：', '', str1)
                        ui.append(str2)
                    if str.strip(ui[1]) != '' and ui[1] != None:
                        table_line[i][ui[1]] = ui[i * 2 + 3]
                table_body.append(table_line[i])
        return table_body


if __name__ == '__main__':
    print(get_power_type('纯电动城市客车'))
