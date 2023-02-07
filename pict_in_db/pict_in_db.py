from connect.MySQL import connect_mysql
from connect.API_rs24 import connect_rs24, rs24_item
from connect.ftp import connect_ftp
from .general_def import directory, add_dir_ftp, search_bd

from config_data.config import Config, load_config

# Загружаем конфиг в переменную config
config: Config = load_config()

import wget, pathlib


def directory_del(code: str) -> list:
    """
    На входе получаем id товара
    На выходе структуру каталогов для загрузки изображений
    :param code:
    :return:
    """
    dl = len(code)
    cat = []
    if dl > 2:
        c = str(code[:(dl - 2)]) + ('0' * 2)
        cat.append(c)
        cat.append(code)
    else:
        cat.append('000')
        cat.append(code)
    return cat


def add_dir_ftp_del(ftp, dir_pict: list):
    '''
    Создаем каталоги для загрузки картинок на FTP
    :param dir:
    :return:
    '''
    catalog = ''
    ftp.cwd('/')
    for s in dir_pict:
        catalog += '/' + s
        # print(f'Создаем каталог {catalog}')
        try:
            ftp.mkd(catalog)
            # print('Каталог создан')
        except:
            pass
            # print('Каталог существует')
    return catalog


def add_image_spec_db(name: str, vendor_code: str, img: list, specifications: list):
    # Ищем по коду в БД
    con = connect_mysql(config.db)
    ftp = connect_ftp(config.ftp_el)
    with con:
        # print(type(vendor_code), vendor_code, name)
        cur = con.cursor()
        query = "SELECT id, title, code, image_url FROM mg_product WHERE code = '" + vendor_code + "'"
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            if row[3] == None:  # Сохраняем картинку только если ее НЕТ
                pict = img[0]['URL']
                outpath = pathlib.Path.cwd() / 'Temp'
                wget.download(pict, str(outpath))
                ftp_server = connect_ftp(config.ftp_el)
                file_name = outpath / pict[(pict.rfind('/') + 1):]
                pict_dir = directory(str(row[0]))
                cat_ftp = add_dir_ftp(ftp_server, pict_dir)
                # print(cat_ftp)
                ftp_server.cwd(cat_ftp)
                # print(ftp_server.retrlines('LIST'))
                # if cat_ftp == '/2700/2789' or cat_ftp == '/3200/3272':
                with open(file_name, "rb") as file:
                    # Command for Uploading the file "STOR filename"
                    ftp_server.storbinary(f"STOR {pict[(pict.rfind('/') + 1):]}", file)

                    sql = "UPDATE mg_product SET image_url='" + pict[(pict.rfind(
                        '/') + 1):] + "' WHERE code = '" + vendor_code + "'"
                    print(f'Загружена картинка для {row[1]} --- {vendor_code}')
                    #
                    cur.execute(sql)
                # ftp_server.close()
                # ftp_server.quit()
        query = "SELECT id, title, code, image_url, description FROM mg_product WHERE code = '" + vendor_code + "'"
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            if row[4] == '':
                sp = ''
                for spec in specifications:
                    sp += '<strong>' + spec['NAME'] + ': </strong>' + spec['VALUE'] + '<br/>'
                query = "UPDATE mg_product SET description='" + sp + "' WHERE code = '" + vendor_code + "'"
                print(f'Загружены характеристики для {row[1]} --- {vendor_code}')
                cur.execute(query)
            else:
                print(f'Характеритсика для {vendor_code} заполнена, наим: {row[1]} --- {row[4]}')

def start_stop():
    page_start = int(input('Введите стартовую страницу: '))
    page_stop = int(input('Введите последнюю страницу: '))
    # Получаем с API страницу со списками товаров
    for page in range(page_start, page_stop + 1):
        api_sesion = connect_rs24(page, config.rs24)
        for item in api_sesion.json()['items']:
            # Получаем с API страницу с характеристиками товара
            api_item = rs24_item(item['CODE'], config.rs24)
            try:
                api_vendor_code = str(api_item.json()['INFO'][0]['VENDOR_CODE'])  # 13, 14, 18б 210, 283
                api_name = api_item.json()['INFO'][0]['DESCRIPTION']
                api_image = api_item.json()["IMG"]
                api_spec = api_item.json()["SPECS"]
                add_image_spec_db(api_name, api_vendor_code, api_image, api_spec)
            except:
                print(f'Ошибка при загрузке {api_item.json()["INFO"][0]}')
                print(item['CODE'], api_item.json())
    input('Загрузка завершена!!!!')
    # --- Соединение с БД MySQL
    # con = connect_mysql(config.db)
    # print(con)
    # --- Соединение с API русский свет
    # api_sesion = connect_rs24(config.rs24)
    # print(api_sesion)
    # --- Соединение с FTP elektra-klin
    # ftp = connect_ftp(config.ftp_el)
    # print(ftp)
