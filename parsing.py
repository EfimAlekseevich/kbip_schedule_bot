import re
import requests
from bs4 import BeautifulSoup


def get_html(url):
    proxies = {'http': '52.35.217.148'}
    response = requests.get(url, proxies=proxies)
    html = response.text
    return html


def get_data_dict(html):
    soup = BeautifulSoup(html, 'html.parser')
    trs = soup.find_all('tr')[2:9]
    schedule = {}
    for tr in trs:
        tds = tr.find_all('td')
        pair_number = tds[0].string
        schedule[pair_number] = []
        day = 1
        for td in tds[1:-1]:
            pair = get_pair(day, td)
            schedule[pair_number].append(pair)
            day += 1

    days = {'1': [],
            '2': [],
            '3': [],
            '4': [],
            '5': [],
            '6': [],
            '7': [],
            }
    print(schedule)
    for pair_number, row_pairs in schedule.items():
        for pair in row_pairs:
            if pair:
                pair['time'] = pair_number
                days[str(pair['day'])].append(pair)
    print(days)
    return days


def get_pair(day, td):
    subject, teachers, place = None, None, None
    pair = td.find_all('div', {'class': 'pair'})
    try:
        subject_teacher = pair[-1].find('div', {'class': ['left-column']})
        subject = subject_teacher.find('div', {'class': ['subject']}).string
        teachers = [teacher.string for teacher in subject_teacher.find_all('div', {'class': ['teacher']})]
        group_place = pair[-1].find('div', {'class': 'right-column'})
        place = group_place.find('div', {'class': ['place']}).string
    except:
        pass
    if subject:
        return ({'day': day,
                 'subject': subject,
                 'teachers': teachers,
                 'place': place})


def get_faculties():
    url = 'https://kbp.by/rasp/timetable/view_beta_kbp/'
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    faculties_block = soup.find('div', class_='find_block')
    faculties = {}
    for facultie_block in faculties_block.find_all('div', class_='spec'):
        facultie_name = facultie_block.find('div', class_='spec-head').string
        faculties[facultie_name] = {}
        groups = facultie_block.find_all('a')
        for group in groups:
            group_id = re.search(r'id=(\d+)', group['href']).group(1)
            group_name = group.string
            faculties[facultie_name][group_name] = group_id
    return faculties