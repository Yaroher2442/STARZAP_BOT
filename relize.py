from telebot import types
import telebot
from vedis import Vedis
import json
import dbworker
import config
import phrases
import methods
import tests
import tasks
import config

print('Попытка запуска relise')

bot = telebot.TeleBot(config.token_test)

ADMIN_MODE = False

def set_A_mode(mode):
    global ADMIN_MODE
    ADMIN_MODE=mode
    return ADMIN_MODE
def get_A_mode():
    global ADMIN_MODE
    return ADMIN_MODE

for_change_var=['mode',0]
def set_change_var_mode(num,mode=None):
    global for_change_var
    for_change_var[0]=num
    for_change_var[1]=mode
    return for_change_var
def get_change_var_mode():
    global for_change_var
    return for_change_var[0],for_change_var[1]

@bot.message_handler(commands=['admin'])
def admin_setings(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_exit = types.KeyboardButton(text="/exit_admin")
    keyboard.add(button_exit)
    set_A_mode(True)
    bot.send_message(message.chat.id, "Admin режим ок! type a password",reply_markup=keyboard)


@bot.message_handler(commands=['exit_admin'])
def exit_admin(message):
    bot.send_message(message.chat.id, "/exit_admin ok!")
    set_A_mode(False)
    get_start(message)

@bot.message_handler(func=lambda message: message.text == config.admin_pass,content_types=["text"])
def pass_chek_true(message):
    if get_A_mode()==True:
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_tasks = types.KeyboardButton(text="Показать задачи")
        button_exit = types.KeyboardButton(text="/exit_admin")
        keyboard.add(button_tasks,button_exit)
        bot.send_message(message.chat.id, "Password ок!",reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_ADMIN.value)
        print('password sucsess')
    else :
        get_start(message)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ADMIN.value and get_A_mode()==True)
def Admin_work(message):
    print(dbworker.get_current_state(message.chat.id))        
    if (message.text == 'Показать задачи' or 'Назад'):
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True,one_time_keyboard=True)
        button_edit = types.KeyboardButton(text="Изменить одну из задач")
        button_del = types.KeyboardButton(text="Удалить одну из задач")
        button_add = types.KeyboardButton(text="Добавть новую задачу")
        button_exit = types.KeyboardButton(text="/exit_admin")
        keyboard.add(button_edit,button_del,button_add,button_exit)
        obj=tasks.Task_worker()
        mes=[i[0]+'-'+i[1]+' \n '+i[2]+' \n ' for i in obj.show_list()]
        bot.send_message(message.chat.id, 'ЗАДАЧИ: \n'+''.join(mes),reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_ADMIN_TASKS_SETTINGS.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ADMIN_TASKS_SETTINGS.value and get_A_mode()==True)
def Admin_task_settigs(message):
    print(dbworker.get_current_state(message.chat.id))
    if (message.text == 'Назад'):
        dbworker.set_state(message.chat.id, config.States.S_ADMIN.value)
        Admin_work(message)
    if (message.text == 'Изменить одну из задач'):
        obj=tasks.Task_worker()
        keyboard = types.ReplyKeyboardMarkup(row_width=2 ,resize_keyboard=True,one_time_keyboard=True)
        lst_btn=[types.KeyboardButton(text='№ '+str(i[0])) for i in obj.show_list()]
        button_back = types.KeyboardButton(text="Назад")
        keyboard.add(*lst_btn,button_back)
        mes=[i[0]+'-'+i[1]+' \n '+i[2]+' \n ' for i in obj.show_list()]
        bot.send_message(message.chat.id, 'Какую задачу изменить? \n' +''.join(mes),reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_ADMIN_TASK_CHANGE.value)
    if (message.text == 'Удалить одну из задач'):
        obj=tasks.Task_worker()
        keyboard = types.ReplyKeyboardMarkup(row_width=2 ,resize_keyboard=True,one_time_keyboard=True)
        lst_btn=[types.KeyboardButton(text='№ '+str(i[0])) for i in obj.show_list()]
        button_back = types.KeyboardButton(text="Назад")
        keyboard.add(*lst_btn,button_back)
        mes=[i[0]+'-'+i[1]+' \n '+i[2]+' \n ' for i in obj.show_list()]
        bot.send_message(message.chat.id, 'Какую задачу Удалить? \n' +''.join(mes),reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_ADMIN_TASK_DELITE.value)
    if (message.text == 'Добавть новую задачу'):
        obj=tasks.Task_worker()
        print('add')
        dbworker.set_state(message.chat.id, config.States.S_ADMIN_TASK_ADD_text.value)
        keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True,one_time_keyboard=True)
        keyboard.add(types.KeyboardButton(text="Назад"))
        bot.send_message(message.chat.id, 'Введите текст задачи:',reply_markup=keyboard)
        Admin_task_add(message)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ADMIN_TASK_CHANGE.value and get_A_mode()==True)
