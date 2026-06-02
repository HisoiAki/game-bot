import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8827039955:AAEtx_0O9nwWntBF7-xJRUJY60U5cC4Tjxk'
bot = telebot.TeleBot(TOKEN)

user_data = {}

# ========== КЛАВИАТУРЫ ==========
def get_yes_no():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Да", "Нет")
    return markup

def get_q1():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Экшен", "РПГ", "Стратегия", "Приключения", "Гонки", "Хоррор", "Симулятор")
    return markup

def get_q2():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Одиночная", "Многопользовательская")
    return markup

def get_q3():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Да, важен", "Не важен")
    return markup

def get_q4():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Простая", "Средняя", "Сложная")
    return markup

def get_q5():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("До 30 минут", "1-2 часа", "Могу играть часами")
    return markup

def get_q6():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Графика", "Геймплей", "Атмосфера", "Общение с друзьями")
    return markup

def get_q7():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Открытый мир", "Линейный", "Песочница")
    return markup

def get_q8():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Киберпанк", "Фэнтези", "Реализм", "Постапокалипсис", "Космос")
    return markup

def get_q9():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Фармить ресурсы", "Короткие забеги", "Глубокий сюжет")
    return markup

def get_q10():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Да", "Всё равно", "Нет")
    return markup

# ========== СТАРТ ==========
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    user_data[uid] = {'step': 0}
    bot.send_message(uid, "🎮 Привет! Я подберу игру по твоим предпочтениям.\n\nОтветь на 10 вопросов. Начнём?", reply_markup=get_yes_no())

# ========== ЛОГИКА ==========
@bot.message_handler(func=lambda message: True)
def handle(message):
    uid = message.chat.id
    text = message.text

    if uid not in user_data:
        bot.send_message(uid, "Напиши /start")
        return

    step = user_data[uid]['step']

    if step == 0:
        if text == "Да":
            user_data[uid]['step'] = 1
            bot.send_message(uid, "1️⃣ Любимый жанр?", reply_markup=get_q1())
        else:
            bot.send_message(uid, "Жми /start, когда захочешь")
            del user_data[uid]
        return

    if step == 1:
        user_data[uid]['genre'] = text
        user_data[uid]['step'] = 2
        bot.send_message(uid, "2️⃣ Одиночная или многопользовательская?", reply_markup=get_q2())
        return

    if step == 2:
        user_data[uid]['mode'] = text
        user_data[uid]['step'] = 3
        bot.send_message(uid, "3️⃣ Сюжет важен?", reply_markup=get_q3())
        return

    if step == 3:
        user_data[uid]['story'] = text
        user_data[uid]['step'] = 4
        bot.send_message(uid, "4️⃣ Какую сложность предпочитаешь?", reply_markup=get_q4())
        return

    if step == 4:
        user_data[uid]['difficulty'] = text
        user_data[uid]['step'] = 5
        bot.send_message(uid, "5️⃣ Сколько времени обычно играешь?", reply_markup=get_q5())
        return

    if step == 5:
        user_data[uid]['time'] = text
        user_data[uid]['step'] = 6
        bot.send_message(uid, "6️⃣ Что для тебя важнее?", reply_markup=get_q6())
        return

    if step == 6:
        user_data[uid]['priority'] = text
        user_data[uid]['step'] = 7
        bot.send_message(uid, "7️⃣ Какой тип мира?", reply_markup=get_q7())
        return

    if step == 7:
        user_data[uid]['world'] = text
        user_data[uid]['step'] = 8
        bot.send_message(uid, "8️⃣ Любимый сеттинг?", reply_markup=get_q8())
        return

    if step == 8:
        user_data[uid]['setting'] = text
        user_data[uid]['step'] = 9
        bot.send_message(uid, "9️⃣ Что тебе ближе?", reply_markup=get_q9())
        return

    if step == 9:
        user_data[uid]['playstyle'] = text
        user_data[uid]['step'] = 10
        bot.send_message(uid, "🔟 Любишь соревноваться?", reply_markup=get_q10())
        return

    if step == 10:
        user_data[uid]['competitive'] = text

        genre = user_data[uid].get('genre')
        mode = user_data[uid].get('mode')
        story = user_data[uid].get('story')
        difficulty = user_data[uid].get('difficulty')
        priority = user_data[uid].get('priority')
        setting = user_data[uid].get('setting')

        # ========== ПОДБОР ИГР ==========
        games = []

        if genre == "РПГ" and story == "Да, важен":
            games += ["The Witcher 3", "Cyberpunk 2077", "Baldur's Gate 3"]
        elif genre == "РПГ":
            games += ["Elden Ring", "Skyrim", "Disco Elysium"]

        if genre == "Экшен":
            if mode == "Многопользовательская":
                games += ["Counter-Strike 2", "Apex Legends", "Call of Duty"]
            else:
                games += ["God of War Ragnarök", "Resident Evil 4", "Doom Eternal"]

        if genre == "Стратегия":
            games += ["Civilization VI", "Age of Empires IV", "StarCraft II"]

        if genre == "Приключения":
            games += ["Red Dead Redemption 2", "Horizon Forbidden West", "The Last of Us"]

        if genre == "Гонки":
            games += ["Forza Horizon 5", "Need for Speed Unbound", "Trackmania"]

        if genre == "Хоррор":
            games += ["Resident Evil Village", "Silent Hill 2", "Outlast"]

        if genre == "Симулятор":
            games += ["Microsoft Flight Simulator", "Farming Simulator", "Euro Truck Simulator 2"]

        if setting == "Киберпанк":
            games += ["Cyberpunk 2077", "Deus Ex", "Ghostrunner"]
        if setting == "Фэнтези":
            games += ["The Witcher 3", "Elden Ring", "Baldur's Gate 3"]
        if setting == "Космос":
            games += ["Mass Effect", "Starfield", "Dead Space"]

        if mode == "Многопользовательская":
            games += ["Dota 2", "CS2", "Valorant"]

        if not games:
            games = ["Roblox", "Minecraft", "Genshin Impact"]

        games = list(dict.fromkeys(games))[:8]

        result = "🎉 Тебе подойдут:\n\n• " + "\n• ".join(games)

        bot.send_message(uid, result + "\n\nНапиши /start чтобы подобрать другую игру")
        del user_data[uid]
        return

print("✅ Бот запущен")
bot.infinity_polling()
