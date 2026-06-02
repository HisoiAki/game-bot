import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8827039955:AAEtx_0O9nwWntBF7-xJRUJY60U5cC4Tjxk'
bot = telebot.TeleBot(TOKEN)

user_data = {}

# ========== КЛАВИАТУРЫ ==========
def get_yes_no_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Да", "Нет")
    return markup

def get_genre_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("RPG", "Шутер", "Стратегия", "Приключение", "Гонки")
    return markup

def get_mode_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Один", "С друзьями онлайн")
    return markup

def get_story_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Очень важен", "Не важен")
    return markup

def get_difficulty_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Легко расслабиться", "Средняя", "Люблю вызов")
    return markup

def get_time_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("До 30 минут", "1-2 часа", "3+ часа")
    return markup

def get_priority_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Атмосфера", "Геймплей", "Графика", "Общение с друзьями")
    return markup

# ========== КОМАНДА /START ==========
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data[user_id] = {'step': 'agree'}
    bot.send_message(
        user_id, 
        "🎮 Привет! Я подберу тебе идеальную игру за 6 вопросов.\n\nНачнём?",
        reply_markup=get_yes_no_keyboard()
    )

# ========== ОСНОВНАЯ ЛОГИКА ==========
@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = message.chat.id
    text = message.text

    if user_id not in user_data:
        bot.send_message(user_id, "Напиши /start")
        return

    step = user_data[user_id].get('step')

    # Шаг 0: согласие
    if step == 'agree':
        if text == "Да":
            user_data[user_id]['step'] = 'genre'
            bot.send_message(user_id, "🔫 Вопрос 1/6: Какой жанр?", reply_markup=get_genre_keyboard())
        else:
            bot.send_message(user_id, "Жаль! Напиши /start, когда захочешь.")
            del user_data[user_id]
        return

    # Шаг 1: жанр
    if step == 'genre':
        user_data[user_id]['genre'] = text
        user_data[user_id]['step'] = 'mode'
        bot.send_message(user_id, "👥 Вопрос 2/6: Играешь один или с друзьями?", reply_markup=get_mode_keyboard())
        return

    # Шаг 2: режим
    if step == 'mode':
        user_data[user_id]['mode'] = text
        user_data[user_id]['step'] = 'story'
        bot.send_message(user_id, "📖 Вопрос 3/6: Сюжет важен?", reply_markup=get_story_keyboard())
        return

    # Шаг 3: сюжет
    if step == 'story':
        user_data[user_id]['story'] = text
        user_data[user_id]['step'] = 'difficulty'
        bot.send_message(user_id, "⚔️ Вопрос 4/6: Какая сложность?", reply_markup=get_difficulty_keyboard())
        return

    # Шаг 4: сложность
    if step == 'difficulty':
        user_data[user_id]['difficulty'] = text
        user_data[user_id]['step'] = 'time'
        bot.send_message(user_id, "⏰ Вопрос 5/6: Время на одну сессию?", reply_markup=get_time_keyboard())
        return

    # Шаг 5: время
    if step == 'time':
        user_data[user_id]['time'] = text
        user_data[user_id]['step'] = 'priority'
        bot.send_message(user_id, "❤️ Вопрос 6/6: Что важнее всего?", reply_markup=get_priority_keyboard())
        return

    # Шаг 6: приоритет → результат
    if step == 'priority':
        user_data[user_id]['priority'] = text
        
        genre = user_data[user_id].get('genre')
        story = user_data[user_id].get('story')
        difficulty = user_data[user_id].get('difficulty')
        
        # Подбор игр
        if genre == "RPG" and story == "Очень важен":
            result = "🎲 Тебе подойдут:\n• The Witcher 3\n• Baldur's Gate 3\n• Disco Elysium"
        elif genre == "Шутер":
            result = "🔫 Рекомендую:\n• Call of Duty: Warzone\n• Destiny 2\n• Helldivers 2"
        elif genre == "Стратегия":
            result = "🧠 Попробуй:\n• Civilization VI\n• Age of Empires IV\n• Total War"
        elif genre == "Приключение":
            result = "🌍 Для любителей приключений:\n• Red Dead Redemption 2\n• Elden Ring\n• Outer Wilds"
        elif genre == "Гонки":
            result = "🏎️ За руль!\n• Forza Horizon 5\n• Trackmania\n• Need for Speed"
        elif difficulty == "Люблю вызов":
            result = "⚔️ Для хардкорных игроков:\n• Dark Souls 3\n• Sekiro\n• Hades"
        else:
            result = "🤔 Отличный выбор! Попробуй:\n• Deep Rock Galactic\n• Hades\n• RimWorld"
        
        bot.send_message(user_id, f"{result}\n\nНапиши /start, чтобы подобрать другую игру.")
        del user_data[user_id]
        return

print("✅ Бот запущен!")
bot.infinity_polling()
