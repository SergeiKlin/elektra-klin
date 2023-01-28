import pymysql


def connect_mysql(*DatabaseConfig):
    conf_db = DatabaseConfig[0]
    bd_server = conf_db.db_host
    bd_user = conf_db.db_user
    bd_password = conf_db.db_password
    bd_name = conf_db.db_name
    bd_charset = conf_db.db_charset
    return pymysql.connect(host=bd_server, user=bd_user, passwd=bd_password, db=bd_name, charset=bd_charset)
