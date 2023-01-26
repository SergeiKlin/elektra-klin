from connect.MySQL import connect_mysql
from connect.ftp import connect_ftp
from .general_def import directory, search_bd
from .ftp_def import deleteAllFiles

from config_data.config import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()


def pict_delete():
    el_code = input('Код в Электра: ')
    con = connect_mysql(config.db)
    row = search_bd(con, el_code)
    if row[0][3] is not None:
        # Очистить содержимое папки на FTP
        pict_dir = '/'.join(directory(str(row[0][0])))
        ftp_server = connect_ftp(config.ftp_el)
        ftp_server.cwd(pict_dir)
        try:
            deleteAllFiles(ftp_server)
        except:
            print('Не удалось очистить папку на FTP')

        # Удалить ссылку на файл в БД
        with con.cursor() as cur:
            query = "UPDATE mg_product SET image_url=NULL WHERE code = '" + el_code + "'"
            print(f'Удалена картинка для {row[0][1]} --- {el_code}')
            cur.execute(query)
