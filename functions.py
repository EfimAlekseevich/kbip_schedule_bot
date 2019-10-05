import json
from datetime import datetime

import parsing
from constantes import base_url, separator


def get_json_data_dict(filename):
    file = open(f'{filename}.json')
    json_data_dict = json.load(file)
    file.close()
    return json_data_dict


def get_daily_schedule(group_id, week_day):
    html = parsing.get_html(f'{base_url}{str(group_id)}')
    schedule = parsing.get_data_dict(html)
    daily_schedule = schedule[str(week_day)]
    if daily_schedule:
        return daily_schedule
    else:
        return list()


def user_is_exist(users, user_id):
    for user in users:
        if user['id'] == user_id:
            return True


def get_user_attributes(users, user_id):
    for number, user in enumerate(users):
        if user['id'] == user_id:
            return number, user['faculty'], user['group']


def save_data(data, filename):
    file = open(f'{filename}.json', 'w')
    json.dump(data, file)
    file.close()
    print(separator + f'Save {filename}.json\n\n')


def day_in_message(upper_message):
    if 'ПН' in upper_message or 'ПОН' in upper_message or 'ПАН' in upper_message:
        return 1
    elif 'ВТ' in upper_message or 'АУТ' in upper_message:
        return 2
    elif 'СР' in upper_message or 'СЕР' in upper_message:
        return 3
    elif 'ЧТ' in upper_message or 'ЧЕТ' in upper_message or 'ЧАЦ' in upper_message:
        return 4
    elif 'ПТ' in upper_message or 'ПЯТ' in upper_message:
        return 5
    elif 'СБ' in upper_message or 'СУБ' in upper_message:
        return 6
    elif 'ВС' in upper_message or 'ВОС' in upper_message or 'НЯД' in upper_message:
        return 7


def get_button_text(text, max_length=8):
    if text:
        difference = len(text) - max_length
        if difference < 0:
            text = text[:max_length]
        else:
            text = text + ' ' * difference
    else:
        text = '###'

    return text


def console_log(message, activity, answer):
    date_time = str(datetime.now())
    username = message.from_user.username
    user_id = message.from_user.id
    message_text = get_button_text(message.text, 50)
    answer = get_button_text(answer, 50)

    action = {
        'data_time': date_time,
        'username': username,
        'user_id': user_id,
        'message': message_text
    }
    activity.append(action)

    log = f'{separator}{date_time}\n' \
        f'Username: @{username}, User ID: {user_id}\n' \
        f'Message: {message_text}\n' \
        f'Answer: {answer}\n\n'

    print(log)





