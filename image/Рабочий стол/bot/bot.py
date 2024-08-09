import telebot
from telebot import types

# Замените 'YOUR_API_TOKEN' на ваш реальный API токен
bot = telebot.TeleBot('7296845868:AAFWvXxzvSeFvN4DEekD9FJDKIZWd_LDoFE')

if usd_or_rub.lower() == "usd":
    сurrency_sign = "$"
elif usd_or_rub.lower() == "rub":
    сurrency_sign = "₽"


def get_price():
    if currency.upper() == "BTC":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=bitcoin").json()
    elif currency.upper() == "ETH":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=ethereum").json()
    elif currency.upper() == "USDT":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=tether").json()
    elif currency.upper() == "BNB":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=binancecoin").json()
    elif currency.upper() == "SOL":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=solana").json()
    elif currency.upper() == "XRP":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=ripple").json()
    elif currency.upper() == "ADA":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=cardano").json()
    elif currency.upper() == "DOGE":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=dogecoin").json()
    elif currency.upper() == "TON":
        response = requests.get(
            f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={usd_or_rub}&ids=the-open-network").json()
    price = response[0]["current_price"]
    return price

async def main_message(user_id):
    try:
        referrals = len(await select_user_id_where_referrer_id_and_referrer_bonus_1(user_id))
    except:
        referrals = 0
    await bot.send_message(user_id,
        "<b>🥳 Дарите подарки и зарабатывайте</b>\n\n"
        f"<b>Отправляйте друзьям подарки и получайте криптовалюту. Вывод станет доступен при накоплении <code>{minimal_withdrawal_amount} {currency}</code> на балансе.</b>\n\n"
        f"<b>Ваша реферальная ссылка:</b>\n"
        f"<b><code>https://t.me/{(await bot.get_me())['username']}?start={user_id}</code></b>\n\n"
        f"<b>Ваша дата регистрации в боте: <code>{await select_entry_date_where_user_id(user_id)}</code> (По МСК)</b>\n\n"
        f"<b>Наш <a href='https://t.me/{channel[1:]}'>канал</a> в Телеграмме:</b>\n"
        f"<b><code>https://t.me/{channel[1:]}</code></b>\n\n"
        f"<b>У вас <code>{referrals}</code> подтвержденных рефералов</b>\n\n"
        f"<b>Ваш баланс: <code>{float((Decimal(await select_user_balance_where_user_id(user_id))).quantize(Decimal('1.1000000')))} {currency}</code>   (<code>{float((Decimal(await select_user_balance_where_user_id(user_id)) * Decimal(get_price())).quantize(Decimal('1.10')))}{сurrency_sign}</code>)</b>\n\n"
        f"<b>Ваш ID: <code>{user_id}</code></b>",
            reply_markup=await main_menu_keyboard())

async def no_follow_message(user_id):
    await bot.send_message(user_id,
        f"<b>Ваш друг отправил вам несколько монет {currency}, чтобы получить их подпишитесь на <a href='https://t.me/{channel[1:]}'>канал</a> затем нажмите эту кнопку.</b>\n\n"
        f"<b>{channel}</b>",
            reply_markup=await update_follow_menu_keyboard(channel))



@dp.message_handler(commands="admin")
async def admin_menu(message: types.Message):
    user_id = message.from_user.id
    await message.delete()
    for i in range(0, len(admins_id)):
        if user_id == admins_id[i]:
            await bot.send_message(user_id,
                "<b>Включено админ меню</b>",
                    reply_markup=await admin_menu_keyboard())


@dp.message_handler(commands="start")
async def start_command(message: types.Message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    if await select_user_id_where_user_id(user_id) is None:
        try:
            referrer = int(message.text.split()[1])
            if user_id != referrer:
                referrer_bonus = 0
            else:
                referrer = None
                referrer_bonus = 1
        except:
            referrer = None
            referrer_bonus = 1
        try:
            user_username = user_username.lower()
        except:
            user_username = None
        await adding_data(user_id, user_username, referrer, referrer_bonus, datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if user_channel_status["status"] != "left":
        await main_message(user_id)
    else:
        await no_follow_message(user_id)


### ---___--- ЮЗЕР МЕНЮ ---___--- ###


@dp.callback_query_handler(text="update_balance")
async def update_balance_call(call: types.CallbackQuery):
    await call.message.delete()
    user_id = call.from_user.id
    user_username = call.from_user.username
    try:
        user_username = user_username.lower()
    except:
        user_username = None
    await changing_username_where_user_id(user_username, user_id)
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if user_channel_status["status"] != "left":
        await main_message(user_id)
    else:
        await no_follow_message(user_id)

@dp.callback_query_handler(text="withdraw_funds")
async def withdraw_funds_call(call: types.CallbackQuery):
    user_id = call.from_user.id
    if await select_user_balance_where_user_id(user_id) < minimal_withdrawal_amount:
        await bot.answer_callback_query(call.id, text=
            "Недостаточно средств.")
    else:
        await bot.send_message(user_id,
            "Введите сумму вывода баланса",
            reply_markup=await deleted_message_menu_keyboard())
        await withdrawal_of_balance.withdrawal_amount_state.set()


@dp.callback_query_handler(text="update_follow")
async def update_follow_call(call: types.CallbackQuery):
    await call.message.delete()
    user_id = call.from_user.id
    user_username = call.from_user.username
    user_channel_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
    if user_channel_status["status"] != "left":
        if await select_referrer_bonus_where_user_id(user_id) == 0:
            await adding_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))
            await changing_referrer_bonus_where_user_id(1, user_id)
            await main_message(user_id)
            try:
                await bot.send_message(await select_referrer_id_where_user_id(user_id),
                    f"<b>У вас новый Реферал ({user_username.lower()}), ваш баланс пополнен на <code>{amount_per_one} {currency}</code></b>\n"
                    f"<b>Ваш баланс: <code>{float(Decimal(await select_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))).quantize(Decimal('1.1000000')))} {currency}</code>   ({float(Decimal((Decimal(await select_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))) * Decimal(get_price()))).quantize(Decimal('1.10')))}{сurrency_sign})</b>",
                        reply_markup=await deleted_message_menu_keyboard())
            except:
                await bot.send_message(await select_referrer_id_where_user_id(user_id),
                    f"<b>У вас новый Реферал ({user_id}), ваш баланс пополнен на <code>{amount_per_one} {currency}</code></b>\n"
                    f"<b>Ваш баланс: <code>{float(Decimal(await select_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))).quantize(Decimal('1.1000000')))} {currency}</code>   ({float(Decimal((Decimal(await select_user_balance_where_user_id(await select_referrer_id_where_user_id(user_id))) * Decimal(get_price()))).quantize(Decimal('1.10')))}{сurrency_sign})</b>",
                        reply_markup=await deleted_message_menu_keyboard())
    else:
        await no_follow_message(user_id)


@dp.message_handler(state=withdrawal_of_balance.withdrawal_amount_state)
async def withdraw_funds_call(message: types.Message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    withdrawal_amount = message.text
    if await select_user_balance_where_user_id(user_id) > float(withdrawal_amount) > minimal_withdrawal_amount:
        await changing_user_balance_where_user_id((await select_user_balance_where_user_id(user_id) - float(withdrawal_amount)), user_id)
        await message.delete()
        await bot.send_message(user_id,
            "<b>Заявка на вывод средств:</b>\n"
            f"<b>Сумма: <code>{withdrawal_amount} {currency}</code></b>\n"
            f"<b>Ваш ID: {user_id}</b>\n"
            f"<b>В случае каких либо проблем с выводом необходимо обратиться: {admin_username}</b>\n",
                reply_markup=await deleted_message_menu_keyboard())
        for i in range(0, len(admins_id)):
            if user_id == admins_id[i]:
                await bot.send_message(user_id,
                    f"<b>Пользователь @{user_username} ({user_id}) хочет вывести {withdrawal_amount} {currency}</b>",
                        reply_markup=await deleted_message_menu_keyboard())
    else:
        if float(withdrawal_amount) > await select_user_balance_where_user_id(user_id):
            await message.delete()
            await bot.send_message(user_id,
                "Не достаточно средств",
                    reply_markup=await deleted_message_menu_keyboard())
        elif minimal_withdrawal_amount > float(withdrawal_amount):
            await message.delete()
            await bot.send_message(user_id,
                f"Минимальная сумма вывода средств: {minimal_withdrawal_amount}",
                    reply_markup=await deleted_message_menu_keyboard())


### ---___--- АДМИН МЕНЮ ---___--- ###


@dp.callback_query_handler(text="number_users")
async def number_users_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_message(user_id,
        f"<b>Всего пользователей</b>: {len(await select_all_user_id())}",
            reply_markup=await info_menu_keyboard())


@dp.callback_query_handler(text="update_info")
async def update_number_users_admin(call: types.CallbackQuery):
    await call.message.delete()
    user_id = call.from_user.id
    await bot.send_message(user_id,
        f"<b>Всего пользователей: {len(await select_all_user_id())}</b>",
            reply_markup=await info_menu_keyboard())


@dp.callback_query_handler(text="download_database")
async def download_database_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_document(user_id,
        open("database.db", "rb"),
            reply_markup=await deleted_message_menu_keyboard())


@dp.callback_query_handler(text="private_message")
async def private_message_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_message(user_id,
        "<b>Введите ID пользователя, либо Username</b>",
            reply_markup=await deleted_message_menu_keyboard())
    await private_message.id_or_username_state.set()


@dp.callback_query_handler(text="mailing")
async def send_all_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_message(user_id,
        "<b>Введите сообещние для рассылки</b>",
            reply_markup=await deleted_message_menu_keyboard())
    await receiving_a_message.receiving_message_state.set()


@dp.callback_query_handler(text="changing_balance")
async def changing_balance_admin(call: types.CallbackQuery):
    user_id = call.from_user.id
    await bot.send_message(user_id,
        "<b>Введите ID пользователя, либо Username</b>",
            reply_markup=await deleted_message_menu_keyboard())
    await changing_the_balance.id_or_username_state.set()


@dp.message_handler(state=private_message.id_or_username_state)
async def private_message_id_or_username_admin_handler(message: types.Message, state: FSMContext):
    await message.delete()
    username_or_id = message.text
    if username_or_id.isnumeric():
        try:
            if username_or_id == str((await select_user_id_where_user_id(username_or_id))[0]):
                await state.update_data(username_or_id=username_or_id)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            text="<b>Введите сообщение для отправки</b>",
                                            reply_markup=await deleted_message_menu_keyboard())
                await private_message.private_message_state.set()
        except:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                        text="<b>Пользователь не найден</b>",
                                        reply_markup=await deleted_message_menu_keyboard())
            await state.finish()
    else:
        try:
            username_or_id = username_or_id.replace("@", "").lower()
            if username_or_id == str(await select_user_username_where_user_name(username_or_id)):
                await state.update_data(username_or_id=username_or_id)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            text="<b>Введите сообщение для отправки</b>",
                                            reply_markup=await deleted_message_menu_keyboard())
                await private_message.private_message_state.set()
        except:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                        text="<b>Пользователь не найден</b>",
                                        reply_markup=await deleted_message_menu_keyboard())
            await state.finish()


