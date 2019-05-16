import sys
import time

from bs4 import BeautifulSoup

import dbutil
from crawl import check_link
from setting import host, user_name, password, db_name, table_name


def get_wheelbase(model):
    print('finding model:%s' % model)
    url = 'https://www.cn357.com/cvi.php?m=cvNotice&search=n&model=%s' % model
    rs = check_link(url)
    if rs == -1:
        return -1
    soup = BeautifulSoup(rs, 'lxml')
    text = soup.find('p', 'detail')
    if text is None:
        return 0
    wheelbase = str(text).split('轴距：')[1].split('，')[0]
    return wheelbase


def wheelbase_run():
    conn = dbutil.get_conn(host, user_name, password, db_name)
    if conn is None:
        print("数据库链接失败")
        sys.exit(1)
    sql = "select model_name from %s where wheelbase='';" % table_name
    m_list = dbutil.find_models(conn, sql)
    wheelbase_count = 0
    if m_list == -1:
        print("查找数据失败")
        sys.exit(1)
    for model in m_list:
        time.sleep(1)
        wheelbase = get_wheelbase(model)
        if wheelbase == 0 or wheelbase == -1:
            pass
        else:
            print('result:', model, wheelbase)
            wheelbase = wheelbase.split(',')[0]
            sql = "UPDATE %s SET wheelbase = '%s' WHERE model_name = '%s'" % (table_name, wheelbase, model)
            dbutil.update(conn, sql)
            wheelbase_count += 1
    print('update wheelbase %d data' % wheelbase_count)


def cal_level(wheelbase):
    if wheelbase < 2200:
        return 'A00'
    elif 2200 <= wheelbase < 2300:
        return 'A0'
    elif 2300 <= wheelbase < 2450:
        return 'A'
    elif 2450 <= wheelbase < 2600:
        return 'B'
    elif 2600 <= wheelbase < 2800:
        return 'C'
    elif 2800 <= wheelbase:
        return 'D'


def level_run():
    conn = dbutil.get_conn(host, user_name, password, db_name)
    if conn is None:
        print("数据库链接失败")
        sys.exit(1)
    sql = "select model_name,wheelbase from %s where level='' and wheelbase!='' and vehicle_type like '%%轿车';" \
          % table_name
    result_list = dbutil.find_many(conn, sql)
    level_count = 0
    if result_list == -1:
        print("查找数据失败")
        sys.exit(1)
    for result in result_list:
        model = result[0]
        wheelbase = int(result[1][0:4])
        level = cal_level(wheelbase)
        print(model, wheelbase, level)
        sql = "UPDATE %s SET level = '%s' WHERE model_name = '%s'" % (table_name, level, model)
        dbutil.update(conn, sql)
        level_count += 1
    print('update %d data' % level_count)


if __name__ == '__main__':
    wheelbase_run()
    level_run()
