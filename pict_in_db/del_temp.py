import pathlib


def del_Temp():
    # https://pythonim.ru/moduli/pathlib-python?ysclid=ldakw0r4u4784799179
    print('Очищаем каталог Temp')
    outpath = pathlib.Path.cwd() / 'Temp'
    path = pathlib.Path(outpath)
    for file in path.iterdir():
        file.unlink()
