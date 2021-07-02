import config #Конфигурация
import requests
import json
import telebot
from telebot import types
##########################################################################################
res = requests.get('https://api.bittrex.com/api/v1.1/public/getmarketsummary?market=USD-BTC').json()['result']
print(res)

for element in res :
    print(element['Ask'])

btc_ask=element['Ask']
btc_bid = element['Bid']
btc_High = element['High']
btc_Low=element['Low']
btc_Volume=element['Volume']
btc_Last=element['Last']
btc_BaseVolume=element['BaseVolume']
btc_OpenBuyOrders=element['OpenBuyOrders']
btc_OpenSellOrders=element['OpenSellOrders']

print(btc_High)

br = '\n'

# Начало Бота 
bot = telebot.TeleBot(config.token) 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Вывод клавиатуры Шаг 1 
    markup_inline =types.InlineKeyboardMarkup(row_width=1)
    btn_inline = types.InlineKeyboardButton(text=" Начать ",callback_data = 'welcome')
    markup_inline.add(btn_inline)
    bot.send_message(message.chat.id, " Привет" + message.from_user.first_name + br +  "Расскажу всю информацию про Биткойн"+ br +"Я использую API bittrex" + br +"✅Ты всегда получишь все данные в реальном времени ",reply_markup=markup_inline)

@bot.callback_query_handler(func=lambda call:True)
def btc(call):
    if call.data== 'welcome':
    # Вывод клавиатуры Шаг 1
        markup_inline_step_2 =types.InlineKeyboardMarkup(row_width=3)
        btn_inline_step_2 = types.InlineKeyboardButton(text="🟡USD\BTC",callback_data = 'btc')
        markup_inline_step_2.add(btn_inline_step_2)
        bot.send_message(call.message.chat.id,"✅Пожалуйста выберете раздел",reply_markup = markup_inline_step_2)
    # Вывод клавиатуры Шаг 2
    if call.data =="btc":
        markup_inline_step_3 =types.InlineKeyboardMarkup(row_width=3)
        btn_inline__step_3 = types.InlineKeyboardButton(text="Покупка",callback_data = 'bid')
        btn_inline_2_step_3 = types.InlineKeyboardButton(text="Продажа",callback_data = 'ask')
        btn_inline_3_step_3 = types.InlineKeyboardButton(text="Узнать всю информацию ",callback_data = 'info')
        markup_inline_step_3.add(btn_inline__step_3,btn_inline_2_step_3,btn_inline_3_step_3)
        bot.send_message(call.message.chat.id,"Выберете интересующийся раздел",reply_markup = markup_inline_step_3)
    #Вывод данных 
    if call.data =="bid":
        bot.send_message(call.message.chat.id,"Курс покупки  = {}".format(btc_bid))
    if call.data =="ask":
        bot.send_message(call.message.chat.id,"Курс продажи  = {}".format(btc_ask))
    if call.data =='info':
        bot.send_message(call.message.chat.id," Курс покупки  = {0} \n Курс продажи = {1} \n Самая высокая цена = {2} \n Самая низкая цена = {3} \n Обьем = {4} \n Последняя цена = {5} \n Количество ордеров на покупку = {6} \n Количество ордеров на продажу = {7}\n Базовый обьем = {8}".format(btc_bid,btc_ask,btc_High,btc_Low,btc_Volume,btc_Last,btc_BaseVolume,btc_OpenBuyOrders,btc_OpenSellOrders))

@bot.message_handler(commands=['help'])
def help (message):
    bot.send_message(message.chat.id, "Привет👋🏻" + message.from_user.first_name + " мой создатель @S19S93 , Бот использует API bittrex ")


bot.polling()