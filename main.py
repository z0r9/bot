#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
import id, const
import logging, pickle, os.path, random
# remove
import time
# /remove

# logging on, loglevel = debug
logging.basicConfig(filename='bot.log', level=logging.DEBUG)
# init bot
bot = telebot.TeleBot(id.token)
# log
logging.debug(u"выполнена инициализация бота с токеном id.token")
# order counter
i = 1
# init order
order = list()
# step
step = 0
# done - id
done = 0

# load stored in file values
if os.path.exists(const.store):
    f = open(const.store, 'rb')
    i, order = pickle.load(f)
    # log
    logging.debug(u"прочитан файл с сохраненными значениями i и order")

# print bot.get_webhook_info(timeout=None)

# log bot info after start
logging.info(u"Bot profile is: {0}".format(bot.get_me()))

# logging messages
# logging.debug('This message should go to the log file')
# logging.info('So should this')
# logging.warning('And this, too')

# eventlog
def message2log(comment, msg):
    from datetime import datetime
    # log comment
    logging.info(u"{0} {1}".format(datetime.now(), comment))
    # log message
    logging.info(u"{0} message from {1} {2} (id = {3}) command: {4}".format(datetime.now(),
                                                                             msg.from_user.first_name,
                                                                             msg.from_user.last_name,
                                                                             msg.from_user.id,
                                                                             msg.text))

# replace value
def replace(dic, id, key, val):
    for l in dic:
        if l['id'] == id:
            l[key] = val


# find value
def find(dic, index, id, key):
    for l in dic:
        if l[index] == id:
            return l[key]


# bot commands

# /start
@bot.message_handler(commands=['start'])
def handle_text(message):
    # check blacklist
    # TODO check is userid in blacklist
    # sending hello message and shop logo
    bot.send_message(message.chat.id, u"Вас приветствует магазин Ёлки")
    # log message
    message2log(u"", message)
    # display gif
    bot.send_document(message.chat.id, const.gif)
    # log display
    message2log(u"", message)
    # show agenda
    bot.send_message(message.chat.id, u"читаем отзывы, правила и прочее")
    # changing keyboard for choosing city
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    # filling cities
    user_markup.row(const.command_city[0], const.command_city[1])
    # adding main menu command
    user_markup.row(const.command_review, const.command_rules, const.command_help)
    # sending message, image and keyboard to user
    bot.send_message(message.chat.id, u"выбери город, товар и покупай ...", reply_markup=user_markup)
    # filling order ... adding user id to order
    order.append(
        {'id': message.from_user.id, 'status': '', 'city': '', 'goods': '', 'value': '', 'sum': '', 'order': ''})


# /stop
@bot.message_handler(commands=['stop'])
def handle_text(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True);
    bot.send_message(message.chat.id, u"пока ... /start", reply_markup=hide_markup)


# /help
@bot.message_handler(commands=['help'])
def handle_text(message):
    bot.send_message(message.chat.id, u"выбери опцию покупка ...")


