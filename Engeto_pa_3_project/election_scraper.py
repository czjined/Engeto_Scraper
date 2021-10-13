import requests
from requests.exceptions import HTTPError
from bs4 import BeautifulSoup
import sys


def input_check(list_for_check: list) -> bool:
    if len(list_for_check) != 3:
        text_for_stop = 'Three arguments expecting!'
        script_stop(text_for_stop)
    else:
        print('Input arguments are OK')
        return True


def request_site(html_argument: str) -> str:
    try:
        home_site = requests.get(html_argument)
        home_site.raise_for_status()
    except HTTPError as http_err:
        text_for_stop = 'HTTP error occurred: {}'.format(http_err)
        script_stop(text_for_stop)
    except Exception as error:
        text_for_stop = 'Other error occurred: {}'.format(error)
        script_stop(text_for_stop)
    else:
        return home_site.text


def crt_rslt_structure() -> list:
    result_structure = list()
    main_row = ['region', 'district', 'city_number', 'city_name', 'registered', 'envelope', 'valid']
    for item in main_row:
        tmp_dict = dict()
        tmp_dict.setdefault(item, '')
        result_structure.append(tmp_dict)
    return result_structure


def script_stop(stop_text: str):
    print(stop_text)
    print('QUITTING..')
    exit()


if __name__ == '__main__':
    input_list = ['SYS', 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103', 'vysledky_prostejov.csv']
    # input_list = sys.argv()
    if input_check(input_list):
        req_site = request_site(input_list[1])
        election_result = crt_rslt_structure()
        soup_site = BeautifulSoup(req_site, 'html.parser')
        selected_location = soup_site.find_all('h3')[:2]
        election_result[0].update({"region": selected_location[0].string.split()[1] + ' kraj'})
        election_result[1].update({"district": selected_location[1].string.split()[1]})
        print(election_result)