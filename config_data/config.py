from dataclasses import dataclass
from environs import Env


@dataclass
class DatabaseConfig:
    db_name: str  # Название базы данных
    db_host: str  # URL-адрес базы данных
    db_user: str  # Username пользователя базы данных
    db_password: str  # Пароль к базе данных
    db_charset: str  # Кодировка


@dataclass
class API_RS24:
    url_items: str  # URL для доступа к списку товаров
    url_item: str  # URL для доступа к характеристикам товара
    # headers: dict  # Логин и пароль для доступа к API Русский свет
    api_user: str
    api_password: str


@dataclass
class ConfigFTP:
    ftp_host: str
    ftp_login: str
    ftp_password: str


@dataclass
class Config:
    rs24: API_RS24
    db: DatabaseConfig
    ftp_el: ConfigFTP


# Создаем экземпляр класса Config и наполняем его данными из переменных окружения
def load_config(path: str | None = None) -> Config:
    # Создаем экземпляр класса Env
    env: Env = Env()

    # Добавляем в переменные окружения данные, прочитанные из файла .env
    env.read_env()
    return Config(rs24=API_RS24(url_items=env('url_items'),
                                url_item=env('url_item'),
                                api_user=env('api_user'),
                                api_password=env('api_password')),
                                # headers=env('headers')),
                  db=DatabaseConfig(db_name=env('db_name'),
                                    db_host=env('db_host'),
                                    db_user=env('db_user'),
                                    db_password=env('db_password'),
                                    db_charset=env('db_charset')),
                  ftp_el=ConfigFTP(ftp_host=env('ftp_host'),
                                   ftp_login=env('ftp_login'),
                                   ftp_password=env('ftp_password')))

# Выводим значения полей экземпляра класса Config на печать,
# чтобы убедиться, что все данные, получаемые из переменных окружения, доступны
# print('url_items:', config.rs24.url_items)
# print('url_item:', config.rs24.url_item)
# print('headers:', config.rs24.headers)
# print()
# print('DATABASE:', config.db.db_name)
# print('DB_HOST:', config.db.db_host)
# print('DB_USER:', config.db.db_user)
# print('DB_PASSWORD:', config.db.db_password)
# print('db_charset:', config.db.db_charset)
# print()
# print('ftp_host:', config.ftp_el.ftp_host)
# print('ftp_login:', config.ftp_el.ftp_login)
# print('ftp_password:', config.ftp_el.ftp_password)