@dp.message_handler(state=private_message.private_message_state)
async def private_message_private_message_admin_handler(message: types.Message, state: FSMContext):
    private_message_text = message.text
    await message.delete()
    data = await state.get_data()
    username_or_id = data.get("username_or_id")
    if username_or_id.isnumeric():
        await bot.send_message(username_or_id,
            private_message_text,
                reply_markup=await deleted_message_menu_keyboard())
    else:
        username_or_id = await select_user_id_where_user_username(username_or_id)
        await bot.send_message(username_or_id,
            private_message_text,
                reply_markup=await deleted_message_menu_keyboard())

    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 2,
                                text=f"<b>Пользователю {username_or_id} отправили сообщение {private_message_text}</b>",
                                reply_markup=await deleted_message_menu_keyboard())
    await state.finish()


@dp.message_handler(state=receiving_a_message.receiving_message_state)
async def receiving_a_message_receiving_message_admin_handler(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    text = message.text
    await state.finish()
    await message.delete()
    for users in await select_all_user_id():
        try:
            await bot.send_message(chat_id=users[0], text=text,
                                   reply_markup=await deleted_message_menu_keyboard())
        except:
            pass
    await bot.send_message(user_id, "<b>Массовая рассылка успешно завершена!</b>",
                           reply_markup=await deleted_message_menu_keyboard())


@dp.message_handler(state=changing_the_balance.id_or_username_state)
async def changing_the_balance_id_or_username_admin_handler(message: types.Message, state: FSMContext):
    username_or_id = message.text
    await message.delete()
    username_or_id = username_or_id.replace("@", "").lower()
    if username_or_id.isnumeric():
        try:
            if username_or_id == str((await select_user_id_where_user_id(username_or_id))[0]):
                await state.update_data(username_or_id=username_or_id)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            text="<b>Введите число на какое изменить баланс</b>",
                                            reply_markup=await deleted_message_menu_keyboard())
                await changing_the_balance.change_amount_state.set()
        except:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                        text="<b>Пользователь не найден</b>",
                                        reply_markup=await deleted_message_menu_keyboard())
            await state.finish()
    else:
        try:
            if username_or_id == str(await select_user_username_where_user_name(username_or_id)):
                await state.update_data(username_or_id=username_or_id)
                await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                            text="<b>Введите число на какое изменить баланс</b>",
                                            reply_markup=await deleted_message_menu_keyboard())
                await changing_the_balance.change_amount_state.set()
        except:
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 1,
                                        text="<b>Пользователь не найден</b>",
                                        reply_markup=await deleted_message_menu_keyboard())
            await state.finish()


