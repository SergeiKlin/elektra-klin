def deleteAllFiles(ftp):
    """
    Очищаем каталог на FTP сервере
    :param ftp:
    :return:
    """
    for n in ftp.nlst():
        try:
            if n not in ('.', '..'):
                print('Найден..' + n)
                try:
                    ftp.delete(n)
                    print('Удаляю...' + n)
                except Exception:
                    print(n + ' Not deleted, we suspect its a directory, changing to ' + n)
                    ftp.cwd(n)
                    deleteAllFiles(ftp)
                    ftp.cwd('..')
                    print('Trying to remove directory ..' + n)
                    ftp.rmd(n)
                    print('Directory, ' + n + ' Removed')
        except Exception:
            print('Trying to remove directory ..' + n)
            ftp.rmd(n)
            print('Directory, ' + n + ' Removed')