def Admin_task_change(message):
    print(dbworker.get_current_state(message.chat.id))
    if (message.text == 'Назад'):
        dbworker.set_state(message.chat.id, config.States.S_ADMIN.value)
        Admin_work(message)
    if ('№' in  message.text) :
        keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True,one_time_keyboard=True)
        btn_text=types.KeyboardButton(text="Текст")
        btn_url=types.KeyboardButton(text="Ссылку")
        btn_key=types.KeyboardButton(text="Key")
        btn_back=types.KeyboardButton(text="Назад")
        keyboard.add(btn_text,btn_url,btn_key,btn_back)
        obj=tasks.Task_worker()
        cur_task=obj.show_cur_task(message.text.split(' ')[1])
        bot.send_message(message.chat.id, "Что меняем? \n" +'\n'.join(cur_task),reply_markup=keyboard)
        set_change_var_mode(cur_task[0],'mode')
    if (message.text ==  "Текст"):
        num,mode=get_change_var_mode()
        set_change_var_mode(num,mode='text')
        keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True,one_time_keyboard=True)
        btn_back=types.KeyboardButton(text="Назад")
        keyboard.add(btn_back)
        meta=getattr(dbworker, 'get_{}'.format(list(get_change_var_mode()).pop(1)))
        meta_str=meta(list(get_change_var_mode()).pop(0))
        bot.send_message(message.chat.id, 'Меняем {} на :'.format(meta_str),reply_markup=keyboard)
        set_change_var_mode(num,mode='mode_change')
    elif (message.text ==  "Ссылку"):
        num,mode=get_change_var_mode()
        set_change_var_mode(num,mode='url')
        keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True,one_time_keyboard=True)
        btn_back=types.KeyboardButton(text="Назад")
        keyboard.add(btn_back)
        meta=getattr(dbworker, 'get_{}'.format(list(get_change_var_mode()).pop(1)))
        meta_str=meta(list(get_change_var_mode()).pop(0))
        bot.send_message(message.chat.id, 'Меняем {} на :'.format(meta_str),reply_markup=keyboard)
        set_change_var_mode(num,mode='mode_change')
    elif (message.text ==  "Key"):
        num,mode=get_change_var_mode()
        set_change_var_mode(num,mode='key')
        keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True,one_time_keyboard=True)
        btn_back=types.KeyboardButton(text="Назад")
        keyboard.add(btn_back)
        meta=getattr(dbworker, 'get_{}'.format(list(get_change_var_mode()).pop(1)))
        meta_str=meta(list(get_change_var_mode()).pop(0))
        bot.send_message(message.chat.id, 'Меняем {} на :'.format(meta_str),reply_markup=keyboard)
        set_change_var_mode(num,mode='mode_change')
    elif (message.text ==  "Верно"):
        bot.send_message(message.chat.id, 'Изменено')
        dbworker.set_state(message.chat.id, config.States.S_ADMIN.value)
        Admin_work(message)
    elif (get_change_var_mode()[1] == 'mode_change' and message.text not in ["Верно","Текст","Ссылку","Key",'Назад']):
        keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True,one_time_keyboard=True)
        btn_confirm=types.KeyboardButton(text="Верно")
        btn_back=types.KeyboardButton(text="Назад")
        keyboard.add(btn_confirm,btn_back)
        bot.send_message(message.chat.id, message.text+' верно?',reply_markup=keyboard)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_ADMIN_TASK_DELITE.value and get_A_mode()==True)
def Admin_task_del(message):
    print(dbworker.get_current_state(message.chat.id))
    if (message.text == 'Назад'):
        dbworker.set_state(message.chat.id, config.States.S_ADMIN.value)
        Admin_work(message)
    state=dbworker.get_current_state(message.chat.id)
    if ('№' in  message.text) :
        keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True)
        btn_confirm=types.KeyboardButton(text="Да")
        btn_back=types.KeyboardButton(text="Назад")
        keyboard.add(btn_confirm,btn_back)
        bot.send_message(message.chat.id, "Выбран {} Уверены ?".format(message.text),reply_markup=keyboard)
    if (message.text == 'Да'):
        bot.send_message(message.chat.id, "Удалено")
        Admin_work(message)


