import json
import requests
import bs4
from fake_headers import Headers


KEYWORDS = ['Django', 'Flask']


def get_fake_headers():
    return Headers(os='win', browser='chrome').generate()


def get_vacancies_info(keywords_list):
    result_list = []
    try:
        print("Получение вакансий...")
        response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2',headers=get_fake_headers())
        response.raise_for_status()
        html_data = response.text
        main_soup = bs4.BeautifulSoup(html_data, features='lxml')
        vacancy_list_container = main_soup.find('div', id='a11y-main-content')
        vacancies_list = vacancy_list_container.find_all('div', class_='serp-item')
        print(f"Найдено {len(vacancies_list)} вакансий.")
        for index, vacancy in enumerate(vacancies_list, start=1):
            print(f"Обработка вакансии {index} из {len(vacancies_list)}...")
            vacancy_link = vacancy.find('a', class_='bloko-link').get('href')
            response_vacancy = requests.get(vacancy_link, headers=get_fake_headers())
            response_vacancy.raise_for_status()
            vacancy_html_data = response_vacancy.text
            vacancy_soup = bs4.BeautifulSoup(vacancy_html_data, features='lxml')
            if vacancy_soup:
                vacancy_description = vacancy_soup.find('div', class_='g-user-content').text
                for keyword in keywords_list:
                    if keyword in vacancy_description:
                        salary_tag = vacancy_soup.find('div', {'data-qa': 'vacancy-salary'})
                        salary = ' '.join(salary_tag.text.split()) if salary_tag else 'не указана'
                        company_name_tag = vacancy_soup.find('span', class_='vacancy-company-name').text.strip()
                        company_name = ' '.join(company_name_tag.split())
                        city_tag = vacancy_soup.find('span', {'data-qa': 'vacancy-view-raw-address'})
                        city = (city_tag.text.strip().split(', ')[0] if city_tag
                                else
                                vacancy_soup.find('p', {'data-qa': 'vacancy-view-location'}).text.strip().split(', ')[0])
                        result_list.append({
                            'link': vacancy_link,
                            'salary': salary,
                            'company': company_name,
                            'city': city
                        })
                        print(f"Найдена подходящая вакансия: {company_name}, {city}, Зарплата: {salary}, Ссылка: {vacancy_link}")
                        break
        print(f"Всего подходящих вакансий: {len(result_list)}")
        with open('vacancies_data.json', 'w', encoding='utf-8') as file:
            json.dump(result_list, file, ensure_ascii=False, indent=4)
            print("Данные успешно записаны в 'vacancies_data.json'")
    except requests.exceptions.RequestException as error:
        print('Ошибка при выполнении запроса:', error)


if __name__ == '__main__':
    get_vacancies_info(KEYWORDS)
