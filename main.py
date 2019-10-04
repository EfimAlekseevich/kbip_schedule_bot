import random
import time

import telebot

import functions as f
import my_markups
from constantes import bot_token, week_days, admins
from parsing import get_faculties


def main():
    while True:
        bot = telebot.TeleBot(bot_token)
        activity = f.get_json_data_dict('activity')
        emodji = f.get_json_data_dict('emodji')
        faculties = get_faculties()
        timing = f.get_json_data_dict('timing')
        users = f.get_json_data_dict('users')
        markups = my_markups.get_all_markups(faculties, week_days.values())
        print('=====START=====')

        try:
            @bot.message_handler(commands=['start'])
            def handle_start(message):
                answer_text = '\n*Привет*, ищи свою группу и смотри расписание,\n' \
                              'изменить группу здесь /changegroup\n' \
                              'что-то непонятно, посмтори здесь /help.\n'

                user_id = message.from_user.id
                if not f.user_is_exist(users, user_id):
                    users.append({'id': user_id,
                                  'faculty': None,
                                  'group': None,
                                  })
                    markup = markups['faculties']
                else:
                    markup = markups['days']
                f.console_log(message, activity, answer_text)
                bot.send_message(user_id, answer_text, reply_markup=markup, parse_mode='Markdown')

            @bot.message_handler(commands=['help'])
            def handle_help(message):
                answer_text = '\nДля изменения группы используйте команду /changegroup,\n' \
                              'после выбора группы будет доспупно расписание по дням недели.\n' \
                              '*АВТОР БОТА НЕ ОТВЕЧАЕТ ЗА ПРАВИЛЬНОСТЬ И КОРРЕКТНОСТЬ ИНФОРМАЦИИ*,\n' \
                              'Сверить расписание можно на [официальном сайте КБИП](https://kbp.by)\n' \
                              'Всё остальное в [тех. поддежку](https://t.me/efi_fi).'
                f.console_log(message, activity, answer_text)
                bot.send_message(message.from_user.id, answer_text, parse_mode='Markdown')

            @bot.message_handler(commands=['changegroup'])
            def handle_changegroup(message):
                user_id = message.from_user.id
                for number in range(len(users)):
                    if users[number]['id'] == user_id:
                        users[number]['faculty'] = None
                        users[number]['group'] = None
                        f.save_data(users, 'users')
                        break
                answer_text = 'Ну что ж выбирайте заново)'
                f.console_log(message, activity, answer_text)
                bot.send_message(user_id, answer_text, reply_markup=markups['faculties'])

            @bot.message_handler(content_types=['text'])
            def handle_text(message):
                user_id = message.from_user.id
                message_text = message.text
                upper_message_text = message_text.upper()
                answer = {
                    'text': random.choice(emodji['all_emodji']),
                    'reply_markup': None,
                    'parse_mode': None
                }
                if not f.user_is_exist(users, user_id):
                    users.append({'id': user_id,
                                  'faculty': None,
                                  'group': None,
                                  })
                    answer['reply_markup'] = markups['faculties']
                if user_id in admins:
                    answer['text'] = random.choice(emodji['good_emodji'])
                    if message_text == 'save activity':
                        f.save_data(activity, 'activity')
                        answer['text'] = 'Файл успешно сохранён.'
                    elif message_text == 'get activity':
                        f.save_data(activity, 'activity')
                        file = open('activity.json')
                        bot.send_document(user_id, file)
                    elif message_text[:10] == 'for vika: ':
                        bot.send_message(519084935, message_text[10:])

                user_number, faculty, group = f.get_user_attributes(users, user_id)

                if not faculty:
                    if message_text in faculties:
                        faculty = message_text
                        users[user_number]['faculty'] = faculty
                        answer['reply_markup'] = markups['groups'][message_text]
                    else:
                        answer['reply_markup'] = markups['faculties']
                elif not group:
                    if upper_message_text in faculties[faculty]:
                        group = upper_message_text
                        users[user_number]['group'] = group
                        answer['reply_markup'] = markups['days']
                        f.save_data(users, 'users')
                    else:
                        answer['reply_markup'] = markups['groups'][faculty]
                else:
                    week_day = f.day_in_message(upper_message_text)
                    if not week_day:
                        answer['reply_markup'] = markups['days']
                    else:
                        group_id = faculties[faculty][group]
                        day_timing = timing['usually'] if week_day < 6 else timing['saturday']
                        answer['reply_markup'] = my_markups.get_daily_schedule_markup(week_day, group_id, day_timing)
                f.console_log(message, activity, answer['text'])
                bot.send_message(user_id, answer['text'], reply_markup=answer['reply_markup'],
                                 parse_mode=answer['parse_mode'])

            @bot.message_handler(func=lambda m: True)
            def handle_all(message):
                f.console_log(message, activity, '-'*10)
                bot.send_message(message.from_user.id, '-'*10)

            bot.polling()

        except:
            f.save_data(users, 'users')
            f.save_data(activity, 'activity')
            print('=====Error=====')
            time.sleep(10)


if __name__ == '__main__':
    main()
