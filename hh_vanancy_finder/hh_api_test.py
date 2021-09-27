import requests
import datetime
HH_API = "https://api.hh.ru"


def get_vacancy_text_by_id(vacancy_id):
    path = 'vacancies/' + str(vacancy_id)
    url = HH_API + '/' + path

    try:
        r = requests.get(url)
    except requests.ConnectionError as e:  # This is the correct syntax
        raise SystemExit(e)

    if (r.status_code != 200):
        raise SystemExit(r.json())

    content = r.json()
    import pprint
    #pprint.pprint(content.keys())
    #pprint.pprint(content)

    ''' 
    Keys and data_for_api.txt that might be helpful:
    description
    experience
    key_skills
    
    '''
    description = content['description']

    #print(type(description))


def get_vacancy_skills_by_id(vacancy_id):
    path = 'vacancies/' + str(vacancy_id)
    url = HH_API + '/' + path

    try:
        r = requests.get(url)
    except requests.ConnectionError as e:  # This is the correct syntax
        raise SystemExit(e)

    if (r.status_code != 200):
        raise SystemExit(r.json())

    content = r.json()
    import pprint
    # pprint.pprint(content.keys())
    pprint.pprint(content)

    ''' 
    Keys and data_for_api.txt that might be helpful:
    description
    experience
    key_skills

    '''
    key_skills_data = content['key_skills']

    print(key_skills_data)
    key_skills = []
    for skill in key_skills_data:
    #Eprint(skill['name'])
        key_skills.append(skill['name'])
    #print(key_skills)

    return key_skills

get_vacancy_skills_by_id(42684107)
