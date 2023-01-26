def directory(code: str) -> list:
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


def add_dir_ftp(ftp, dir_pict: list):
    """
    Создаем каталоги для загрузки картинок на FTP
    :param ftp:
    :param dir_pict:
    :return:
    """
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



def search_bd(con, code):
    with con.cursor() as cur:
        id = None
        query = "SELECT id, title, code, image_url FROM mg_product WHERE code = '" + code + "'"
        cur.execute(query)
        rows = cur.fetchall()
        if len(rows) == 0:
            print("Такого кода нет")
        elif len(rows) > 1:
            print('Уточните код, найдено несколько')
        else:
            print('Найдено: ', rows[0][1])
            return rows