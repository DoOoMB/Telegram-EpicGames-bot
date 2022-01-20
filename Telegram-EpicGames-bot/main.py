import telebot
import threading
import sqlite3
import datetime
import time
from telebot import types
from link_parser import FindLink


# data base manager
def data_base(function, our_chat, obj=None, value=None):
    conn = sqlite3.connect("config.db")  # connect data base
    cur = conn.cursor()  # cursor for change data base
    if function == 'launch':  # add chat id
        action = cur.execute(f"select {obj} from CustomerData Where our_chat = {our_chat}")
        if action.fetchall():
            pass
        else:
            cur.execute("""insert into CustomerData(our_chat, mailing, weekday, past_link, launch)
                           values(?, ?, ?, ?, ?)""", (our_chat, True,
                        datetime.datetime.today().weekday(), None, True))
            conn.commit()
    elif function == 'take':  # take something from data base
        action = cur.execute(f"select {obj} from CustomerData where our_chat = {our_chat}")
        take = action.fetchall()[0][0]
        conn.commit()
        return take
    elif function == 'set':  # change value from data base
        cur.execute("UPDATE CustomerData SET (%s) = ? WHERE our_chat = ?" % obj, [value, our_chat])
        conn.commit()


bot = telebot.TeleBot("2092401673:AAF1Vxcq3Sg8scHqGg9dw15rxhzqGAogPF0")  # bot token
hb = FindLink()  # instance of class FindLink (to parse website)


@bot.message_handler(commands=['start', 'options'])  # main menu (commands /start and /options call this function)
def options(message):
    data_base('launch', message.chat.id, 'our_chat', message.chat.id)
    launch = data_base('take', our_chat=message.chat.id, obj='launch')
    keyboard = types.InlineKeyboardMarkup()  # create inline keyboard
    off_but = types.InlineKeyboardButton(text='Отключить рассылку', callback_data='off')  # create button
    on_but = types.InlineKeyboardButton(text='Включить рассылку', callback_data='on')
    change_weekday = types.InlineKeyboardButton(text='Выбрать день недели для рассылки', callback_data='weekday')
    keyboard.add(on_but, off_but, change_weekday)  # add all buttons to keyboard
    bot.send_message(message.chat.id,
                "Приветствую ♂Boss of this gym♂! Тут вы можете включить и отключить рассылку, и выбрать день недели "
                "для рассылки сообщения.", reply_markup=keyboard)
    # launch of parsing
    if launch:
        data_base("set", message.chat.id, "launch", False)
        print("launch:", launch)
        threading.Thread(target=parse(message.chat.id))  # create new thread


def weekday_keyb(message):  # keyboard for choice week day to sending
    weekday_keyboard = types.InlineKeyboardMarkup()
    monday = types.InlineKeyboardButton(text='Пн', callback_data='0')
    tuesday = types.InlineKeyboardButton(text='Вт', callback_data='1')
    wednesday = types.InlineKeyboardButton(text='Ср', callback_data='2')
    thursday = types.InlineKeyboardButton(text='Чт', callback_data='3')
    friday = types.InlineKeyboardButton(text='Пт', callback_data='4')
    saturday = types.InlineKeyboardButton(text='Сб', callback_data='5')
    sunday = types.InlineKeyboardButton(text='Вс', callback_data='6')
    weekday_keyboard.add(monday, tuesday, wednesday, thursday, friday, saturday, sunday)
    bot.send_message(message.chat.id, "Выберите день недели:", reply_markup=weekday_keyboard)


@bot.callback_query_handler(func=lambda funct: True)  # here we "catch" all buttons' callbacks
def mailing_on_off(funct):
    if funct.data == 'on':  # processing the callback argument
        mailing = True
        data_base('set', funct.message.chat.id, 'mailing', mailing)
        bot.send_message(funct.message.chat.id, "Рассылка активирована!")
    elif funct.data == 'off':
        mailing = False
        data_base('set', funct.message.chat.id, 'mailing', mailing)
        bot.send_message(funct.message.chat.id, "Рассылка деактивирована!")
    elif funct.data == 'weekday':
        weekday_keyb(funct.message)
    elif funct.data == '0':
        weekday = 0
        print("weekday:", weekday)
        data_base('set', funct.message.chat.id, "weekday", weekday)
        bot.send_message(funct.message.chat.id, "Время установлено на Пн!")
    elif funct.data == '1':
        weekday = 1
        print("weekday:", weekday)
        bot.send_message(funct.message.chat.id, "Время установлено на Вт!")
        data_base('set', funct.message.chat.id, "weekday", weekday)
    elif funct.data == '2':
        weekday = 2
        print("weekday:", weekday)
        bot.send_message(funct.message.chat.id, "Время установлено на Ср!")
        data_base('set', funct.message.chat.id, "weekday", weekday)
    elif funct.data == '3':
        weekday = 3
        print("weekday:", weekday)
        bot.send_message(funct.message.chat.id, "Время установлено на Чт!")
        data_base('set', funct.message.chat.id, "weekday", weekday)
    elif funct.data == '4':
        weekday = 4
        print("weekday:", weekday)
        bot.send_message(funct.message.chat.id, "Время установлено на Пт!")
        data_base('set', funct.message.chat.id, "weekday", weekday)
    elif funct.data == '5':
        weekday = 5
        print("weekday:", weekday)
        bot.send_message(funct.message.chat.id, "Время установлено на Сб!")
        data_base('set', funct.message.chat.id, "weekday", weekday)
    elif funct.data == '6':
        weekday = 6
        print("weekday:", weekday)
        bot.send_message(funct.message.chat.id, "Время установлено на Вс!")
        data_base('set', funct.message.chat.id, "weekday", weekday)


def parse(chat):
    while True:
        print("weekday today:", datetime.datetime.today().weekday())
        mailing = data_base('take', chat, 'mailing')
        weekday = data_base('take', chat, 'weekday')
        past_link = data_base('take', chat, 'past_link')
        if datetime.datetime.today().weekday() == weekday and mailing:
            print('It have to run today.')
            link = hb.find_link()  # take new link
            if past_link == link:  # if new link matches with new link, we wait while new link appear
                time.sleep(5)
                pass
            else:
                data_base('set', chat, "past_link", link)  # add tht link to data base if as old
                text = '[Отличное время, чтобы получить лишнюю игру в Epic games, не так ли, ♂master♂?]({})'.format(
                    link)  # create hyperlink
                bot.send_message(chat, text, parse_mode="Markdown")  # send the hyperlink with our free game
        time.sleep(5)


bot.infinity_polling()  # launch the bot