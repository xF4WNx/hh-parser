import sys
import os
import bs4
import requests
from fake_useragent import UserAgent
from pathlib import Path
from yaml import safe_load as YMLSL


def print_hi(name):
    print(f'{name} started')


def get_yaml_config():
    with open('config.yaml', 'r') as yaml_conf:
        return YMLSL(yaml_conf)


def get_argv():
    if sys.argv[1:]:
        return sys.argv[1:]
    else:
        return config['default_profession']


def get_user_agent() -> str:
    return UserAgent().random


def check_or_create_path():
    Path(f"{config['result_html_path']}{profession}/").mkdir(parents=True, exist_ok=True)


def get_page_counts(raw_page: str) -> int:
    soup = bs4.BeautifulSoup(raw_page, 'html5lib')
    counts = []
    for count in soup.find_all('a', {'data-qa':'pager-page'}):
        counts.append(int(count.text))
    return max(counts)


def hh_get_pages_req(max_page: int):
    ...


def hh_get_first_req():
    headers = {
        'User-Agent': get_user_agent()
    }

    req = requests.get(config['hh_link'] + profession, headers=headers)
    if req.status_code == 200:
        req_text = req.text
        with open(config['result_html_path'] + 'page 1.html', 'w', encoding='utf-8') as pars_result:
            pars_result.write(req_text)
        max_page = get_page_counts(req_text) - 1
        hh_get_pages_req(max_page)
    else:
        print(f'Error page, status code: {req.status_code}')


if __name__ == '__main__':
    print_hi('HH_vacancy_parser')
    print(f'{os.listdir()}')
    config = get_yaml_config()
    profession = get_argv()

    check_or_create_path()
    hh_get_first_req()

else:
    print(f'File not main: {__name__}')