# chat message
@bot.message_handler(content_types=['text'])
def handle_text(message):
    global i
    global order
    global step, done
    # rules
    if message.text == const.command_rules:
        bot.send_message(message.chat.id, u"выбираем, оплачиваем, получаем ...")
        message2log(u"правила", message)
    # back
    elif message.text == const.command_back:
        # going back one step
        bot.send_message(message.chat.id, u"возвращаемся на шаг назад ...")
        # backward one step
        step -= 1
        # log message
        message2log(u"возврат назад", message)
    # begin
    elif message.text == const.command_menu:
        # return to begining
        bot.send_message(message.chat.id, u"возвращаемся в начало ...")
        # goto first step
        step = 0
        # log message
        message2log(u"возврат в меню", message)
    # review
    elif message.text == const.command_review:
        # display reviews
        bot.send_message(message.chat.id, u"отзывы тут")
        # log message
        message2log(u"отзывы", message)
    # city selection check
    elif message.text in const.command_city:
        # insert city in the order
        replace(order, message.from_user.id, 'city', message.text)
        # goto product selection step
        step = 1
        # log message
        message2log(u"выбор города", message)
    # goods selection check
    elif message.text in const.command_goods:
        # insert goods in the order
        replace(order, message.from_user.id, 'goods', message.text)
        # goto value selection step
        step = 2
        # log message
        message2log(u"выборан товар", message)
    elif message.text in const.command_g_value or message.text in const.command_t_value:
        replace(order, message.from_user.id, 'value', message.text)
        # TODO replace with good alorithm
        # filling sum
        if message.text == const.command_g_value[0]:
            replace(order, message.from_user.id, 'sum', 1500)
        elif message.text == const.command_g_value[1]:
            replace(order, message.from_user.id, 'sum', 3000)
        elif message.text == const.command_g_value[2]:
            replace(order, message.from_user.id, 'sum', 4500)
        elif message.text == const.command_g_value[3]:
            replace(order, message.from_user.id, 'sum', 6000)
        elif message.text == const.command_t_value[0]:
            replace(order, message.from_user.id, 'sum', 4000)
        elif message.text == const.command_t_value[1]:
            replace(order, message.from_user.id, 'sum', 6000)
        elif message.text == const.command_t_value[2]:
            replace(order, message.from_user.id, 'sum', 8000)
        elif message.text == const.command_t_value[3]:
            replace(order, message.from_user.id, 'sum', 10000)
        # goto chechout step
        step = 3
        # log message
        message2log(u"выбран размер", message)
    elif message.text == const.command_checkout:
        replace(order, message.from_user.id, 'order', str(i))
        step = 4
        i += 1
        # saving orders and index
        with open(const.store, 'wb') as f:
            pickle.dump([i, order], f)
        message2log(u"оформление заказа", message)
        logging.debug(order)
    elif message.text == "@" and str(message.from_user.id) == id.boss:
        bot.send_message(message.chat.id, u"hi, master")
        # statistics
        message2log(u"¿cómo está el jefe?", message)
    elif message.text == "!" and ((str(message.from_user.id) == id.operator1) or
                                      (str(message.from_user.id) == id.operator2)):
        # goto selection order number step
        step = 10
        # prepare keyboard to enter order number
        hide_markup = telebot.types.ReplyKeyboardRemove(True);
        # sending message to operator
        bot.send_message(message.chat.id, u"введи номер заказа", reply_markup=hide_markup)
        # log message
        message2log(u"выбор заказа оператором", message)
    else:
        if ((str(message.from_user.id) == id.operator1) or
                (str(message.from_user.id) == id.operator2)) and step == 10:
            bot.send_message(message.chat.id, u"введи адрес")
            step = 11
        elif ((str(message.from_user.id) == id.operator1) or
                  (str(message.from_user.id) == id.operator2)) and step == 11:
            step = 12
        else:
            # invalid input
            bot.send_message(message.chat.id, u"прочитай раздел помощь ...")
            # log user message
            message2log(u"некорректный ввод, вывод раздела с помощью", message)
    #
    #
    # choosing city
    if step == 0:
        # changing keyboard
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # filling cities
        user_markup.row(const.command_city[0], const.command_city[1])
        # adding main menu commands
        user_markup.row(const.command_review, const.command_rules, const.command_help)
        # sending message and request user action
        bot.send_message(message.chat.id, u"выбирай город и покупай ...", reply_markup=user_markup)

    # choosing goods
    elif step == 1:
        # change keyboard
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # filling goods positions
        user_markup.row(const.command_goods[0], const.command_goods[1])
        # adding main menu commands
        user_markup.row(const.command_back, const.command_rules, const.command_help)
        # show current cart options
        bot.send_message(message.chat.id, u"-- заказ --\n"
                                          u"город: {0}\n"
                                          u"-- ... --".format(find(order, 'id', message.from_user.id, 'city')))
        # sending message and request user action
        bot.send_message(message.chat.id, u"выбери наименование ...", reply_markup=user_markup)

    # choosing conditions for first goods
    elif step == 2 and find(order, 'id', message.from_user.id, 'goods') == const.command_goods[0]:
        # prepare keyboard for change
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # filling goods conditions
        user_markup.row(const.command_g_value[0], const.command_g_value[1])
        user_markup.row(const.command_g_value[2], const.command_g_value[3])
        # adding main menu commands
        user_markup.row(const.command_back, const.command_rules, const.command_help)
        # show current cart options
        bot.send_message(message.chat.id, u"-- заказ --\n"
                                          u"город: {0}\n"
                                          u"товар: {1}\n"
                                          u"-- ... --".format(find(order, 'id', message.from_user.id, 'city'),
                                                              find(order, 'id', message.from_user.id, 'goods')))
        # sending message and request user action
        bot.send_message(message.chat.id, u"выбери размер ...", reply_markup=user_markup)

    # choosing conditions for second goods
    elif step == 2 and find(order, 'id', message.from_user.id, 'goods') == const.command_goods[1]:
        # prepare keyboard for change
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # filling goods conditions
        user_markup.row(const.command_t_value[0], const.command_t_value[1])
        user_markup.row(const.command_t_value[2], const.command_t_value[3])
        # adding main menu commands
        user_markup.row(const.command_back, const.command_rules, const.command_help)
        # show current cart options
        bot.send_message(message.chat.id, u"-- заказ --\n"
                                          u"город: {0}\n"
                                          u"товар: {1}\n"
                                          u"-- ... --".format(find(order, 'id', message.from_user.id, 'city'),
                                                              find(order, 'id', message.from_user.id, 'goods')))
        # sending message and request user action
        bot.send_message(message.chat.id, u"выбери размер ...", reply_markup=user_markup)

    # checkout
    elif step == 3:
        # prepare keyboard for change
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # filling checkout key
        user_markup.row(const.command_menu, const.command_checkout)
        # adding main menu commands
        user_markup.row(const.command_back, const.command_rules, const.command_help)
        # show current cart options
        bot.send_message(message.chat.id, u"-- заказ --\n"
                                          u"город: {0}\n"
                                          u"товар: {1}\n"
                                          u"размер: {2}\n"
                                          u"к оплате: {3} руб.\n"
                                          u"-- ... --".format(find(order, 'id', message.from_user.id, 'city'),
                                                              find(order, 'id', message.from_user.id, 'goods'),
                                                              find(order, 'id', message.from_user.id, 'value'),
                                                              str(find(order, 'id', message.from_user.id, 'sum'))))
        # sending message and request user action
        bot.send_message(message.chat.id, u"оформление заказа ...", reply_markup=user_markup)

    # sending order to operator
    elif step == 4:
        match = next((l for l in order if l['id'] == message.from_user.id), None)
        bot.send_message(message.chat.id, u"заказ № {0} в {1} на {2} {3} к оплате {4} руб.".format(
            match['order'],
            match['city'],
            match['goods'],
            match['value'],
            match['sum']))
        bot.send_message(message.chat.id, u"оплату необходимо произвести на кошелек\n"
                                          u"qiwi {0} или\n"
                                          u"yandex {1}\n"
                                          u"указав в комментарии № заказа".format(random.choice(const.q_wallets),
                                                                                  random.choice(const.y_wallets)))
        if find(order, 'id', message.from_user.id, 'city') == const.command_city[0]:
            id_oper = id.operator1
        else:
            id_oper = id.operator2

        bot.send_message(id_oper, u"{0} {1} id({2}) заказ № {3} в {4} на {5} {6} стоимостью {7} руб.".format(
            message.from_user.first_name,
            message.from_user.last_name,
            str(message.from_user.id),
            match['order'],
            match['city'],
            match['goods'],
            match['value'],
            match['sum']))
        message2log(u"заказ № {0} в {1} на {2} {3} стоимостью {4} руб.".format(
            match['order'],
            match['city'],
            match['goods'],
            match['value'],
            match['sum']), message)
        hide_markup = telebot.types.ReplyKeyboardRemove(True);
        bot.send_message(message.chat.id, u"для повторной покупки /start ...", reply_markup=hide_markup)
        # clear step for next order
        step = 0

    # operator`s mode
    elif step == 10:
        logging.debug(u"шаг {0}".format(str(step)))

    # operator set order that was payed
    elif step == 11:
        # search order id for completing
        done = find(order, 'order', message.text, 'id')
        # set order status complete
        replace(order, done, 'status', "done")
        # log
        logging.debug(u"шаг {0}, id = {1}".format(str(step), done))
    #
    elif step == 12:
        bot.send_message(done, u"по вашему заказу поступила оплата")
        bot.send_message(done, u"адрес получения: {0} ".format(message.text))
        step = 0
    #
    else:
        bot.send_message(message.chat.id, u"какая-то фигня ...")


bot.polling(none_stop=True, interval=0)
# this is the end.
