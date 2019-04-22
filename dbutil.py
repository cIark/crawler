import MySQLdb
import csv


def get_conn(host, user, passwd, db):
    """
    mysql数据库链接
    :param host:地址
    :param user:用户名
    :param passwd:密码
    :param db:数据库
    :return:返回链接对象，失败返回空
    """
    try:
        conn = MySQLdb.connect(host, user, passwd, db, charset='utf8')
        return conn
    except Exception as e:
        print(e)
        return


def insert_many(conn, insert_sql, insert_list):
    """
    mysql批量写入多条数据
    :param conn: 链接对象
    :param insert_sql:
    :param insert_list:数据列表 list[tuple1,tuple2.....]
    :return: 返回插入数据条数，-1为异常
    """
    cursor = conn.cursor()
    try:
        cursor.executemany(insert_sql, insert_list)
        conn.commit()
        return cursor.rowcount
    except Exception as e:
        print(e)
        print('入库写数据失败！！')
        conn.rollback()
        return -1


def find_many(conn, find_sql):
    """
    mysql查询方法
    :param conn:
    :param find_sql:
    :return:
    """
    cursor = conn.cursor()
    try:
        cursor.execute(find_sql)
        results = cursor.fetchall()
        return results
    except Exception as e:
        print(e)
        print("Error: unable to fecth data")
        return -1


def find_models(conn, find_sql):
    results = find_many(conn, find_sql)
    if results == -1:
        return -1
    else:
        return [row[0] for row in results]


# 保存到本地方法
# 保存资源
def save_contents(table_body):
    tableh = [
        '型号', '生产企业', '品牌', '车辆类型', '配置ID', '外廓尺寸长（mm）', '外廓尺寸宽（mm）', '外廓尺寸高（mm）', '总质量（kg）', '整备质量（kg）',
        '最高车速（km/h）', '30分钟最高车速（km/h）', '续驶里程（km，工况法）', '续驶里程（km，等速法）', '电池系统能量密度（Wh/kg）',
        '工况条件下百公里耗电量（Y）（kWh/100km）', '储能装置种类', '驱动电机类型', '驱动电机峰值功率/转速/转矩（kW /r/min/N.m）', 'Ekg单位载质量能量消耗量（Wh/km・kg）',
        '吨百公里电耗（kWh/t・100km）', '储能装置总储电量（kWh）', '燃料种类', '是否允许外接充电', '纯电动模式下续驶里程（km，工况法）', '发动机生产企业', '排量/功率（ml/kW）',
        '发动机型号', '节油率水平（%）', '燃料消耗量（L/100km，电量平衡运行阶段）', '燃料消耗量（L/100km，B状态）', '燃料电池系统生产企业（主要包含电堆）',
        '燃料电池系统额定功率（kW）', '燃料电池系统峰值功率（kW）', '电池系统总质量占整车整备质量比例（%）', '纯电动模式下续驶里程（km，等速法）', '快充倍率',
        '轴距'
        # ,'None'
    ]
    with open('C:\\Users\\clark\\Desktop\\' + '写死' + ".csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, tableh)
        writer.writeheader()
        for line in table_body:
            writer.writerow(line)
        print(" 完成")
