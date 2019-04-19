from crawl import check_link, get_contents
from dbutil import get_conn, insert_many
import sys

"""
爬工信部数据，去重，直接刷入mysql数据库
"""

t_map = {'model_name': '型号', 'manufacture': '生产企业', 'brand': '品牌', 'vehicle_type': '车辆类型',
         'configuration_ID': '配置ID', 'length': '外廓尺寸长（mm）', 'width': '外廓尺寸宽（mm）', 'height': '外廓尺寸高（mm）',
         'max_weight': '总质量（kg）', 'curb_weight': '整备质量（kg）', 'max_speed': '最高车速（km/h）',
         'max_speed_30m': '30分钟最高车速（km/h)', 'drive_range1': '续驶里程（km，工况法）', 'drive_range2': '续驶里程（km，等速法）',
         'energy_density': '电池系统能量密度（Wh/kg）', 'kwh_100km': '工况条件下百公里耗电量（Y）（kWh/100km）', 'battery_type': '储能装置种类',
         'motor_type': '驱动电机类型', 'motor_max_power_rev_torquecomment': '驱动电机峰值功率/转速/转矩（kW /r/min/N.m)',
         'ekg': 'Ekg单位载质量能量消耗量（Wh/km・kg）', 'etkg': '吨百公里电耗（kWh/t・100km）', 'power_amount': '储能装置总储电量（kWh）',
         'fuel_type': '燃料种类', 'chargable': '是否允许外接充电', 'drive_range_ev2': '纯电动模式下续驶里程（km，工况法）',
         'engine_manufature': '发动机生产企业', 'displacement_power': '排量/功率（ml/kW）', 'engine_model': '发动机型号',
         'fuel_saving_rate': '节油率水平（%）', 'fuel_l100km': '燃料消耗量（L/100km，电量平衡运行阶段）',
         'fuel_l100km2': '燃料消耗量（L/100km，B状态）', 'fuel_cell_manufacture': '燃料电池系统生产企业（主要包含电堆）',
         'fuel_cell_power_rating': '燃料电池系统额定功率（kW）', 'fuel_cell_max_power': '燃料电池系统峰值功率（kW）',
         'battery_weight_rate': '电池系统总质量占整车整备质量比例（%）', 'drive_range_ev': '纯电动模式下续驶里程（km，等速法）',
         'fast_charging_ratio': '快充倍率', 'wheelbase': '轴距'
         }


def format_url():
    pass


def prepare_sql(table):
    insert_keys = ','.join(t_map.keys())
    insert_sql = 'insert ignore %s (%s) values ' \
                 '(%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,' \
                 '%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s,%%s); ' % (table, insert_keys)  # 38个占位符
    return insert_sql


def prepare_list(table_body):
    insert_list = []
    if len(table_body) == 0:
        print("没有数据！！")
    else:
        for row in table_body:
            insert_list.append(tuple([row.get(value, '') for value in t_map.values()]))
    return insert_list


def insert_mysql():
    # url = sys.argv[1]
    url = "http://123.127.164.29:18082/CVT/Jsp/zjgl/nerds/201812.html"
    rs = check_link(url)
    table_body = get_contents(rs)
    conn = get_conn("192.168.6.105", "root", "root", "bg_analysis")
    insert_sql = prepare_sql("python_test")
    insert_list = prepare_list(table_body)
    if conn is None:
        print("数据库链接失败")
        sys.exit(1)
    rs = insert_many(conn, insert_sql, insert_list)
    print("写入%d条数据" % rs)


if __name__ == '__main__':
    insert_mysql()