@bot.message_handler(func=lambda message: (dbworker.get_current_state(message.chat.id) == config.States.S_ADMIN_TASK_ADD.value
                                                                                        or config.States.S_ADMIN_TASK_ADD_text.value
                                                                                        or config.States.S_ADMIN_TASK_ADD_url.value
                                                                                        or config.States.S_ADMIN_TASK_ADD_key.value) 
                                                                                        and get_A_mode()==True)
def Admin_task_add(message):
    print(dbworker.get_current_state(message.chat.id))
    def keyboard_gen():
        keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True)
        btn_confirm=types.KeyboardButton(text="Верно")
        btn_unconfirm=types.KeyboardButton(text="Не верно")
        btn_back=types.KeyboardButton(text="Назад")
        keyboard.add(btn_confirm,btn_unconfirm,btn_back)
        return keyboard
    if (message.text == 'Назад'):
        dbworker.set_state(message.chat.id, config.States.S_ADMIN.value)
        Admin_work(message)
    else:
        state=dbworker.get_current_state(message.chat.id)
        if state == config.States.S_ADMIN_TASK_ADD_text.value:
            if message.text == 'Верно':
                dbworker.set_state(message.chat.id, config.States.S_ADMIN_TASK_ADD_url.value)
                # obj=tasks.Task_worker()
                keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True,one_time_keyboard=True)
                keyboard.add(types.KeyboardButton(text="Назад"))
                bot.send_message(message.chat.id, 'Введите ссылку  задачи:',reply_markup=keyboard)
                message.text='Введите ссылку  задачи:'
                Admin_task_add(message)
            elif message.text == 'Не верно':
                bot.send_message(message.chat.id, 'Введите текст ещё раз :')
            elif message.text != 'Добавть новую задачу' and  message.text != 'Введите текст задачи:':
                bot.send_message(message.chat.id, message.text+' - Верно ?',reply_markup=keyboard_gen())

        if state == config.States.S_ADMIN_TASK_ADD_url.value:           
            if message.text == 'Верно':
                dbworker.set_state(message.chat.id, config.States.S_ADMIN_TASK_ADD_key.value)
                # obj=tasks.Task_worker()
                keyboard = types.ReplyKeyboardMarkup(row_width=1 ,resize_keyboard=True,one_time_keyboard=True)
                keyboard.add(types.KeyboardButton(text="Назад"))
                bot.send_message(message.chat.id, 'Введите key  задачи:',reply_markup=keyboard)
                message.text='Введите key задачи:'
                Admin_task_add(message)
            elif message.text == 'Не верно':
                bot.send_message(message.chat.id, 'Введите url ещё раз :')
            elif message.text != 'Введите ссылку  задачи:':
                bot.send_message(message.chat.id, message.text+' - Верно ?',reply_markup=keyboard_gen())

        if state == config.States.S_ADMIN_TASK_ADD_key.value:
            if message.text == 'Верно':
                dbworker.set_state(message.chat.id, config.States.S_ADMIN_TASK_ADD.value)
                obj=tasks.Task_worker()
                bot.send_message(message.chat.id, 'Добавлено')
                message.text='Назад'
                Admin_task_add(message)
            elif message.text == 'Не верно':
                bot.send_message(message.chat.id, 'Введите url ещё раз :')
            elif message.text != 'Введите key задачи:':
                bot.send_message(message.chat.id, message.text+' - Верно ?',reply_markup=keyboard_gen())
    
'''------------------------------------------------------------------------------------------------------------------------------------------'''

@bot.message_handler(commands=['start'])
def get_start(message):
    set_A_mode(False)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_startCashing = types.KeyboardButton(text="Начать зарабатывать 💴")
    keyboard.add(button_startCashing)
    bot.send_message(message.chat.id, phrases.welcomeMessage, reply_markup=keyboard)
    dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)

@bot.message_handler(commands=['reset'])
def bot_reset(message):
    bot.send_message(message.chat.id, "Настройки сброшены, введите /start")
    dbworker.set_state(message.chat.id, config.States.S_START.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_START_EARNING.value)
def openMainMenu(message):
    print('lol')
    if (message.text == 'Начать зарабатывать 💴' or message.text == 'Вернуться в меню ⬅'):
        state = dbworker.get_current_state(message.chat.id)
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_earning = types.KeyboardButton(text="Заработать 🤑")
        button_partners = types.KeyboardButton(text="Партнёры 👥")
        button_balance = types.KeyboardButton(text="Счет 💰")
        button_help = types.KeyboardButton(text="Помощь ❓")
        keyboard.add(button_earning, button_partners, button_balance, button_help)
        bot.send_message(message.from_user.id, 'Выберите одно из предложенных действий', reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_CHOISE_METHOD.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CHOISE_METHOD.value)
