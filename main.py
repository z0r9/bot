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


# bot info
print ("Bot profile is: {0}".format(bot.get_me()))

# eventlog
def log(question, answer):
    from datetime import datetime
    print ("\n---{0}---".format(datetime.now()))
    print("Message from {0} {1} (id = {2})\nText: {3}".format(question.from_user.first_name,
                                                                question.from_user.last_name,
                                                                str(question.from_user.id),
                                                                question.text))
    print("Answer: {0}".format(answer))

# bot commands

# .start
@bot.message_handler(commands=['start'])
def handle_text(message):
    bot.send_message(message.chat.id, "Вас приветствует магазин [Ёлки]({0})".format(const.logo), parse_mode="Markdown")
    bot.send_photo(message.chat.id, "AgADAgADDqgxG-osSEvKHpohZmjRgblMtw0ABGXOtqSQDsEYa_QBAAEC")
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
# remove
    user_markup.row('/start','/stop')
# /remove
    user_markup.row(const.command_buy)
    user_markup.row(const.command_review, const.command_rules, const.command_help)
    bot.send_message(message.chat.id, "Выбирай купить и покупай ...", reply_markup=user_markup)

# stop
@bot.message_handler(commands=['stop'])
def handle_text(message):
    hide_markup = telebot.types.ReplyKeyboardRemove(True);
    bot.send_message(message.chat.id,"Пока ...", reply_markup=hide_markup)

# help
@bot.message_handler(commands=['help'])
def handle_text(message):
        bot.send_message(message.chat.id,"Выбери опцию покупка ...")

# chat message
@bot.message_handler(content_types=['text'])
def handle_text(message):
    global i
    step = 0
    if message.text == const.command_rules:
        bot.send_message(message.chat.id, "Выбираем, оплачиваем, получаем ...")
#        log(message, u"правила просты ...")
    elif message.text == const.command_review:
        bot.send_message(message.chat.id, "Все елочки лучшего качества ...")
#        log(message, u"отзывы шикарны ...")
    elif message.text == const.command_buy:
        step = 1
 #       log(message, u"выбор ёлочного базара")
    elif message.text in const.command_reg:
        step = 2
#       log(message, u"выбор ёлочки или ели")
    elif message.text == "!" and str(message.from_user.id) == id.boss:
        bot.send_message(message.chat.id, "hi, master")
        answer = "виват ..."
#        log(message, answer)
    else:
        bot.send_message(message.chat.id, "прочитай раздел помощь ...")
        answer = "прочитай раздел помощь ..."
#        log(message, answer)
    if step == 1:
        user_parkup = telebot.types.ReplyKeyboardMarkup(True, False)
        # remove
        user_parkup.row('/start', '/stop')
        # /remove
        user_parkup.row(const.command_reg[8], const.command_reg[1], const.command_reg[2])
        user_parkup.row(const.command_reg[7], const.command_reg[0], const.command_reg[3])
        user_parkup.row(const.command_reg[5], const.command_reg[6], const.command_reg[4])
        user_parkup.row(const.command_review, const.command_rules, const.command_help)
        bot.send_message(message.chat.id, "Продажа осуществляется в Москве.\nВыбирай район базара ...", reply_markup=user_parkup)
    elif step == 2:
        user_parkup = telebot.types.ReplyKeyboardMarkup(True, False)
        # remove
        user_parkup.row('/start', '/stop')
        # /remove
        user_parkup.row(const.command_goods[0], const.command_goods[1])
        user_parkup.row(const.command_review, const.command_rules, const.command_help)
        bot.send_message(message.chat.id, "Выбирай купить и покупай ...", reply_markup=user_parkup)
    else:
        bot.send_message(message.chat.id, "прочитай раздел помощь ...")

bot.polling(none_stop=True, interval=0)