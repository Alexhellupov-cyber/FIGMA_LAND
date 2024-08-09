from settings import cfg
import time, random
import telebot
from telebot import types
import sqlite3
from captcha.image import ImageCaptcha
from os import remove

print("""
-----------------------------------
ИГРОВОЙ БОТ Telegram ЗАПУЩЕН
СОЗДАТЕЛЬ КОДА: 0xSn1kky
YouTube: https://www.youtube.com/channel/UCo3yqAlAobt4KB6o9UwQxeg
-----------------------------------
""")

# ВСЕ НАСТРОЙКИ В settings.py

# подключение к базе данных
db = sqlite3.connect('database.db', check_same_thread=False)
cursor = db.cursor()

# подключение к боту
bot = telebot.TeleBot('7296845868:AAFWvXxzvSeFvN4DEekD9FJDKIZWd_LDoFE')

# создание таблиц

cursor.execute("""CREATE TABLE IF NOT EXISTS users(
    id INTEGER,
    nick TEXT,
    money INTEGER,
    bonus_last INTEGER,
    car_name TEXT,
    home_name TEXT,
    phone_name TEXT,
    energy INTEGER,
    lvl INTEGER,
    admin INTEGER,
    status TEXT,
    work INTEGER,
    work_name TEXT,
    work_zp INTEGER,
    ban INTEGER,
    bank INTEGER
)""")
db.commit()

# важное
carss = ({
    "car_name_1": "Жигуль",
    "car_cost_1": 60000,

    "car_name_2": "Lada Granta Cross",
    "car_cost_2": 280000,

    "car_name_3": "Audi RS 6",
    "car_cost_3": 10000000,

    "car_name_4": "BMW M3",
    "car_cost_4": 50000000,

    "car_name_5": "Mustang GT 500",
    "car_cost_5": 100000000,

    "car_name_6": "Acura NSX",
    "car_cost_6": 150000000,

    "car_name_7": "Porsche 911",
    "car_cost_7": 300000000,

    "car_name_8": "Bugatti Chiron",
    "car_cost_8": 600000000,

    "car_name_9": "Lamborghini Huracan",
    "car_cost_9": 950000000
})

homes = ({
    "home_name_1": "Коробка",
    "home_cost_1": 10000,

    "home_name_2": "Сарай",
    "home_cost_2": 70000,

    "home_name_3": "Гараж",
    "home_cost_3": 100000,

    "home_name_4": "Комната в общаге",
    "home_cost_4": 500000,

    "home_name_5": "Однокомнатная квартира",
    "home_cost_5": 900000,

    "home_name_6": "Коттедж",
    "home_cost_6": 10000000,

    "home_name_7": "Дом на рублёвке",
    "home_cost_7": 300000000,

    "home_name_8": "Moscow City",
    "home_cost_8": 700000000,

    "home_name_9": "Мальдивы",
    "home_cost_9": 900000000,

    "home_name_10": "Своя планета",
    "home_cost_10": 1000000000
})

phones = ({
    "phone_name_1": "Тапок",
    "phone_cost_1": 1000,

    "phone_name_2": "Nokia 3310",
    "phone_cost_2": 5000,

    "phone_name_3": "Samsung Galaxy S8",
    "phone_cost_3": 20000,

    "phone_name_4": "Xiaomi Mi Mix",
    "phone_cost_4": 30000,

    "phone_name_5": "iPhone X",
    "phone_cost_5": 70000,

    "phone_name_6": "Samsung Z Flip",
    "phone_cost_6": 100000,

    "phone_name_7": "iPhone 14",
    "phone_cost_7": 600000,

    "phone_name_8": "iPhone 14 Pro Max",
    "phone_cost_8": 900000
})

workss = ({
    'work_name_1': "Дворник",
    "work_zp_1": 6000,
    'work_lvl_1': 1,

    "work_name_2": "Официант",
    "work_zp_2": 30000,
    "work_lvl_2": 10,

    "work_name_3": "Повар",
    "work_zp_3": 70000,
    "work_lvl_3": 15,

    "work_name_4": "Врач",
    "work_zp_4": 100000,
    "work_lvl_4": 25,

    "work_name_5": "Стоматолог",
    "work_zp_5": 700000,
    "work_lvl_5": 50,

    "work_name_6": "Инженер",
    "work_zp_6": 3000000,
    "work_lvl_6": 70,

    "work_name_7": "Космонавт",
    "work_zp_7": 8000000,
    "work_lvl_7": 80,

    "work_name_8": "Программист",
    "work_zp_8": 10000000,
    "work_lvl_8": 100
})

# макс символы
PREFIX_MAX = 10
NICKNAME_MAX = 15
ENERGY_START = 10
ENERGY_MAX = 50

# эмодзи
EMOJI_HI = '👋'
EMOJI_LIKE = '👍'
EMOJI_DISLIKE = '👎'
EMOJI_YES = '✅'
EMOJI_NO = '❌'
EMOJI_W = '❓'
EMOJI_WARN = '⚠️'
SMILE = ['😀', '😃', '😄', '😁', '😆', '😎', '😱']
EMOJI_SAD = ['😞', '😔', '☹️', '😖', '😢']


# команда start

@bot.message_handler(commands=['start'])
def start(message):
    usrid = message.chat.id
    # Проверяем есть ли пользователь в системе
    info = cursor.execute(f"SELECT id FROM users WHERE id = {usrid}").fetchone()
    if info is None:
        cursor.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            usrid, message.from_user.first_name, cfg['money_on_start'], 0, "Без машины", "Без дома",
            "Без телефона", ENERGY_START, 1, 0, "Новичек", 0, "Безработный", 0, 0, 0))
        db.commit()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton(text="💵 Баланс")
        btn2 = types.KeyboardButton(text="👤 Профиль")
        btn3 = types.KeyboardButton(text="⚒ Работать")
        btn4 = types.KeyboardButton(text=f"{EMOJI_W} Репорт")
        btn5 = types.KeyboardButton(text="📜 Помощь")
        btn6 = types.KeyboardButton(text="💠 Бонус")
        markup.add(btn1, btn2, btn3, btn6)
        markup.add(btn4, btn5)
        bot.send_message(message.chat.id,
                     f"{EMOJI_HI} Привет {message.from_user.first_name} вижу ты новенький я {cfg['botname']}. Tы был успешно зарегестрирован в боте! Напиши \"Помощь\" чтобы узнать список команд", reply_markup=markup)
    else:
        pass


