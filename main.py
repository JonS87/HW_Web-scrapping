import requests
import fake_headers
from bs4 import BeautifulSoup
from pprint import pprint
import unicodedata
import json

headers_gen = fake_headers.Headers(browser='firefox', os='win')
params = {
        #"page": 0,
        "text": "python",
        "items_on_page": 100,
        "area": [1, 2]
    }
response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', params=params, headers=headers_gen.generate()).text
hh_main = BeautifulSoup(response, 'lxml')
article_list_tag = hh_main.find('div', id="a11y-main-content")

article_tags = article_list_tag.find_all('div', class_='serp-item')

vacancy_list = []
for article_tag in article_tags:
    a_tag = article_tag.find('a')
    link = a_tag['href']

    vacancy_response = requests.get(link, headers=headers_gen.generate()).text
    vacancy_main = BeautifulSoup(vacancy_response, 'lxml')
    vacancy_info = vacancy_main.find('div', class_='bloko-columns-row').text


    if 'Django' in vacancy_info or 'Flask' in vacancy_info:
        
        vacancy_name = vacancy_main.find('h1',class_='bloko-header-section-1').text
        salary_fork = vacancy_main.find('div', class_='vacancy-title').find('span', class_='bloko-header-section-2 bloko-header-section-2_lite')
        if salary_fork == None:
            salary_fork = ''
        else:
            salary_fork = unicodedata.normalize("NFKD", salary_fork.text)
        company_name = unicodedata.normalize("NFKD", vacancy_main.find('div', class_='bloko-column bloko-column_container bloko-column_xs-4 bloko-column_s-8 bloko-column_m-12 bloko-column_l-0').find('span', class_='bloko-header-section-2 bloko-header-section-2_lite').text)
        city = vacancy_main.find('div', class_='vacancy-company-redesigned').find('p')
        if city == None:
            city = unicodedata.normalize("NFKD", vacancy_main.find('div', class_='vacancy-company-redesigned').find('a', class_='bloko-link bloko-link_kind-tertiary bloko-link_disable-visited').find('span').text)
        else:
            city = unicodedata.normalize("NFKD", city.text)
        
        
        vacancy_list.append({
            'Вакансия': vacancy_name,
            'Ссылка': link,
            'Вилка зп': salary_fork,
            'Название компании': company_name,
            'Город': city
            })

with open('vacancy_list.json', 'w', encoding='utf-8') as file:
    json.dump(vacancy_list, file, indent=2, ensure_ascii=False)