def mainMenu(message):  

    if (message.text == 'Заработать 🤑'):

        if (dbworker.get_choosen_task(message.chat.id) == config.Default_Values.D_CHOOSE.value):
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
            keyboard.add(button_back)
        else:
            keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
            button_done = types.KeyboardButton(text="Выполнено")
            button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
            keyboard.add(button_back, button_done)

        if (dbworker.get_choosen_task(message.chat.id) == config.Default_Values.D_CHOOSE.value):

            tasks       =   methods.Task_page(message.chat.id)
            if (tasks != config.Default_Values.D_TASK.value):
                bot.send_message(message.from_user.id, 'Выберите задание', reply_markup=keyboard)
                for i in range(0,len(tasks)):
                    bot.send_message(message.from_user.id, str(i+1) + ') ' + dbworker.get_text(tasks[i][1]), reply_markup=keyboard)
            else:
                bot.send_message(message.from_user.id, tasks, reply_markup=keyboard)
        else:
            full_task   =   methods.Choosen_task(message.chat.id,dbworker.get_choosen_task(message.chat.id))
                
            if (full_task != config.Default_Values.D_CORRECT.value):

                full_task[0]    += ' ' + full_task[1]
                full_task[1]    =   message.text

            print(full_task)
            bot.send_message(message.from_user.id, full_task, reply_markup=keyboard)
        
        dbworker.set_state(message.chat.id, config.States.S_EARNING.value)

    if (message.text == 'Партнёры 👥'):

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_back)  

        bot.send_message(message.from_user.id, 'страница партнёры', reply_markup=keyboard)
        bot.send_message(message.from_user.id, 'количество партнеров: ' + dbworker.get_partners_count(message.chat.id), reply_markup=keyboard)
        bot.send_message(message.from_user.id, 'прибыль от партнеров: ' + dbworker.get_partners_profit(message.chat.id), reply_markup=keyboard)
        bot.send_message(message.from_user.id, 'ваш партнерский ключ: ' + str(message.chat.id), reply_markup=keyboard)
        bot.send_message(message.from_user.id, 'если хотите стать партнером введите ключ ', reply_markup=keyboard)

        dbworker.set_state(message.chat.id, config.States.S_PARTNERS.value)

    if (message.text == 'Счет 💰'):

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_back)

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_balance = types.KeyboardButton(text="Баланс 💰")
        button_cashout = types.KeyboardButton(text="Вывод 🤑")
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_balance, button_cashout,button_back)
        bot.send_message(message.from_user.id, 'страница счета', reply_markup=keyboard)
        bot.send_message(message.from_user.id, 'Выберите одно из предложенных действий', reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_CASH.value)
    
    if (message.text == 'Помощь ❓'):

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_back)

        dbworker.set_state(message.chat.id, config.States.S_GETHELP.value)
        bot.send_message(message.from_user.id, 'страница помощи', reply_markup=keyboard)

    print(dbworker.get_current_state(message.chat.id))

"""func listening in start earning page"""
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_EARNING.value)
def startEarning(message):

    if (message.text == 'Вернуться в меню ⬅'):
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)
    else:

        if (dbworker.get_choosen_task(message.chat.id) == config.Default_Values.D_CHOOSE.value):
            if (message.text.isdigit()):
                full_task   =   methods.Choosen_task(message.chat.id,message.text)
                    
                if (full_task != config.Default_Values.D_CORRECT.value):

                    full_task[0]    += ' ' + full_task[1]
                    full_task[1]    =   message.text

                    dbworker.set_choosen_task(message.chat.id, full_task[2])
                    message.text = 'Заработать 🤑'
                    dbworker.set_state(message.chat.id, config.States.S_CHOISE_METHOD.value)
                    mainMenu(message)

                print(full_task)

            else:
                
                bot.send_message(message.from_user.id, config.Default_Values.D_CORRECT.value)

        else:
            print(bot.get_chat_member( str(dbworker.get_key(dbworker.get_choosen_task(message.chat.id))),message.chat.id))
            try:
                chat_message    =   bot.get_chat_member( str(dbworker.get_key(dbworker.get_choosen_task(message.chat.id))),message.chat.id).status #dbworker.get_key(dbworker.get_choosen_task(message.chat.id))
            except:
                chat_message    =   "not member"

            print (chat_message)

            if (chat_message == "member"):

                dbworker.del_task_id(message.chat.id,dbworker.get_choosen_task(message.chat.id))
                dbworker.del_choosen_task(message.chat.id)

                dbworker.set_user_cash(message.chat.id, str(int(dbworker.get_user_cash(message.chat.id)) + int(config.Default_Values.D_TASK_COST.value)))

                bot.send_message(message.from_user.id, "Подпика подтверждена")
                bot.send_message(message.from_user.id, "Получено " + config.Default_Values.D_TASK_COST.value + " " + config.Default_Values.D_CURRENCY.value)

                partner                                 =   dbworker.get_partner(message.chat.id)

                dbworker.set_user_cash(partner, str(int(dbworker.get_user_cash(partner)) + int(config.Default_Values.D_TASK_PARTCOST.value)))
                dbworker.set_partners_profit(partner, str(int(dbworker.get_user_cash(partner)) + int(config.Default_Values.D_TASK_PARTCOST.value)))

            else:

                bot.send_message(message.from_user.id, 'Подписка не выполнена')

        