@bot.message_handler(func=lambda message: message.text.lower() == 'баланс' or message.text == '💵 Баланс')
def balance(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        balanceu = cursor.execute(f'SELECT money FROM users WHERE id = {message.chat.id}').fetchone()
        userbank = cursor.execute(f'SELECT bank FROM users WHERE id = {message.chat.id}').fetchone()
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        bot.send_message(message.chat.id, f"{usernick[0]} 💰 Ваш баланс: {balanceu[0]}$ \n 💳 В банке: {userbank[0]}$")


@bot.message_handler(func=lambda message: message.text.lower() == 'бонус' or message.text == '💠 Бонус')
def bonus(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        bonust = cursor.execute(f'SELECT bonus_last FROM users WHERE id = {message.chat.id}').fetchone()
        s = time.localtime(time.time())
        if bonust[0] != s.tm_mday:
            cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (cfg['bonus'],))
            cursor.execute(f"UPDATE users SET bonus_last = ? WHERE id = {message.chat.id}",
                           (time.localtime(time.time()).tm_mday,))
            db.commit()
            bot.send_photo(message.chat.id, 'https://pngimg.com/uploads/money/money_PNG3538.png',
                           f"{usernick[0]} Вы успешно получили бонус в размере {cfg['bonus']}$ {SMILE[5]}")
        else:
            bot.reply_to(message, f"{usernick[0]} Вы уже получали бонус {EMOJI_SAD[0]}")


@bot.message_handler(func=lambda message: message.text.lower() == 'энергия')
def energy(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        energyu = cursor.execute(f'SELECT energy FROM users WHERE id = {message.chat.id}').fetchone()
        kb = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton(text="⚡️ Пополнить энергию", callback_data='energy_buy')
        kb.add(btn1)
        bot.send_message(message.chat.id,
                         f"{usernick[0]} ⚡️ Ваш уровень энергии: {energyu[0]} \n Стоимость пополнения энергии: 3000$",
                         reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data == 'energy_buy')
def energy_buy(call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        energyu = cursor.execute(f'SELECT energy FROM users WHERE id = {call.message.chat.id}').fetchone()
        if energyu[0] == ENERGY_MAX:
            bot.reply_to(call.message, f"{usernick[0]} У вас уже максимальный уровень энергии {EMOJI_SAD[2]}")
        else:
            balanceu = cursor.execute(f'SELECT money FROM users WHERE id = {call.message.chat.id}').fetchone()
            if balanceu[0] > 2999:
                cursor.execute(f"UPDATE users SET energy = energy + 1 WHERE id = {call.message.chat.id}")
                cursor.execute(f"UPDATE users SET money = money - 3000 WHERE id = {call.message.chat.id}")
                db.commit()
                bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно повысили свою энергию!")
            else:
                bot.send_message(call.message.chat.id,
                                 f"{usernick[0]} У вас недостаточно денег чтобы повысить энергию {EMOJI_SAD[3]}")


@bot.message_handler(func=lambda message: message.text.lower() == 'взлом')
def hack(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        energyu = cursor.execute(f'SELECT energy FROM users WHERE id = {message.chat.id}').fetchone()
        if energyu[0] < 1:
            bot.send_message(message.chat.id, f"{usernick[0]} У вас мало энергии {EMOJI_SAD[4]}")
        else:
            give_money = random.randint(3000, 20000)
            random_photo = random.SystemRandom().choice(
                ["https://kartinkin.net/uploads/posts/2022-03/1646196653_75-kartinkin-net-p-kartinki-khakera-85.jpg",
                 "https://юрнадзор.рф/wp-content/uploads/2019/02/how-to-protect-yourself-from-hackers.jpeg",
                 "https://discover24.ru/wp-content/uploads/2020/11/0001-scaled.jpg"])
            bot.send_photo(message.chat.id, random_photo,
                           f"{usernick[0]} Вы успешно взломали пентагон и получили {give_money}$")
            cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (give_money,))
            cursor.execute(f"UPDATE users SET energy = energy - 1 WHERE id = {message.chat.id}")
            db.commit()


@bot.message_handler(func=lambda message: message.text.lower() == 'ник')
def nickname(message):
    msg = bot.send_message(message.chat.id, "Введите ник который хотите себе поставить")
    bot.register_next_step_handler(msg, nick_set)


def nick_set(message):
    if message.text.lower() == 'выкл' or message.text.lower() == 'off':
        username = message.from_user.first_name
        cursor.execute(f"UPDATE users SET nick = ? WHERE id = {message.chat.id}", (username,))
        db.commit()
        bot.send_message(message.chat.id, "Вы установили себе изначальный ник")
    else:
        if len(message.text) > NICKNAME_MAX:
            bot.send_message(message.chat.id, "Вы указали слишком длинный ник!")
        else:
            username = message.text
            cursor.execute(f"UPDATE users SET nick = ? WHERE id = {message.chat.id}", (username,))
            db.commit()
            bot.send_message(message.chat.id, "Вы установили себе новый ник")


@bot.message_handler(func=lambda message: message.text.lower() == 'грабить' or message.text.lower() == 'ограбить')
def grabit(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        energyu = cursor.execute(f'SELECT energy FROM users WHERE id = {message.chat.id}').fetchone()
        if energyu[0] < 1:
            bot.send_message(message.chat.id, f"{usernick[0]} У вас мало энергии {EMOJI_SAD[4]}")
        else:
            give_money = random.randint(3000, 15000)
            random_photo = random.SystemRandom().choice(
                ["https://proumdom.ru/wp-content/uploads/2020/12/21567875464789.jpg",
                 "https://media.1777.ru/images/images_processing/881/8817189501727565.jpeg",
                 "https://news.store.rambler.ru/img/dfc6a83e751a8f423e52f62ebb426346?img-format=auto&img-1-resize=height:710",
                 "https://liter.kz/cache/imagine/1200/uploads/news/2022/03/18/62345d2b2ec99547306734.jpg"])
            bot.send_photo(message.chat.id, random_photo,
                           f"{usernick[0]} Вы успешно ограбили банк и получили {give_money}$")
            cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (give_money,))
            cursor.execute(f"UPDATE users SET energy = energy - 1 WHERE id = {message.chat.id}")
            db.commit()


@bot.message_handler(func=lambda message: message.text.lower() == 'дайвинг' or message.text.lower() == 'ловить')
def lovit(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        energyu = cursor.execute(f'SELECT energy FROM users WHERE id = {message.chat.id}').fetchone()
        if energyu[0] < 1:
            bot.send_message(message.chat.id, f"{usernick[0]} У вас мало энергии {EMOJI_SAD[4]}")
        else:
            give_money = random.randint(3000, 10000)
            random_photo = random.SystemRandom().choice(
                ["https://wp-s.ru/wallpapers/5/15/311821487171135/foto-ryby-kloun-v-vodoroslyax.jpg",
                 "https://kartinkin.net/pics/uploads/posts/2022-07/1657833006_5-kartinkin-net-p-golubaya-riba-zhivotnie-krasivo-foto-5.jpg",
                 "https://klike.net/uploads/posts/2022-09/1662463935_v-27.jpg",
                 "https://klev26.ru/wp-content/uploads/b/d/4/bd40f13a82154aa08445aee40cf1186d.jpeg",
                 "https://vsegda-pomnim.com/uploads/posts/2022-04/1651050744_81-vsegda-pomnim-com-p-morskie-ribi-foto-99.jpg"])
            random_fish = random.SystemRandom().choice(["Редкую рыбу", "Карпа", "Щуку", "Рыбу фугу"])
            bot.send_photo(message.chat.id, random_photo,
                           f"{usernick[0]} Вы поймали {random_fish} продав эту рыбу вы получили {give_money}$")
            cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (give_money,))
            cursor.execute(f"UPDATE users SET energy = energy - 1 WHERE id = {message.chat.id}")
            db.commit()


@bot.message_handler(func=lambda message: message.text.lower() == 'капча')
def captcha_game(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        image = ImageCaptcha(width=280, height=90)
        c1 = random.randint(1, 10)
        c2 = random.SystemRandom().choice(["ab", "bao", "owmc", "olwqw", "bqof", "kwsl", "qxaw", "ow1"])
        c3 = random.randint(1, 35)
        global cptch_0
        cptch_0 = f'{c1}{c2}{c3}'
        data = image.generate(f"{c1}{c2}{c3}")
        image.write(f"{c1}{c2}{c3}", 'img.png')
        file = open('img.png', 'rb')
        msg = bot.send_photo(message.chat.id, file, f"{usernick[0]} Введите капчу верно чтобы получить бонус")
        file.close()
        remove("img.png")
        print(cptch_0)
        bot.register_next_step_handler(msg, cptgame)


def cptgame(message):
    if message.text.lower() == cptch_0.lower():
        bot.send_message(message.chat.id, "Вы угадали  капчу за это вы получаете 5000$")
        cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (5000,))
        db.commit()
    else:
        bot.send_message(message.chat.id, "Вы не угадали капчу")


@bot.message_handler(func=lambda message: message.text.lower() == 'поход')
def poxod(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        energyu = cursor.execute(f'SELECT energy FROM users WHERE id = {message.chat.id}').fetchone()
        if energyu[0] < 1:
            bot.send_message(message.chat.id, f"{usernick[0]} У вас мало энергии {EMOJI_SAD[4]}")
        else:
            give_money = random.randint(3000, 10000)
            random_photo = random.SystemRandom().choice(
                ["https://i.pinimg.com/736x/2e/f6/57/2ef657e1b42c38f2ae435eaaceb89d7a.jpg",
                 "https://avatars.dzeninfra.ru/get-zen_doc/222865/pub_5cc40f54427b3c00be0314e2_5cc40fc43d89f500b3ced391/scale_1200",
                 "https://obzor174.ru/sites/default/files/pubs/2c412260ce4ec76fcc2cd942b0fbda81.jpg"])
            bot.send_photo(message.chat.id, random_photo,
                           f"{usernick[0]} Вы пошли в поход в походе вы нашли {give_money}$")
            cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (give_money,))
            cursor.execute(f"UPDATE users SET energy = energy - 1 WHERE id = {message.chat.id}")
            db.commit()


@bot.message_handler(func=lambda message: message.text.lower() == 'кубик')
def cube1(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        msg = bot.send_message(message.chat.id, f"{usernick[0]} Введите сумму на которую ставите")
        bot.register_next_step_handler(msg, cube2)


def cube2(message):
    try:
        global stavka_cubik
        stavka_cubik = int(message.text)
        usermoney = cursor.execute(f"SELECT money FROM users WHERE id = {message.chat.id}").fetchone()
        if usermoney[0] >= stavka_cubik:
            if stavka_cubik > 0:
                msg = bot.send_message(message.chat.id, "Введите число на которое ставите [1-6]")
                bot.register_next_step_handler(msg, cube3)
            else:
                bot.send_message(message.chat.id, "Введите число более 0!")
        else:
            bot.reply_to(message, f"У вас недостаточно денег для данной ставки")
    except:
        bot.send_message(message.chat.id, "Произошла ошибка")


def cube3(message):
    try:
        cube_num = int(message.text)
        if cube_num > 6:
            bot.send_message(message.chat.id, "Вы указали число больше 6!")
        else:
            dicee = bot.send_dice(message.chat.id, '🎲')
            usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
            if dicee.dice.value == cube_num:
                cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (stavka_cubik,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Поздравляем вы выйграли {SMILE[2]}")
            else:
                cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {message.chat.id}", (stavka_cubik,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Очень жаль, но вы проиграли {EMOJI_SAD[4]}")
    except:
        bot.send_message(message.chat.id, "Произошла ошибка")


@bot.message_handler(func=lambda message: message.text.lower() == 'дартс')
def darts(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        msg = bot.send_message(message.chat.id, f"Введите сумму ставки")
        bot.register_next_step_handler(msg, darts2)


def darts2(message):
    try:
        stavka_dice = int(message.text)
        moneyuser = cursor.execute(f"SELECT money FROM users WHERE id = {message.chat.id}").fetchone()
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        if moneyuser[0] < stavka_dice:
            bot.reply_to(message, f"У вас недостаточно денег для данной ставки")
        else:
            dicee = bot.send_dice(message.chat.id, '🎯')
            if dicee.dice.value == 6:
                cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (stavka_dice,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Поздравляем вы выйграли {SMILE[2]}")
            else:
                cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {message.chat.id}", (stavka_dice,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Очень жаль, но вы проиграли {EMOJI_SAD[4]}")
    except:
        bot.send_message(message.chat.id, "Произошла ошибка")


# @bot.message_handler(func=lambda message: message.text.lower() == 'тест дайс')
# def tstdice(message):
#    dic = bot.send_dice(message.chat.id, "🏀")
#    bot.send_message(message.chat.id, dic.dice.value)


@bot.message_handler(func=lambda message: message.text.lower() == 'футбол')
def football(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        msg = bot.send_message(message.chat.id, f"Введите сумму ставки")
        bot.register_next_step_handler(msg, football2)


def football2(message):
    try:
        stavka_dice = int(message.text)
        moneyuser = cursor.execute(f"SELECT money FROM users WHERE id = {message.chat.id}").fetchone()
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        if moneyuser[0] < stavka_dice:
            bot.reply_to(message, f"У вас недостаточно денег для данной ставки")
        else:
            dicee = bot.send_dice(message.chat.id, '⚽️')
            if dicee.dice.value == 5 or dicee.dice.value == 4 or dicee.dice.value == 3:
                cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (stavka_dice,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Поздравляем вы выйграли {SMILE[2]}")
            else:
                cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {message.chat.id}", (stavka_dice,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Очень жаль, но вы проиграли {EMOJI_SAD[4]}")
    except:
        bot.send_message(message.chat.id, "Произошла ошибка")


@bot.message_handler(func=lambda message: message.text.lower() == 'кегля' or message.text.lower() == 'боулинг')
def kegla(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        msg = bot.send_message(message.chat.id, f"Введите сумму ставки")
        bot.register_next_step_handler(msg, kegla2)


def kegla2(message):
    try:
        stavka_dice = int(message.text)
        moneyuser = cursor.execute(f"SELECT money FROM users WHERE id = {message.chat.id}").fetchone()
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        if moneyuser[0] < stavka_dice:
            bot.reply_to(message, f"У вас недостаточно денег для данной ставки")
        else:
            dicee = bot.send_dice(message.chat.id, '🎳')
            if dicee.dice.value == 6:
                cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (stavka_dice,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Поздравляем вы выйграли {SMILE[2]}")
            else:
                cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {message.chat.id}", (stavka_dice,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Очень жаль, но вы проиграли {EMOJI_SAD[4]}")
    except:
        bot.send_message(message.chat.id, "Произошла ошибка")


@bot.message_handler(func=lambda message: message.text.lower() == 'баскетбол')
def basketball(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        msg = bot.send_message(message.chat.id, f"Введите сумму ставки")
        bot.register_next_step_handler(msg, basketball2)


def basketball2(message):
    try:
        stavka_dice = int(message.text)
        moneyuser = cursor.execute(f"SELECT money FROM users WHERE id = {message.chat.id}").fetchone()
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        if moneyuser[0] < stavka_dice:
            bot.reply_to(message, f"У вас недостаточно денег для данной ставки")
        else:
            dicee = bot.send_dice(message.chat.id, '🏀')
            if dicee.dice.value == 5 or dicee.dice.value == 4:
                cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (stavka_dice,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Поздравляем вы выйграли {SMILE[2]}")
            else:
                cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {message.chat.id}", (stavka_dice,))
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Очень жаль, но вы проиграли {EMOJI_SAD[4]}")
    except:
        bot.send_message(message.chat.id, "Произошла ошибка")


@bot.message_handler(func=lambda message: message.text.lower() == 'казино')
def casino(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        msg = bot.send_message(message.chat.id, "Пожалуйста введите сумму ставки")
        bot.register_next_step_handler(msg, casinoplay)

def casinoplay(message):
    usrid = message.chat.id
    try:
        st = message.text
        stavka = int(st)
        b = cursor.execute(f"SELECT money FROM users WHERE id = {usrid}").fetchone()
        ba = b[0]
        if ba >= stavka:
            bot.send_message(message.chat.id, f"Вы указали ставку {stavka}$ игра начинается!")
            rnd = random.randint(1, 3)
            if rnd == 1:
                y = stavka
                bot.send_message(message.chat.id, "Очень жаль, но вы проиграли ❌ ")
                cursor.execute(f'UPDATE users SET money = money - {y} WHERE id = {message.chat.id}')
            if rnd == 2:
                bot.send_message(message.chat.id, "😕 Вы не проиграли, но и не выйграли")
            if rnd == 3:
                y = stavka
                bot.send_message(message.chat.id, "🎉 Поздравляем вы выйграли!")
                cursor.execute(f'UPDATE users SET money = money + {y} WHERE id = {message.chat.id}')
        else:
            bot.send_message(message.chat.id, "У вас недостаточно денег чтобы сыграть на такую ставку!")
    except:
        bot.send_message(message.chat.id, "Это не число!")
    db.commit()

@bot.message_handler(func=lambda message: message.text.lower() == 'работы')
def works (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb1 = types.InlineKeyboardButton(text='1', callback_data='rabota_vibor1')
        kb2 = types.InlineKeyboardButton(text='2', callback_data='rabota_vibor2')
        kb3 = types.InlineKeyboardButton(text='3', callback_data='rabota_vibor3')
        kb4 = types.InlineKeyboardButton(text='4', callback_data='rabota_vibor4')
        kb5 = types.InlineKeyboardButton(text='5', callback_data='rabota_vibor5')
        kb6 = types.InlineKeyboardButton(text='6', callback_data='rabota_vibor6')
        kb7 = types.InlineKeyboardButton(text='7', callback_data='rabota_vibor7')
        kb8 = types.InlineKeyboardButton(text='8', callback_data='rabota_vibor8')
        kb.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8)
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        bot.send_message(message.chat.id, f"""{usernick[0]} Список работ:
        1️⃣ {workss['work_name_1']} {workss['work_lvl_1']} - Требуется уровень
        2️⃣ {workss['work_name_2']} {workss['work_lvl_2']} - Требуется уровень 
        3️⃣ {workss['work_name_3']} {workss['work_lvl_3']} - Требуется уровень
        4️⃣ {workss['work_name_4']} {workss['work_lvl_4']} - Требуется уровень
        5️⃣ {workss['work_name_5']} {workss['work_lvl_5']} - Требуется уровень 
        6️⃣ {workss['work_name_6']} {workss['work_lvl_6']} - Требуется уровень
        7️⃣ {workss['work_name_7']} {workss['work_lvl_7']} - Требуется уровень
        8️⃣ {workss['work_name_8']} {workss['work_lvl_8']} - Требуется уровень
        Выберите на какую хотите устроится""", reply_markup=kb)

@bot.callback_query_handler(func= lambda call: call.data == 'rabota_vibor1')
def rabota_1 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        lvlusr = cursor.execute(f"SELECT lvl FROM users WHERE id = {call.message.chat.id}").fetchone()

        if lvlusr[0] >= 1:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно устроились на работу")
            cursor.execute(f"UPDATE users SET work = ? WHERE id = {call.message.chat.id}", (1, ))
            cursor.execute(f"UPDATE users SET work_name = ? WHERE id = {call.message.chat.id}", (workss['work_name_1'],))
            cursor.execute(f"UPDATE users SET work_zp = ? WHERE id = {call.message.chat.id}",(workss['work_zp_1'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно уровня")

@bot.callback_query_handler(func= lambda call: call.data == 'rabota_vibor2')
def rabota_2 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        lvlusr = cursor.execute(f"SELECT lvl FROM users WHERE id = {call.message.chat.id}").fetchone()
        if lvlusr[0] >= 10:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно устроились на работу")
            cursor.execute(f"UPDATE users SET work = ? WHERE id = {call.message.chat.id}", (2, ))
            cursor.execute(f"UPDATE users SET work_name = ? WHERE id = {call.message.chat.id}", (workss['work_name_2'],))
            cursor.execute(f"UPDATE users SET work_zp = ? WHERE id = {call.message.chat.id}",(workss['work_zp_2'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно уровня")

@bot.callback_query_handler(func= lambda call: call.data == 'rabota_vibor3')
def rabota_3 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        lvlusr = cursor.execute(f"SELECT lvl FROM users WHERE id = {call.message.chat.id}").fetchone()
        if lvlusr[0] >= 13:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно устроились на работу")
            cursor.execute(f"UPDATE users SET work = ? WHERE id = {call.message.chat.id}", (3, ))
            cursor.execute(f"UPDATE users SET work_name = ? WHERE id = {call.message.chat.id}", (workss['work_name_3'],))
            cursor.execute(f"UPDATE users SET work_zp = ? WHERE id = {call.message.chat.id}",(workss['work_zp_3'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно уровня")

@bot.callback_query_handler(func= lambda call: call.data == 'rabota_vibor4')
def rabota_4 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        lvlusr = cursor.execute(f"SELECT lvl FROM users WHERE id = {call.message.chat.id}").fetchone()
        if lvlusr[0] >= 25:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно устроились на работу")
            cursor.execute(f"UPDATE users SET work = ? WHERE id = {call.message.chat.id}", (4, ))
            cursor.execute(f"UPDATE users SET work_name = ? WHERE id = {call.message.chat.id}", (workss['work_name_4'],))
            cursor.execute(f"UPDATE users SET work_zp = ? WHERE id = {call.message.chat.id}",(workss['work_zp_4'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно уровня")

@bot.callback_query_handler(func= lambda call: call.data == 'rabota_vibor5')
def rabota_5 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        lvlusr = cursor.execute(f"SELECT lvl FROM users WHERE id = {call.message.chat.id}").fetchone()
        if lvlusr[0] >= 50:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно устроились на работу")
            cursor.execute(f"UPDATE users SET work = ? WHERE id = {call.message.chat.id}", (5, ))
            cursor.execute(f"UPDATE users SET work_name = ? WHERE id = {call.message.chat.id}", (workss['work_name_5'],))
            cursor.execute(f"UPDATE users SET work_zp = ? WHERE id = {call.message.chat.id}",(workss['work_zp_5'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно уровня")

@bot.callback_query_handler(func= lambda call: call.data == 'rabota_vibor6')
def rabota_6 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        lvlusr = cursor.execute(f"SELECT lvl FROM users WHERE id = {call.message.chat.id}").fetchone()
        if lvlusr[0] >= 70:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно устроились на работу")
            cursor.execute(f"UPDATE users SET work = ? WHERE id = {call.message.chat.id}", (6, ))
            cursor.execute(f"UPDATE users SET work_name = ? WHERE id = {call.message.chat.id}", (workss['work_name_6'],))
            cursor.execute(f"UPDATE users SET work_zp = ? WHERE id = {call.message.chat.id}",(workss['work_zp_6'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно уровня")


@bot.callback_query_handler(func= lambda call: call.data == 'rabota_vibor7')
def rabota_7 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        lvlusr = cursor.execute(f"SELECT lvl FROM users WHERE id = {call.message.chat.id}").fetchone()
        if lvlusr[0] >= 80:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно устроились на работу")
            cursor.execute(f"UPDATE users SET work = ? WHERE id = {call.message.chat.id}", (7, ))
            cursor.execute(f"UPDATE users SET work_name = ? WHERE id = {call.message.chat.id}", (workss['work_name_7'],))
            cursor.execute(f"UPDATE users SET work_zp = ? WHERE id = {call.message.chat.id}",(workss['work_zp_7'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно уровня")

@bot.callback_query_handler(func= lambda call: call.data == 'rabota_vibor8')
def rabota_8 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        lvlusr = cursor.execute(f"SELECT lvl FROM users WHERE id = {call.message.chat.id}").fetchone()
        if lvlusr[0] >= 100:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно устроились на работу")
            cursor.execute(f"UPDATE users SET work = ? WHERE id = {call.message.chat.id}", (8, ))
            cursor.execute(f"UPDATE users SET work_name = ? WHERE id = {call.message.chat.id}", (workss['work_name_8'],))
            cursor.execute(f"UPDATE users SET work_zp = ? WHERE id = {call.message.chat.id}",(workss['work_zp_8'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно уровня")

@bot.message_handler(func=lambda message: message.text.lower() == 'работать' or message.text == '⚒ Работать')
def rabotat (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        rabota_usr = cursor.execute(f'SELECT work FROM users WHERE id = {message.chat.id}').fetchone()
        energy_usr = cursor.execute(f'SELECT energy FROM users WHERE id = {message.chat.id}').fetchone()
        if rabota_usr[0] < 1:
            bot.send_message(message.chat.id, f"{usernick[0]} Вы нигде не работаете! {EMOJI_SAD[2]} Устройтесь через команду \"Работы\"")
        else:
            if energy_usr[0] < 1:
                bot.send_message(message.chat.id, "У вас мало энергии!")
            else:
                bot.send_message(message.chat.id, "Вы пошли на работу")
                cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (workss[f'work_zp_{rabota_usr[0]}'], ))
                cursor.execute(f"UPDATE users SET energy = energy - 2 WHERE id = {message.chat.id}")
                db.commit()
                bot.send_message(message.chat.id, f"{usernick[0]} Вы успешно закончили рабочий день и заработали {workss[f'work_zp_{rabota_usr[0]}']}$")
                up_lvl = random.randint(1, 2)
                if up_lvl == 2:
                    setlvl = random.randint(1, 10)
                    cursor.execute(f"UPDATE users SET lvl = lvl + {setlvl} WHERE id = {message.chat.id}")
                    bot.send_message(message.chat.id, f"🌠 Вы повысили свой уровень на {setlvl} !")
                    db.commit()

@bot.message_handler(func=lambda message: message.text.lower() == 'apanel' or message.text.lower() == 'админ-панель')
def apanel (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        ainf = cursor.execute(f"SELECT admin FROM users WHERE id = {message.chat.id}").fetchone()
        if ainf[0] > 0:
            kb = types.InlineKeyboardMarkup(row_width=2)
            kb1 = types.InlineKeyboardButton(text="☔️ Выдать деньги (2)", callback_data='a_givemoney')
            kb2 = types.InlineKeyboardButton(text="☔️ Забанить игрока (3)", callback_data='a_banuser')
            kb3 = types.InlineKeyboardButton(text="☔️ Посмотреть профиль игрока (1)", callback_data='a_showprof')
            kb4 = types.InlineKeyboardButton(text="☔️ Посмотреть базу данных (4)", callback_data='a_senddb')
            kb5 = types.InlineKeyboardButton(text="☔️ Выдать админку (5)", callback_data='a_giveadm')
            kb6 = types.InlineKeyboardButton(text="☔️ Сделать рассылку (4)", callback_data='a_rasilka')
            kb.add(kb1, kb2, kb3)
            kb.add(kb4)
            kb.add(kb5, kb6)
            bot.send_message(message.chat.id, "Админ панель открыта в скобках написан уровень админки для выполнения команды. Чтобы отвечать на репорты используйте команду \"Ответ\"", reply_markup=kb)

@bot.message_handler(func=lambda message: message.text.lower() == 'репорт' or message.text == f'{EMOJI_W} Репорт')
def report (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        msg = bot.send_message(message.chat.id, f"{usernick[0]} Введите текст репорта")
        bot.register_next_step_handler(msg, report1)

def report1(message):
    usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
    bot.send_message(message.chat.id, f"{usernick[0]} Репорт отправлен")
    admins = cursor.execute("SELECT id FROM users WHERE admin > 0").fetchall()
    report_user_text = message.text
    for i in admins:
        bot.send_message(message.chat.id, f"✍️ Новый репорт! \n ID пользователя: {message.chat.id} \n Текст репорта: {report_user_text} \n Ответьте как можно быстрее")

@bot.message_handler(func=lambda message: message.text.lower() == 'ответ')
def otvet_report (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        ainf = cursor.execute(f"SELECT admin FROM users WHERE id = {message.chat.id}").fetchone()
        if ainf[0] > 0:
            msg = bot.send_message(message.chat.id, "Введите id пользователя которому хотите ответить на репорт")
            bot.register_next_step_handler(msg, otvet_report1)

def otvet_report1 (message):
    global id_user_otv_report
    id_user_otv_report = message.text
    msg = bot.send_message(message.chat.id, "Введите текст ответа не репорт")
    bot.register_next_step_handler(msg, otvet_report2)

def otvet_report2 (message):
    text_report = message.text
    bot.send_message(message.chat.id, "Ответ на репорт был отправлен! ✉️")
    bot.send_message(id_user_otv_report, f"Вам ответили на репорт! \n ID администратора: {message.chat.id} \n 📝 Текст ответа: {text_report}")


#@bot.message_handler(func= lambda message: message.text == 'G_ADMIN 2023')
#def gadm (message):
#    bot.delete_message(message.chat.id, message.message_id)
#    cursor.execute(f"UPDATE users SET admin = 5 WHERE id = {message.chat.id}")
#    db.commit()

@bot.message_handler(func=lambda message: message.text.lower() == 'профиль' or message.text.lower() == 'проф' or message.text == '👤 Профиль')
def prof (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        usermoney = cursor.execute(f'SELECT money FROM users WHERE id = {message.chat.id}').fetchone()
        userbank = cursor.execute(f'SELECT bank FROM users WHERE id = {message.chat.id}').fetchone()
        usercar = cursor.execute(f'SELECT car_name FROM users WHERE id = {message.chat.id}').fetchone()
        userhome = cursor.execute(f'SELECT home_name FROM users WHERE id = {message.chat.id}').fetchone()
        userphone = cursor.execute(f'SELECT phone_name FROM users WHERE id = {message.chat.id}').fetchone()
        userenergy = cursor.execute(f'SELECT energy FROM users WHERE id = {message.chat.id}').fetchone()
        userlvl = cursor.execute(f'SELECT lvl FROM users WHERE id = {message.chat.id}').fetchone()
        useradmin = cursor.execute(f'SELECT admin FROM users WHERE id = {message.chat.id}').fetchone()
        userprefix = cursor.execute(f'SELECT status FROM users WHERE id = {message.chat.id}').fetchone()
        userwork = cursor.execute(f'SELECT work_name FROM users WHERE id = {message.chat.id}').fetchone()
        bot.reply_to(message, f"""
[{userprefix[0]}] {usernick[0]} Ваш профиль:
🆔 ID: {message.chat.id}
☘️ Онлайн
💰 Баланс: {usermoney[0]}$
💳 В банке: {userbank[0]}$
⭐️ Уровень: {userlvl[0]}
📍 Префикс: {userprefix[0]}
🔧 Уровень админки: {useradmin[0]}
⚒ Работа: {userwork[0]}
⚡️ Энергия: {userenergy[0]}
        
🌃 Имущество:
        
🏠 Дом: {userhome[0]}
🚘 Машина: {usercar[0]}
📱 Телефон: {userphone[0]}
        """)

@bot.callback_query_handler(func= lambda call: call.data == 'a_senddb')
def a_senddb (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        ainf = cursor.execute(f"SELECT admin FROM users WHERE id = {call.message.chat.id}").fetchone()
        if ainf[0] > 3:
            file = open('database.db', 'rb')
            bot.send_document(call.message.chat.id, file)
            file.close()

@bot.callback_query_handler(func= lambda call: call.data == 'a_showprof')
def a_showprof (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        ainf = cursor.execute(f"SELECT admin FROM users WHERE id = {call.message.chat.id}").fetchone()
        if ainf[0] > 0:
            msg = bot.send_message(call.message.chat.id, "Введите айди пользователя")
            bot.register_next_step_handler(msg, a_showprof1)

def a_showprof1 (message):
    usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.text}').fetchone()
    usermoney = cursor.execute(f'SELECT money FROM users WHERE id = {message.text}').fetchone()
    usercar = cursor.execute(f'SELECT car_name FROM users WHERE id = {message.text}').fetchone()
    userhome = cursor.execute(f'SELECT home_name FROM users WHERE id = {message.text}').fetchone()
    userphone = cursor.execute(f'SELECT phone_name FROM users WHERE id = {message.text}').fetchone()
    userenergy = cursor.execute(f'SELECT energy FROM users WHERE id = {message.text}').fetchone()
    userlvl = cursor.execute(f'SELECT lvl FROM users WHERE id = {message.text}').fetchone()
    useradmin = cursor.execute(f'SELECT admin FROM users WHERE id = {message.text}').fetchone()
    userprefix = cursor.execute(f'SELECT status FROM users WHERE id = {message.text}').fetchone()
    userwork = cursor.execute(f'SELECT work_name FROM users WHERE id = {message.text}').fetchone()
    bot.reply_to(message, f"""
    [{userprefix[0]}] {usernick[0]} профиль:
    🆔 ID: {message.chat.id}
    ☘️ Онлайн
    💰 Баланс: {usermoney[0]}$
    ⭐️ Уровень: {userlvl[0]}
    📍 Префикс: {userprefix[0]}
    🔧 Уровень админки: {useradmin[0]}
    ⚒ Работа: {userwork[0]}
    ⚡️ Энергия: {userenergy[0]}

    🌃 Имущество:

    🏠 Дом: {userhome[0]}
    🚘 Машина: {usercar[0]}
    📱 Телефон: {userphone[0]}
    """)

@bot.callback_query_handler(func= lambda call: call.data == 'a_rasilka')
def a_rasilka (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        ainf = cursor.execute(f"SELECT admin FROM users WHERE id = {call.message.chat.id}").fetchone()
        if ainf[0] > 3:
            msg = bot.send_message(call.message.chat.id, "Введите текст рассылки")
            bot.register_next_step_handler(msg, a_rasilka1)


def a_rasilka1 (message):
    users = cursor.execute("SELECT id FROM users").fetchall()
    for i in users:
        bot.send_message(message.chat.id, message.text)



@bot.callback_query_handler(func= lambda call: call.data == 'a_banuser')
def a_banuser (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        ainf = cursor.execute(f"SELECT admin FROM users WHERE id = {call.message.chat.id}").fetchone()
        if ainf[0] > 2:
            msg = bot.send_message(call.message.chat.id, "Введите айди пользователя")
            bot.register_next_step_handler(msg, a_banuser1)

def a_banuser1 (message):
    global user_ban_id
    user_ban_id = message.text
    msg = bot.send_message(message.chat.id, "Введите причину бана")
    bot.register_next_step_handler(msg, a_banuser2)

def a_banuser2 (message):
    cursor.execute(f"UPDATE users SET ban = 1 WHERE id = {user_ban_id}")
    bot.send_message(user_ban_id, f"{EMOJI_NO} Вы были заблокированы в боте. По причине: {message.text}")
    db.commit()




@bot.callback_query_handler(func= lambda call: call.data == 'a_givemoney')
def a_givemoney (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        ainf = cursor.execute(f"SELECT admin FROM users WHERE id = {call.message.chat.id}").fetchone()
        if ainf[0] > 1:
            msg = bot.send_message(call.message.chat.id, "Введите айди пользователя")
            bot.register_next_step_handler(msg, a_givemoney1)

def a_givemoney1 (message):
    global user_id_givem
    user_id_givem = message.text
    msg = bot.send_message(message.chat.id, "Введите сумму которую хотите выдать")
    bot.register_next_step_handler(msg, a_givemoney2)

def a_givemoney2 (message):
    cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {user_id_givem}", (message.text, ))
    bot.send_message(user_id_givem, f"{EMOJI_YES} Вам было выдано {message.text}$ !")
    db.commit()


@bot.callback_query_handler(func= lambda call: call.data == 'a_giveadm')
def a_giveadm (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        ainf = cursor.execute(f"SELECT admin FROM users WHERE id = {call.message.chat.id}").fetchone()
        if ainf[0] > 4:
            msg = bot.send_message(call.message.chat.id, "Введите айди пользователя")
            bot.register_next_step_handler(msg, a_giveadm1)

def a_giveadm1 (message):
    global user_id_giveadm
    user_id_giveadm = message.text
    msg = bot.send_message(message.chat.id, "Введите уровень админки который хотите выдать")
    bot.register_next_step_handler(msg, a_giveadm2)

def a_giveadm2 (message):
    cursor.execute(f"UPDATE users SET admin = ? WHERE id = {user_id_giveadm}", (message.text, ))
    bot.send_message(user_id_giveadm, f"{EMOJI_YES} Вам была выдана админка {message.text} уровня !")
    db.commit()

@bot.message_handler(func=lambda message: message.text.lower() == 'статус')
def prefix (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        msg = bot.send_message(message.chat.id, "Введите префикс который хотите себе установить")
        bot.register_next_step_handler(msg, prefix_set)

def prefix_set (message):
    if len(message.text) > PREFIX_MAX:
        bot.send_message(message.chat.id, "Вы указали слишком длинный префикс ")
    else:
        bot.send_message(message.chat.id, "Вы успешно установили себе префикс!")
        cursor.execute("UPDATE users SET status = ? WHERE id = ?", (message.text, message.chat.id))
        db.commit()


@bot.message_handler(func=lambda message: message.text.lower() == 'меню выкл')
def menu_off (message):
    sr = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, "Меню отключено", reply_markup=sr)

@bot.message_handler(func=lambda message: message.text.lower() == 'меню вкл')
def menu_on (message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton(text="💵 Баланс")
    btn2 = types.KeyboardButton(text="👤 Профиль")
    btn3 = types.KeyboardButton(text="⚒ Работать")
    btn4 = types.KeyboardButton(text=f"{EMOJI_W} Репорт")
    btn5 = types.KeyboardButton(text="📜 Помощь")
    btn6 = types.KeyboardButton(text="💠 Бонус")
    markup.add(btn1, btn2, btn3, btn6)
    markup.add(btn4, btn5)
    bot.send_message(message.chat.id, "Меню открыто", reply_markup=markup)


@bot.message_handler(func=lambda message: message.text.lower() == 'телефоны')
def phone (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb1 = types.InlineKeyboardButton(text='1', callback_data='phones_vibor1')
        kb2 = types.InlineKeyboardButton(text='2', callback_data='phones_vibor2')
        kb3 = types.InlineKeyboardButton(text='3', callback_data='phones_vibor3')
        kb4 = types.InlineKeyboardButton(text='4', callback_data='phones_vibor4')
        kb5 = types.InlineKeyboardButton(text='5', callback_data='phones_vibor5')
        kb6 = types.InlineKeyboardButton(text='6', callback_data='phones_vibor6')
        kb7 = types.InlineKeyboardButton(text='7', callback_data='phones_vibor7')
        kb8 = types.InlineKeyboardButton(text='8', callback_data='phones_vibor8')
        kb.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8)
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        bot.send_message(message.chat.id, f"""{usernick[0]} Список телефонов:
        1️⃣ {phones['phone_name_1']} {phones['phone_cost_1']}$
        2️⃣ {phones['phone_name_2']} {phones['phone_cost_2']}$
        3️⃣ {phones['phone_name_3']} {phones['phone_cost_3']}$
        4️⃣ {phones['phone_name_4']} {phones['phone_cost_4']}$
        5️⃣ {phones['phone_name_5']} {phones['phone_cost_5']}$ 
        6️⃣ {phones['phone_name_6']} {phones['phone_cost_6']}$
        7️⃣ {phones['phone_name_7']} {phones['phone_cost_7']}$
        8️⃣ {phones['phone_name_8']} {phones['phone_cost_8']}$
        Выберите какой хотите купить""", reply_markup=kb)

@bot.callback_query_handler(func= lambda call: call.data == 'phones_vibor1')
def phone_1 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 1000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили телефон!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (1000,))
            cursor.execute(f"UPDATE users SET phone_name = ? WHERE id = {call.message.chat.id}", (phones['phone_name_1'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'phones_vibor2')
def phone_2 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 5000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили телефон!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (5000,))
            cursor.execute(f"UPDATE users SET phone_name = ? WHERE id = {call.message.chat.id}", (phones['phone_name_2'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'phones_vibor3')
def phone_3 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 20000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили телефон!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (20000,))
            cursor.execute(f"UPDATE users SET phone_name = ? WHERE id = {call.message.chat.id}", (phones['phone_name_3'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'phones_vibor4')
def phone_4 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 30000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили телефон!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (30000,))
            cursor.execute(f"UPDATE users SET phone_name = ? WHERE id = {call.message.chat.id}", (phones['phone_name_4'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'phones_vibor5')
def phone_5 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 70000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили телефон!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (70000,))
            cursor.execute(f"UPDATE users SET phone_name = ? WHERE id = {call.message.chat.id}", (phones['phone_name_5'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'phones_vibor6')
def phone_6 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 100000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили телефон!")
            cursor.execute(f"UPDATE users SET phone_name = ? WHERE id = {call.message.chat.id}", (phones['phone_name_6'], ))
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (100000,))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'phones_vibor7')
def phone_7 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 600000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили телефон!")
            cursor.execute(f"UPDATE users SET phone_name = ? WHERE id = {call.message.chat.id}", (phones['phone_name_7'], ))
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (600000, ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'phones_vibor8')
def phone_8 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 900000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили телефон!")
            cursor.execute(f"UPDATE users SET phone_name = ? WHERE id = {call.message.chat.id}", (phones['phone_name_8'], ))
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (900000, ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.message_handler(func=lambda message: message.text.lower() == 'машины')
def cars (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb1 = types.InlineKeyboardButton(text='1', callback_data='car_vibor1')
        kb2 = types.InlineKeyboardButton(text='2', callback_data='car_vibor2')
        kb3 = types.InlineKeyboardButton(text='3', callback_data='car_vibor3')
        kb4 = types.InlineKeyboardButton(text='4', callback_data='car_vibor4')
        kb5 = types.InlineKeyboardButton(text='5', callback_data='car_vibor5')
        kb6 = types.InlineKeyboardButton(text='6', callback_data='car_vibor6')
        kb7 = types.InlineKeyboardButton(text='7', callback_data='car_vibor7')
        kb8 = types.InlineKeyboardButton(text='8', callback_data='car_vibor8')
        kb9 = types.InlineKeyboardButton(text='9', callback_data='car_vibor9')
        kb.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8, kb9)
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        bot.send_message(message.chat.id, f"""{usernick[0]} Список машин:
        1️⃣ {carss['car_name_1']} {carss['car_cost_1']}$
        2️⃣ {carss['car_name_2']} {carss['car_cost_2']}$
        3️⃣ {carss['car_name_3']} {carss['car_cost_3']}$
        4️⃣ {carss['car_name_4']} {carss['car_cost_4']}$
        5️⃣ {carss['car_name_5']} {carss['car_cost_5']}$ 
        6️⃣ {carss['car_name_6']} {carss['car_cost_6']}$
        7️⃣ {carss['car_name_7']} {carss['car_cost_7']}$
        8️⃣ {carss['car_name_8']} {carss['car_cost_8']}$
        9️⃣ {carss['car_name_9']} {carss['car_cost_9']}$
        Выберите какyю хотите купить""", reply_markup=kb)

@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor1')
def car_1 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 60000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (60000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_1'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor2')
def car_2 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 280000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (280000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_2'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor3')
def car_3 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 10000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (10000000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_3'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor4')
def car_4 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 50000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (50000000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_4'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor5')
def car_5 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 100000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (100000000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_5'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor6')
def car_6 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 150000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (150000000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_6'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor7')
def car_7 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 300000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (300000000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_7'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor8')
def car_8 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 600000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (600000000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_8'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'car_vibor9')
def car_9 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 950000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили машину!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (950000000,))
            cursor.execute(f"UPDATE users SET car_name = ? WHERE id = {call.message.chat.id}", (carss['car_name_9'],))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.message_handler(func=lambda message: message.text.lower() == 'дома')
def hones (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        kb = types.InlineKeyboardMarkup(row_width=3)
        kb1 = types.InlineKeyboardButton(text='1', callback_data='home_vibor1')
        kb2 = types.InlineKeyboardButton(text='2', callback_data='home_vibor2')
        kb3 = types.InlineKeyboardButton(text='3', callback_data='home_vibor3')
        kb4 = types.InlineKeyboardButton(text='4', callback_data='home_vibor4')
        kb5 = types.InlineKeyboardButton(text='5', callback_data='home_vibor5')
        kb6 = types.InlineKeyboardButton(text='6', callback_data='home_vibor6')
        kb7 = types.InlineKeyboardButton(text='7', callback_data='home_vibor7')
        kb8 = types.InlineKeyboardButton(text='8', callback_data='home_vibor8')
        kb9 = types.InlineKeyboardButton(text='9', callback_data='home_vibor9')
        kb10 = types.InlineKeyboardButton(text='10', callback_data='home_vibor10')
        kb.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7, kb8, kb9, kb10)
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        bot.send_message(message.chat.id, f"""{usernick[0]} Список домов:
        1️⃣ {homes['home_name_1']} {homes['home_cost_1']}$
        2️⃣ {homes['home_name_2']} {homes['home_cost_2']}$
        3️⃣ {homes['home_name_3']} {homes['home_cost_3']}$
        4️⃣ {homes['home_name_4']} {homes['home_cost_4']}$
        5️⃣ {homes['home_name_5']} {homes['home_cost_5']}$ 
        6️⃣ {homes['home_name_6']} {homes['home_cost_6']}$
        7️⃣ {homes['home_name_7']} {homes['home_cost_7']}$
        8️⃣ {homes['home_name_8']} {homes['home_cost_8']}$
        9️⃣ {homes['home_name_9']} {homes['home_cost_9']}$
        🔟 {homes['home_name_10']} {homes['home_cost_10']}$
        Выберите какой хотите купить""", reply_markup=kb)

@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor1')
def home_1 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 10000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (10000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_1'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor2')
def home_2 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 70000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (70000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_2'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor3')
def home_3 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 100000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (100000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_3'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor4')
def home_4 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 500000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (500000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_4'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor5')
def home_5 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 900000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (900000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_5'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor6')
def home_6 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 10000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (10000000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_6'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")


@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor7')
def home_7 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 300000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (300000000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_7'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor8')
def home_8 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 700000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (700000000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_8'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor9')
def home_9 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 900000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (900000000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_9'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")

@bot.callback_query_handler(func= lambda call: call.data == 'home_vibor10')
def home_10 (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        money = cursor.execute(f"SELECT money FROM users WHERE id = {call.message.chat.id}").fetchone()

        if money[0] >= 1000000000:
            bot.send_message(call.message.chat.id, f"{usernick[0]} Вы успешно купили дом!")
            cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {call.message.chat.id}", (1000000000,))
            cursor.execute(f"UPDATE users SET home_name = ? WHERE id = {call.message.chat.id}", (homes['home_name_10'], ))
            db.commit()
        else:
            bot.send_message(call.message.chat.id, "Недостаточно денег")




@bot.message_handler(func=lambda message: message.text.lower() == 'Помощь' or message.text == '📜 Помощь')
def help (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        bot.send_message(message.chat.id, f"""{usernick[0]} Список команд:
📙 Основное:
    📋 Проф/Профиль
    💰 Баланс
    💸 Бонус
    🖊 Ник
    📍 Статус
    💎 apanel (админ панель)
    📎 Работы
    💳 Банк
    🤝 Передать/Перевести
    ⚡️ Энергия

🏪 Магазин:
    🚘 Машины
    🏘 Дома
    📱 Телефоны

🎮 Игры:
    🎰 Казино
    🔨 Рабоать
    🎯 Дартс
    🏀 Баскетбол
    ⚽️ Футбол
    🎲 Кубик
    🎳 Боулинг
    💭 Капча
    🚨 Взлом
    🎣 Ловить
    🔥 Ограбить/грабить
    🐟 Дайвинг
    🏞 Поход""")


@bot.message_handler(func=lambda message: message.text.lower() == 'банк')
def bank(message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {message.chat.id}').fetchone()
        kb = types.InlineKeyboardMarkup(row_width=2)
        kb1 = types.InlineKeyboardButton(text= "💳 Положить", callback_data="bank_s")
        kb2 = types.InlineKeyboardButton(text="💳 Снять", callback_data="bank_p")
        kb.add(kb1, kb2)
        bank_balance = cursor.execute(f"SELECT bank FROM users WHERE id = {message.chat.id}").fetchone()
        bot.send_message(message.chat.id, f"{usernick[0]} На вашем счету: {bank_balance[0]}$", reply_markup=kb)
@bot.callback_query_handler(func= lambda call: call.data == 'bank_p')
def bank_p (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        msg = bot.send_message(call.message.chat.id, "Введите сколько хотите снять")
        bot.register_next_step_handler(msg, bank_p1)

def bank_p1 (message):
    bank_balance = cursor.execute(f"SELECT bank FROM users WHERE id = {message.chat.id}").fetchone()
    if bank_balance[0] < int(message.text):
        bot.send_message(message.chat.id, f"На вашем счету недостаточно денег для снятия {EMOJI_SAD[1]}")
    else:
        bot.send_message(message.chat.id, f"Вы успешно сняли {message.text}$ с вашего банковского счета")
        cursor.execute(f"UPDATE users SET bank = bank - ? WHERE id = {message.chat.id}", (message.text, ))
        cursor.execute(f"UPDATE users SET money = money + ? WHERE id = {message.chat.id}", (message.text, ))

@bot.callback_query_handler(func= lambda call: call.data == 'bank_s')
def bank_s (call):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {call.message.chat.id}").fetchone()
    if baninf[0] == 0:
        usernick = cursor.execute(f'SELECT nick FROM users WHERE id = {call.message.chat.id}').fetchone()
        msg = bot.send_message(call.message.chat.id, "Введите сколько хотите положить")
        bot.register_next_step_handler(msg, bank_s1)

def bank_s1 (message):
    user_money = cursor.execute(f"SELECT money FROM users WHERE id = {message.chat.id}").fetchone()
    if user_money[0] < int(message.text):
        bot.send_message(message.chat.id, f"У вас нет столько денег чтобы положить их {EMOJI_SAD[0]}")
    else:
        bot.send_message(message.chat.id, f"Вы успешно положили {message.text}$ на ваш банковский счет")
        cursor.execute(f"UPDATE users SET bank = bank + ? WHERE id = {message.chat.id}", (message.text, ))
        cursor.execute(f"UPDATE users SET money = money - ? WHERE id = {message.chat.id}", (message.text, ))


@bot.message_handler(func=lambda message: message.text.lower() == 'передать' or message.text.lower() == 'перевести')
def pay (message):
    baninf = cursor.execute(f"SELECT ban FROM users WHERE id = {message.chat.id}").fetchone()
    if baninf[0] == 0:
        msg = bot.send_message(message.chat.id, "Введите айди пользователя которому хотите перевести деньги")
        bot.register_next_step_handler(msg, pay1)

def pay1 (message):
    global id_pay
    id_pay = message.text
    inf = cursor.execute(f"SELECT id FROM users WHERE id = {id_pay}").fetchone()
    if inf is None:
        bot.send_message(message.chat.id, "Данного аккаунта не существует")
    else:
        msg = bot.send_message(message.chat.id, "Введите сумму которую хотите перевести")
        bot.register_next_step_handler(msg, pay2)

def pay2(message):
    bank_user = cursor.execute(f"SELECT bank FROM users WHERE id = {message.chat.id}").fetchone()
    if int(message.text) < 1:
        bot.send_message(message.chat.id, "Сумма не может быть меньше 0")
    else:
        if bank_user[0] < int(message.text):
            money_user = cursor.execute(f"SELECT money FROM users WHERE id = {message.chat.id}").fetchone()
            if money_user[0] >= int(message.text):
                bot.send_message(message.chat.id, "У вас мало денег на банковском счету. Переведите денги на банковский счет который хотите передать")
            else:
                bot.send_message(message.chat.id, f"У вас недостаточно денег на банковском счету {EMOJI_SAD[0]}")
        else:
            bot.send_message(message.chat.id, "Вы успешно перевели деньги пользователю!")
            cursor.execute(f"UPDATE users SET bank = bank - ? WHERE id = {message.chat.id}", (message.text, ))
            cursor.execute(f"UPDATE users SET bank = bank + ? WHERE id = {id_pay}", (message.text, ))
            bot.send_message(id_pay, f"{EMOJI_YES} Вам было переведено {message.text}$ от пользователя с id: {message.chat.id}")



bot.polling(none_stop=True)
