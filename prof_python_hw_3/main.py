import requests
import bs4
import json
from fake_headers import Headers


def get_headers():
    return Headers(os='win', browser='chrome').generate()


def load_data_to_json_file(data):
    with open('vacancies_data.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def main():
    url = 'https://spb.hh.ru/search/vacancy?area=1&area=2&ored_clusters=true&text=NAME%3Apython+and+DESCRIPTION%3ADjango+and+Flask&order_by=publication_time'
    print('Загрузка данных...')
    response = requests.get(url, headers=get_headers())

    if response.status_code == 200:
        print('Данные успешно загружены.')
        main_html_data = response.text
        main_soup = bs4.BeautifulSoup(main_html_data, 'lxml')
        tag_main_vacancy_serp_content = main_soup.find('main', class_='vacancy-serp-content')
        vacancies_tags = tag_main_vacancy_serp_content.find_all('div', class_='serp-item serp-item_link')
        parsed_data = []

        for vacancy_tag in vacancies_tags:
            h3_tag = vacancy_tag.find('h3', class_='bloko-header-section-3')
            a_tag = h3_tag.find('a')
            link = a_tag['href']

            salary_tag = vacancy_tag.find('span', class_='bloko-header-section-2')
            salary_text = salary_tag.text.replace('\xa0', ' ').replace(' ',
                                                                       ' ') if salary_tag else 'Зарплата не указана'

            company_section = vacancy_tag.find('div', class_='vacancy-serp-item-company')
            company_info = company_section.find('div', class_='vacancy-serp-item__info')
            company_name_section = company_info.find('div',
                                                     class_='bloko-v-spacing-container bloko-v-spacing-container_base-2')
            company_name_text = company_name_section.find('div', class_='bloko-text').text.replace('\xa0', ' ').replace(
                ' ', ' ') if company_name_section else 'Компания не указана'

            city_section = company_info.find('div', {'data-qa': 'vacancy-serp__vacancy-address'})
            city_text = city_section.text.replace('\xa0', ' ').replace(' ', ' ') if city_section else 'Город не указан'

            parsed_data.append({
                'link': link,
                'salary': salary_text,
                'company': company_name_text,
                'city': city_text
            })

        load_data_to_json_file(parsed_data)
        print('Данные успешно записаны в файл vacancies_data.json.')
    else:
        print(f'Ошибка при загрузке данных. Код ошибки: {response.status_code}')


if __name__ == '__main__':
    main()