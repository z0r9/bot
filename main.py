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
def find(dic, id, key):
    for l in dic:
        if l['id'] == id:
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
    order.append({'id':message.from_user.id, 'status':'', 'city':'', 'region':'', 'goods':'', 'value':'', 'order':''})

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
    global step
    if message.text == const.command_rules:
        bot.send_message(message.chat.id, u"выбираем, оплачиваем, получаем ...")
        log(message, u"правила просты ...")
    elif message.text == const.command_back:
        bot.send_message(message.chat.id, u"возвращаемся на шаг назад ...")
        step -= 1
        log(message, u"возвращаемся назад ...")
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
        step = 3
        log(message, u"выбран размер: {0}".format(message.text))
    elif message.text == const.command_checkout:
        replace(order,message.from_user.id,'order',str(i))
        step = 4
        i += 1
        log(message, u"оформление заказа")
    elif message.text == "!" and str(message.from_user.id) == id.boss:
        bot.send_message(message.chat.id, u"hi, master")
        log(message, u"виват ...")
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
                                          u"-- ... --".format(find(order,message.from_user.id,'city')))
        # sending message and request user action
        bot.send_message(message.chat.id,u"выбери наименование ...", reply_markup=user_markup)

    # choosing conditions for first goods
    elif step == 2 and find(order,message.from_user.id,'goods') == const.command_goods[0]:
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
                                          u"-- ... --".format(find(order,message.from_user.id,'city'),
                                                          find(order, message.from_user.id, 'goods')))
        # sending message and request user action
        bot.send_message(message.chat.id, u"выбери размер ...", reply_markup=user_markup)

    # choosing conditions for second goods
    elif step == 2 and find(order,message.from_user.id,'goods') == const.command_goods[1]:
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
                                          u"-- ... --".format(find(order,message.from_user.id,'city'),
                                                          find(order, message.from_user.id, 'goods')))
        # sending message and request user action
        bot.send_message(message.chat.id, u"выбери размер ...", reply_markup=user_markup)

    # checkout
    elif step == 3:
        # prepare keyboard for change
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        # filling checkout key
        user_markup.row(const.command_checkout)
        # adding main menu commands
        user_markup.row(const.command_menu, const.command_rules, const.command_help)
        # show current cart options
        bot.send_message(message.chat.id, u"-- заказ --\n"
                                          u"город: {0}\n"
                                          u"товар: {1}\n"
                                          u"размер: {2}"
                                          u"-- ... --".format(find(order,message.from_user.id,'city'),
                                                              find(order, message.from_user.id, 'goods'),
                                                              find(order, message.from_user.id, 'value')))
        # sending message and request user action
        bot.send_message(message.chat.id, u"оформление заказа ...", reply_markup=user_markup)

    # sending order to operator
    elif step == 4:
        match = next((l for l in order if l['id'] == message.from_user.id), None)
        bot.send_message(message.chat.id, u"заказ № {0} в {1} {2} на {3}".format(
                        match['order'],
                        match['city'],
                        match['goods'],
                        match['value']))
        bot.send_message(id.boss, u"{0} {1} id({2}) заказ № {3} в {4} на {5} в {6}".format(
                        message.from_user.first_name,
                        message.from_user.last_name,
                        str(message.from_user.id),
                        match['order'],
                        match['city'],
                        match['goods'],
                        match['value']))
        log(message, u"{0} {1} id({2}) заказ № {3} в {4} {5} на {6}".format(
                        message.from_user.first_name,
                        message.from_user.last_name,
                        str(message.from_user.id),
                        match['order'],
                        match['city'],
                        match['region'],
                        match['goods']))
        hide_markup = telebot.types.ReplyKeyboardRemove(True);
        bot.send_message(message.chat.id, u"Для повторной покупки набери /start ...", reply_markup=hide_markup)
    else:
        bot.send_message(message.chat.id, u"какая-то фигня ...")

bot.polling(none_stop=True, interval=0)
##a = any(d['id'] == 2 for d in dicts) # True or False