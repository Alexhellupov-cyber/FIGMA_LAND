import telebot
from telebot import types

# Замените 'YOUR_API_TOKEN' на ваш реальный API токен
bot = telebot.TeleBot('7438062994:AAGZtpLpUeT23cnRn9wVaAs8TWWkm6GujQY')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Услуги')
    btn2 = types.KeyboardButton('Как заказать?')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Привет! Выберите один из вариантов:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Услуги')
def services_menu(message):
    with open('C:/Users/380674914614/Desktop/bot/photo/услуги.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Рассылка')
    btn2 = types.KeyboardButton('Реклама')
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn1, btn2,btn_back)
    bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Рассылка')
def software(message):
    with open('C:/Users/380674914614/Desktop/bot/photo/рассылка.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Комбайн')
    btn2 = types.KeyboardButton('Рассылка в лс')
    btn3 = types.KeyboardButton('Рассылка по чатам')
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn1,btn2,btn3, btn_back)
    bot.send_message(message.chat.id, "Отправляет ваш текст с фото и видео в личку\чатам.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Комбайн')
def software(message):
    with open('C:/Users/380674914614/Desktop/bot/photo/Комбайн.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Заказать')
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn1, btn_back)
    bot.send_message(message.chat.id, "Комбайн - в нем сразу содержится пару услуг: парсер, инвайтер, спаммер классик, автоподписка на каналы. Цена: 70$", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Рассылка в лс')
def software(message):
    with open('C:/Users/380674914614/Desktop/bot/photo/рассылкавлс.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Заказать')
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn1, btn_back)
    bot.send_message(message.chat.id, "Отправляет ваш текст с фото и видео в лс. Цена: 60$", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Рассылка по чатам')
def software(message):
    with open('C:/Users/380674914614/Desktop/bot/photo/рассылкапочатам.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Заказать')
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn1, btn_back)
    bot.send_message(message.chat.id, "Отправляет ваш текст с фото и видео в чатам. Цена: 50$", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Заказать')
def order_service(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn_back)
    bot.send_message(message.chat.id, "Заказать вы можете у администратора @elison_smm", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Реклама')
def advertisement(message):
    with open('C:/Users/380674914614/Desktop/bot/photo/фото.jpg', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Заказать')
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn1, btn_back)
    bot.send_message(message.chat.id, """Рекламируем:

Работа/Фриланс 
Биржа каналов
Бизнес
Инвестиции 
Коучинг
Банки/Кредиты
Криптовалюта
Майнинг
МЛМ
Экзотерика
Теневая тематика
Психология 
Cтaвки/Kaзино
Авто 
Aрбитрaж 
Beйп/Табaк 
Маркетплейсы

а так же любое другое""", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == 'Как заказать?')
def how_to_order(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Заказать')
    btn_back = types.KeyboardButton('Назад')
    markup.add(btn1, btn_back)
    bot.send_message(message.chat.id, "Заказать вы можете у администратора @elison_smm", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Назад')
def back_to_main_menu(message):
    send_welcome(message)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == 'Комбайн':
        bot.reply_to(message, "Комбайн - в нем сразу содержится пару услуг: парсер, инвайтер, спаммер классик, автоподписка на каналы. Цена: 70$")
    elif message.text == 'Рассылка в ЛС':
        bot.reply_to(message, "Рассылка в ЛС - отправляет ваш текст с фото и видео в личку. Цена: 50$")
    elif message.text == 'Автоподписка на каналы':
        bot.reply_to(message, "Автоподписка на каналы. Цена: 35$")
    elif message.text == 'Правила сайта':
        bot.reply_to(message, "https://vm.tiktok.com/ZMrxhH1C6")
    elif message.text == 'Создатель':
        bot.reply_to(message, "@alexhellupov")
    elif message.text == 'Пасхалка':
        bot.reply_to(message, "1488")
    else:
        bot.reply_to(message, "Извините, я не понимаю эту команду.")

if __name__ == '__main__':
    bot.infinity_polling()
