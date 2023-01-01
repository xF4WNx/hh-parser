import sys
import bs4
import requests
from os import listdir, mkdir
from datetime import datetime
from fake_useragent import UserAgent
from pathlib import Path
from yaml import safe_load as ymlsl


def print_hi(name):
    print(f'{name} started')


def get_yaml_config() -> {}:
    """
    Загружает в программу конфигурацию через YAML
    :return: возвращает словарь конфигурации
    """
    with open('config.yaml', 'r') as yaml_conf:
        return ymlsl(yaml_conf)


def get_argv() -> str:
    """
    Считывает из консоли название профессии для её поиска
    :return: возвращает строку с названием профессии
    """
    if sys.argv[1:]:
        defenition_profession = ''.join(sys.argv[1:])
        return defenition_profession
    else:
        return config['default_profession']


def get_user_agent() -> {}:
    """
    Создание web заголовков
    :return: возвращает словарь заголовков
    """
    headers_def = {
        'User-Agent': UserAgent().random
    }
    return headers_def


def check_or_create_directory() -> str:
    """
    Проверка на существование директории и создание ее, если она отсутствует,
    а если не пустая, то создает по текущему времени
    :return: возвращает строковое значение директории, куда скидывать результаты
    """
    today = datetime.now()
    directory_check = f'{config["result_html_path"]}{profession}/{today.strftime("%d.%m.%Y")}'
    Path(directory_check).mkdir(parents=True, exist_ok=True)
    if listdir(directory_check):
        directory_check = f'{directory_check}&&{today.strftime("%H.%M.%S")}/'
        Path(directory_check).mkdir(parents=True, exist_ok=True)
        return directory_check
    else:
        return f'{directory_check}/'


def get_page_counts(raw_page: str) -> int:
    """
    Парсит количество страниц, которые нужно спарсить из первой страницы
    :param raw_page: получает сырой текст первой страницы
    :return: возвращает численное зеначение максимальной страницы ( на hh[.]ru счет страниц начаинается с 0 )
    """
    soup = bs4.BeautifulSoup(raw_page, 'html5lib')
    counts = []
    for count in soup.find_all('a', {'data-qa': 'pager-page'}):
        counts.append(int(count.text))
    print(f'{profession} have {max(counts)} pages')
    return max(counts)


def hh_get_request(page: int) -> str:
    """
    Скачаивает запрашиваемую страницу
    :param page: получает номер нужной страницы
    :return: возвращает сырой текст страницы
    """
    path = f"{config['hh_link']}{profession}&page'{page}"
    req = requests.get(path, headers=headers)
    if req.status_code == 200:
        return req.text
    else:
        print(f'Error page, status code: {req.status_code}')


def write_response_to_file(page: int, raw_data: str):
    """
    Записывает сырой хтмл в файл
    :param page: принимает номер страницы
    :param raw_data: принимает данные
    """
    file = f'{directory}{profession} page {page + 1}.html'
    with open(file, 'w', encoding='utf-8') as pars_result:
        pars_result.write(raw_data)


def hh_get_pages_req(max_page: int):
    """
    Скачивает номера страницы по номеру кроме первой
    :param max_page: получает номер страницы
    """
    for page in range(max_page):
        response = str(hh_get_request(page))
        write_response_to_file(page, raw_data=response)


def hh_get_first():
    """
    Скачивает первую страницу и передает на скачаивание остальные
    """
    response = str(hh_get_request(0))
    write_response_to_file(0, raw_data=response)
    max_page = get_page_counts(response) - 1
    hh_get_pages_req(max_page)


if __name__ == '__main__':
    print_hi('HH_vacancy_parser')
    config = get_yaml_config()
    profession = get_argv()
    headers = get_user_agent()
    directory = check_or_create_directory()
    hh_get_first()
else:
    print(f'File not main: {__name__}')