@dp.message_handler(state=changing_the_balance.change_amount_state)
async def changing_the_balance_change_amount_admin_handler(message: types.Message, state: FSMContext):
    change_amount_state = message.text
    await message.delete()
    await state.update_data(change_amount=change_amount_state)
    data = await state.get_data()
    username_or_id = data.get("username_or_id")
    change_amount_state = data.get("change_amount")
    if username_or_id.isnumeric():
        await changing_user_balance_where_user_id(change_amount_state, username_or_id)
    else:
        await changing_user_balance_where_user_username(change_amount_state, username_or_id)
    await bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id - 2,
                                text=f"<b>У пользователя {username_or_id} баланс {change_amount_state}</b>",
                                reply_markup=await deleted_message_menu_keyboard())
    await state.finish()


### ---___--- УДАЛЕНИЕ СООБЩЕНИЙ ---___--- ###


@dp.callback_query_handler(text="deleted_message", state="*")
async def deleted_message_call(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.delete()


### ---___--- ИНЛАЙН СООБЩЕНИЯ ---___--- ###


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    all_text = ["🥳 Хочу подарить тебе немного криптовалюты",
                f"🥳 Привет, хочу подарить тебе немного криптовалюты {currency}",
                f"🥳 Привет, мне тоже захотелось присоединиться к этому тренду и подарить тебе немного криптовалюты {currency}",
                f"🥳 Привет, у меня для тебя есть подарок — немного криптовалюты {currency}"]

    random_text = random.choice(all_text)
    text = query.query or "echo"
    result_id: str = hashlib.md5(text.encode()).hexdigest()

    articles = [types.InlineQueryResultArticle(
        id=result_id,
        title=random_text,
        reply_markup=await get_gift_menu_keyboard((await bot.get_me())["username"], query.from_user.id),
        input_message_content=types.InputMessageContent(
            message_text=random_text))]
    await query.answer(articles, cache_time=1, is_personal=True)





if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_database())
    executor.start_polling(dp)
