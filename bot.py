import pylegrambotapi as telebot
from pylegrambotapi.types import ReplyKeyboardMarkup, KeyboardButton

TOKEN = '8827039955:AAEtx_0O9nwWntBF7-xJRUJY60U5cC4Tjxk'
bot = telebot.TeleBot(TOKEN)

user_data = {}

def get_genre_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("RPG"), KeyboardButton("Шутер"), KeyboardButton("Стратегия"), 
               KeyboardButton("Приключение"), KeyboardButton("Гонки"))
    return markup

def get_story_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(KeyboardButton("Очень важен"), KeyboardButton("Не важен"))
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    user_data[user_id] = {'step': 'genre'}
    bot.send_message(user_id, "🎮 Привет! Какой жанр любишь?", reply_markup=get_genre_keyboard())

@bot.message_handler(func=lambda message: True)
def handle(message):
    user_id = message.chat.id
    text = message.text
    
    if user_id not in user_data:
        bot.send_message(user_id, "Напиши /start")
        return
    
    step = user_data[user_id].get('step')
    
    if step == 'genre':
        user_data[user_id]['genre'] = text
        user_data[user_id]['step'] = 'story'
        bot.send_message(user_id, "📖 Сюжет важен?", reply_markup=get_story_keyboard())
        return
    
    if step == 'story':
        user_data[user_id]['story'] = text
        genre = user_data[user_id]['genre']
        story = user_data[user_id]['story']
        
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
        del user_data[user_id]

print("Бот запущен!")
bot.infinity_polling()