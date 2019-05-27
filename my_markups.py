from telebot.types import ReplyKeyboardMarkup
from functions import get_daily_schedule, get_button_text
from constantes import week_days


def get_all_markups(faculties, week_days):
    markups = dict()
    markups['faculties'] = get_markup(faculties)
    markups['groups'] = dict()
    for faculty, groups in faculties.items():
        markups['groups'][faculty] = get_markup(groups)
    markups['days'] = get_markup(week_days)
    return markups


def get_markup(elements):
    markup = ReplyKeyboardMarkup(True)
    for element in elements:
        markup.add(element)
    return markup


def get_daily_schedule_markup(week_day, group_id, timing):
    markup = ReplyKeyboardMarkup(True)
    daily_schedule = get_daily_schedule(group_id, week_day)
    markup.add(week_days[str(week_day)])
    for pair in daily_schedule:
        time = timing[pair['time']][0] + '\n' + timing[pair['time']][1]
        subject = get_button_text(pair['subject'])
        teacher = get_button_text(pair['teachers'][0])
        if pair['teachers'][1]:
            teacher += '\n' + get_button_text(pair['teachers'][1])
        place = 'К.' + get_button_text(pair['place'], 4)
        markup.row(time, subject, teacher, place)
    markup.add('Назад')
    return markup
