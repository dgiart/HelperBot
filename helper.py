# 13.45 08/07/22 PyCharm
from flask import Flask
from flask import request
# import requests
import time
import sys
import json
import telebot
import pymongo
from telebot import types
from datetime import datetime
import csv
from bot_funcs import T, log, get_chat_id, get_name, \
    get_text  # send_message, send_image, send_keyboard, delete_keyboard, get_chat_id, get_name, get_text
from bot_funcs import date_verificator, delete_keyboard, send_message, send_keyboard

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["citizens_database"]
token = '5400393109:AAGWSE_fmn0sW61LTONHXkPy8q0L34yxc3k'  # helper2022
bot = telebot.TeleBot(token)
app = Flask(__name__)
url = "https://api.telegram.org/bot" + token + "/"
id_list = []
citizens = {}


@app.route('/')
def index():
    t = time.asctime()
    return f'<h1> new hi from main at {t} !</h1>'


class Citizen(object):
    """docstring for ."""

    def __init__(self, id, name):
        self._id = id
        self._name = name
        self.round = 0
        self.info_type = ''
        self.quastions = ['', 'Введите ФИО', 'Введите телефон', 'Введите дату рождения (дд.мм.гггг)',
                          'Введите адрес', 'Введите число проживающих', 'Введите ФИО и возраст проживающих',
                          'Есть ли среди проживающих инвалиды?', 'Есть ли дети?',
                          'Если есть, укажите возраст', 'Нужны ли продукты питания?', 'Вода?',
                          'Лекарства?', 'Укажите количество', 'Средства личной гигиены?',
                          'Укажите количество', 'Памперсы?', 'Особенности диеты и т.п.',
                          'Даю согласие на обработку персональных данных.',
                          'Даю согласие на фото/видео.']
        self.citizen_data = {'fio': '', 'phone': '', 'birth': '', 'addr': '', 'people_num': '', 'people_fio': '',
                             'invalids': '', 'children': '', 'children_age': '', 'food': '', 'drugs': '', 'water': '',
                             'products_detail': '', 'gigien': '', 'gigien_num': '', 'pampers': '', 'diet': '',
                             'pers_data_agreement': '', 'photo_agreement': ''}

    def conversation(self, user_text):
        # log_text = 'line 88 in conversation'
        # log(log_text)

        if 'start' in user_text.lower() or 'старт' in user_text.lower() or 'Начать сначала'.lower() in user_text.lower() or 'Изменить'.lower() in user_text.lower():
            t = time.asctime()
            # log(f'row67 {t}')
            keys = ['Внести данные.', 'Правила.', 'Просмотреть информацию.', 'Начать сначала.']#, '/start']
            text = f'Привет {self._name}! Вас приветствует бот-помошник'
            send_keyboard(self._id, keys, text, bot)
            self.round = 0
        if user_text.lower() == 'правила.':
            text_to_send = 'Для того чтобы внести данные нажмите кнопку  "Внести данные" и введите данные в формате:\n' \
                           '1. ФИО\n' \
                           '2. Телефон\n' \
                           '3. Дату рождения (дд.мм.гггг)\n' \
                           '4. Адрес\n' \
                           '5. Число проживающих\n' \
                           '6. ФИО и возраст проживающих\n' \
                           '7. Есть ли среди проживающих инвалиды?\n' \
                           '8. Есть ли дети?\n' \
                           '9. Если есть, укажите возраст\n' \
                           '10. Нужны ли продукты питания?\n' \
                           '11. Вода?\n' \
                           '12. Лекарства?\n' \
                           '13. Укажите количество\n' \
                           '14. Средства личной гигиены?\n' \
                           '15. Укажите количество\n' \
                           '16. Памперсы?\n' \
                           '17. Особенности диеты и т.п.\n' \
                           '18. Даю согласие на обработку персональных данных.\n' \
                           '19. Даю согласие на фото/видео.\n' \
                           'Для просмотра данных нажмите кнопку "Просмотр информации",' \
                           ' далее выберите какие данные Вас интересуют: полный список,' \
                           ' данные по конкретному человеку, данные по группе лиц. Далее следуйте подсказкам\n'
            send_message(url, self._id, text_to_send)
            self.round = 0
            return
        if user_text == 'Внести данные.':
            self.command = 'Внести данные'
            self.round += 1
            # log('Внести данные row 87')
            self.insert_data(user_text)
            return
        if user_text == 'Просмотреть информацию.':
            self.command = 'Просмотреть информацию'
            self.round += 1
            # log('Просмотреть информацию 95')
            self.show_data(user_text)
            return
        if self.round > 0:
            if self.command == 'Внести данные':
                # log('Внести данные row 127')
                self.insert_data(user_text)
                return

            if self.command == 'Просмотреть информацию':
                # log('Просмотреть информацию 103')
                self.show_data(user_text)
                return

    def show_data(self, user_text):
        # log(f'TEXT: {user_text}, R = {self.round}, row 109!!!')
        if self.round == 1:
            keys = ['Полный список', 'Информация по человеку', 'Информация по группе людей', 'Начать сначала']
            text = f'Какая информация Вас интересует?'
            send_keyboard(self._id, keys, text, bot)
            # log('show_data row 140')
            self.round += 1
            return
        # log('row 143')
        if self.round == 2:
            # log(f'TEXT: {user_text}, R = {self.round}, row 145')
            if user_text == 'Полный список':

                mycol = mydb["people"]
                log('Full unformation row 149')
                cit = []
                text_to_send = ''
                row_num = 1
                for x in mycol.find():
                    cit.append(x)
                # text_to_send = str(cit)
                for i in range(len(cit)):
                    # log(text_to_send)
                    try:
                        text_to_send = text_to_send + str(i) + '. ' + cit[i]['fio'] + '\n'

                    # text_to_send = text_to_send + cit + '\n'
                    except:
                        pass
                send_message(url, self._id, text_to_send)
                # self.round += 1
                return
            if user_text == 'Информация по человеку':
                # log(user_text + 'row164')
                self.info_type = 'конкретному'
                text_to_send = 'Ввидите ФИО (что бы увидеть список нажмите "Полный список" )'
                send_message(url, self._id, text_to_send)
                self.round += 1
                return
            if user_text == 'Информация по группе людей':
                # log(user_text + 'row171')
                self.info_type = 'группа'
                text_to_send = 'Введите интервал лет в формате: \"год1 - год2\"'
                send_message(url, self._id, text_to_send)
                self.round += 1
                return
            # if self.info_type == 'группа':
            #     log(self.info_type + 'row200')
            #     # if user_text == 'Информация по конкретному человеку':
            #     text_to_send = 'Введите интервал лет'
            #     send_message(url, self._id, text_to_send)

        if self.round == 3:
            # log(self.info_type + 'row178')
            if self.info_type == 'конкретному':
                person = user_text
                # get list of citizens
                try:
                    cits = mydb.people
                    # find person by name
                    cit = cits.find_one({'fio': person})
                    text_to_send = f"1. ФИО: {cit['fio']}\n" \
                                   f"2. Телефон: {cit['phone']}\n" \
                                   f"3. Датa рождения: {cit['birth']}\n" \
                                   f"4. Адрес: {cit['addr']}\n" \
                                   f"5. Число проживающих: {cit['people_num']}\n" \
                                   f"6. ФИО и возраст проживающих: {cit['people_fio']}\n" \
                                   f"7. Есть ли среди проживающих инвалиды? {cit['invalids']}\n" \
                                   f"8. Наличие детей: {cit['children']}\n" \
                                   f"9. Возраст детей: {cit['children_age']}\n" \
                                   f"10. Небходимость продуктов питания: {cit['food']}\n" \
                                   f"11. Воды: {cit['water']}\n" \
                                   f"12. Лекарств: {cit['drugs']}\n" \
                                   f"13. Kоличество: {cit['products_detail']}\n" \
                                   f"14. Средства личной гигиены: {cit['gigien']}\n" \
                                   f"15. Kоличество {cit['gigien_num']}\n" \
                                   f"16. Памперсы: {cit['pampers']}\n" \
                                   f"17. Особенности диеты и т.п.: {cit['diet']}\n" \
                                   f"18. Cогласие на обработку персональных данных: {cit['pers_data_agreement']} \n" \
                                   f"19. Cогласие на фото/видео: {cit['photo_agreement']}\n"
                    # text_to_send = f"1. ФИО: {cit['fio']}\n" \
                    #                f"2. Дату рождения: {cit['birth']}\n" \
                    #                f"3. Диагноз: {cit['diag']}\n" \
                    #                f"4. История: {cit['history']}\n" \
                    #                f"5. Адрес: {cit['addr']}\n" \
                    #                f"6. Примечание: {cit['note']}\n" \
                    #                f"7. Сопровождающий: {cit['accompan']}\n" \
                    #                f"8. Телефон: {cit['phone']}\n" \
                    #                f"9. Район: {cit['district']}"
                    send_message(url, self._id, text_to_send)
                    # log(str(self.round) + 'line199')
                    return
                except:
                    # log(str(self.round) + 'line201')
                    self.round -= 1
                    self.show_data(user_text)
                    return
                    # pass
                # self.round -= 1
                # log(str(self.round) + 'line204')

                return
            if self.info_type == 'группа':
                # log(self.info_type + 'row200')
                try:
                    years = user_text.split('-')
                    start_year = int(years[0])
                    fin_year = int(years[1])
                except:
                    text_to_send = 'Неверный формат. Введите интервал лет в формате: \"год1 - год2\"'
                    send_message(url, self._id, text_to_send)
                    return

                # lof(f"start_year = ")
                if start_year >= fin_year:
                    text_to_send = 'Неверный формат. Введите интервал лет в формате: \"год1 - год2\"'
                    send_message(url, self._id, text_to_send)
                    return
                else:
                    # log('line 226')
                    mycol = mydb["people"]
                    people_in_range = mycol.find({"birth_year": {"$gt": start_year, "$lt": fin_year}})
                    # if user_text == 'Информация по конкретному человеку':
                    # log(str(people_in_range) + 'line 230')
                    text_to_send = ''
                    people_list = []
                    for x in people_in_range:
                        people_list.append(x)
                        # print(f"ФИО: {x['fio']}, дата рождения: {x['birth']}")
                    for i in range(len(people_list)):
                        text_to_send += str(
                            i + 1) + f") ФИО: {people_list[i]['fio']}, дата рождения: {people_list[i]['birth']}\n"
                    send_message(url, self._id, text_to_send)
                    self.round -= 1
                    return

    def insert_data(self, user_text):
        if self.round == 1:
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 2:
            self.citizen_data['fio'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return

        if self.round == 3:
            self.citizen_data['phone'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return

        if self.round == 4:
            self.citizen_data['birth'] = user_text
            # self.date = self.citizen_data['birth']
            if date_verificator(self.citizen_data['birth']):
                # log(user_text + 'row187')
                birth_date = datetime.strptime(user_text, '%d.%m.%Y')
                bith_year = birth_date.year
                self.citizen_data['birth_year'] = bith_year
                text_to_send = self.quastions[self.round]
                send_message(url, self._id, text_to_send)
                self.round += 1
                return
            else:
                text_to_send = 'Неверный формат даты!!!'
                send_message(url, self._id, text_to_send)
                return
        if self.round == 5:
            self.citizen_data['addr'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 6:
            self.citizen_data['people_num'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 7:
            self.citizen_data['people_fio'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 8:
            self.citizen_data['invalids'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 9:
            self.citizen_data['children'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 10:
            self.citizen_data['children_age'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 11:
            self.citizen_data['food'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 12:
            self.citizen_data['drugs'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 13:
            self.citizen_data['water'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 14:
            self.citizen_data['products_detail'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 15:
            self.citizen_data['gigien'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 16:
            self.citizen_data['gigien_num'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 17:
            self.citizen_data['pampers'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 18:
            self.citizen_data['diet'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        if self.round == 19:
            self.citizen_data['pers_data_agreement'] = user_text
            # log(user_text)
            text_to_send = self.quastions[self.round]
            send_message(url, self._id, text_to_send)
            self.round += 1
            return

        if self.round == 20:
            self.citizen_data['photo_agreement'] = user_text
            text_to_send= f'Проверьте внесенные данные'
            send_message(url, self._id, text_to_send)
            text_to_send = f"1. ФИО: {self.citizen_data['fio']}\n" \
                                   f"2. Телефон: {self.citizen_data['phone']}\n" \
                                   f"3. Датa рождения: {self.citizen_data['birth']}\n" \
                                   f"4. Адрес: {self.citizen_data['addr']}\n" \
                                   f"5. Число проживающих: {self.citizen_data['people_num']}\n" \
                                   f"6. ФИО и возраст проживающих: {self.citizen_data['people_fio']}\n" \
                                   f"7. Есть ли среди проживающих инвалиды? {self.citizen_data['invalids']}\n" \
                                   f"8. Наличие детей: {self.citizen_data['children']}\n" \
                                   f"9. Возраст детей: {self.citizen_data['children_age']}\n" \
                                   f"10. Небходимость продуктов питания: {self.citizen_data['food']}\n" \
                                   f"11. Воды: {self.citizen_data['water']}\n" \
                                   f"12. Лекарств: {self.citizen_data['drugs']}\n" \
                                   f"13. Kоличество: {self.citizen_data['products_detail']}\n" \
                                   f"14. Средства личной гигиены: {self.citizen_data['gigien']}\n" \
                                   f"15. Kоличество {self.citizen_data['gigien_num']}\n" \
                                   f"16. Памперсы: {self.citizen_data['pampers']}\n" \
                                   f"17. Особенности диеты и т.п.: {self.citizen_data['diet']}\n" \
                                   f"18. Cогласие на обработку персональных данных: {self.citizen_data['pers_data_agreement']} \n" \
                                   f"19. Cогласие на фото/видео: {self.citizen_data['photo_agreement']}\n"
            send_message(url, self._id, text_to_send)
            keys = ['Сохранить', 'Изменить', 'Начать сначала']
            text = f'Что дальше?'
            send_keyboard(self._id, keys, text, bot)
            self.round += 1
            return
            # log(user_text)
        if self.round == 21:
            # if user_text == 'Просмотреть':
            #     text_to_send = 'You data'
            #     send_message(url, self._id, text_to_send)
            # mycol = mydb["people"]
            citizenDataToCSV = [self.citizen_data]
            print(citizenDataToCSV)
            citizenDataToDb = self.citizen_data
            write_to_base(citizenDataToDb)
            write_to_csv(citizenDataToCSV)
            text_to_send = str(self.citizen_data)
            # send_message(url, self._id, text_to_send)
            # try:
            #     mycol.insert_one(citizenDataToDb)
            # except:
            #     pass
            # log('line401')
            # log(citizenDataToDb)
            # text_to_send = str(citizenDataToDb)
            send_message(url, self._id, text_to_send)
            self.round += 1
            return
        # if self.round == 11:
        #     log('line 405')
        #     self.round += 1
        #     return


def write_to_base(citizenDataToDb):
    mycol = mydb["people"]
    try:
        mycol.insert_one(citizenDataToDb)
    except:
        pass


def write_to_csv(citizenDataToCSV):
    citizen_info = ['fio', 'phone', 'birth', 'addr', 'people_num', 'people_fio',
                    'invalids', 'children', 'children_age', 'food', 'drugs', 'water',
                    'products_detail', 'gigien', 'gigien_num', 'pampers', 'diet',
                    'pers_data_agreement', 'photo_agreement', 'birth_year', '_id']
    with open('citizens.csv', 'w') as file:
        writer = csv.DictWriter(file, fieldnames=citizen_info)
        writer.writeheader()
        writer.writerows(citizenDataToCSV)


@app.route('/helper2022', methods=['POST', 'GET'])
def helper2022():
    t = time.asctime()
    # log('line 381')
    if request.method == 'POST':
        # log('line_383')
        try:
            # log('line_385')
            r = request.get_json()
            req = str(r)
            log(t + 'line_427' + t)
            # log(str(get_chat_id(r)) + 'line 389')
            chat_id = get_chat_id(r)
            name = get_name(r)
            user_text = get_text(r)
            t = time.asctime()
        except:
            user_text = 'exception'
            # log(user_text)
        if chat_id not in id_list:
            id_list.append(chat_id)
            new_citizen = Citizen(chat_id, name)
            citizens[chat_id] = new_citizen
            citizen = new_citizen
            expirience = 'new'
        else:
            citizen = citizens[chat_id]
            # log_text = f'{citizen}'
            expirience = 'old'
        citizen.conversation(user_text)

    return f'<h1>Привет.Hi from helper2022 at {t} </h1>'


keys = ['AaA', 'BaB', 'CcC']
text = 'Hop-Hop'
if __name__ == '__main__':
    print(sys.version)
    print(time.asctime())
    # ff = jj
    app.run(debug=True, port=5000)
