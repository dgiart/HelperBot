from telebot import types
import time
import requests
T = time.asctime()


# getters
def get_chat_id(res):
    if 'message' in res:
        log('in get_chat_id' + str(res) + 'line_11')
        id = res['message']['chat']['id']
    else:
        return 0
        # id = res['edited_message']['chat']['id']
        # log('line_14_in funcs id = ' + str(id))
    return id


def get_chat_type(res):
    chat_type = res['message']['chat']['type']
    return chat_type


def get_name(res):
    if 'message' in res:
        name = res['message']['from']['first_name']
    else:
        return ''
    return name


def get_title(res):
    title = res['message']['chat']['title']
    return title


def get_text(res):
    if 'message' in res:
        text = res['message']['text']
    else:
         return ''
    return text


def get_loc(res):
    location = res['message']['location']
    lat = location['latitude']
    lon = location['longitude']
    return lat, lon


def get_update_id(res):
    update_id = res['update_id']
    return update_id


# senders
def send_message(url, chat_id, text):
    params = {'chat_id': chat_id, 'text': text, 'disable_web_page_preview': 0}
    req = requests.post(url + 'sendMessage', data=params)
    return req


def send_keyboard(chat_id, keys, text, _bot):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in keys])
    _bot.send_message(chat_id, text, reply_markup=keyboard)  # reply_markup=keyboard)


def delete_keyboard(chat_id, text, _bot):
    _del = types.ReplyKeyboardRemove()
    _bot.send_message(chat_id, text, reply_markup=_del)

# def calendar_handler(bot,update):
#     update.message.reply_text("Please select a date: ",
#                         reply_markup=telegramcalendar.create_calendar())
#
#
# def inline_handler(bot,update):
#     selected,date = telegramcalendar.process_calendar_selection(bot, update)
#     if selected:
#         bot.send_message(chat_id=update.callback_query.from_user.id,
#                         text="You selected %s" % (date.strftime("%d/%m/%Y")),
#                         reply_markup=ReplyKeyboardRemove())

# Loogger
def log(log_text):
    with open('log.txt', 'a') as f:
        f.write(log_text + 'at: ' + T + '\n')


# Verificators
def date_verificator(date):
    verificated = True
    dates = date.split('.')
    if len(dates) == 3:
        try:
            day, month, year = tuple([int(i) for i in dates])
        except:
            verificated = False
            return verificated
        if not (0 < day < 31):
            verificated = False
        if not (0 < month < 13):
            verificated = False
        if not (1900 < year < 2022):
            verificated = False
    else:
        verificated = False

    return verificated
