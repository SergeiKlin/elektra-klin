from connect.MySQL import connect_mysql
from connect.API_rs24 import rs24_item
from connect.ftp import connect_ftp
from .general_def import directory, add_dir_ftp, search_bd

from config_data.config import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()

import wget, pathlib


def add_image_db(row, vendor_code: str, img_url: str, con):
    # Ищем по коду в БД
    ftp = connect_ftp(config.ftp_el)
    cur = con.cursor()
    if row[0][3] == None or row[0][3] == '':  # Сохраняем картинку только если ее НЕТ
        # pict = img[0]['URL']
        pict = img_url
        outpath = pathlib.Path.cwd() / 'Temp'
        wget.download(pict, str(outpath))
        ftp_server = connect_ftp(config.ftp_el)
        file_name = outpath / pict[(pict.rfind('/') + 1):]
        pict_dir = directory(str(row[0][0]))
        cat_ftp = add_dir_ftp(ftp_server, pict_dir)
        ftp_server.cwd(cat_ftp)
        with open(file_name, "rb") as file:
            ftp_server.storbinary(f"STOR {pict[(pict.rfind('/') + 1):]}", file)
            query = "UPDATE mg_product SET image_url='" + pict[(pict.rfind('/') + 1):] + "' WHERE code = '" + vendor_code + "'"
            print(f'Загружена картинка для {row[0][1]} --- {vendor_code}')
            cur.execute(query)
    # # ftp_server.close()
    # # ftp_server.quit()

def add_spec_db(row, vendor_code: str, specifications: list, con):
    cur = con.cursor()
    sp = ''
    print(row)
    if row[0][4] == None or row[0][4] == '':
        for spec in specifications:
            sp += '<strong>' + spec['NAME'] + ': </strong>' + spec['VALUE'] + '<br/>'
        query = "UPDATE mg_product SET description='" + sp + "' WHERE code = '" + vendor_code + "'"
        print(f'Загружены характеристики для {row[0][1]} --- {vendor_code}')
        cur.execute(query)
    else:
        if input('Характеристтики заполнены, перезаписываем? (1 - Да, другое - НЕТ) ___ ') == '1':
            for spec in specifications:
                sp += '<strong>' + spec['NAME'] + ': </strong>' + spec['VALUE'] + '<br/>'
            query = "UPDATE mg_product SET description='" + sp + "' WHERE code = '" + vendor_code + "'"
            print(f'Загружены характеристики для {row[0][1]} --- {vendor_code}')
            cur.execute(query)

def pict_insert():
    el_code = input('Код в Электра (exit для выхода): ')
    while el_code != 'exit':
        con = connect_mysql(config.db)
        row = search_bd(con, el_code)
        if id is not None:
            url_pict = input('URL загружаемой каринки: ')
            zagruz = input('Загружаем картинку на сайт? (1 - Да, другое - НЕТ) ___ ')
            if zagruz:
                # Загружаем картинку на FTP сервер
                # api_image = api_item.json()["IMG"]
                add_image_db(row, el_code, url_pict, con)
            el_code = input('Код в Электра (exit для выхода): ')
