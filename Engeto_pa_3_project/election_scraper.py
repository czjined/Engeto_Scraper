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
    main_row = ['region', 'district', 'city_number', 'city_name', 'city_link', 'registered', 'envelope', 'valid']
    for item in main_row:
        tmp_dict = dict()
        tmp_dict.setdefault(item, '')
        result_structure.append(tmp_dict)
    return result_structure


def htmltable_to_list(soup, class_sel='', tag_sel='td', id_sel='', header_sel='', href_sel=False) -> list:
    result_list = list()
    for row in soup.findAll(tag_sel, attrs={'class': class_sel,'id': id_sel, 'header':header_sel}):
        if href_sel:
            result_list.append(row.a['href'])
        else:
            result_list.append(row.text)
    return result_list


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
        soup_table = soup_site.find('table', attrs={'class': 'table'})
        cities_number = htmltable_to_list(soup_table, class_sel='cislo')
        election_result[2].update({"city_number": cities_number})
        cities_names = htmltable_to_list(soup_table, class_sel='overflow_name')
        election_result[3].update({"city_name": cities_names})
        cities_links = htmltable_to_list(soup_table, class_sel='cislo', href_sel=True)
        election_result[4].update({"city_link": cities_links})
        if len(election_result[2]) == len(election_result[3]) and len(election_result[2]) == len(election_result[4]):
            print(election_result[2], '\n')
            print(election_result[3], '\n')
            print(election_result[4], '\n')
        else:
            print('Chyba scrappingu obci, ruzna delka listu!')
        tmp_list = list()
        for i, odkaz in enumerate(election_result[4]['city_link']):
            odkaz = 'https://volby.cz/pls/ps2017nss/' + odkaz
            req_cities = request_site(odkaz)
            soup_cities = BeautifulSoup(req_cities, 'html.parser')
            soup_table = soup_cities.find('table', attrs={'class': 'table'})
            # print(soup_table)
            # cities_registered = htmltable_to_list(soup_table, class_sel='cislo', header_sel='sa2')
            cities_registered = soup_table.find('td', attrs={'class': 'cislo', 'headers': 'sa2'})
            try:
                tmp_list.append(cities_registered.text)
            except AttributeError:
                print(f'Mesto {election_result[3]["city_name"][i]} ma problem!')
        election_result[5].update({"registered": tmp_list})
        print(election_result[5], '\n')