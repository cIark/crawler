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


def get_wheelbase():
    pass


def cal_level(wheelbase):
    pass


def update(table, wheelbase, leval, model_name):
    sql = "UPDATE %s SET wheelbase = '%s',leval= '%s' WHERE model_name = '%s'" % (table, wheelbase, leval, model_name)


model = get_model("python_test")
print(len(model))
