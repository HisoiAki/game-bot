import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8827039955:AAEtx_0O9nwWntBF7-xJRUJY60U5cC4Tjxk'
bot = telebot.TeleBot(TOKEN)

user_data = {}

# ========== КЛАВИАТУРЫ ==========
def get_yes_no():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Давай", "Не сейчас")
    return markup

def get_q1():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Экшен", "РПГ", "Стратегия", "Приключения", "Гонки", "Хоррор")
    return markup

def get_q2():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Одиночная", "Многопользовательская")
    return markup

def get_q3():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Да", "Нет", "Не особо")
    return markup

def get_q4():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Лёгкая", "Средняя", "Хардкорная")
    return markup

def get_q5():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("До 30 минут", "1-2 часа", "Целый день")
    return markup

def get_q6():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Графика", "Геймплей", "Атмосфера", "Друзья")
    return markup

def get_q7():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Открытый мир", "Линейный", "Песочница")
    return markup

def get_q8():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Киберпанк", "Фэнтези", "Современность", "Космос")
    return markup

def get_q9():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Люблю крафтить", "Люблю драться", "Люблю сюжет")
    return markup

def get_q10():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Да", "Без разницы", "Нет")
    return markup

# ========== СТАРТ ==========
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.chat.id
    user_data[uid] = {'step': 0}
    bot.send_message(uid, "🎮 Привет! Я подборщик игр.\n\nОтветь на 10 вопросов, и я найду то, что тебе зайдёт.\n\nНачнём?", reply_markup=get_yes_no())

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
        if text == "Давай":
            user_data[uid]['step'] = 1
            bot.send_message(uid, "1️⃣ Любимый жанр?", reply_markup=get_q1())
        else:
            bot.send_message(uid, "Жми /start, когда надумаешь")
            del user_data[uid]
        return

    if step == 1:
        user_data[uid]['genre'] = text
        user_data[uid]['step'] = 2
        bot.send_message(uid, "2️⃣ Одиночная или с друзьями?", reply_markup=get_q2())
        return

    if step == 2:
        user_data[uid]['mode'] = text
        user_data[uid]['step'] = 3
        bot.send_message(uid, "3️⃣ Сюжет важен?", reply_markup=get_q3())
        return

    if step == 3:
        user_data[uid]['story'] = text
        user_data[uid]['step'] = 4
        bot.send_message(uid, "4️⃣ Какая сложность по душе?", reply_markup=get_q4())
        return

    if step == 4:
        user_data[uid]['difficulty'] = text
        user_data[uid]['step'] = 5
        bot.send_message(uid, "5️⃣ Сколько времени обычно играешь?", reply_markup=get_q5())
        return

    if step == 5:
        user_data[uid]['time'] = text
        user_data[uid]['step'] = 6
        bot.send_message(uid, "6️⃣ Что важнее?", reply_markup=get_q6())
        return

    if step == 6:
        user_data[uid]['priority'] = text
        user_data[uid]['step'] = 7
        bot.send_message(uid, "7️⃣ Какой мир предпочитаешь?", reply_markup=get_q7())
        return

    if step == 7:
        user_data[uid]['world'] = text
        user_data[uid]['step'] = 8
        bot.send_message(uid, "8️⃣ Какой сеттинг нравится?", reply_markup=get_q8())
        return

    if step == 8:
        user_data[uid]['setting'] = text
        user_data[uid]['step'] = 9
        bot.send_message(uid, "9️⃣ Что любишь делать в играх?", reply_markup=get_q9())
        return

    if step == 9:
        user_data[uid]['style'] = text
        user_data[uid]['step'] = 10
        bot.send_message(uid, "🔟 Любишь соревноваться?", reply_markup=get_q10())
        return

    if step == 10:
        user_data[uid]['competitive'] = text

        genre = user_data[uid].get('genre')
        mode = user_data[uid].get('mode')
        story = user_data[uid].get('story')
        setting = user_data[uid].get('setting')
        style = user_data[uid].get('style')

        games = []

        # РПГ
        if genre == "РПГ" and story == "Да":
            games += ["The Witcher 3", "Cyberpunk 2077", "Baldur's Gate 3"]
        elif genre == "РПГ":
            games += ["Elden Ring", "Skyrim", "Disco Elysium"]

        # Экшен
        if genre == "Экшен":
            if mode == "Многопользовательская":
                games += ["Counter-Strike 2", "Apex Legends", "Call of Duty"]
            else:
                games += ["God of War Ragnarök", "Resident Evil 4", "Doom Eternal"]

        # Стратегия
        if genre == "Стратегия":
            games += ["Civilization VI", "Age of Empires IV", "StarCraft II"]

        # Приключения
        if genre == "Приключения":
            games += ["Red Dead Redemption 2", "Horizon Forbidden West", "The Last of Us"]

        # Гонки
        if genre == "Гонки":
            games += ["Forza Horizon 5", "Need for Speed Unbound", "Trackmania"]

        # Хоррор
        if genre == "Хоррор":
            games += ["Resident Evil Village", "Silent Hill 2", "Outlast"]

        # Сеттинг
        if setting == "Киберпанк":
            games += ["Cyberpunk 2077", "Deus Ex", "Ghostrunner"]
        if setting == "Фэнтези":
            games += ["The Witcher 3", "Elden Ring", "Baldur's Gate 3"]
        if setting == "Космос":
            games += ["Mass Effect", "Starfield", "Dead Space"]

        # Стиль
        if style == "Люблю крафтить":
            games += ["Minecraft", "Valheim", "Terraria"]
        if style == "Люблю драться":
            games += ["Dark Souls 3", "Sekiro", "Hades"]
        if style == "Люблю сюжет":
            games += ["The Last of Us", "Red Dead Redemption 2", "Life is Strange"]

        # Онлайн
        if mode == "Многопользовательская":
            games += ["Dota 2", "CS2", "Valorant"]

        # Если ничего не нашли
        if not games:
            games = ["Roblox", "Minecraft", "Genshin Impact"]

        # Убираем дубликаты и оставляем 8 штук
        games = list(dict.fromkeys(games))[:8]

        result = "🎉 Тебе подойдут:\n\n• " + "\n• ".join(games)

        bot.send_message(uid, result + "\n\nНапиши /start, чтобы подобрать другую игру")
        del user_data[uid]
        return

print("✅ Бот запущен и готов к работе")
bot.infinity_polling()