"""func listening in partners page"""
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_PARTNERS.value)
def startEarning(message):
    if (message.text == 'Вернуться в меню ⬅'):
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)
    else:
        if (message.text.isdigit()):

            if (int(message.text) != message.from_user.id):

                if (dbworker.set_partner(message.from_user.id,message.text)):

                    bot.send_message(message.from_user.id, 'партнер добавлен')
                    dbworker.set_partners_count(message.text, str(int(dbworker.get_partners_count(message.text)) + 1))
                    dbworker.set_user_cash(message.from_user.id, str(int(dbworker.get_user_cash(message.from_user.id)) + int(config.Default_Values.D_REF_CASH.value)))
                    print (dbworker.get_partners_count(message.text))

                else:
                    bot.send_message(message.from_user.id, config.Default_Values.D_CORRECT.value)

            else:
                bot.send_message(message.from_user.id, config.Default_Values.D_CORRECT.value)

        else:
            bot.send_message(message.from_user.id, config.Default_Values.D_CORRECT.value)

"""func listening in balance page"""
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_BALANCE.value)
def startEarning(message):
    if (message.text == 'Вернуться в меню ⬅'):
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)

"""func listening in getting help page"""
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_GETHELP.value)
def startEarning(message):
    if (message.text == 'Вернуться в меню ⬅'):
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)

"""func listening in getting cash"""
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_CASH.value)
def startEarning(message):
    if (message.text == 'Вернуться в меню ⬅'):
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)
    if (message.text == 'Баланс 💰'):
        
        bot.send_message(message.from_user.id, methods.Balance_page(message.chat.id))

    if (message.text == 'Вывод 🤑'):
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_balance = types.KeyboardButton(text="Qiwi")
        button_cashout = types.KeyboardButton(text="Steam")
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_balance, button_cashout,button_back)
        bot.send_message(message.from_user.id, 'страница вывода', reply_markup=keyboard)
        bot.send_message(message.from_user.id, 'Выберите одно из предложенных действий', reply_markup=keyboard)
        dbworker.set_state(message.chat.id, config.States.S_OUT.value)

"""func listening in getting out"""
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_OUT.value)
def startEarning(message):
    if (message.text == 'Вернуться в меню ⬅'):
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)

    if (message.text == 'Steam'):
        bot.send_message(message.from_user.id, 'данный раздел пока в разработке')
        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_back)


    if (message.text == 'Qiwi'):

        keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        button_back = types.KeyboardButton(text="Вернуться в меню ⬅")
        keyboard.add(button_back)
        
        bot.send_message(message.from_user.id, 'введите количество '+config.Default_Values.D_CURRENCY.value+' для перевода и номер телефона( без 8 и через пробел )', reply_markup=keyboard)

        dbworker.set_state(message.chat.id, config.States.S_QIWI.value)

"""func listening in getting qiwi"""
@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == config.States.S_QIWI.value)
def startEarning(message):

    if (message.text == 'Вернуться в меню ⬅'):
        dbworker.set_state(message.chat.id, config.States.S_START_EARNING.value)
        openMainMenu(message)
    else:

        entering            =   message.text.split()

        try:
            bot.send_message(message.from_user.id, methods.Out(message.chat.id,entering[0],entering[1]))
        except:
            bot.send_message(message.from_user.id, 'введено не коректное значение, повторите ввод')



#tests.db_test()

print('relise')

def main():
    ADMIN_MODE= False
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()