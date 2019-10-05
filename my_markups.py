from telebot.types import ReplyKeyboardMarkup
from functions import get_daily_schedule, get_button_text
from constantes import week_days


def get_all_markups(faculties):
    markups = dict()
    markups['faculties'] = get_markup(faculties)
    markups['groups'] = dict()
    for faculty, groups in faculties.items():
        markups['groups'][faculty] = get_markup(groups)
    markups['days'] = get_markup(week_days.values())
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
        cols = get_pair_row(pair, timing)
        markup.row(cols['time'], cols['subject'], cols['teacher'], cols['place'])
    markup.add('Назад')
    return markup


def get_pair_row(pair, timing):
    pair_row = dict()
    pair_row['time'] = timing[pair['time']][0] + '\n' + timing[pair['time']][1]
    pair_row['subject'] = get_button_text(pair['subject'])
    pair_row['teacher'] = get_button_text(pair['teachers'][0])
    if pair['teachers'][1]:
        pair_row['teacher'] += '\n' + get_button_text(pair['teachers'][1])
    pair_row['place'] = 'К.' + get_button_text(pair['place'], 4)
    return pair_row
