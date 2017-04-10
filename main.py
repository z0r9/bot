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
    user_markup.row(const.buy)
    user_markup.row('/reviews','/rules','/help')
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
    answer = "hey, read help another!"
    global i
    if message.text == "rules":
        bot.send_message(message.chat.id,"Выбираем, оплачиваем, получаем ...")
#       log(message, answer)
    elif message.text == const.buy.decode('utf-8'):
        bot.send_message(message.chat.id,"заказ {0} подготовлен".format(str(i)))
        bot.send_message(message.chat.id, "[Checkout]({0})".format(const.logo), parse_mode="Markdown")
        # remove in prod
        time.sleep(5)
        # end of remove
        bot.send_message(message.chat.id, "оплата заказа № {0} завершена".format(str(i)))
        bot.send_message(message.chat.id, "заказ {0} передан в доставку".format(str(i)))
        i += 1
        answer = "оплата произведена"
#       log(message, answer)
    elif message.text == "!" and str(message.from_user.id) == id.boss:
        bot.send_message(message.chat.id, "hi, master")
#       log(message, answer)
    else:
        bot.send_message(message.chat.id, "hey, read help another!")
#       log(message, answer)

bot.polling(none_stop=True, interval=0)