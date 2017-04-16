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

# bot commands

# /start
@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id, u"Вас приветствует магазин [Ёлки]({0})".format(const.logo), parse_mode="Markdown")
    bot.send_photo(message.chat.id, "AgADAgADDqgxG-osSEvKHpohZmjRgblMtw0ABGXOtqSQDsEYa_QBAAEC")
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row(const.command_buy)
    user_markup.row(const.command_review, const.command_rules, const.command_help)
    bot.send_message(message.chat.id, u"Выбирай купить и покупай ...", reply_markup=user_markup)
    order.append({'id':message.from_user.id, 'step':0, 'city':'', 'region':'', 'goods':'', 'order':''}) # add user_id to order

# /stop
@bot.message_handler(commands=['stop'])
def handle_text(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True);
    bot.send_message(message.chat.id, u"Пока ...", reply_markup=hide_markup)

# /help
@bot.message_handler(commands=['help'])
def handle_text(message):
        bot.send_message(message.chat.id,u"Выбери опцию покупка ...")

# chat message
@bot.message_handler(content_types=['text'])
def handle_text(message):
    global i
    global order
    global step
    if message.text == const.command_rules:
        bot.send_message(message.chat.id, u"Выбираем, оплачиваем, получаем ...")
        log(message, u"правила просты ...")
    elif message.text == const.command_review:
        bot.send_message(message.chat.id, u"возвращаемся на шаг назад ...")
        step -= 1
        log(message, u"возвращаемся назад ...")
    elif message.text == const.command_buy:
        replace(order,message.from_user.id,'city',u'Москва')
        step = 1
        log(message, u"выбор ёлочного базара")
    elif message.text in const.command_reg:
        replace(order,message.from_user.id,'region',message.text)
        step = 2
        log(message, u"выбор ёлочки или ели")
    elif message.text in const.command_goods:
        replace(order,message.from_user.id,'goods',message.text)
        step = 3
        log(message, u"оформление заказа")
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
    if step == 0:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row(const.command_buy)
        user_markup.row(const.command_review, const.command_rules, const.command_help)
        bot.send_message(message.chat.id, u"Выбирай купить и покупай ...", reply_markup=user_markup)
    elif step == 1:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row(const.command_reg[8], const.command_reg[1], const.command_reg[2])
        user_markup.row(const.command_reg[7], const.command_reg[0], const.command_reg[3])
        user_markup.row(const.command_reg[5], const.command_reg[6], const.command_reg[4])
        user_markup.row(const.command_review, const.command_rules, const.command_help)
        bot.send_message(message.chat.id, u"Продажа осуществляется в Москве.\nВыбирай район расположения базара ...",
                         reply_markup=user_markup)
    elif step == 2:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row(const.command_goods[0], const.command_goods[1])
        user_markup.row(const.command_review, const.command_rules, const.command_help)
        bot.send_message(message.chat.id, u"Выбирай купить и покупай ...", reply_markup=user_markup)
    elif step == 3:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row(const.command_checkout)
        user_markup.row(const.command_review, const.command_rules, const.command_help)
        bot.send_message(message.chat.id, u"Оформляй покупку ...", reply_markup=user_markup)
    elif step == 4:
        match = next((l for l in order if l['id'] == message.from_user.id), None)
        bot.send_message(message.chat.id, u"Заказ № {0} в {1} {2} на {3}".format(
                        match['order'],
                        match['city'],
                        match['region'],
                        match['goods']))
        bot.send_message(id.boss, u"{0} {1} id({2}) заказ № {3} в {4} {5} на {6}".format(
                        message.from_user.first_name,
                        message.from_user.last_name,
                        str(message.from_user.id),
                        match['order'],
                        match['city'],
                        match['region'],
                        match['goods']))
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