#!/usr/bin/python
# -*- coding: utf-8 -*-

import telebot
import id, const
# remove
import time
# /remove

# init
bot = telebot.TeleBot(id.token)
# order counter
i = 1
# order
order = list()
# step
step = 0
done = 0

#print bot.get_webhook_info(timeout=None)

# bot info
print ("Bot profile is: {0}".format(bot.get_me()))

# eventlog
def log(question, answer):
    from datetime import datetime
    print ("\n---{0}---".format(datetime.now()))
    print(u"Message from {0} {1} (id = {2})\nCommand: {3}".format(question.from_user.first_name,
                                                                question.from_user.last_name,
                                                                str(question.from_user.id),
                                                                question.text))
    print(u"Comment: {0}".format(answer))

# replace value
def replace(dic, id, key ,val):
    for l in dic:
        if l['id'] == id:
            l[key] = val
# find value
def find(dic, index ,id, key):
    for l in dic:
        if l[index] == id:
            return l[key]

# bot commands

# /start
@bot.message_handler(commands=['start'])
def handle_text(message):
    # sending hello message and shop logo
    bot.send_message(message.chat.id, u"Вас приветствует магазин [Ёлки]({0})".format(const.logo), parse_mode="Markdown")
#    bot.send_photo(message.chat.id, "AgADAgADDqgxG-osSEvKHpohZmjRgblMtw0ABGXOtqSQDsEYa_QBAAEC")
#    bot.send_document(message.chat.id, "AAQEABOOUmEZAATpKMKLiH_i9HmCAgABAg")
    # changing keyboard for choosing city
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    # filling cities
    user_markup.row(const.command_city[0], const.command_city[1])
    # adding main menu command
    user_markup.row(const.command_review, const.command_rules, const.command_help)
    # sending message, image and keyboard to user
    bot.send_message(message.chat.id, u"Выбирай город и покупай ...", reply_markup=user_markup)
    # filling order ... adding user id to order
    order.append({'id':message.from_user.id, 'status':'', 'city':'', 'goods':'', 'value':'', 'sum':'', 'order':''})

# /stop
@bot.message_handler(commands=['stop'])
def handle_text(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True);
    bot.send_message(message.chat.id, u"пока ... /start", reply_markup=hide_markup)

# /help
@bot.message_handler(commands=['help'])
def handle_text(message):
        bot.send_message(message.chat.id,u"выбери опцию покупка ...")

# chat message
@bot.message_handler(content_types=['text'])
def handle_text(message):
    global i
    global order
    global step, done
    # rules
    if message.text == const.command_rules:
        bot.send_message(message.chat.id, u"выбираем, оплачиваем, получаем ...")
        log(message, u"правила просты ...")
    # back
    elif message.text == const.command_back:
        bot.send_message(message.chat.id, u"возвращаемся на шаг назад ...")
        step -= 1
        log(message, u"возвращаемся назад ...")
    # begin
    elif message.text == const.command_menu:
        bot.send_message(message.chat.id, u"возвращаемся в начало ...")
        step = 0
        log(message, u"возвращаемся назад ...")
    elif message.text == const.command_review:
        bot.send_message(message.chat.id, u"Отзывы о нас тут ...")
        log(message, u"возвращаемся назад ...")
    elif message.text in const.command_city:
        # check city that user chosen and place city in the order
        replace(order,message.from_user.id,'city', message.text)
        step = 1
        log(message, u"выбран город: {0}".format(message.text))
    elif message.text in const.command_goods:
        replace(order,message.from_user.id,'goods', message.text)
        step = 2
        log(message, u"выборан товар: {0}".format(message.text))
    elif message.text in const.command_g_value or message.text in const.command_t_value:
        replace(order,message.from_user.id,'value', message.text)
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
        # goto next step
        step = 3
        log(message, u"выбран размер: {0}".format(message.text))
    elif message.text == const.command_checkout:
        replace(order,message.from_user.id,'order', str(i))
        step = 4
        i += 1
        log(message, u"оформление заказа")
    elif message.text == "@" and str(message.from_user.id) == id.boss:
        bot.send_message(message.chat.id, u"hi, master")
        # statistics
        log(message, u"виват ...")
    elif message.text == "!" and ((str(message.from_user.id) == id.operator1) or
                                      (str(message.from_user.id) == id.operator2)):
        # operator must enter order number
        step = 10
        # prepare keyboard to enter order number
        hide_markup = telebot.types.ReplyKeyboardRemove(True);
        # sending message to operator
        bot.send_message(message.chat.id, u"введи номер заказа", reply_markup=hide_markup)
        # statistics
        # logging
        log(message, u"виват ...")
    else:
        if ((str(message.from_user.id) == id.operator1) or
            (str(message.from_user.id) == id.operator2)) and step == 10:
            bot.send_message(message.chat.id, u"введи адрес")
            step = 11
        elif ((str(message.from_user.id) == id.operator1) or
            (str(message.from_user.id) == id.operator2)) and step == 11:
            step = 12
        else:
            bot.send_message(message.chat.id, u"прочитай раздел помощь ...")
            log(message, u"раздел помощь ...")
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
                                          u"-- ... --".format(find(order, 'id', message.from_user.id,'city')))
        # sending message and request user action
        bot.send_message(message.chat.id,u"выбери наименование ...", reply_markup=user_markup)

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
                                          u"-- ... --".format(find(order, 'id', message.from_user.id,'city'),
                                                              find(order, 'id', message.from_user.id, 'goods')))
        # sending message and request user action
        bot.send_message(message.chat.id, u"выбери размер ...", reply_markup=user_markup)

    # choosing conditions for second goods
    elif step == 2 and find(order, 'id', message.from_user.id,'goods') == const.command_goods[1]:
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
                                          u"-- ... --".format(find(order, 'id', message.from_user.id,'city'),
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
                                          u"-- ... --".format(find(order, 'id', message.from_user.id,'city'),
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
                                          u"qiwi 7890654321 или\n"
                                          u"yandex 1234567890\n"
                                          u"указав в комментарии № заказа")
        if find(order, 'id', message.from_user.id, 'city') == const.command_city[0]:
            id_oper = id.operator1
        else: id_oper = id.operator2
        bot.send_message(id_oper, u"{0} {1} id({2}) заказ № {3} в {4} на {5} {6} стоимостью {7} руб.".format(
                        message.from_user.first_name,
                        message.from_user.last_name,
                        str(message.from_user.id),
                        match['order'],
                        match['city'],
                        match['goods'],
                        match['value'],
                        match['sum']))
        log(message, u"{0} {1} id({2}) заказ № {3} в {4} на {5} {6} стоимостью {7} руб.".format(
                        message.from_user.first_name,
                        message.from_user.last_name,
                        str(message.from_user.id),
                        match['order'],
                        match['city'],
                        match['goods'],
                        match['value'],
                        match['sum']))
        hide_markup = telebot.types.ReplyKeyboardRemove(True);
        bot.send_message(message.chat.id, u"для повторной покупки /start ...", reply_markup=hide_markup)
        # clear step for next order
        step = 0

    elif step == 10:
        print u"шаг ", step

    #
    elif step == 11:
        print u"шаг ", step
        done = find(order, 'order', message.text, 'id')
        print done

    elif step == 12:
        bot.send_message(done, u"по вашему заказу поступила оплата")
        bot.send_message(done, u"адрес получения: {0} ".format(message.text))
        step =0
    #
    else:
        bot.send_message(message.chat.id, u"какая-то фигня ...")

bot.polling(none_stop=True, interval=0)
# this is the end.