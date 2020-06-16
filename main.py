from telebot import types
import telebot

from vedis import Vedis
import sqlite3

import dump_worker
import dbworker
import foto_worker
import config

import json
import time
import sys

from pprint import pprint

print('Попытка запуска')

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def get_start(message):
    print(message.chat.id,dbworker.get_current_state(message.chat.id))
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_start = types.KeyboardButton(text="Начать!")
    keyboard.add(button_start)
    phrase='Здравствуйте , я бот Starzap, помогу Вам найти и подобрать новые или б/у запчасти '
    bot.send_message(message.chat.id, phrase, reply_markup=keyboard)
    dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
    connection = sqlite3.connect(config.db_user_dataset)
    dump_worker.add_user(connection,message.chat.id)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START_EARNING.value)
def openMainMenu(message):
    print(message.chat.id,dbworker.get_current_state(message.chat.id))
    if (message.text == 'Начать!' or message.text == 'Вернуться в меню ⬅'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_earning = types.KeyboardButton(text="Найти запчати по каталогу 🚗")
        button_partners = types.KeyboardButton(text="Найти по vin (в разработке)")
        # button_options = types.KeyboardButton(text="Опции ⚙️")
        button_help = types.KeyboardButton(text="Помощь ❓")
        keyboard.add(button_earning, button_partners,button_help)
        bot.send_message(message.from_user.id, 'Выберите одно из предложенных действий', reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_CHOISE_METHOD.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CHOISE_METHOD.value)
def mainMenu(message): 
    print(message.chat.id,dbworker.get_current_state(message.chat.id))
    if (message.text== 'Вернуться в меню ⬅') :
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)
    # if (message.text == 'Опции ⚙️'):
    #     keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True,one_time_keyboard=True)
    #     button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
    #     btn_update = types.KeyboardButton(text="Обновить базу данных бота 🔨")
    #     keyboard.add(btn_update,button_back)
    #     bot.send_message(message.from_user.id,'Выбирете',reply_markup=keyboard)
    #     dbworker.set_state(message.chat.id,config.States.S_OPTION.value)
    if (message.text == 'Найти запчати по каталогу 🚗'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_back)
        bot.send_message(message.from_user.id,'Выбирете',reply_markup=keyboard)
        dbworker.set_state(message.chat.id,config.States.S_EASY_SEARCH.value)
        S_EASY_SEARCH(message)
    if (message.text == 'Найти по vin (в разработке)'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_back)
        phrase='''Данный раздел в стадии разработки'''
        bot.send_message(message.from_user.id, phrase,reply_markup=keyboard)
        dbworker.set_state(message.chat.id,config.States.S_VIN_SEARCH.value)
    if (message.text == 'Помощь ❓'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_back)
        bot.send_message(message.from_user.id, 'тут текст помощи', reply_markup=keyboard)
        pass

# @bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_OPTION.value)
# def option(message):
#     if message.text=='Вернуться в меню ⬅':
#         dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
#         openMainMenu(message)
#     if message.text=='Обновить базу данных бота 🔨':
#         bot.send_message(message.from_user.id, 'Обновляемся ...')
#         dump_worker.create_dump()
#         bot.send_message(message.from_user.id, 'Готово, наслаждайтесь использованием')
#         dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
#         message.text='Начать!'
#         openMainMenu(message)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_EASY_SEARCH.value)
def S_EASY_SEARCH(message):
    if message.text=='Вернуться в меню ⬅':
        connection = sqlite3.connect(config.db_user_dataset)
        dump_connection= sqlite3.connect(config.db_database_dump_file)
        dump_worker.user_chose_reset(connection,message.chat.id)
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)
    else:
        connection = sqlite3.connect(config.db_user_dataset)
        dump_connection= sqlite3.connect(config.db_database_dump_file)
        l=dump_worker.search_unic_data(connection,dump_connection,message.chat.id)
        keys=create_inline(l)
        bot.send_message(message.chat.id, "из списка: ", reply_markup=keys)
        # data=dump_worker.get_data()
        # keyboard=create_inline(data)
        # dbworker.set_chose(message.chat.id,1)
  
def create_inline(data):
    if max([len(i) for i in data])>10:
        shape=1
    else: shape=3
    shaper = lambda lst, sz: [lst[i:i+sz] for i in range(0, len(lst), sz)]
    data_shape= shaper(data,shape)
    keyboard = types.InlineKeyboardMarkup()
    for i in data_shape:
        btns=[]
        for j in i:
            callback_button = types.InlineKeyboardButton(text=j, callback_data=str(data.index(j)))
            btns.append(callback_button)
        keyboard.add(*btns)
    return keyboard

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        try:
            u_id=call.message.chat.id
            c = sqlite3.connect(config.db_user_dataset)
            d_c = sqlite3.connect(config.db_database_dump_file)
            # data=dump_worker.get_data()
            dump_worker.user_pik_append(c,u_id,dump_worker.chek_pik(c,d_c,u_id,int(call.data)))
            dump_worker.user_chose_update(c,u_id)
            unic=dump_worker.search_unic_data(c,d_c,u_id)
            if type(unic[0])==dict:
                bot.edit_message_text(chat_id=u_id, message_id=call.message.message_id, text='Вот то что мы сумели найти: ')
                for i in unic:
                    items=list(i.items())
                    up_str=''
                    for item in items:
                        if item[1]=='':
                            continue
                        else:
                            up_str=up_str+item[0]+': '+item[1]+'\n'
                    bot.send_message(u_id,text=up_str)
                    foto_way=foto_worker.read_foto(u_id,i['photo'])
                    bot.send_photo(u_id,photo = open(foto_worker.create_way(foto_way), 'rb'))
                    foto_worker.delite_foto(foto_worker.create_way(foto_way))
                    # foto_worker.delite_foto(foto_way)
            elif unic[0]=='':
                bot.send_message(u_id,'Для этой модели/категории пока ничего нет, попробуйте позже или свяжитесь с нами')
                dump_worker.user_chose_reset(с,u_id)
                dbworker.set_state(u_id, config.States.S_START_EARNING.value)
            else:
                key=create_inline(unic)
            bot.edit_message_text(chat_id=u_id, message_id=call.message.message_id, text='из списка:',reply_markup=key)
        except:
            bot.send_message(call.message.chat.id,text='что-то пошло не так нажмите "Вернуться в меню"')

        

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_VIN_SEARCH.value)
def S_VIN_SEARCH(message):    
    if message.text=='Вернуться в меню ⬅':
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)

print('Запущенно')



def main():
    # ADMIN_MODE= False
    bot.infinity_polling(True)
    # bot.polling(none_stop=True, interval=0)
    # while True:
    #     try:
    #         bot.infinity_polling(True)
    #     except :
    #         bot.send_message(446387634, 'БОТ УПАЛ')
    #         bot.send_message(446387634, '{}'.format(sys.exc_info()[0]))
    #         time.sleep(1)


if __name__ == '__main__':
    main()