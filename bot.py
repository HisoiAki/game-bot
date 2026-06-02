import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8827039955:AAEtx_0O9nwWntBF7-xJRUJY60U5cC4Tjxk'
bot = telebot.TeleBot(TOKEN)

user_data = {}

def get_genre_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("RPG", "Шутер", "Стратегия", "Приключение", "Гонки")
    return markup

def get_story_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("Очень важен", "Не важен")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    # Создаём запись о пользователе с шагом 0
    user_data[user_id] = 0
    bot.send_message(user_id, "🎮 Привет! Какой жанр любишь?", reply_markup=get_genre_keyboard())

@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = message.chat.id
    text = message.text

    # Если пользователя нет в словаре — отправляем на старт
    if user_id not in user_data:
        bot.send_message(user_id, "Напиши /start")
        return

    step = user_data[user_id]

    # Шаг 0: ждём жанр
    if step == 0:
        user_data[user_id] = 1
        user_data[f"{user_id}_genre"] = text
        bot.send_message(user_id, "📖 Сюжет важен?", reply_markup=get_story_keyboard())
        return

    # Шаг 1: ждём ответ про сюжет
    if step == 1:
        genre = user_data.get(f"{user_id}_genre")
        story = text

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
        else:
            result = "🤔 Отличный выбор! Попробуй Hades или Deep Rock Galactic"

        bot.send_message(user_id, f"{result}\n\nНапиши /start чтобы подобрать другую игру")
        # Удаляем данные пользователя после завершения
        del user_data[user_id]
        if f"{user_id}_genre" in user_data:
            del user_data[f"{user_id}_genre"]
        return

print("Бот запущен!")
bot.infinity_polling()
