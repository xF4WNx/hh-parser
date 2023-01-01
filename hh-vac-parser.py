import sys
import bs4
import requests
from fake_useragent import UserAgent
from pathlib import Path
from yaml import safe_load as ymlsl


def print_hi(name):
    print(f'{name} started')


def get_yaml_config() -> {}:
    with open('config.yaml', 'r') as yaml_conf:
        return ymlsl(yaml_conf)


def get_argv() -> {}:
    if sys.argv[1:]:
        return sys.argv[1:]
    else:
        return config['default_profession']


def get_user_agent() -> {}:
    headers_def = {
        'User-Agent': UserAgent().random
    }
    return headers_def


def check_or_create_path():
    Path(f"{config['result_html_path']}{profession}/").mkdir(parents=True, exist_ok=True)


def get_page_counts(raw_page: str) -> int:
    soup = bs4.BeautifulSoup(raw_page, 'html5lib')
    counts = []
    for count in soup.find_all('a', {'data-qa': 'pager-page'}):
        counts.append(int(count.text))
    return max(counts)


def hh_get_request(page: int) -> str:
    req = requests.get(f"{config['hh_link']}{profession}'&page'{page}", headers=headers)
    if req.status_code == 200:
        return req.text
    else:
        print(f'Error page, status code: {req.status_code}')


def write_response_to_file(page: int, response: str):
    with open(f"{config['result_html_path']}{profession}/page {page + 1}.html", 'w', encoding='utf-8') as pars_result:
        pars_result.write(response)


def hh_get_pages_req(max_page: int):
    for page in range(max_page):
        response = hh_get_request(page)
        write_response_to_file(page, response=response)


def hh_get_first():
    response = hh_get_request(0)
    write_response_to_file(0, response=response)
    max_page = get_page_counts(response) - 1
    hh_get_pages_req(max_page)


if __name__ == '__main__':
    print_hi('HH_vacancy_parser')
    config = get_yaml_config()
    profession = get_argv()
    headers = get_user_agent()

    check_or_create_path()
    hh_get_first()

else:
    print(f'File not main: {__name__}')
