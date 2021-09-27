# API from hh.ru website https://github.com/hhru/api

"""
Ключевое слово для поиска вакансий :
Python

Дополнительные сведения о вакансии:

Кто работодатель? название компании
количество сотрудников
регион и город
уровень заработной платы
стаж
иные ...

необходимо узнать требования и условия для вакансий:
навыки и технологии
иные

"""

import requests
import pandas as pd
from time import *
import datetime

pd.set_option('display.max_colwidth', None)

HH_API = "https://api.hh.ru"
headers = {
    "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36 '}


def get_vacancies_data(text, page, per_page):
    vacancy_requests = "?text=" + str(text) + "&page=" + str(page) + "&per_page=" + str(per_page)
    path = 'vacancies/' + str(vacancy_requests)
    url = HH_API + '/' + path

    try:
        r = requests.get(url, headers=headers)
    except requests.ConnectionError as e:  # This is the correct syntax
        raise SystemExit(e)

    if (r.status_code != 200):
        raise SystemExit(r.json())

    content = r.json()

    return content

def get_vacancies_by_keyword(text, page, per_page):
    """

    :param text:
    :param page:
    :param per_page:
    :return: csv file
    """

    content = get_vacancies_data(text, page, per_page)

    # print(content.keys())
    total_found_vacancies = content['found']
    print("Total found:" + str(total_found_vacancies))

    count = 0
    passed_count = 0
    total_count = 0
    data = {}
    appended_alternate_url = []
    appended_vacancy_area = []
    appended_vacancy_id = []
    appended_created_at = []
    appended_employer_id = []
    appended_vacancy_name = []
    appended_requirement = []
    appended_responsibility = []
    appended_salary_from = []
    appended_salary_to = []
    appended_salary_currency = []
    appended_salary_gross = []
    appended_schedule = []
    appended_description = []
    appended_key_skills = []

    while total_count <= 1990:  # total_found_vacancies:

        content = get_vacancies_data(text, page, per_page)
        vacancy_data = content["items"]
        print("Page is:", page)
        print("Vacancy data length:", len(vacancy_data))

        alternate_url = []
        vacancy_area = []
        vacancy_id = []
        created_at = []
        employer_id = []
        vacancy_name = []
        requirement = []
        responsibility = []
        salary_from = []
        salary_to = []
        salary_currency = []
        salary_gross = []
        schedule = []
        description = []
        key_skills = []

        for vacancy in vacancy_data:
            alternate_url.append(vacancy['alternate_url'])
            area_data = vacancy['area']
            vacancy_id.append((vacancy['id']))
            # print(type(vacancy['id']))
            try:
                description_and_key_skills_data = get_vacancy_text_by_id(vacancy['id'])
                # print(description_and_key_skills_data[0])
                description.append(description_and_key_skills_data[0])
                key_skills.append(description_and_key_skills_data[1])
            except Exception as e:
                description.append("None")
                key_skills.append('None')
                pass

            vacancy_area.append(area_data['name'])  # absorb vacancy area
            created_at.append(vacancy['created_at'])  # absorb date of created vacancy
            try:
                employer_data = vacancy['employer']
                # print(employer_data['id'])
                employer_id.append(employer_data['id'])  # absorb employer id
            except Exception as e:
                employer_id.append('None')
                pass
            vacancy_name.append(vacancy['name'])

            snippet_data = vacancy['snippet']
            requirement.append(snippet_data['requirement'])
            responsibility.append(snippet_data['responsibility'])
            schedule_data = vacancy['schedule']
            schedule.append(schedule_data['name'])

            salary_data = (vacancy['salary'])
            # print(salary_data)
            if salary_data is None:
                # print("None Data detected")
                # pprint.pprint(vacancy)
                salary_from.append('None')
                # print(salary_data['to'])
                salary_to.append('None')
                # print(salary_data['currency'])
                salary_currency.append('None')
                # print(salary_data['gross'])
                salary_gross.append('None')
                passed_count += 1
                pass
            if salary_data is not None:

                try:
                    # print(salary_data['from'])
                    salary_from.append(salary_data['from'])
                    # print(salary_data['to'])
                    salary_to.append(salary_data['to'])
                    # print(salary_data['currency'])
                    salary_currency.append(salary_data['currency'])
                    # print(salary_data['gross'])
                    salary_gross.append(salary_data['gross'])

                    count += 1
                except Exception as e:
                    print("Exception raised")
                    raise SystemExit(e)


        page += 1




        print("Counted " + str(count))
        print("Passed " + str(passed_count))
        total_count = count + passed_count
        print("Total count " + str(total_count))
        print('Page ' + str(page))

        appended_alternate_url.extend(alternate_url)
        appended_vacancy_area.extend(vacancy_area)
        appended_created_at.extend(created_at)
        appended_employer_id.extend(employer_id)
        appended_vacancy_name.extend(vacancy_name)
        appended_requirement.extend(requirement)
        appended_responsibility.extend(responsibility)
        appended_salary_from.extend(salary_from)
        appended_salary_to.extend(salary_to)
        appended_salary_currency.extend(salary_currency)
        appended_salary_gross.extend(salary_gross)
        appended_schedule.extend(schedule)
        appended_vacancy_id.extend(vacancy_id)
        appended_description.extend(description)
        appended_key_skills.extend(key_skills)

        if page == 20:
            # page = 19
            # per_page = 99
            total_count = 2000

    data.update({
        'alternate_url': appended_alternate_url,
        'vacancy_area': appended_vacancy_area,
        'vacancy_id': appended_vacancy_id,
        'created_at': appended_created_at,
        'employer_id': appended_employer_id,
        'vacancy_name': appended_vacancy_name,
        'requirement': appended_requirement,
        'responsibility': appended_responsibility,
        'description': appended_description,
        'key_skills': appended_key_skills,
        'from': appended_salary_from,
        'to': appended_salary_to,
        'currency': appended_salary_currency,
        'gross': appended_salary_gross,
        'schedule': appended_schedule,

         }, ignoreindex=True)

    df = pd.DataFrame(data)
    # df2 = pd.DataFrame(df['comment_time'].value_counts())
    print(df.head(20))
    df.to_csv('all_data_hh_' + str(text) + '_' + str(datetime.date.today()) + '.csv')
    # df2.to_csv('timecodes_hh_'+str(text)+'.csv')
    print("Done")


def get_vacancy_text_by_id(vacancy_id) -> str:
    """

    :param vacancy_id:
    :return:
    """

    path = 'vacancies/' + str(vacancy_id)
    url = HH_API + '/' + path

    try:
        r = requests.get(url, headers=headers)
    except requests.ConnectionError as e:  # This is the correct syntax
        raise SystemExit(e)

    if (r.status_code != 200):
        raise SystemExit(r.json())

    content = r.json()

    description = content['description']
    key_skills_data = content['key_skills']

    key_skills = []
    for skill in key_skills_data:
        key_skills.append(skill['name'])

    sleep(1)
    return description, key_skills


get_vacancies_by_keyword("Python", 0, 99)  # text, page (max items 2000), per_page (100 max)

# TODO Написать код для анализа description вакансий (статистика по одинаковым словам, исключение нерелевантных слов и т.д)
