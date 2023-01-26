from ftplib import FTP


def connect_ftp(*ftp_el):
    conf_ftp = ftp_el[0]
    ftp_host = conf_ftp.ftp_host
    ftp_login = conf_ftp.ftp_login
    ftp_password = conf_ftp.ftp_password
    ftp = FTP(ftp_host)
    ftp.login(ftp_login, ftp_password)
    return ftp
