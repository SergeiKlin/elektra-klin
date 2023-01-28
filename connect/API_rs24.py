import requests


def connect_rs24(page, *API_RS24):
    conf_rs24 = API_RS24[0]
    s = requests.session()
    url = conf_rs24.url_items + str(page)
    print(url)
    # url_item = conf_rs24.url_items
    login_user = conf_rs24.api_user
    login_password = conf_rs24.api_password
    page_items = s.get(url=url, auth=(login_user, login_password))
    return page_items


def rs24_item(code, *API_RS24):
    conf_rs24 = API_RS24[0]
    s = requests.session()
    url = conf_rs24.url_item + str(code)
    login_user = conf_rs24.api_user
    login_password = conf_rs24.api_password
    page_item = s.get(url=url, auth=(login_user, login_password))
    return page_item
