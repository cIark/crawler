from dbutil import get_conn, find_models


def get_model(table):
    """
    查找没有轴距的车型
    :return: model_list 车型列表
    """
    conn = get_conn("192.168.6.105", "root", "root", "bg_analysis")
    sql = "select model_name from %s where wheelbase='';" % table
    model_list = find_models(conn, sql)
    return model_list


model = get_model("python_test")
print(model[0])
